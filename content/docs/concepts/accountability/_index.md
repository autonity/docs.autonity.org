
---
title: "Accountability and fault detection"
linkTitle: "Accountability and fault detection"
weight: 6
description: >
  Autonity's Accountability Fault Detection model -- reporting mechanism, temporal constraints and economics for reporting offences and penalties for Byzantine behaviour.
---


## Overview

This section describes the Autonity accountability and fault detection protocol, the role of validators in submitting and verifying accountability event proofs (fault, accusation, innocence), the lifecycle for fault accountability and detection, and slashing.

Autonity implements an _accountability and fault detection_ (AFD) protocol for detecting infractions of consensus rules by validators participating in [consensus](/glossary/#consensus) as [consensus committee](/glossary/#consensus-committee) members. [Consensus](/glossary/#consensus) rules govern committee behaviour while participating in block proposal and voting. Failure to adhere to these rules is a _rule infraction_.

Proven rule infractions are reported as _faults_ and slashing makes faults _accountable_. Faults are _detected_ by validators and submitted on chain as accountability _events_ providing proof of misbehaviour. Proofs are derived from consensus messaging between validators during consensus rounds and submitted on-chain to the Accountability Contract.

It is important to note that AFD runs alongside Autonity's Tendermint proof of stake consensus implementation and is _fully automated_: accountability events are generated and processed by protocol; no manual intervention by validator operators is required. 

AFD functions by submitting, verifying, and processing accountability event proofs by epoch. Rule infractions can be:

- directly submitted as a _fault_ proof by a _reporting_ validator
- promoted from accusations, which in turns are:
  - reported as an _accusation_, submitted by a _reporting_ validator against an _offending_ validator
  - eventually defended by an _innocence_ proof, submitted by the _offending_ validator within a proof submission window measured in blocks
  - if not defended, promoted to _fault_ by the protocol once the innocence window has expired.

Slashing penalties are computed by protocol and  applied for proven faults at epoch end. The penalty amount is computed based on a base slashing rate and slashing factors including the total number of slashable offences committed in the epoch (collusion) and the individual _offending_ validator's own slashing history.

Slashing is applied as part of the state finalisation function. As the last block of an epoch is finalized, the Autonity contract will: apply accountability for _faults_ to _offending_ validators, slashing [self-bonded](/glossary/#self-bonded) and [delegated](/glossary/#delegated) stake  according to Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model.

Rewards are paid for reporting a slashable _fault_ at epoch end. The _offending_ validator's share of the epoch's staking rewards is forefeited and paid to the  _reporting_ validator `treasury` account for distribution along with the staking rewards at epoch end.

### Accountability prerequisites 

To participate in AFD a [validator](/glossary/#validator) must be a [consensus committee](/glossary/#consensus-committee) member.

## Accountability and Fault Detection protocol

AFD roles, core concepts, and the lifecycle of accountability event processing from accusation to slashing.

### Roles

As consensus committee members, validators play the following roles in AFD processing:

- _reporting_: as the validator reporting a (suspected) rule infraction and submitting new _fault proof_ / _accusation_ on-chain
- _offending_: as the validator committing a suspected rule infraction and being requested to submit _innocence_ proofs on-chain.
- _committee member_: as a validator in the consensus committee executing Autonity's consensus protocol and for AFD handling and processing accountability events, maintaining system state for accountability events, and computing and applying slashing penalties.

Validators play the following economic roles in AFD processing:

- _offender_: loss of stake, validator reputation, staking reward revenue as the _offending_ validator of a slashed _fault_
- _beneficiary_: gain of the _offending_ validator's protocol rewards as the _reporting_ validator of a slashed _fault_.

Autonity community play the following economic role in AFD processing:

- _beneficiary_: gain of slashed stake token for community funds.

### Protocol primitives

Essential primitives of AFD are: accusation, innocence, and fault proofs; slashing and severity; jailing.

#### Accusations

An _accusation_ is a claim that a consensus committee member has failed to participate correctly in consensus. Protocol only allows a validator to be under _accusation_ once at a time. New _accusations_ are made by submitting evidence of an accusable rule infraction on-chain as an accountability event of type `Accusation`.

Accusations do not automatically cause slashing and an _innocence proof window_ measured in blocks gives the accused _offending_ validator a window to detect an _accusation_ and prove _innocence_ by submitting an _innocence_ proof on-chain.

After successful [handling and verification](/reference/api/aut/op-prot/#handleevent-accountability-contract) of an _accusation_ on-chain a `NewAccusation` event is emitted logging the _offending_ [validator identifier](/concepts/validator/#validator-identifier) address, _severity_ of rule infraction, and the event ID.

There are protocol constraints on when an _accusation_ can be made. A _reporting_ validator can only submit an _accusation_ _proof_ if:

- the _offending_ validator:
  - has not been already punished in the epoch for which the new _accusation_ is being made for an offence with a higher severity.
  - is not currently already accused of committing a rule infraction, i.e. there is a _pending accusation_. In this case, a _new accusation_ cannot be made until expiry of the _innocence proof window_. This creates a _deadline_ measured in block height before which a new `accusation` cannot be submitted.
- it is within the _accusation window_:
  - an accusation must be made `<= 256` blocks after the detected accountability event.

As each block is finalized, AFD will attempt to promote _expired accusations_ (where the _innocence proof submission window_ has elapsed) to proven _faults_.
<!--
To check if an _offending_ validator has a _pending accusation_, a _reporting_ validator calls protocol functions:

- [`canAccuse()`](/reference/api/accountability/#canaccuse): to determine if (a) an offending validator is accusable, and, (b) the _deadline_ number of blocks remaining in the _innocence proof submission window_ if there is a _pending accusation_.
- [`canSlash()`](/reference/api/accountability/#canslash): to determine if the  _offending_ validator already has a _fault_ for a rule infraction in the epoch with a _severity_ higher than the new accusable rule infraction detected.
-->

#### Innocence

An _innocence_ is a claim refuting an _accusation_ for an accusable rule infraction. An _innocence_ is made by an _offending_ validator to prove innocence from a _pending accusation_ against it. Claims of _innocence_ are made by submitting _proof_ of innocence on-chain as an event of type `Innocence`. If successful, a proof of innocence cancels the _pending accusation_.

The _offending_ validator has a limited time window to submit a _proof_ of _innocence_, otherwise, the _accusation_ may be _promoted_ to a _fault_ and be slashable at the end of epoch.

An _innocence_ must be submitted within an _innocence proof submission window_ to be accepted, a designated number of blocks set as a protocol parameter. The window begins at the block height number at which the _accusation_ was reported.

If the _innocence_ is successfully verified, then the _accusation_ queue is checked and the corresponding _accusation_ is cancelled. The _pending accusation_ state is cleared and a _reporting_ validator is now able to submit a _new accusation_ against the _offending_ validator.
<!--
To check if a _new accusation_ has been made against it, an _offending_ validator:

- subscribes to `NewAccusation` events where it is the offender, retrieves the accountability event ID and queries the `Events` data structure to retrieve the _pending accusation_ against it.
-->
After successful [handling and verification](/reference/api/aut/op-prot/#handleevent-accountability-contract) of an _innocence_ on-chain an `InnocenceProven` event is emitted logging: _offending_ [validator identifier](/concepts/validator/#validator-identifier) address, and `0` indicating there are no pending accusations against the validator.

{{% alert title="Note" %}}
As noted under [Accusations](/concepts/accountability/#accusations) above, a validator with a _pending accusation_ is not accusable because protocol has to wait to determine if the _pending accusation_ has been defended or, if not, promoted to a fault or not. Until then, protocol cannot determine if the _offending_ validator has committed a rule infraction with a higher _severity_ or not in the epoch.
{{% /alert %}}

#### Faults 

A _fault_ is a proven consensus rule infraction in an epoch. A _fault_ is created by:

- **direct submission**: a _reporting_ validator submits a _fault proof_ on-chain.  Directly submitted faults:
  - does not offer possibility of defence
  - are unforgeable evidence of rule infraction

- **_promotion_ of an _accusation_**:
  - offers the possibility of defence by submission of an _innocence_ proof
  - promotion to _fault_ requires the _accusation_ to have a higher _severity_ than any _fault_ the _offending_ validator has for the epoch.

{{% alert title="Note" %}}
Unlike _accusations_ where an accusation must be made within a `<= 256` block window of the rule infraction, there is no _window_ constraint for direct _fault_ submissions.

A direct fault proof can be reported at any time.
{{% /alert %}}

Slashing for _faults_ is applied at the end of each epoch. For each validator with _fault(s)_ slashing is applied for the _fault_ with the highest _severity_.

After successful [handling and verification](/reference/api/aut/op-prot/#handleevent-accountability-contract) of a directly submitted _fault_ on-chain a `NewFaultProof` event is emitted logging the _offending_ [validator identifier](/concepts/validator/#validator-identifier) address, _severity_ of rule infraction, and the event ID.

#### Slashing and severity

The AFD protocol will only apply slashing to an _offending_ validator once in an epoch, only slashing the reported _fault_ with the highest _severity_ in an epoch.

Rule infraction _severity_ has two key influences:

- determining if a new _fault_ is created or not, conditional on the _offending_ validator not having an existing _fault_ with a _severity_ `>=` to that of the candidate new _fault_
- determining the amount of the slashing applied.

Slashing amount is calculated by a number of parameters, including _severity_. 

For the severity taxonomy see [Rule severity](/concepts/accountability/#rule-severity).

For slashing calculation and parameters see [Slashing](/concepts/accountability/#slashing).

{{% alert title="Note" %}}
A validator can theoretically be slashed for committing a fault in an epoch more than once in an edge case scenario. For example:

- **epoch `n`**: _offending_ validator slashed for highest severity fault committed in epoch `n`
- **Epoch `n+1`**: new _faults_ are reported for the _offending_ validator: (1) one for the current **epoch `n+1`**; (2) one for **epoch `n`** with a higher _severity_ than the _fault_ already slashed in **epoch `n`**.
- The _offending_ validator has two slashings applied applied in **epoch `n+1`**:
  - for epoch `n+1`
  - for epoch `n`.
{{% /alert %}}


#### Jail

Jailing is a protocol action that excludes a validator from selection to the consensus committee for a period of time measured as a number of blocks.

Jailing may be applied as part of a slashing penalty depending on the _severity_ of the _fault_ being _slashed_. Jailing changes a validator's state from `active` to `jailed`. Validators in a `jailed` state are debarred from [consensus committee selection](/concepts/consensus/committee/#committee-member-selection).

The jail period is computed by `current block number + jail factor * proven fault count * epoch period` where:

- `current block number`: the block number at the time of computation (i.e. the last block of an epoch when slashing is applied)
- `jail factor`: a set number of epochs, defined as a protocol parameter in the [slashing protocol configuration](/concepts/accountability/#slashing-protocol-configuration).
- `proven fault count`: the number of faults that the validator has been slashed for since registration. This applies a reputational factor based on the validator's slashing history
- `[epoch period](/glossary/#epoch-period)`: The period of time for which a consensus committee is elected, defined as a number of blocks in the Autonity network's [protocol parameterisation](/reference/protocol/) and set in the network's [genesis configuration](/reference/genesis/#public-autonity-network-configuration).

This computes the validator's jail release block number, after which a validator may get out of jail by [re-activating](/concepts/validator/#validator-re-activation) to revert to an `active` state and resume [eligibility for consensus committee selection](/concepts/validator/#eligibility-for-selection-to-consensus-committee).

{{% alert title="Note" %}}
Validator's **must** [re-activate](/concepts/validator/#validator-re-activation) to get out of jail.

The protocol **does not** automatically revert validator state from `jailed` to `active` at the jail release block number. 
{{% /alert %}}

### Accountability event lifecycle

Accountability event lifecycle management comprises: accountability event submission on-chain, event handling on-chain, accusations, innocence, fault promotion, slashing.

 Rule infractions can be:

- directly submitted as a _fault_ proof by a _reporting_ validator
- promoted from accusations where they are:
  - reported as an _accusation_, submitted by a _reporting_ validator against an _offending_ validator
  - eventually defended by an _innocence_ proof, submitted by the _offending_ validator within a proof submission window measured in blocks
  - if not defended, promoted to _fault_ by the protocol once the innocence window has expired.


The sequence of lifecycle events for an accountability event is:

- Detected by validator and submitted on-chain. An accountability event is detected by AFD protocol and submitted on-chain by a validator.
- Event handling. The event is verified and according to its event type:
  - `FaultProof`: recorded if the severity is greater than the severity of a fault in the offending validator's slashing history for the epoch. Else, discarded.
  - `Accusation`: recorded if the severity is greater than the severity of a fault in the offending validator's slashing history for the epoch, and, the validator does not already have a pending accusation. Else, discarded.
  - `InnocenceProof`: recorded and corresponding `Accusation` it defends against deleted if: the validator has an associated pending accusation being processed, and, the innocence proof and associated accusation proof have matching: rule identifiers, block number, message hash. Else, discarded
- Fault promotion. Each block until epoch end, protocol attempt to promote `Accusations` to new `FaultProofs`: promoted if the proof innocence window has expired, and, the severity is greater than the severity of a fault in the offending validator's slashing history for the epoch. Else, discarded.
- Queued for slashing. Accountability `FaultProof` events are queued until slashing end of epoch when: for each offending validator with one or more proven faults, a slashing penalty is applied for the `FaultProof` with the highest severity for its fault epoch.
- Validator jailing: validators may be [jailed](/concepts/accountability/#jail) as part of slashing for a fault. The validator’s node transitions from `n `active` to a `jailed` state and will only resume an `active` state when `re-activated` by the validator operator after the [jail period](/glossary/#jail-period) expires.

## Slashing

Slashing penalties are computed by protocol and  applied for proven faults at epoch end. The penalty amount is computed based on a base slashing rate and slashing factors including the total number of slashable offences committed in the epoch and the individual _offending_ validator's own slashing history. For parameters see [slashing protocol configuration](/concepts/accountability/#slashing-protocol-configuration) beneath.

Slashing is applied as part of the state finalisation function. As the last block of an epoch is finalized, AFD will apply slashing for proven _faults_ to validator stake, slashing [self-bonded](/glossary/#self-bonded) and [delegated](/glossary/#delegated) stake  according to Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model.

### Slashing protocol configuration

Slashing protocol parameter settings:

- _slashing rate precision_ = `10_000`, the division precision used as the denominator when computing the slashing amount of a penalty
- _innocence proof submission window_ = `600`, the number of blocks forming a window within which an accused offending validator has to submit a proof of innocence on-chain refuting an accusation`.
- _base slashing rate low_ = `1000` (10%), base slashing rate for a fault of _Low_ severity 
- _base slashing rate mid_ = `2000` (20%), base slashing rate for a fault of _Mid_ severity
- _collusion factor_ = `800` (8%), the percentage factor applied to the total number of slashable offences committed during an epoch when computing the slashing amount of a penalty
- _history factor_ = `500` (5%), the percentage factor applied to the proven fault count of an offending validator used as a factor when computing the slashing amount of a penalty
- _jail factor_ = `2`, the number of epochs used as a factor when computing the jail period of an offending validator.

### Autonity slashing amount calculation

The slashing amount to fine for the fault is computed based on slashing factors: base rate from fault severity, validator reputation (the validator’s proven fault count), count of offences committed in the epoch, slashing rate precision.

- Inputs:
  - [slashing protocol configuration](/concepts/accountability/#slashing-protocol-configuration) parameters, and,
  - `base rate`: assigned the [rule severity](/concepts/accountability/#rule-severity) of the rule broken by the fault event
  - `history`: assigned the count of proven faults committed by the offending validator
  - `epoch offences count`: assigned the count of proven faults created by all validators in the epoch
- `slashing rate` is computed:
  - `base rate + epoch offences count * collusion factor + history * history factor`.
- `slashing amount` of the fine is computed:
  - `(slashing rate * validator bonded stake)/slashing rate precision`
- the slashing is computed:
  - the slashed amount of NTN stake token is subtracted from the validator’s bonded stake and transferred to the Autonity Protocol global `treasury` account for community funding
  - the slashing fine is applied to validator bonded stake according to the protocol’s [Penalty-Absorbing Stake (PAS)](/concepts/accountability/#penalty-absorbing-stake-pas) model
  - the `jail period` of the validator is computed to determine the validator's jail release block number: `current block number + jail factor * history * epoch period`.
- the validator state is updated: (a) the self-bonded and total staked amounts, (b) the slashing amount is added to the validator's `totalSlashed` amount.

### Penalty-Absorbing Stake (PAS) 

Slashing penalties for accountability events are applied according to Autonity's [_penalty-absorbing stake_](/glossary/#penalty-absorbing-stake-pas) model. 

The _offending_ validator's own [self-bonded](/glossary/#self-bonded) stake is slashed in priority to [delegated](/glossary/#delegated) stake when applying slashing penalties for accountability events.

To learn more about PAS, see the concept Staking, [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas).

## Rules

### Accountability rules

Accountability rules are applied to detect faults in the three Tendermint consensus round phases *propose*, *prevote*, *precommit*. Rules are detailed in the table below.

{{% alert title="Info" color="info"%}}
In the table:

- Rule ID: is the unique identifier for the Rule defined in the AFD rule engine. ID prefixes correspond to Tendermint consensus phases:
  - `P`: *propose*
  - `PV`: *prevote*
  - `C`: *precommit*
{{% /alert %}}

| Rule ID | Description |
| --| --|
| `PN` | Proposer has proposed a new block proposal having already sent a _non-nil_ precommit message earlier <!--, or (b) has received sufficiently many prevotes for an earlier proposal block proposal during the same round. --> |
| `PO` | Proposer has proposed a block proposal that has already been proposed without attaching as justification the `2f + 1` prevotes from the same round for the value. |
| `PVN` | Committee member has sent two distinct prevotes during the same round. |
| `PVO` | Committee member has prevoted for a block proposal in more than one consensus round. |
| `PVO12` | Committee member has prevoted for a block proposal having already precommitted for that block proposal or a different block proposal in an earlier round.  |
| `PVO3` | Committee member has prevoted for an invalid old block proposal (i.e. sent an invalid message) |
| `C`  | Committee member has precommitted for an invalid block proposal  (i.e. sent an invalid message) |
| `C1` | Committee member has precommitted for a block proposal having already precommitted for that block proposal in an earlier round. |
| `InvalidProposal` | Proposer has proposed a block proposal that fails blockchain validation |
| `InvalidProposer` | Proposer of a block proposal is not the committee's elected Proposer. |
| `Equivocation` | Validator has sent conflicting messages during a consensus round: a committee member has sent conflicting votes  (prevote, precommit), a  proposer has broadcast conflicting block proposals to different committee members. |
| `InvalidRoundStep` | Consensus round message contains invalid round number or step |
| `AccountableGarbageMessage` | Consensus round message was signed by sender, but it cannot be decoded |
| `MsgNotFromCommitteeMember` | Consensus round message sender is not a member of the current consensus committee |

### Rule severity

Rules are given a severity rating according to the risk that failure to adhere to the rule brings to block chain finality and integrity. For example:

- failing to finalize a block and/or halting the chain
- proposing an invalid block
- voting for multiple and/or conflicting blocks

| Severity | Description |
| --| --|
| `Minor` | _Not currently implemented_ |
| `Low` | Invalid message: invalid proposal, invalid voting message |
| `Mid` | Equivocation message: (a) proposer has sent conflicting block proposal messages; (b) committee member has sent conflicting prevote or precommit messages. Inconsistent message: (a) proposer sends new proposal having already pre-committed for an earlier value in an earlier round; (b) proposer sends an old value that the proposer has never locked on. |
| `High` | _Not currently implemented_ |
| `Critical` | _Not currently implemented_ |

## Events

### Event handling

Accountability _events_ are submitted to the system by validator's submitting proofs of behaviour from consensus messaging on-chain. See [`handleEvent()`](/reference/api/aut/op-prot/#handleevent-accountability-contract) for a description of event handling logic.

### Event types

There are three accountability _event_ types in AFD:

| Event type | Description |
| --| --| 
| `Accusation` | an _accusation_ of a committee member validator failing to adhere to or violating a consensus rule submitted by another validator committee member |
| `InnocenceProof` | a proof of _innocence_ from an _accusation_ submitted by the accused validator committee member, refuting and cancelling the _accusation_ if valid |
| `FaultProof` | a misbehaviour _fault_. |

{{% alert title="Note" %}}
See distinction between _direct_ and _promoted_ in [Faults](/concepts/accountability/#faults) above.
{{% /alert %}}

### Event structure

`struct` Event:

| Field | Datatype | Description |
| --| --| --|
| `chunks` | `uint8` | counter of the number of chunks in the accountability event (for oversize accountability event) |
| `chunkId` | `uint8` | chunk index to construct the oversize accountability event |
| `eventType` | `EventType` | the accountability event type, one of: `FaultProof` (proven misbehaviour), `Accusation` (pending accusation), `InnocenceProof` (proven innocence) |
| `rule` | `Rule` | the identifier of the accountability Rule defined in the Accountability Fault Detector (AFD) rule engine. Enumerated values are defined for each AFD Rule ID. |
| `reporter` | `address` | the node address of the validator that reported this accountability event |
| `offender` | `address` | the node address of the validator accused of the accountability event |
| `rawProof` | `bytes` | the `rlp` encoded bytes of the accountability proof object |
| `block` | `uint256` | the number of the block at which the accountability event occurred. Assigned during event handling by internal processing of raw proof data |
| `epoch` | `uint256` | the identifier of the epoch in which the accountability event `block` occurred. Assigned during event handling by internal processing of raw proof data |
| `reportingBlock` | `uint256` | the number of the block at which the accountability event was verified. Assigned during event handling by internal processing of raw proof data|
| `messageHash` | `uint256` | hash of the main evidence for the accountability event. Assigned during event handling by internal processing of raw proof data |


## Slashing economics

Slashing economics have facets: slashing penalties, slashing rewards for reporting validators. <!--, and transaction fee refund for the last accepted new accusation of an epoch.-->

### Slashing penalties

Economic loss to validators and their delegators from penalties is multi-dimensional:

- stake token: the _offending_ validator stake is slashed for the penalty amount, taken at epoch end from [self-bonded](/glossary/#self-bonded) then [delegated](/glossary/#delegated) stake according to the protocol's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model. The amount of stake token slashed varies according to the severity of the fault committed and the slashing factors applied.
- staking rewards: the _offending_ validator staking rewards earned if a member of the consensus committee in the epoch when the slashing penalty is applied are lost. The forfeited staking rewards are distributed to the _reporting_ validator.
- future staking rewards: if the slashing penalty applies [jailing](/glossary/#jailing) for the fault, then the _offending_ validator is excluded from consensus committee selection and so the opportunity to earn staking rewards as a committee member while in a `jailed` state.

{{% alert title="Note" %}}
After the expiry of the [jailing period](/glossary/#jail-period) the validator can reactivate itself to resume an `active` state and once again become eligible for committee selection.

Note that the _offending_ validator will remain in a `jailed` state even after jail period expiry _until_ the validator operator [re-activates](/concepts/validator/#validator-re-activation) by calling the [`activateValidator()`](/reference/api/aut/#activatevalidator) function.
{{% /alert %}}

### Slashing rewards
Slashing rewards are provided by forfeiture of an _offending_ validator's staking rewards.

Slashing rewards are distributed for reporting provable faults committed by an _offending_ validator to the _reporting_ validator. Rewards are only distributed to the *last* reporter of a slashing penalty applied to an _offending_ validator in an epoch. Reward revenue is determined by the _offender's_ share of the stake active ([voting power](/glossary/#voting-power)) in the committee at the time the slashing penalty is applied.

Slashing rewards earned by a _reporting_ validator are conditional on:

- the _offending_ validator being a member of the consensus committee in the epoch when the slashing penalty is applied
- the _offending_ validator's share of the [voting power](/glossary/#voting-power) in the committee, as staking rewards are distributed _pro rata_ to voting power
- the slashable offence reported by the _reporting_ validator is the last slashing penalty applied to an _offending_ validator in an epoch. If multiple slashing events are committed by the same _offending_ validator during the same epoch, then rewards are only distributed to the last _reporter_.

Slashing rewards are distributed to the _reporting_ validator at epoch end.

{{% alert title="Note" %}}
The protocol distributes rewards for reporting provable faults committed by an _offending_ validator to the _reporting_ validator.

If multiple slashing events are committed by the same offending validator during the same epoch, then rewards are only distributed to the last reporter.

If the distribution of rewards to the _reporting_ validator’s `treasury` account fails, then the slashing rewards are sent to the Autonity Protocol `treasury` account for community funds.
{{% /alert %}}
<!--
### Transaction fee refund

The fees for submitting a new accusation may be refunded to the _reporting_ validator if:

- the accusation is the last new accusation submitted in an epoch.

{{% alert title="Note" %}}
Note the validator can determine if a detected fault is accusable by calling the [`canAccuse()`](/reference/api/accountability/#canaccuse) and [`canSlash()`](/reference/api/accountability/#canslash) contract functions.
{{% /alert %}}
-->

