
---
title: "Omission fault detection (OFD)"
description: >
  Autonity's Omission Fault Detection model -- reporting mechanism, temporal constraints, and economics for reporting offences and penalties for failure to participate in consensus.
---

## Overview

This section describes the Autonity omission fault detection protocol. It covers the role of the block proposer in creating proof of which committee members have participated in consensus voting of that block, the role of validators in validating that _activity proof_, and the incentives and disincentives applied to validators for proven inactivity during consensus.

Autonity implements an _omission fault detection_ (OFD) protocol for detecting if [consensus committee](/glossary/#consensus-committee) members are _actively_ participating in [consensus](/glossary/#consensus) voting rounds. To ensure the maximum level of network liveness committee members should be online and participating in each [consensus](/glossary/#consensus) voting round. An _inactive committee member_ is a committee member that is failing to do this. It is _inactive_, it is not participating in consensus in a timely fashion. To be _inactive_ the validator is either not sending consensus messages when it should (failure to vote) or it is sending consensus messages too late to be included in a consensus round (failure to vote on time). Both scenarios result in the validator missing voting. In either scenario the validator is considered to have lost liveness and is considered _inactive_ by protocol.

Autonity's [Tendermint BFT consensus](/concepts/consensus/pos/) is coordinated by committee member voting via the broadcasting of consensus messages in a consensus channel in the [communication layer](/concepts/architecture/#communication-layer). It assumes a stable broadcast communication channel and a [semi-synchronous network timing model (_GST & Delta_) for message reception](/concepts/system-model/#networking). The Tendermint algorithm assumes that at _GST + Delta_, all the consensus messages sent at _GST_ should have been received by committee members. Consensus messages arriving after the _GST + Delta_ time point are arriving too late for inclusion in consensus round voting.

The OFD protocol is based upon the processing of consensus messages and their timing allowing for the delta latency, therefore. [Consensus committee](/concepts/consensus/committee/) members participate in [consensus rounds](/concepts/consensus/pos/#consensus-round-and-internal-state) with block _proposal_, _prevote_, and _precommit_ stages before a block is committed to [system state](/concepts/system-model/#system-state). (See the concept description [Consensus round and internal state](/concepts/consensus/pos/#consensus-round-and-internal-state)). 

A committee member is considered online by another node if the latter receives the consensus messages it expects in a timely manner. This information is then used to generate the activity report of the consensus participants.

Note that every committee member node generates an activity report based on its _local view_ of network activity. Local views may differ across committee members depending on the network and individual committee member liveness. For example, node `X` sent a message which never arrived at node `Y` due to networking issues.

Inactivity is _detected_ by the use of BLS signatures to prove activity. Validators sign consensus messages using their [consensus key](/concepts/validator/#p2p-node-keys-autonitykeys). During block proposal, the block proposer for height $h$ will aggregate the _precommit_ signatures of height $h - \Delta$ into an $ActivityProof$, which is included in the header of $h$. $\Delta$ is defined as a number of blocks, so each block header contains a historical record of committee activity at block height $h - \Delta$.

$\Delta$ is the number of blocks committee members wait for before generating an activity proof. I.e. activity proof for block $x$ is going to be computed at block $x+\Delta$. The $\Delta$ allows for two temporal factors, epoch periods and the network semi-synchronous nature. Firstly, it allows for a fair start of an epoch and prevents the _block proposer_ looking for inactivity in the previous epoch where it would be unaware of the committee as committee changes end of epoch. Secondly, it allows for the p2p networks _GST + Delta_ latency assumption for timely consensus gossiping.

::: {.callout-note title="What is BLS signature aggregation?" collapse="false"}
A BLS Signature is a digital signature using the BLS12-381 elliptic curve. An aggregation of signatures created with this curve can be efficiently verified.

Autonity uses BLS signature aggregation verification to cryptographically verify which consensus committee members  posted a _precommit_ vote and so _actively_ participated in consensus. A large committee size is an Autonity design goal for scalability. The BLS curve property of verification efficiency makes it suited use as a signature aggregation algorithm in consensus computation.

Autonity Go Client uses the BLS12-381 [`blst`](https://github.com/supranational/blst) C library (<https://www.supranational.net/press/introducing-blst>).

For a deep-dive into BLS signature aggregation some great resources are the eth2 book section [BLS Signatures](https://eth2book.info/capella/part2/building_blocks/signatures/) or the IETF research group Internet-Draft [BLS Signatures](https://www.ietf.org/archive/id/draft-irtf-cfrg-bls-signature-05.html).
:::

It is important to note that OFD runs alongside Autonity's Tendermint proof of stake consensus implementation and is _fully automated_: omission accountability events are generated and processed by protocol; no manual intervention by validator operators is required. 

As noted above the block proposer generates and includes a BLS signature aggregation of _precommit_ signatures of height $h - \Delta$ into the $ActivityProof$ included in the header of $h$. Each block header contains a historical record of committee activity in the current epoch, allowing for the $\Delta$ discussed above.

OFD inspects the $ActivityProof$ to determine committee _inactivity_ historically over a block window defined by the OFD protocol configuration parameter $LookbackWindow$. The $ActivityProof$, like an AFD fault proof, is on-chain, therefore.

Unlike [AFD](/concepts/accountability/) though, accountability events are not detected by committee member nodes and submitted to the AFD's Accountability Contract on chain as _accountability events_. For OFD the _activity proof_ is generated by the block proposer and included in the block header to submit on-chain. 

The Omission Accountability Contract is invoked on each block finalisation to determine inactivity and compute inactivity penalties. Any penalties computed are then tracked in memory for application at epoch end.

OFD functions, therefore, by submitting, verifying, and processing activity proofs for omission faults captured over a rolling block window by epoch.

Omission slashing penalties are computed by protocol and applied to the validator proportionally to the validator's liveness history measured by an _inactivity score_ during the epoch. Penalties are threefold:

- withholding of OFD proposer fee reward incentives proportionally to the offline % of in the epoch, measured by the % of blocks the validator was offline for in the epoch
- withholding of proposer [Newton inflation](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) rewards proportionally to the offline % of in the epoch, measured by the % of blocks the validator was offline for in the epoch
- jailing if the validator's offline % in the epoch is greater than a permitted threshold set by protocol
- stake slashing if the validator is seen as inactive when under probation after repeated jailings.

Penalties are applied as part of the state finalization function. As the last block of an epoch is finalized, the Autonity contract will: apply omission accountability for _inactivity_ to _offending validators_: witholding rewards, applying jailing, and slashing according to Autonity’s [Penalty-Absorbing Stake (PAS)](/concepts/accountability/#penalty-absorbing-stake-pas) model.

Rewards are paid to block proposers for including as many signatures in the $ActivityProof$ as possible. The _block proposer_ reward is a fraction of transaction fees earned by protocol in the epoch. The block proposer's reward amount is computed based on the number of _activity proofs_ with signatures for more than $\frac{2}{3}$ quorum voting power generated by the proposer in the epoch. Rewards are paid to the  _reporting validator_ `treasury` account for distribution along with the staking rewards at epoch end.

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
| _offending_ | as the validator found to be inactive by the OFD and the object of slashing penalties |

The economic impact of the OFD protocol on a validator depends on their role.

| Role | Economic impact |
|:--|:--|
| _offender_ | loss of stake, validator reputation, OFD proposer fee reward revenue, Newton inflation rewards for self-bonded stake, and jailing as the _offending validator_ found inactive during an epoch |
| _block proposer_ | gain of OFD proposer fee rewards for generating _activity proofs_ with precommit signatures $> \frac{2}{3}$ quorum voting power |

The Autonity community is also a _beneficiary_ of OFD processing. Slashed stake token, withheld proposer fee rewards, and withheld Newton inflation rewards will be used for community funds.

### Protocol primitives

Essential primitives of OFD are: activity proof; delta; lookback window; inactivity score and thresholds; jailing.

#### Activity proof

An _activity proof_ is a BLS signature aggregation of committee member _precommit_ votes submitted for a block during a Tendermint consensus voting round. The _block proposer_ includes an _activity proof_ in the block header and it is validated by the other committee members as part of block validation by all committee members.

Each block header contains a historical record of committee activity at block height $h$ is computed at $h + \Delta$ and used for activity signalling.  

#### Delta $\Delta$

The _delta_ $\Delta$ is a set number of blocks at the start of an epoch in which the protocol does not require _block propsoers_ to provide an _activity proof_. During the _delta_ period the _activity proof_ is empty.

The $\Delta$ allows for two temporal factors, epoch periods and the network's semi-synchronous nature. Firstly, it allows for a fair start of an epoch and prevents the _block proposer_ looking for inactivity in the previous epoch where it would be unaware of the committee as the committee changes end of epoch. Secondly, it allows for the p2p networks _GST + Delta_ latency assumption for timely consensus gossiping.

If the _activity proof_ is empty past the $\Delta$ period, then this is an _omission fault_ (_offence_) and the _block proposer_ is subject to penalty. The $\Delta$ period is set as a protocol configuration parameter.

The delta size is set by default in the OFD [protocol configuration](/concepts/ofd/#omission-accountability-protocol-configuration) at genesis. It can be changed post-genesis by governance [`setDelta()`](/reference/api/aut/op-prot/#setdelta-omission-accountability-contract).


#### Lookback window

The _lookback window_ ($L_{P}$) is a rolling window of blocks over which OFD searches to determine activity at a certain block.

A validator is considered _active_ for block $h-\Delta$ if its _precommit_ signature was included in at least 1 $ActivityProof$ in the range
($h - \Delta - L_{P},h-\Delta$].

The _lookback window_ is extended by 1 for each empty $ActivityProof$ it includes. I.e. if there are 2 empty $ActivityProof$ in the _lookback window_, $L_{P}' = L_{P} + 2$, with $L_{P}$ being the default value).

The _lookback window_ default value is set in the OFD [protocol configuration](/concepts/ofd/#omission-accountability-protocol-configuration) at genesis. It can be changed post-genesis by governance [`setLookbackWindow()`](/reference/api/aut/op-prot/#setlookbackwindow-omission-accountability-contract).


#### Inactivity score, probation and thresholds

The OFD protocol will apply penalties to an _offending validator_ for proven omission faults. Penalties are influenced by the average offline percentage of a committee member during an epoch and its historical performance. The offline percentage is measured as the % of blocks in an epoch that the validator has failed to participate in consensus for. This measure is used to record a validator's _inactivity score_ and _thresholds_ which if broken trigger omission penalties. The _inactivity threshold_ sets a floor for the % of blocks in an epoch that a validator must be active for else it will be determined to be an _offending validator_ at the end of the epoch. The _withholding threshold_ sets a floor which if broken triggers withholding of staking rewards. The _negligible threshold_ sets a floor which if broken triggers jailing.

The average offline percentage of a committee member for the current and preceding epoch is recorded as an aggregated _inactivity score_. Penalties are applied only if a committee member's _inactivity score_ breaks the _inactivity threshold_ during an epoch. Penalties are then computed according based on the validator's historical _omission fault_ history and a _probation period_. Historical _omission faults_ are maintained by an _offence_ counter, incrementing by `1` for each _omission fault_. The _offence_ count is used as a weighting when computing penalties. To incentivise liveness OFD also sets a _probation period_ measured in epochs. The duration of the _probation period_ for a validator is determined by the protocol's _initial probation period_ configured value multiplied by the individual validator's _offence_ count squared. Until the validator has committed a first _offence_ its _probation period_ is nil (`0`) epochs. Once offence count is `>0` the validator is in _probation_ and its _probation period_ will begin to number epochs. As soon as an _offending validator_ completes an entire _probation period_ without offences its _offence_ count is reset to `0`, taking the validator out of _probation_ and so incentivising liveness.

On breaking the _inactivity threshold_ at the end of the epoch the validator is determined to be an offender and subject to penalties.

Penalties applied to an _offending validator_ are:

- on breaking the _withholding threshold_: withholding of staking rewards and newton inflation rewards for the epoch proportionally to the validator's _inactivity score_ in the epoch. The lost rewards are transferred to the withheld rewards pool for community funding.

- on breaking the _negligible threshold_: jailing and withholding of all staking rewards and newton inflation rewards for the epoch. The _offending validator_ is jailed for a number of epochs determined by the protocol's _initial jailing period_ configured value and the number of inactivity _offences_ committed by the validator. The lost rewards are transferred to the withheld rewards pool for community funding.

- on committing an _offence_ when on _probation_: slashing and permanent jailing. The _offending validator_ is slashed according to the protocol's _initial slashing rate_ configured value, validator's offences squared, and the number of other validators committing omission offences in the epoch (collusion degree). The validator is permanently jailed.


#### Jail

Jailing for omission accountability is as described in the concept [Accountable fault detection (AFD), Protocol primitives, Jail](/concepts/accountability/#jail) with the exception that:

- jailing for inactivity may be applied as part of a slashing penalty if the _offending validator_ commits an _offence_ while on _probation_.
- jailing transitions the _offending validator_ from an `active` to a `jailedForInactivity` or `jailboundForInactivity` state. Jailing is either *temporary* or *permanent*.

On *temporary* jailing the validator enters a `jailedForInactivity` state and is *impermanently* jailed for a number of blocks, the [jail period](/glossary/#jail-period). The validator's jail release block number is computed based on its proven fault history as described in [Jail period calculation](/concepts/ofd/#jail-period-calculation). After expiry of the jail period a validator may get out of jail by [re-activating](/concepts/validator/#validator-re-activation) to revert to an `active` state and resume [eligibility for consensus committee selection](/concepts/validator/#eligibility-for-selection-to-consensus-committee).

::: {.callout-note title="Note" collapse="false"}
The _offending validator_ will remain in a `jailedForInactivity` state even after jail period expiry.  The validator operator _must_ manually [re-activate](/concepts/validator/#validator-re-activation) by calling the [`activateValidator()`](/reference/api/aut/#activatevalidator) function to get out of jail.

The protocol **does not** automatically revert validator state from `jailedForInactivity` to `active` at the jail release block number. 
:::

On *permanent* jailing the validator enters a `jailboundForInactivity` state and is *permanently* jailed. It becomes [jailbound](/glossary/#jailbound) and cannot get out of jail. Permanent jailing is only applied in the case where a validator is found guilty by the [omission fault detection protocol](/concepts/ofd/) of an omission fault while on _probation_ as a member of the consensus committee.

::: {.callout-note title="How AFD and OFD differ in distributing staking rewards lost through validator jailing" collapse="false"}

Validator jailing has a penalty of _losing all staking rewards earned by the validator for its share of voting power in the epoch_. I.e. there is no validator commission paid on the rewards earned and no distribution of staking rewards for stake delegated to that validator for that epoch.

Both AFD and OFD have the concept of jailing, the distinction being OFD jails for _inactivity_ and AFD jails for _accountability faults_.

If a validator has been jailed by AFD then all staking rewards earned by the validator in the epoch are _forfeited_ and distributed to the _reporting validator_ as described in [Accountability fault Detection (AFD), Slashing penalties](/concepts/accountability/#slashing-penalties).

If a validator has been jailed by OFD then all staking rewards earned by the validator in the epoch are _wittheld_ and distributed to the _withheld rewards pool account_ for community funding as described in [Slashing penalties](/concepts/ofd/#slashing-penalties) on this page.

:::

## Slashing

Slashing penalties are computed by the protocol and applied for proven omission faults at epoch end. The penalty amount is computed based on an initial slashing rate and slashing factors including the total number of omission offences committed in the epoch and the individual _offending validator's_ own omission offence history. For parameters see [slashing protocol configuration](/concepts/ofd/#slashing-protocol-configuration) beneath.

Slashing is applied as part of the state finalization function. As the last block of an epoch is finalized, OFD will apply slashing for proven _omission faults_ to withhold ATN staking rewards and NTN inflation rewards, slash validator stake per Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model, and applying validator jailing if detected committing an _omission fault_ while on _probation_.


### Omission accountability protocol configuration

OFD protocol parameters are set by default to:

| Protocol parameter | Description | Value |
|:--:|:--|:--:|
| _inactivity threshold_ | the threshold to determine if a committee member is an _offending validator_ at the end of the epoch | `1000` (10%) |
| _lookback window_ | the number of blocks over which the protocol will look for inactivity | `40` (40 blocks) |
| _past performance weight_ | a factor that determines how much weight is given to past performance of the validator in the preceding epoch. The factor is subtracted from the validator's performance in the current epoch when computing the aggregated inactivity score | `1000` (10%) |
| _initial jailing period_ | the initial number of epoch(s) that an _offending validator_ will be jailed for | `10_000` (10000 blocks) |
| _initial probation period_ | the initial number of epoch(s) that an _offending validator_ will be set under probation for | `24` (24 epochs) |
| _initial slashing rate_ | the division precision used as the denominator when computing the slashing amount of a penalty | `25` (0.25%) |
| _delta_ | the number of blocks to wait before generating am activity proof. E.g. activity proof of block `x` is for block `x - delta` | `5` (5 blocks) |
| _slashing rate scale factor_ | the division precision used as the denominator when computing the slashing amount of a penalty | `10_000` (0.01%) |

