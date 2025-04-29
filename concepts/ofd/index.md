
---
title: "Omission fault detection (OFD)"
description: >
  Autonity's Omission Fault Detection model -- reporting mechanism, temporal constraints, and economics for reporting offences and penalties for failure to participate in consensus.
---

## Overview

This section describes the Autonity omission fault detection protocol. It covers the role of the block proposer in creating proof of which committee members have participated in consensus voting of that block, the role of validators in validating that _activity proof_, and the incentives and disincentives applied to validators for proven inactivity during consensus.

Autonity implements an _omission fault detection_ (OFD) protocol for detecting if [consensus committee](/glossary/#consensus-committee) members are _actively_ participating in [consensus](/glossary/#consensus) voting rounds. To ensure the maximum level of network liveness committee members should be online and participating in each [consensus](/glossary/#consensus) voting round. An _inactive committee member_ is a committee member that is failing to do this. To be _inactive_ the validator is either not sending consensus messages when it should (failure to vote) or it is sending consensus messages too late to be included in a consensus round (failure to vote on time). In either scenario the validator is considered to have lost liveness and is deemed _inactive_ by protocol.

Autonity's [Tendermint BFT consensus](/concepts/consensus/pos/) is coordinated by committee member voting via the broadcasting of consensus messages in the [communication layer](/concepts/architecture/#communication-layer). It assumes a stable broadcast communication channel and a [semi-synchronous network timing model (_GST & Delta_) for message reception](/concepts/system-model/#networking). The Tendermint algorithm assumes that at _GST + Delta_, all the consensus messages sent at _GST_ should have been received by committee members.

The OFD protocol is based upon the processing of consensus messages and their timing, allowing for $\Delta$  blocks of latency. [Consensus committee](/concepts/consensus/committee/) members participate in [consensus rounds](/concepts/consensus/pos/#consensus-round-and-internal-state) with block _proposal_, _prevote_, and _precommit_ stages before a block is committed to [system state](/concepts/system-model/#system-state). (See the concept description [Consensus round and internal state](/concepts/consensus/pos/#consensus-round-and-internal-state)). 

A committee member is considered online by another node if the latter receives the consensus messages it expects in a timely manner. This information is then used to generate the activity report of the consensus participants.

Note that every committee member node generates an activity report based on its _local view_ of network activity. Local views may differ across committee members depending on the network and individual committee member liveness. For example, node `X` sent a message which never arrived at node `Y` due to networking issues.

Inactivity is _detected_ by the use of BLS signatures to prove activity. Validators sign consensus messages using their [consensus key](/concepts/validator/#p2p-node-keys-autonitykeys). During block proposal, the block proposer for height $h$ will aggregate the _precommit_ signatures of height $h - \Delta$ into an $ActivityProof$, which is included in the header of $h$. $\Delta$ is defined as a number of blocks, so each block header contains a historical record of committee activity at block height $h - \Delta$. For example, the _activity proof_ for block height $h$ is not computed until block height $h + \Delta$.

::: {.callout-note title="What is BLS signature aggregation?" collapse="true"}
A BLS Signature is a digital signature using the BLS12-381 elliptic curve. An aggregation of signatures created with this curve can be efficiently verified.

Autonity uses BLS signature aggregation verification to cryptographically verify which consensus committee members  posted a _precommit_ vote and so are _actively_ participated in consensus. A large committee size is an Autonity design goal for scalability. The BLS curve property of verification efficiency makes it suited use as a signature aggregation algorithm in consensus computation.

Autonity Go Client uses the BLS12-381 [`blst`](https://github.com/supranational/blst) C library (<https://www.supranational.net/press/introducing-blst>).

For a deep-dive into BLS signature aggregation some great resources are the eth2 book section [BLS Signatures](https://eth2book.info/capella/part2/building_blocks/signatures/) or the IETF research group Internet-Draft [BLS Signatures](https://www.ietf.org/archive/id/draft-irtf-cfrg-bls-signature-05.html).
:::

It is important to note that OFD runs alongside Autonity's Tendermint proof of stake consensus implementation and is _fully automated_: omission accountability events are generated and processed by protocol; no manual intervention by validator operators is required. 

As noted above the block proposer generates and includes a BLS signature aggregation of _precommit_ signatures of height $h - \Delta$ into the $ActivityProof$ included in the header of $h$.

OFD inspects the $ActivityProof$ to determine committee _inactivity_ historically over a block window defined by the OFD protocol configuration parameter $LookbackWindow$. The $ActivityProof$, like an [AFD](/concepts/accountability/) fault proof, is therefore stored on-chain.

Unlike [AFD](/concepts/accountability/) though, accountability events are not detected by committee member nodes and submitted to the AFD's Accountability Contract on chain as _accountability events_. For OFD the _activity proof_ is generated by the block proposer and included in the block header to submit on-chain. 

The Omission Accountability Contract is invoked on each block finalisation to determine inactivity and compute inactivity scores. Inactivity penalties are computed and applied at epoch end.

OFD functions, therefore, by submitting, verifying, and processing activity proofs for omission faults captured over a rolling block window by epoch.

Omission slashing penalties are computed by protocol and applied to the validator proportionally to the validator's liveness history measured by an _inactivity score_ during the epoch. The offline % of a validator in an epoch is measured by the % of blocks in the epoch that the validator failed to participate in consensus. Penalty scope covers:

- withholding of ATN [staking rewards](/glossary/#staking-rewards) proportionally to the offline % of the validator in the epoch
- withholding of [Newton inflation](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) rewards proportionally to the offline % of the validator in the epoch
- jailing and probation if the validator's offline % in the epoch is greater than a permitted threshold set by the OFD protocol
- stake slashing if the validator is seen as inactive when under probation after being jailed.

Penalties are applied as part of the state finalization function. As the last block of an epoch is finalized, the Autonity contract will: apply omission accountability for _inactivity_ to _offending validators_: witholding rewards, applying jailing, and slashing according to Autonity’s [Penalty-Absorbing Stake (PAS)](/concepts/accountability/#penalty-absorbing-stake-pas) model.

Rewards are paid to block proposers for including as many signatures in the $ActivityProof$ as possible. The _block proposer_ reward is a fraction of the epoch rewards. The block proposer's reward amount is computed based on the proposer effort that he provided in the epoch. The proposer effort of an $ActivityProof$ is determined as the voting power of the signatures exceeding the quorum value. ATN rewards are paid to the  _reporting validator_ `treasury` account, while NTN rewards are autobonded.

### Omission accountability prerequisites 

To participate in OFD a [validator](/glossary/#validator) must be a [consensus committee](/glossary/#consensus-committee) member.


## Omission Fault Detection protocol

OFD roles, core concepts, and the lifecycle of omission accountability processing from detection to applying penalties at epoch end.

### Roles

As a consensus committee member the validator may play the roles in the table beneath during OFD processing.

| Role | Description |
|:--|:--|
| _committee member_ | as a validator in the consensus committee executing Autonity's consensus protocol. For OFD generating and validating _activity proofs_, maintaining system state for inactivity scores, and computing and applying slashing penalties |
| _block proposer_ | as the validator proposing blocks, generating an _activity proof_ and including that in the block header for validation and submission on-chain |
| _offender_ | as the validator found to be inactive by the OFD and the object of slashing penalties |

The economic impact of the OFD protocol on a validator depends on their role.

| Role | Economic impact |
|:--|:--|
| _offender_ | loss of stake, validator reputation, withholding of ATN staking rewards and NTN inflation rewards, and jailing as the _offending validator_ found inactive during an epoch |
| _block proposer_ | gain of OFD proposer fee rewards for generating _activity proofs_ with precommit signatures $> \frac{2}{3}$ quorum voting power |

The Autonity community is also a _beneficiary_ of OFD processing. Slashed stake token, withheld proposer fee rewards, and withheld Newton inflation rewards will be used for community funds.

### Protocol primitives

Essential primitives of OFD are: activity proof; delta; lookback window; inactivity score and thresholds; jailing.

#### Activity proof

An _activity proof_ is a BLS signature aggregation of committee member _precommit_ votes submitted for a block during a Tendermint consensus voting round. The _block proposer_ includes an _activity proof_ in the block header and it is validated by the other committee members as part of block validation.

Each block header $h$ contains a historical record of committee activity at block height $h - \Delta$. This information is used for activity signalling.  

#### Delta $\Delta$

The _delta_ $\Delta$ is the number of blocks that a _block proposer_ waits for before generating an _activity proof_.

The $\Delta$ allows for the p2p network's [_GST + Delta_](/concepts/system-model/#networking) latency assumption for timely consensus gossiping.

If the _activity proof_ is empty past the first $\Delta$ block of the epoch, then this is an _omission fault_ (_offence_) and the _block proposer_ is subject to penalty. The $\Delta$ period is set as a protocol configuration parameter.

The delta size is set by default in the OFD [protocol configuration](/concepts/ofd/#omission-accountability-protocol-configuration) at genesis. It can be changed post-genesis by governance [`setDelta()`](/reference/api/aut/op-prot/#setdelta-omission-accountability-contract).


#### Lookback window

The _lookback window_ ($L_{P}$) is a rolling window of blocks over which OFD searches to determine activity at a certain block.

A validator is considered _active_ for block $h-\Delta$ if its _precommit_ signature was included in at least 1 $ActivityProof$ in the range
($h - \Delta - L_{P},h-\Delta$].

The _lookback window_ is extended by 1 for each empty $ActivityProof$ it includes. I.e. if there are 2 empty $ActivityProof$ in the _lookback window_, $L_{P}' = L_{P} + 2$, with $L_{P}$ being the default value.

The _lookback window_ default value is set in the OFD [protocol configuration](/concepts/ofd/#omission-accountability-protocol-configuration) at genesis. It can be changed post-genesis by governance [`setLookbackWindow()`](/reference/api/aut/op-prot/#setlookbackwindow-omission-accountability-contract).


#### Inactivity score

The average offline percentage of a committee member for an epoch is computed as an _inactivity score_. The offline percentage is measured as the % of blocks in an epoch that the validator has failed to timely participate in consensus for.

The _inactivity scores_ for the current and past epoch are combined to compute an _aggregated inactivity score_. Penalties are applied only if a committee member's _aggregated inactivity score_ breaks the _inactivity threshold_ during an epoch. Penalties are then computed based on the validator's historical _omission fault_ history. A validator's history of _omission faults_ is maintained by an _offence_ counter. The counter increments by `1` for each _omission fault_ committed, but is reset to `0` if a validator's _probation period_ expires without the validator committing an _offence_ while on [_probation_](/concepts/ofd/#probation). The validator's _aggregated inactivity score_ and _offence_ count are used as weighting factors when computing omission penalties.

#### Probation

To incentivise liveness OFD sets a _probation period_ measured in epochs. The duration of the _probation period_ for a validator is determined by the protocol's _initial probation period_ configured value multiplied by the individual validator's _offence_ count squared. Until the validator has committed a first _offence_ its _probation period_ is nil (`0`) epochs. Once offence count is `>0` the validator is in _probation_ and its _probation period_ will begin to number epochs. As soon as an _offending validator_ completes an entire _probation period_ without offences its _offence_ count is reset to `0`, taking the validator out of _probation_.

#### Thresholds

_Thresholds_ set floors which if broken trigger omission penalties. OFD has multiple thresholds:

- The _inactivity threshold_ sets a floor for a validator's _inactivity score_ in an epoch, above which it will be determined to be an _offending validator_ at the end of the epoch.

- The _withholding threshold_ sets a floor for a validator's _inactivity score_ in an epoch, which if exceeded triggers _withholding_ of staking rewards and Newton inflation rewards.

#### Inactivity penalties

The OFD protocol will apply penalties to an _offending validator_ for proven omission faults after a _threshold_ has been crossed. Penalties applied to an _offending validator_ are:

- on breaking the _withholding threshold_: withholding of staking rewards and newton inflation rewards for the epoch proportionally to the validator's _inactivity score_ in the epoch. The lost rewards are transferred to the withheld rewards pool for community funding.

- on breaking the _inactivity threshold_: jailing and withholding of all staking rewards and newton inflation rewards for the epoch. The _offending validator_ is jailed for a number of epochs determined by the protocol's _initial jailing period_ and the number of inactivity _offences_ committed by the validator. The lost rewards are transferred to the withheld rewards pool for community funding.

- on committing an _offence_ when on _probation_: slashing and jailing. The _offending validator_ is slashed according to the protocol's _initial slashing rate_ configuration, validator's offences squared, and the number of other validators committing omission offences in the epoch (_collusion degree_). If the slashing penalty is 100% of the validator's stake, then the validator is permanently jailed.

#### Jail

Jailing for omission accountability is as described in the concept [Accountable fault detection (AFD), Protocol primitives, Jail](/concepts/accountability/#jail) with the exception that:

- jailing for inactivity may be applied as part of a slashing penalty if the _offending validator_ commits an _offence_ while on _probation_.
- jailing transitions the _offending validator_ from an `active` to a `jailedForInactivity` or `jailboundForInactivity` state. Jailing is either *temporary* or *permanent*.

On *temporary* jailing the validator enters a `jailedForInactivity` state and is *impermanently* jailed for a number of blocks, the [jail period](/glossary/#jail-period). The validator's jail release block number is computed based on its proven fault history as described in [Jail period calculation](/concepts/ofd/#jail-period-calculation). After expiry of the jail period a validator may get out of jail by [re-activating](/concepts/validator/#validator-re-activation) to revert to an `active` state and resume [eligibility for consensus committee selection](/concepts/validator/#eligibility-for-selection-to-consensus-committee).

::: {.callout-note title="Note" collapse="false"}
The _offending validator_ will remain in a `jailedForInactivity` state even after jail period expiry.  The validator operator _must_ manually [re-activate](/concepts/validator/#validator-re-activation) by calling the [`activateValidator()`](/reference/api/aut/#activatevalidator) function to get out of jail.

The protocol **does not** automatically revert validator state from `jailedForInactivity` to `active` at the jail release block number. 
:::

On *permanent* jailing the validator enters a `jailboundForInactivity` state and is *permanently* jailed. The validator becomes [jailbound](/glossary/#jailbound) and cannot get out of jail. Permanent jailing is only applied in the case where a validator on _probation_ commits an _offence_ that results in 100% of the validator's stake being slashed.

::: {.callout-note title="How AFD and OFD differ in distributing staking rewards lost through validator jailing" collapse="false"}

Validator jailing has a penalty of _losing all staking rewards earned by the validator for its share of voting power in the epoch_. I.e. there is no validator commission paid on the rewards earned and no distribution of staking rewards for stake delegated to that validator for that epoch.

Both AFD and OFD have the concept of jailing, the distinction being OFD jails for _inactivity_ and AFD jails for _accountability faults_.

If a validator has been jailed by AFD then all staking rewards earned by the validator in the epoch are _forfeited_ and distributed to the _reporting validator_ as described in [Accountability fault Detection (AFD), Slashing penalties](/concepts/accountability/#slashing-penalties).

If a validator has been jailed by OFD then all staking rewards earned by the validator in the epoch are _wittheld_ and distributed to the _withheld rewards pool account_ for community funding as described in [Slashing penalties](/concepts/ofd/#slashing-penalties) on this page.

:::

## Protocol configuration

Slashing penalties for an _offending validator_ are computed by the protocol based on the offending validator's _aggregated inactivity score_, its _offence_ history, if it is on _probation_, and the total number of offences committed in the current epoch by other committee members, i.e. a _collusion degree_. For the omission fault parameters see [slashing protocol configuration](/concepts/ofd/#slashing-protocol-configuration) beneath.

Applied slashing penalties cover withholding of ATN staking rewards and NTN Newton inflation rewards proportional to the % of offline blocks in the epoch, probation, jailing, and slashing a percentage of stake. Slashing and probation scale up quadratically by the number of repeated offences.

Penalties are applied for proven omission faults at epoch end. 

Slashing is applied as part of the state finalization function. As the last block of an epoch is finalized, OFD will apply penalties for proven _omission faults_ to withhold ATN staking rewards and NTN inflation rewards, slash validator stake per Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model, and applying validator jailing if detected committing an _omission fault_ while on _probation_.

### Protocol parameters

OFD protocol parameters are set by default to:

| Protocol parameter | Description | Value |
|:--:|:--|:--:|
| _inactivity threshold_ | the threshold to determine if a committee member is an _offending validator_ at the end of the epoch | `1000` (10%) |
| _lookback window_ | the number of blocks over which the protocol will look for inactivity | `40` (40 blocks) |
| _past performance weight_ | a factor that determines how much weight is given to past performance of the validator in the preceding epoch| `1000` (10%) |
| _initial jailing period_ | the initial number of epoch(s) that an _offending validator_ will be jailed for | `10_000` (10000 blocks) |
| _initial probation period_ | the initial number of epoch(s) that an _offending validator_ will be set under probation for | `24` (24 epochs) |
| _initial slashing rate_ | the initial slashing rate used with the offence count and collusion degree when computing the slashing amount of a penalty | `25` (0.25%) |
| _delta_ | the number of blocks to wait before generating an activity proof. E.g. activity proof of block `x` is for block `x - delta` | `5` (5 blocks) |
| _slashing rate scale factor_ | the division precision used as the denominator when computing the slashing amount of a penalty | `10_000` (0.01%) |

::: {.callout-important title="A note on the initial value settings" collapse="false"}

Initial values for jailing, probation, and slashing are used to determine the scaling up a validator's _jailing period_, _probation period_, and _slashing percentage_ by the number of repeated offences quadratically.

Slashing will also scale up linearly with the collusion degree, since it helps to safeguard the liveness of the network.
:::

### Inactivity score calculation

Validator inactivity is calculated as an _aggregated inactivity score_, which is computed based upon the validator's active participation in consensus during the current and preceding epochs.

If the score is above the OFD thresholds, then penalties are applied accordingly.

The inactivity score of a validator for one epoch is computed as:

$$in_{i}(e) = \frac{Nin_{i}(e)}{el(e)}$$

where

- $in_{i}(e)$ is the inactivity score for validator $i$ at epoch $e$
- $Nin_{i}(e)$ is the number of block(s) during which validator $i$ was deemed as inactive in epoch $e$
- $el(e)$ is the epoch length (in blocks) of epoch $e$

The aggregated epoched inactivity score is a weighted sum of the validator's current epoch performance and the past epoch's performance:

$$Ain_{i}(e) = in_{i}(e) * (1-k) + Ain_{i}(e-1) * k$$

where

- $Ain_{i}(e)$ is the **aggregated** inactivity score for validator $i$ at epoch $e$
- $in_{i}(e)$ is the inactivity score for validator $i$ at epoch $e$
- $k$ is the governable protocol parameter **past performance weight** which determines how much weight is given to the validator's past performance. It has to respect the relation $0 =< k < 1$.

### Rewards withholding calculation

The epoch rewards withheld amount of a validator for the epoch is computed as:

$$ewh_{i}(e) = EpochReward_{i}(e) * Ain_{i}(e)$$

where

- $ewh_{i}(e)$ means the withheld reward of validator $i$ at epoch $e$.
- $EpochReward_{i}(e)$ means the original PoS distributed reward of validator $i$ at epoch $e$ without accounting the omission fault.
- $Ain_{i}(e)$ is the **aggregated** inactivity score for validator $i$ at epoch $e$

::: {.callout-note title="Applied to the reward withholding calculation for both ATN and NTN rewards" collapse="false"}

This calculation is used to compute the withholding of rewards for both ATN staking rewards _and_ NTN Newton inflation rewards.

At code-level the ATN and NTN rewards for a validator are calculated proportionally to the validator's [voting power](/glossary/#voting-power) share of the consensus committee's _total voting power_.
:::

### Jailing period calculation

The jailing period for a validator is calculated as:

$$JailingPeriod_{i} = InitialJailingPeriod * {offence_{i}}^2$$

where

- $JailingPeriod_{i}$ is the number of epochs validator $i$ will be jailed for
- $InitialJailingPeriod$ is a governable protocol parameter
- $offence_{i}$ is the number of repeated offences committed by validator $i$.
  
  The $offence_{i}$ counter is reset as soon as an entire $ProbationPeriod$ is completed without offence.

### Probation period calculation

The probation period for a validator is calculated as:

$$ProbationPeriod_{i} = InitialProbationPeriod * {offence_{i}}^2$$

where

- $ProbationPeriod_{i}$ is the number of epochs validator $i$ will be set under probation for
- $InitialProbationPeriod$ is a governable protocol parameter
- $offence_{i}$ is the number of repeated offences committed by validator $i$.
  
  The $offence_{i}$ counter is reset as soon as an entire $ProbationPeriod$ is completed without offence.

### Slashing amount calculation

The _slashing_ amount is calculated by the formula:

<!-- markdownlint-disable-next-line line-length -->
$$ep_{i} = BondedStake_{i} * InitialSlashingRatio * {offence_{i}}^2 * {CollusionDegree_{e}} $$

where

- $ep_{i}$ means the epoch omission fault slashing penalty of validator $i$.
- $BondedStake_{i}$ means the bonded stake of validator $i$.
- $InitialSlashingRatio$ is the system parameter of the initial slashing percentage which is configurable.
- $offence_{i}$ means the number of offences (jailed times) that a
  validator $i$ committed in the history. This counter gets reset as
  soon as an entire $ProbationPeriod$ is completed without offences.
- $CollusionDegree_{e}$ means the number of omission faulty nodes that are addressed on current epoch $e$, it indicate that the more omission faulty node there are, the heavier slashing will be applied. Only validators which get jailed due to omission are counted for collusion.

The slashing fine is then applied to validator bonded stake according to the protocol’s [Penalty-Absorbing Stake (PAS)](/concepts/ofd/#penalty-absorbing-stake-pas) model: [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake. The validator state is updated: (a) the self-bonded and total staked amounts adjusted, (b) the slashing amount is added to the validator's `totalSlashed` counter. The slashed NTN stake token is then transferred to the Autonity Protocol global `treasury` account for community funding.


### Proposer reward calculation

Block proposer rewards are calculated by the formula:

$$epr_{i} = er_{e} * aprr_{e} * {cs_{e} \over MCS} * {eec_{i}
\over \displaystyle\sum_{k=1}^{cs_{e}} eec_k }$$

where:

- $epr_{i}$ means the epoch proposer reward for validator $i$.
- $er_{e}$ means the accumulated fee reward of the epoch $e$.
- $aprr_{e}$ means the activity proof reward ratio of the epoch $e$, it is configurable
  and it describe a fraction of the epoch fee reward.
- $cs_{e}$ means the committee size of epoch $e$.
- $MCS$ means the maximum committee size of the protocol.
- $eec_{i}$ means the epoch effort count, it counts the efforts/signatures  for more than quorum of the voting power.

::: {.callout-note title="Info" collapse="false"}

Proposer rewards are an incentive for the proposer to include as many signatures as possible in an [activity proof](/concepts/ofd/#activity-proof).

A percentage of both the ATN staking rewards coming from transaction fees and NTN rewards coming from the Newton inflation mechanism are allocated for proposer incentivisation.

Only signatures that contribute further than the $\frac{2}{3}$ voting power are incentivized. In other words:

- if the proposer provided an empty $ActivityProof$ and we are not at the first $\Delta$ block of the epoch, the proposer is considered as faulty and does not receive any incentive.
- if the proposer includes signatures for exactly $\frac{2}{3}$ of the voting power, the $ActivityProof$ is valid BUT the proposer does not receive any incentive.
- if the proposer includes signatures for more than $\frac{2}{3}$ of the voting power, then he starts to get incentives.

:::

## OFD economics

There are two aspects to omission fault detection economics of slashing: inactivity penalties for _offending validators_ and proposer rewards for _block proposers_.

### Inactivity penalties

The economic loss to consensus committee members and their delegators from inactivity penalties covers loss of staking and Newton inflation rewards, block proposer rewards, jailing, and stake slashing.

| Economic loss | Receiving account | Distribution | Description |
|:-- |:--|:--|:--|
| Loss of current epoch staking rewards | [`withheldRewardsPool`](/reference/genesis/#config.autonity-object) account  | epoch end | The _offending validator_ loses a % of staking rewards proportional to its _inactivity score_ in the epoch the omission penalty is applied. The forfeited rewards are transferred to the _withheld rewards pool_ account for community funding. Amount is determined by the [Rewards withholding calculation](/concepts/ofd/#rewards-withholding-calculation). |
| Loss of current epoch Newton inflation rewards | [`withheldRewardsPool`](/reference/genesis/#config.autonity-object) account  | epoch end | The _offending validator_ loses a % of Newton inflation rewards proportional to its _inactivity score_ in the epoch the omission penalty is applied. The forfeited rewards are transferred to the _withheld rewards pool_ account for community funding. Amount is determined by the [Rewards withholding calculation](/concepts/ofd/#rewards-withholding-calculation). |
| Loss of current epoch block proposer rewards | n/a  | n/a | The _block proposer_ does not earn proposer rewards for a block if it includes an [_activity proof_](/concepts/ofd/#activity-proof) that does not contain signatures for $> \frac{2}{3}$ of block quorum voting power. See [Proposer reward calculation](/concepts/ofd/#proposer-reward-calculation) formula.|
| Loss of future staking rewards - '_jailing_' | n/a | n/a | If the inactivity penalty applies [jailing](/glossary/#jailing) for the fault, then the validator is temporarily or permanently barred from selection to the consensus committee. The _offending validator_ loses the opportunity to earn future staking rewards as a committee member until it resumes an `active` state. Jail period determined by the [Jailing period calculation](/concepts/ofd/#jailing-period-calculation). |
| Slashing of stake token | Autonity Protocol [`treasury`](/reference/genesis/#config.autonity-object) account | epoch end | The _offending validator's_ bonded stake is slashed for the omission penalty amount. Slashing is applied at epoch end according to the protocol's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model. Amount determined by the [Slashing amount calculation](/concepts/ofd/#slashing-amount-calculation). |


### Rewards

Economic rewards are provided to _block proposers_ and through the withholding of staking and Newton inflation rewards to the _community_.

Proposer rewards are distributed as incentive for _block proposers_ that have included [activity proofs](/concepts/ofd/#activity-proof) in blocks where the number of signatures is greater than the $\frac{2}{3}$ quorum of voting power required for consensus. See [Proposer reward calculation](/concepts/ofd/#proposer-reward-calculation) for the formula.

Withheld rewards distributed to the _community_ are conditional on the extent to which the _offending validator_ was inactive during the epoch, if it was jailed, and the amount of stake delegated to _offending validator_.

| Economic gain | Receiving account | Distribution | Description |
|:-- |:--|:--|:--|
| proposer rewards | [`treasury`](/concepts/validator/#treasury-account) account | epoch end | The block proposer rewards earned by the validator for the epoch. Amount determined by the [Proposer reward calculation](/concepts/ofd/#proposer-reward-calculation) formula. |
| withheld rewards | [`withheldRewardsPool`](/reference/genesis/#config.autonity-object) account | epoch end | ATN staking rewards and NTN inflation rewards earned by the _offending validator_ for the epoch are forfeited and are sent to the withheld pool account for community funding. Amount determined by the validator's share of the committee's [voting power](/glossary/#voting-power), the number of transactions processed during the epoch, the emission of the [Newton inflation mechanism](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation). |
