
---
title: "Accountability and fault detection"
linkTitle: "Accountability and fault detection"
weight: 6
description: >
  Autonity's Accountability Fault Detection model, reporting, proving innocence or guilt, temporal constraints, and economics for reporting offences and penalties for Byzantine behaviour.
---


## Overview

This section describes the Autonity accountability and fault detection protocol, the role of validators in submitting and verifying accountability event proofs (fault, accusation, innocence), the lifecycle for fault accountability and detection, and slashing.

Autonity implements an _accountability and fault detection_ (AFD) protocol for detecting infractions of consensus rules by validators participating in [consensus](/glossary/#consensus) as [consensus committee](/glossary/#consensus-committee) members. [Consensus](/glossary/#consensus) rules govern committee behaviour during consensus while participating in block proposal and voting as a committee member. Failure to adhere to these rules is a _rule infraction_ and AFD will detect and apply slashing penalties for proven rule infractions.

Proven rule infractions are reported as _faults_ and slashing makes faults _accountable_. Faults are _detected_ by validators and submitted on chain as accountability _events_ providing proof of behaviour. This proof is derived from consensus messaging between validators during consensus rounds and submitted on-chain to the Accountability Contract.

It is important to note that AFD is embedded into Autonity's Tendermint proof of stake consensus implementation and is _fully automated_: accountability events are generated and processed by protocol; no manual intervention by validator operators is required. 

AFD functions by submitting, verifying, and processing accountability event proofs by epoch. Suspected rule infractions are:

- reported as an _accusation_ proof, submitted by a _reporting_ validator against an _offending_ validator
- defended by an _innocence_ proof, submitted by the _offending_ validator within a proof submission window measured in blocks
- promoted to _fault_ proofs, _accusation_ promoted to _fault_ by protocol on individual block finalisation if not refuted by _innocence_ and the _offending_ validator does not already have a _fault_ with a higher or equivalent severity. 

Slashing penalties are computed by protocol and  applied for proven faults at epoch end. The penalty amount is computed based on a base slashing rate and slashing factors including the total number of slashable offences committed in the epoch and the individual _offending_ validator's own slashing history.

Slashing is applied as part of the state finalisation function:

- As each block is finalised, AFD will: promote within protocol constraints new _accusations_ to proven _faults_ after expiry of an _innocence_ proof submission window
- As the last block of an epoch is finalised, AFD will: apply accountability for _faults_ to _offending_ validators, slashing [self-bonded](glossary/#self-bonded) and [delegated](glossary/#delegated) stake  according to Autonity's [Penalty-Absorbing Stake (PAS)](glossary/#penalty-absorbing-stake-pas) model.

Rewards are paid for reporting a slashable _fault_ at epoch end. The _offending_ validator's share of the epoch's staking rewards is forefeited and paid to the  _reporting_ validator `treasury` account for distribution along with the staking rewards at epoch end.

### Accountability prerequisites 

To participate in AFD a [validator](/glossary/#validator) must be a [consensus committee](/glossary/#consensus-committee) member.

## Accountability and Fault Detection protocol

### Validator roles

Consensus committee members play the following roles in AFD:

- _reporting_: the validator reporting a suspected rule infraction and submitting new _accusation_ proofs on-chain
- _offending_: the validator committing a suspected rule infraction and submitting new _innocence_ proofs on-chain
- _committee member_: the validator as a consensus committee member executing Autonity's consensus protocol and for AFD handling and processing accountability events, processing and maintaining system state, and computing and applying slashing penalties.

### Protocol primitives

Essential primitives of AFD are accusations, proof of innocence, fault promotion, and jailing.

#### Accusations

- pending accusation. Only one pending accusation at a time; new accusations cannot be submitted whilst there is a pending accusation subject with an open proof submission window.
  - see notes on `canAccuse`
  - see notes on `canSlash`
  - hence these methods; called by validator before accusation submission to determine economic viability.

#### Innocence

- innocence proof submission window. The reported validator has a certain amount of time to submit a proof-of-innocence, otherwise, he gets slashed. innocence window.

After receiving a proof-of-innocence cancelling an accusation.

Event emitted after verifying an innocence proof.

#### Faults

Fault promotion

Event emitted after verifying a fault proof.

#### Slashing and severity

- slashing only applied for highest severity fault in an epoch
  - see notes on `canSlash`
- slashing amount variable
- slashing applied per PAS

#### Jail

- applied or may be applied as part of a slashing penalty
- changes validator state
- jail period
- re-activate to get out of jail


## Slashing

Slashing penalties are computed by protocol and  applied for proven faults at epoch end. The penalty amount is computed based on a base slashing rate and slashing factors including the total number of slashable offences committed in the epoch and the individual _offending_ validator's own slashing history.

Slashing is applied as part of the state finalisation function:

- As each block is finalised, AFD will: promote within protocol constraints new accusations to proven faults after expiry of an _innocence_ proof submission window
- As the last block of an epoch is finalised, AFD will: apply slashing for proven faults to validator stake, slashing [self-bonded](glossary/#self-bonded) and [delegated](glossary/#delegated) stake  according to Autonity's [Penalty-Absorbing Stake (PAS)](glossary/#penalty-absorbing-stake-pas) model.

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



### Penalty Absorbing Stake (PAS) 

NOTE: MAIN ENTRY FOR THIS SHOULD BE MOVED TO **Staking** Concept AND THEN LINKED TO FROM HERE.

[Penalty-Absorbing Stake (PAS)](glossary/#penalty-absorbing-stake-pas) model for slashing validator stake for proven misbehaviour offences.

- skin in the game
- slashing priority:
  - [self-bonded](glossary/#self-bonded) as first priority until exhausted
  - [delegated](glossary/#delegated) as second priority until exhausted.



## Rules

### Accountability rules

Rules and Rule ID

Type of accountability rules - equivocation, etc

Add placeholder for omission rules are to be added in next protocol upgrade?

Datatype enumerations

| Datatype | Enum | Description |
| --| --| --|
| `Rule` | | Rule ID defined in AFD rule engine. `Rule` is an enumerated type with enumerations: |
| | `PN` | JC: The value proposed by proper does not match the precommit |
| | `PO` | JC: The value proposed by proposer is not new |
| | `PVN` | JC: Prevote for a proposal that does not exist |
| | `PVO` | JC: |
| | `PVO1` | JC: |
| | `PVO2` | JC: |
| | `PVO3` | JC: Prevote for an invalid old proposal |
| | `C`  | JC: |
| | `C1` | JC: |
| | `InvalidProposal` | The value proposed by proposer cannot pass the blockchain's validation |
| | `InvalidProposer` | A proposal sent from none proposer nodes of the committee |
| | `Equivocation` | Multiple distinguish votes(proposal, prevote, precommit) sent by validator) |
| | `InvalidRoundStep` | Consensus round message contains invalid round number or step |
| | `AccountableGarbageMessage` | Consensus round message was signed by sender, but it cannot be decoded |
| | `MsgNotFromCommitteeMember` | Consensus round message sender is not the member of current committee |


### Rule severity

Datatype enumerations

| Datatype | Enum | Description |
| --| --| --|
| `Severity` | | the severity of the fault. `Severity` is an enumerated type with enumerations: |
| | `Minor` | |
| | `Low` | |
| | `Mid` | |
| | `High` | |
| | `Critical` | |

## Events

### Event handling

Processing of raw proof data by precompiled contracts

See API Ref and docs of event handling methods - remove from there and use as input here.
### Event types

There are three accountability _event_ types in AFD:

- _accusation_: an accusation of a committee member validator failing to adhere to or violating a consensus rule submitted by another validator committee member
- _innocence_: a proof of innocence from an _accusation_ submitted by the accused validator committee member, refuting and cancelling the _accusation_ if valid
- _fault_: a proven fault generated by protocol from an _accusation_ that has not been been successfully refuted by an _innocence_ proof and has been promoted to a _fault_.


Datatype enumerations:

| Datatype | Enum | Description |
| --| --| --|
| `EventType` | | Accountability event types. `EventType` is an enumerated type with enumerations: | 
| | `FaultProof` | Misbehaviour |
| | `Accusation` | Accusation |
| | `InnocenceProof` | Innocence |

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

- stake token: the _offending_ validator stake is slashed for the penalty amount, taken at epoch end from [self-bonded](glossary/#self-bonded) then [delegated](glossary/#delegated) stake according to the protocol's [Penalty-Absorbing Stake (PAS)](glossary/#penalty-absorbing-stake-pas) model. The amount of stake token slashed varies according to the severity of the fault committed and the slashing factors applied.
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

Slashing rewards are distributed to the _reporting_ validator along with the validator's other staking rewards at epoch end:

- the validator receives commission revenue on the slashing rewards according to its commission rate
- stake delegators receive their share of the slashing rewards _pro rata_ to the amount of stake they have bonded to the _reporting_ validator.

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

