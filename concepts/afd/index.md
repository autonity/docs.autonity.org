
---
title: "Accountability Fault Detection (AFD)"
description: >
  Autonity's Accountability Fault Detection model -- reporting mechanism, temporal constraints, and economics for reporting offences and penalties for Byzantine behavior.
---

## Overview

This section describes the Autonity Accountability Fault Detection protocol, the role of validators in submitting and verifying accountability event proofs (fault, accusation, innocence), the lifecycle for fault accountability and detection, and slashing.

Autonity implements an _Accountability Fault Detection_ (AFD) protocol for detecting infractions of consensus rules by validators participating in [consensus](/glossary/#consensus) as [consensus committee](/glossary/#consensus-committee) members. [Consensus](/glossary/#consensus) rules govern committee behavior while participating in block proposal and voting. Failure to adhere to these rules is a _rule infraction_.

Proven rule infractions are reported as _faults_ and slashing makes faults _accountable_. Faults are _detected_ by validators and submitted on chain as _accountability events_ providing proof of misbehavior. Proofs are derived from cryptographically signed messages broadcast between committee members during Tendermint consensus rounds as validators propose, prevote, and precommit blocks (see the concept description [Consensus round and internal state](/concepts/consensus/pos/#consensus-round-and-internal-state)). The proofs are then submitted on-chain to the Accountability Contract.

It is important to note that AFD runs alongside Autonity's Tendermint proof of stake consensus implementation and is _fully automated_: accountability events are generated and processed by protocol; no manual intervention by validator operators is required. 

AFD functions by submitting, verifying, and processing accountability event proofs for Rule infractions by epoch. There are two ways for Rule infractions to be created.

Rule infractions can be directly submitted as a _fault_ proof by a _reporting validator_.

Rule infractions can also be promoted from _accusations_. In this case, the Rule infraction is reported as an _accusation_, submitted by a _reporting validator_ against an _offending validator_. An _accusation_ may be defended by an _innocence_ proof submitted by the _offending validator_ within a proof submission window measured in blocks. If not defended against, the _accusation_ may be promoted to a _fault_ by the protocol once the innocence window has expired.

Slashing penalties are computed by protocol and  applied for proven faults at epoch end. The penalty amount is computed based on a base slashing rate and slashing factors including the total number of slashable offences committed in the epoch (collusion) and the individual _offending validator's_ own slashing history.

Slashing is applied as part of the state finalization function. As the last block of an epoch is finalized, the Autonity contract will: apply accountability for _faults_ to _offending validators_, slashing [self-bonded](/glossary/#self-bonded) and [delegated](/glossary/#delegated) stake  according to Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model.

Rewards are paid for reporting a slashable _fault_ at epoch end. The offending_ validator's_ share of the epoch's staking rewards is forfeited and paid to the  _reporting validator_ `treasury` account for distribution along with the staking rewards at epoch end.

### Accountability prerequisites 

To participate in AFD a [validator](/glossary/#validator) must be a [consensus committee](/glossary/#consensus-committee) member.

## Accountability Fault Detection protocol

AFD roles, core concepts, and the lifecycle of accountability event processing from accusation to slashing.

### Roles

As a consensus committee member the validator may play the roles in the table beneath during AFD processing.

| Role | Description |
|:--|:--|
| _reporting_ | as the validator reporting a (suspected) rule infraction and submitting new _fault proof_ / _accusation_ on-chain |
| _offending_ | as the validator committing a suspected rule infraction and being requested to submit _innocence_ proofs on-chain |
| _committee member_ | as a validator in the consensus committee executing Autonity's consensus protocol and for AFD handling and processing accountability events, maintaining system state for accountability events, and computing and applying slashing penalties |

The economic impact of the AFD protocol on a validator depends on their role.

| Role | Economic impact |
|:--|:--|
| _offender_ | loss of stake, validator reputation, staking reward revenue as the _offending validator_ of a slashed _fault_ |
| _reporting_ | gain of the _offending validator's_ protocol rewards as the _reporting validator_ of a slashed _fault_ |

The Autonity community is also a _beneficiary_ of AFD processing as slashed stake tokens will be used for community funds.

### Protocol primitives

Essential primitives of AFD are: accusation, innocence, and fault proofs; slashing and severity; jailing.

#### Accusations

An _accusation_ is a claim that a consensus committee member has failed to participate correctly in consensus. The protocol only allows a validator to have one pending _accusation_ at a time. New _accusations_ are made by submitting evidence of an accusable rule infraction on-chain as an accountability event of type `Accusation`.

Accusations do not automatically cause slashing, as an _innocence proof window_ measured in blocks gives the accused _offending validator_ a window to detect an _accusation_ and prove _innocence_ by submitting an _innocence_ proof on-chain.

::: {.callout-note title="A note on why a new accusation cannot be submitted until the innocence window has expired" collapse="false"}
If the _offending validator_ already has an _accusation_ pending, the accountability protocol determines the offender is not currently accusable. This is because the protocol has to wait to determine if the pending _accusation_ has been defended or, if not, promoted to a _fault_. Until then, it cannot determine if the offending validator has committed a rule infraction with a higher severity than the new candidate _accusation_ in the epoch or not.
:::

After successful [handling and verification](/reference/api/aut/op-prot/#handleevent-accountability-contract) of an _accusation_ on-chain, a `NewAccusation` event is emitted logging the _offending_ [validator identifier](/concepts/validator/#validator-identifier) address, _severity_ of rule infraction, and the event ID.

There are protocol constraints on when an _accusation_ can be made. A _reporting validator_ can only submit an _accusation_ against an _offending validator_ within the constraints described in the table beneath.

| Constraint | Description |
|:--|:--|
| A fault with a higher _severity_ has not already been reported for the epoch | The _offending validator_ does not already have a _fault_ in the current epoch `n` with a higher severity than the fault of the new _accusation_ being made. If the _accusation_ is for an earlier epoch, e.g. `n-1`, then the protocol checks that the _offending validator_ has not already been slashed in that epoch for an offence with a higher severity. Slashing history is checked to determine this. |
| There is not a _pending accusation_ | The _offending validator_ does not already have an _accusation_ for committing a rule infraction in the epoch. If there is a _pending accusation_, then the accountability protocol has to wait until the _innocence proof submission window_ for the _pending accusation_ expires to determine whether a _new accusation_ can be made or not. This creates a _deadline_ measured in block height *before* it becomes possible to submit a new _accusation_. The _innocence proof submission window_ length is set in the [slashing protocol configuration](/concepts/afd/#slashing-protocol-configuration). |
| The _accusation_ is being made within a number of blocks after the detected rule infraction | An accusation must be made within an _accusation window_ that is `<= 256` blocks after the detected accountability event. This creates a _deadline_ measured in block height *after* which an `accusation` cannot be submitted. |

As each block is finalized, AFD will attempt to promote _expired accusations_ (where the _innocence proof submission window_ has elapsed) to proven _faults_.

#### Innocence

Accusations do not automatically cause slashing. An _offending validator_ can present a claim of _innocence_ to refute a _pending accusation_ for an accusable rule infraction. 

Claims of _innocence_ are made by submitting an _innocence_ claim on-chain as an event of type `InnocenceProof`. If successful, the proof of _innocence_ cancels the _pending accusation_.

An _innocence_ claim must be submitted within an _innocence proof submission window_ to be accepted. The window length is measured as a count of blocks set as a parameter in the [slashing protocol configuration](/concepts/afd/#slashing-protocol-configuration). The window begins at the block height number at which the _accusation_ was reported and gives the accused validator a window of opportunity to detect if an accusation against it has been made, and if so to defend itself and prove innocence by submitting an _innocence_ claim on-chain. Otherwise, the _accusation_ may be _promoted_ to a _fault_ and become slashable at the end of epoch.

If the _innocence_ claim is successfully verified, then the _accusation_ queue is checked and the corresponding _accusation_ is cancelled. The _pending accusation_ state is cleared and a _reporting validator_ is now able to submit a _new accusation_ against the _offending validator_.

After successful [handling and verification](/reference/api/aut/op-prot/#handleevent-accountability-contract) of an _innocence_ claim on-chain, an `InnocenceProven` event is emitted that logs: _offending_ [validator identifier](/concepts/validator/#validator-identifier) address, and `0` indicating there are no pending accusations against the validator.

#### Faults 

A _fault_ is a proven consensus rule infraction in an epoch. A _fault_ is created *directly* or by *promotion of an accusation*.

In the direct submission method a _fault proof_ is submitted on-chain directly by a _reporting validator_. This method of fault reporting is reserved for rule infractions that rely on unforgeable evidence. It does not offer the possibility of defence.

A _pending accusation_ can be automatically *promoted* to a _fault_ after expiry of an _innocence proof submission window_. This method offers the possibility of defence by submission of an _innocence proof_. If the _offending validator_ has not submitted a successfully verified _innocence_ claim within the window, and a _fault_ with a higher _severity_ for the epoch has not already been proven against the _offending validator_ during that epoch, then the _accusation_ is promoted to a _fault_. 

::: {.callout-note title="Note" collapse="false"}
Unlike _accusations_ where an accusation must be made within a `<= 256` block window of the rule infraction, there is no _window_ constraint for direct _fault_ submissions.

A direct fault proof can be reported at any time.
:::

After successful [handling and verification](/reference/api/aut/op-prot/#handleevent-accountability-contract) of a directly submitted _fault_ on-chain, a `NewFaultProof` event is emitted logging the _offending_ [validator identifier](/concepts/validator/#validator-identifier) address, _severity_ of rule infraction, and the event ID.

#### Slashing and severity

The AFD protocol will apply slashing to an _offending validator_ for the _fault_ with the highest _severity_ reported in an epoch. A validator can only be slashed more than once in an epoch in the case where faults committed in _different_ epochs are reported and applied in the _same_ epoch.

::: {.callout-note title="Note" collapse="false"}
In certain cases, a validator can be slashed for committing a fault in an epoch more than once. For example:

- **Epoch `n`**: The _offending validator_ is slashed for a fault committed in epoch `n`.
- **Epoch `n+1`**: New _faults_ are reported for the _offending validator_: (1) one for the current **epoch `n+1`**; (2) one for **epoch `n`** with a higher _severity_ than the _fault_ already slashed in **epoch `n`**.
- **Slashing applied in epoch `n+1`**: The _offending validator_ is slashed twice: (a) once for the fault committed in epoch `n+1`, and (2) once for the fault committed in epoch `n`.
:::

Rule infraction _severity_ has two key influences. Firstly, it will determine if a new _fault_ is created or not. New fault creation is conditional on whether the _offending validator_ already has an existing _fault_ with a _severity_ `>=` to that of the candidate new _fault_ for the epoch. Secondly, _severity_ will determine the amount of the slashing applied.

The slashing amount is calculated from a number of parameters, including _severity_. For slashing calculation and parameters see [Slashing](/concepts/afd/#slashing). For the severity taxonomy see [Rules](/concepts/afd/#rules).

#### Jail

Jailing is a protocol action that excludes a validator from [consensus committee selection](/concepts/consensus/committee/#committee-member-selection). Jailing may be applied as part of a slashing penalty depending on the _severity_ of the _fault_ being _slashed_.

Jailing transitions the _offending validator_ from an `active` to a `jailed` or `jailbound` state. Jailing is either *temporary* or *permanent*.

On *temporary* jailing the validator enters a `jailed` state and is *impermanently* jailed for a number of blocks, the [jail period](/glossary/#jail-period). The validator's jail release block number is computed based on its proven fault history as described in [Jail period calculation](/concepts/afd/#jail-period-calculation). After expiry of the jail period a validator may get out of jail by [re-activating](/concepts/validator/#validator-re-activation) to revert to an `active` state and resume [eligibility for consensus committee selection](/concepts/validator/#eligibility-for-selection-to-consensus-committee).

::: {.callout-note title="Note" collapse="false"}
The _offending validator_ will remain in a `jailed` state even after jail period expiry.  The validator operator _must_ manually [re-activate](/concepts/validator/#validator-re-activation) by calling the [`activateValidator()`](/reference/api/aut/#activatevalidator) function to get out of jail.

The protocol **does not** automatically revert validator state from `jailed` to `active` at the jail release block number. 
:::

On *permanent* jailing the validator enters a `jailbound` state and is *permanently* jailed. It becomes [jailbound](/glossary/#jailbound) and cannot get out of jail. Permanent jailing is only applied in the case where a validator is found guilty by AFD of a fault with a 100% stake slashing penalty as a member of the consensus committee.

### Accountability event lifecycle

Accountability event lifecycle management comprises: accountability event submission on-chain, event handling on-chain, accusations, innocence, fault promotion, and slashing. Rule infractions are detected by validators and submitted on-chain. As noted under [Protocol Primitives](/concepts/afd/#protocol-primitives) above, [Faults](/concepts/afd/#faults) may be directly submitted as `FaultProofs` or promoted from `Accusations`.

Rule infractions can be directly submitted as a _fault_ proof by a _reporting validator_ or promoted from an accusation. In the latter case, they are promoted when:

  - reported as an _accusation_, submitted by a _reporting validator_ against an _offending validator_
  - eventually defended by an _innocence_ proof, submitted by the _offending validator_ within a proof submission window measured in blocks
  - if not defended, promoted to _fault_ by the protocol once the innocence window has expired.

The sequence of lifecycle events for an accountability event is:

- An accountability event is detected by the AFD protocol and submitted on-chain by a _reporting validator_.
- Event handling takes place. The event is verified and processed based on event type:
  - `FaultProof`: If the severity is greater than the severity of a fault in the _offending validator's_ slashing history for the epoch, the event is recorded. Else, discarded.
  - `Accusation`: If the severity is greater than the severity of a fault in the offending validator's slashing history for the epoch, and the validator does not already have a pending accusation, then the event is recorded. Else, it is discarded.
  - `InnocenceProof`: If the innocence proof matches to a pending accusation against an _offending validator_, then the event is recorded and the corresponding `Accusation` is deleted. Else, it is discarded.
- Fault promotion is tried. Each block until epoch end, the protocol attempts to promote `Accusations` to new `FaultProofs`. Promotion only takes place if the proof innocence window has expired and the _severity_ is greater than the _severity_ of an existing _fault_ in the _offending validator's_ slashing history for the epoch. Else, it is discarded.
- Faults are queued for slashing. Accountability `FaultProof` events are placed on a slashing queue for slashing at the end of epoch. For each _offending validator_ with one or more proven faults, a slashing penalty is applied for the `FaultProof` with the highest _severity_ for its fault epoch.
- Validators are jailed. Validators may be [jailed](/concepts/afd/#jail) as part of the slashing penalty for a fault. The validator’s node transitions from `active` to a `jailed` state and is barred from consensus committee selection. (The validator will only resume an `active` state when `re-activated` by the validator operator after the [jail period](/glossary/#jail-period) expires.)


## Protocol configuration

Slashing penalties are computed by the protocol and applied for proven faults at epoch end. The penalty amount is computed based on a base slashing rate and slashing factors including the total number of slashable offences committed in the epoch and the individual _offending validator's_ own slashing history. For parameters see [slashing protocol configuration](/concepts/afd/#slashing-protocol-configuration) beneath.

Slashing is applied as part of the state finalization function. As the last block of an epoch is finalized, AFD will apply slashing for proven _faults_ to validator stake, slashing stake per Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model, and applying validator jailing.

### Protocol parameters

Accountability protocol parameters are set by default to:

| Protocol parameter | Description | Value |
|:--:|:--|:--:|
| _innocence proof submission window_ | the number of blocks within which an accused _offending validator_ can submit a proof of innocence on-chain refuting an `accusation` | `100` (100 blocks) |
| _base slashing rate low_ | the base slashing rate for a fault of _Low_ severity | `400` (4%) |
| _base slashing rate mid_ | the base slashing rate for a fault of _Mid_ severity | `600` (6%) |
| _base slashing rate high_ | the base slashing rate for a fault of _High_ severity | `800` (8%) |
| _collusion factor_ | a factor that measures the number of validators committing slashable offences in the same epoch. The factor is applied as a multiplicand to the total number of slashable offences committed in the epoch when computing the slashing amount of a penalty | `200` (2%) |
| _history factor_ | a factor that measures the number of proven faults committed by a validator since registration. The factor is applied as a multiplicand to that proven fault count when computing the slashing amount of a penalty | `500` (5%) |
| _jail factor_ | the number of epochs applied as a multiplier to the proven fault count of a validator. The factor is applied when computing the jail period of an _offending validator_ | `48` (1 day at 30 mins epoch)|
| _slashing rate scale factor_ | the division precision used as the denominator when computing the slashing amount of a penalty | `10_000` (0.01%) |


### Slashing amount calculation

The economic cost of a stake slashing is calculated by applying  a _slashing rate_ to a validator's bonded stake to compute a _slashing amount_.

The _slashing rate_ is calculated by the formula:

<!-- markdownlint-disable-next-line line-length -->

$$
\text{baseRate} + \text{epochOffencesCount} * \text{collusionFactor} + \text{history} * \text{historyFactor}
$$

Where,

- $\text{baseRate}$: is determined by the [severity](/concepts/afd/#slashing-and-severity) of the [rule](/concepts/afd/#rules) infraction
- $\text{epochOffencesCount}$: is the count of proven faults created by all validators in the epoch, which is used as evidence of collusion
- $\text{history}$: is the count of proven faults committed by the offending validator since it first registered
- $\text{collusionFactor}$ and $\text{historyFactor}$: are used to compute a percentage of individual and total validator offence counts to supplement the $\text{baseRate}$ and scale the $\text{slashingRate}$ according to the individual validator history and evidence of general validator collusion in the current epoch.

The _slashing amount_ is calculated by the formula:

$$
\frac{(\text{slashingRate} * \text{validatorBondedStake})}{\text{slashingRateScaleFactor}}
$$

Applying the computed $\text{slashingRate}$ as a multiplier to the $\text{validatorBondedStake}$ amount divided by the [slashing protocol configuration](/concepts/afd/#slashing-protocol-configuration) $\text{slashingRateScaleFactor}$.

The slashing fine is then applied to validator bonded stake according to the protocol’s [Penalty-Absorbing Stake (PAS)](/concepts/afd/#penalty-absorbing-stake-pas) model: [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake. The validator state is updated: (a) the self-bonded and total staked amounts adjusted, (b) the slashing amount is added to the validator's `totalSlashed` counter. The slashed NTN stake token is then transferred to the Autonity Protocol global `treasury` account for community funding.

### Jail period calculation

Depending upon fault severity, a slashing penalty may apply *temporary* or *permanent* validator jailing.

If *temporary*, jailing will bar the validator from committee selection for a number of blocks known as a `jail period`. The jail release block number is computed by the formula:

$$
\text{currentBlockNumber + jailFactor * history * epochPeriod}
$$

Where,

- $\text{currentBlockNumber}$: is the block number at the time of computation (i.e. the last block of an epoch when slashing is applied).
- $\text{jailFactor}$: is a multiplier measured as a number of epochs, defined as a protocol parameter in the [slashing protocol configuration](/concepts/afd/#slashing-protocol-configuration).
- $\text{history}$: is the number of faults that the validator has been slashed for since registration. This applies a reputational factor based on the validator's slashing history over time.
- $\text{epochPeriod}$: is the [period of time](/glossary/#epoch-period) for which a consensus committee is elected. This is defined as a number of blocks in the Autonity network's [protocol parameterisation](/reference/protocol/) and set in the network's [genesis configuration](/reference/genesis/#public-autonity-network-configuration).

If *permanent*, the validator becomes [jailbound](/glossary/#jailbound) and there is no jail release block. Permanent jailing is only applied in the case where a validator suffers 100% stake slashing as a member of the consensus committee.

### Penalty-Absorbing Stake (PAS) 

Slashing penalties for accountability events are applied according to Autonity's [_penalty-absorbing stake_](/glossary/#penalty-absorbing-stake-pas) model. 

The _offending validator's_ own [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake when applying slashing penalties for accountability events.

To learn more about PAS, see the section on [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) in [Staking](/concepts/staking).

## Rules

Accountability rules are applied to detect faults in the three Tendermint consensus round phases *propose*, *prevote*, and *precommit*.

Rules are assigned a severity rating according to (a) the risk that failure to adhere to the rule brings to blockchain finality and integrity, (b) if the fault is accidental or Byzantine in nature. The severity taxonomy is:

- `Low`: severity `1`
- `Mid`: severity `2`
- `High`: severity `3`

The table below lists each of the rules defined in the AFD rule engine, identified by a unique Rule ID.

::: {.callout-note title="Info" collapse="false"}
The ID prefixes `P`, `PV`, and `C` that are used in Rule IDs correspond to Tendermint consensus phases:

- `P`: *propose*
- `PV`: *prevote*
- `C`: *precommit*

:::

| Rule ID | Severity | Description | 
| --| --| --|
| `PN` - `PO` | `Mid` | Propose step related consensus rule infraction. | 
| `PVN` - `PVO` - `PVO12` | `Mid` | Prevote step related consensus rule infraction. |
| `C` - `C1` | `Mid` | Precommit step related consensus rule infraction. |
| `InvalidProposal` | `High` | Proposer has proposed a block that fails blockchain validation. |
| `InvalidProposer` | `High` | Proposer of a block proposal is not the committee's elected Proposer. |
| `Equivocation` | `Low` | Validator has sent conflicting messages during a consensus round: a committee member sending multiple prevotes/precommits for different values, or a proposer has broadcast conflicting block proposals to different committee members. |


## Events

### Event handling

Accountability _events_ are submitted on-chain by validator's submitting proofs of behavior from consensus messaging. See [`handleEvent()`](/reference/api/aut/op-prot/#handleevent-accountability-contract) for a description of event handling logic.

### Event types

There are three accountability _event_ types in AFD:

| Event type | Description |
| --| --| 
| `Accusation` | an _accusation_ of a committee member validator failing to adhere to, or violating, a consensus rule submitted by another validator committee member |
| `InnocenceProof` | a _proof of innocence_ from an _accusation_ submitted by the accused committee member, which refutes and cancels the _accusation_ if the proof is valid |
| `FaultProof` | a misbehavior _fault_ |

::: {.callout-note title="Note" collapse="false"}
See distinction between _direct_ and _promoted_ in [Faults](/concepts/afd/#faults) above.
:::

### Event structure

`struct` Event:

| Field | Datatype | Description |
| --| --| --|
| `chunks` | `uint8` | Counter for the number of chunks in an oversize accountability event. (Large events are chunked into smaller segments with ID's and stored in a map; see  [`handleEvent()`](/reference/api/aut/op-prot/#handleevent-accountability-contract)). |
| `chunkId` | `uint8` | Chunk index to construct an oversize accountability event. |
| `eventType` | `EventType` | The accountability event type, one of: `FaultProof` (proven misbehavior), `Accusation` (pending accusation), or `InnocenceProof` (proven innocence). |
| `rule` | `Rule` | The identifier of the accountability Rule defined in the Accountability Fault Detector (AFD) rule engine. Enumerated values are defined for each AFD Rule ID. |
| `reporter` | `address` | The node address of the validator that reported this accountability event. |
| `offender` | `address` | The node address of the validator accused of the accountability event. |
| `rawProof` | `bytes` | The `rlp` encoded bytes of the accountability proof object. |
| `block` | `uint256` | The block number in which the accountability event occurred. Assigned during event handling by internal processing of raw proof data. |
| `epoch` | `uint256` | The epoch identifier in which the accountability event `block` occurred. Assigned during event handling by internal processing of raw proof data. |
| `reportingBlock` | `uint256` | The number of the block at which the accountability event was verified. Assigned during event handling by internal processing of raw proof data. |
| `messageHash` | `uint256` | Hash of the main evidence for the accountability event. Assigned during event handling by internal processing of raw proof data. |

## AFD economics

There are two aspects to Accountability Fault Detection economics: slashing penalties for _offending validators_ and slashing rewards for _reporting validators_.

### Slashing penalties

The economic loss to validators and their delegators from slashing penalties covers stake token and staking rewards.

| Economic loss | Receiving account | Distribution | Description |
|:-- |:--|:--|:--|
| Slashing of stake token | Autonity Protocol [`treasury`](/reference/genesis/#config.autonity-object) account | epoch end | The _offending validator's_ bonded stake is slashed for the penalty amount. Slashing is applied at epoch end according to the protocol's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model. The amount of stake token slashed varies according to the _severity_ of the fault committed and the slashing factors applied. The slashed NTN stake token are transferred to the Autonity Protocol global `treasury` account for community funding. |
| Loss of current epoch staking rewards | _reporting validator_ [`treasury`](/concepts/validator/#treasury-account) account | epoch end | The _offending validator_ loses staking rewards earned if a member of the consensus committee in the epoch when the slashing penalty is applied. The forfeited staking rewards are distributed to the _reporting validator_. |
| Loss of future staking rewards - '_jailing_' | n/a | n/a | If the slashing penalty applies [jailing](/glossary/#jailing) for the fault, then the validator is temporarily or permanently barred from selection to the consensus committee. The _offending validator_ loses the opportunity to earn future staking rewards as a committee member until it resumes an `active` state. |

### Slashing rewards

Slashing rewards are provided by forfeiture of an _offending validator's_ staking rewards.

Slashing rewards are distributed for reporting provable faults committed by an _offending validator_ to the _reporting validator_. Rewards are only distributed to the *last* reporter of a slashing penalty applied to an _offending validator_ in an epoch. Reward revenue is determined by the offender's share of the stake active ([voting power](/glossary/#voting-power)) in the committee at the time the slashing penalty is applied.

Slashing rewards earned by a _reporting validator_ are conditional on the _offending validator_ being a member of the consensus committee in the epoch when the slashing penalty is applied. If multiple slashing events are committed by the same _offending validator_ during the same epoch, then rewards are only distributed to the last _reporter_ for the last slashing penalty applied to an _offending validator_ in the epoch.

Staking rewards earned by the _offending validator_ for the epoch are distributed to the _reporting validator_ at epoch end.

| Economic gain | Receiving account | Distribution | Description |
|:-- |:--|:--|:--|
| slashing rewards |  [`treasury`](/concepts/validator/#treasury-account) account | epoch end | The staking rewards earned by the _offending validator_ for the epoch are forfeited and become the slashing rewards sent to the _reporting validator_ |

::: {.callout-note title="Note" collapse="false"}
The protocol distributes rewards for reporting provable faults committed by an _offending validator_ to the _reporting_ validator.

If multiple slashing events are committed by the same _offending validator_ during the same epoch, then rewards are only distributed to the last reporter.

If the distribution of rewards to the _reporting validator’s_ `treasury` account fails, then the slashing rewards are sent to the Autonity Protocol `treasury` account for community funds.
:::

<!--
### Transaction fee refund

The fees for submitting a new accusation may be refunded to the _reporting_ validator if the accusation is the last new accusation submitted in an epoch.

::: {.callout-note title="Note" collapse="false"}
Note the validator can determine if a detected fault is accusable by calling the [`canAccuse()`](/reference/api/afd/#canaccuse) and [`canSlash()`](/reference/api/afd/#canslash) contract functions.
:::
-->
