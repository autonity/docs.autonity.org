
---
title: "Accountability and fault detection"
linkTitle: "Accountability and fault detection"
weight: 6
description: >
  Autonity's Accountability Fault Detection model, reporting, proving innocence or guilt, temporal constraints, and economics for reporting offences and penalties for Byzantine behaviour.
---


## Overview

synopsis: rules, accusations, innocence window, fault promotion,

## Slashing logic and factors

## Sequence

Logical flow and state transition - accusation - innocence - guilt

### Accusations
only one pending accusation at a time; constraint; hence canSlash andn can Accuse methods.
### Innocence
The reported validator has a certain amount of time to submit a proof-of-innocence, otherwise, he gets slashed. innocence window.

After receiving a proof-of-innocence cancelling an accusation.

Event emitted after verifying an innocence proof.


### Fault promotion

Event emitted after verifying a fault proof.

### Jail
### Slashing parameters

    uint256 constant internal SLASHING_RATE_PRECISION = 10_000;

    /** Todo(youssef): config struct with genesis.json initialization */
    uint256 constant public INNOCENCE_PROOF_SUBMISSION_WINDOW = 600;

    // Slashing parameters
    uint256 constant public BASE_SLASHING_RATE_LOW = 1000; // 10%
    uint256 constant public BASE_SLASHING_RATE_MID = 2000; // 20%
    uint256 constant public COLLUSION_FACTOR = 800; // 8%
    uint256 constant public HISTORY_FACTOR = 500; // 5%
    uint256 constant public JAIL_FACTOR = 2; // two epochs

### event handling

Processing of raw proof data by precompiled contracts

See API Ref and docs of event handling methods - remove from there and use as input here.

### economics

the reporting validator essentially gets the tx fees that would have gone to the offender.  see https://github.com/clearmatics/autonity-internal/blob/f5444e159d6917efc9e5be6c9c3fa8a479b6f5eb/autonity/solidity/contracts/Autonity.sol#L807


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

### Event types

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


## Economics

### distributeRewards (Accountability Contract)

The Accountability Contract reward distribution function, called at epoch finalisation as part of the state finalisation function [`finalize`](/reference/api/aut/op-prot/#finalize). 

The function:

- distributes rewards for reporting provable faults committed by an offending validator to the reporting validator.
- if multiple slashing events are committed by the same offending validator during the same epoch, then rewards are only distributed to the last reporter.
- if funds can't be transferred to the reporter's `treasury` account, then rewards go to the autonity protocol `treasury` account for community funds (see also [Protocol Parameters](/reference/protocol/#parameters) Reference).

After distribution, the reporting validator is removed from the `beneficiaries` array.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator node being slashed |

#### Response

None.

#### Event

None.


## Internal functions (REMOVE)

### setEpochPeriod (Accountability Contract)

Called by the Autonity Contract [`setEpochPeriod`](/reference/api/aut/op-prot/#setepochperiod) method when the epoch period is updated.

The function maintains the epoch period setting of the Accountability Contract in sync with that of the Autonity Contract.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_newPeriod` | `uint256` | the new epoch period |

#### Response

None.

#### Event

None.


## Event handling

## handleEvent (Accountability Contract)

The accountability event handling function, invoked Called by a validator node in the consensus committee to handle processing of accountability event proof data.

Constraint checks are applied:
 
 - the function is called by a registered [validator identifier](/concepts/validator/#validator-identifier), else the transaction reverts. (Rewards for reporting a successful slashing event are distributed to the validator's [`treasury` account](/concepts/validator/#treasury-account).)
 - the `msg.sender` calling the function and the slashing event reporter addresses are the same.
 - chunk segments are contiguous for oversize events that have been chunked for storage into a map. If an event's raw proof data is above a floor byte size, then the event is `chunked` into `16kb` size chunks and stored in a map. Chunk id's must be contiguous; i.e. a map can only contain chunks from one and not multiple events.

The function checks the event data:

- If the raw proof contains `>1` chunk, then the function stores the event into a map and then returns.

The function then processes the event according to event type:

- If the event type is `FaultProof`, then the function invokes [`_handleFaultProof`](/reference/api/accountability/#_handleFaultProof) and returns.
- If the event type is `Accusation`, then the function invokes [`_handleAccusation`](/reference/api/accountability/#_handleAccusation) and returns.
- If the event type is `InnocenceProof`, then the function invokes [`_handleInnocenceProof `](/reference/api/accountability/#_handleInnocenceProof) and returns.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_event` | `Event` | event data object |

On proof submission an `_event` object data structure is constructed in memory, populated with fields ready for proof processing:

| Field | Datatype | Description |
| --| --| --|
| `chunks` | `uint8` | counter of the number of chunks in the accountability event (for oversize accountability event) |
| `chunkId` | `uint8` | chunk index to construct the oversize accountability event |
| `eventType` | `EventType` | the accountability event type, one of: `FaultProof` (proven misbehaviour), `Accusation` (pending accusation), `InnocenceProof` (proven innocence) |
| `rule` | `Rule` | the identifier of the accountability Rule defined in the Accountability Fault Detector (AFD) rule engine. Enumerated values are defined for each AFD Rule ID. |
| `reporter` | `address` | the node address of the validator that reported this accountability event |
| `offender` | `address` | the node address of the validator accused of the accountability event |
| `rawProof` | `bytes` | the `rlp` encoded bytes of the accountability proof object |
| `block ` | `uint256` | the number of the block at which the accountability event occurred. Will be populated internally. |
| `epoch` | `uint256` | the identifier of the epoch in which the accountability event occurred. Will be populated internally. |
| `reportingBlock` | `uint256` | the number of the block at which the accountability event was reported. Will be populated internally. |
| `messageHash` | `uint256` | hash of the main evidence for the accountability event. Will be populated internally. |


### Response

None.

### Event

On success the function emits events for handling of:

- Fault proof: a `NewFaultProof` event, logging: round `_offender` validator address, `_severity` of the fault, and `_eventId`.
- Accusation proof: a `NewAccusation` event, logging: round `_offender` validator address, `_severity` of the fault, and `_eventId`.
- Innocence proof: an `InnocenceProven` event, logging: `_offender` validator address, `0` indicating there are no pending accusations against the validator.


## _handleFaultProof

The function validates the misbehaviour fault proof, passing the event's `rawProof` data to a precompiled `MISBEHAVIOUR_CONTRACT` for verification. The precompiled contract returns verification outcome to the method:

- `_success` - boolean flag indicating if proof verification succeeded or failed
- `_offender` - validator identifier address of the fault offender
- `_ruleId` - ID of the accountability rule tested
- `_block` - number of the block in which the fault occurred
- `_messageHash` - cryptographic hash of the main fault evidence

Constraint checks are applied:

- the raw proof verification passed: `_success` is `true`
- there are no mismatches between the event data and the verified raw proof data fields:
  - the returned `_offender` and event `offender` address values match
  - the returned `_ruleId` and event `rule` identifier values match
- the`_block` number returned by the verification is less than the current `block.number` - the proof is for a historical and not future event
- the severity of the fault event is greater than the severity of the offender's current slashing history for the epoch
- the validator has not already been slashed for a fault with a higher severity in the proof's epoch.

The `event` data object is then updated using data returned by processing of the raw proof during proof verification processing:

On successful constraint checking:

1. Event data is updated to add the data fields assigned during event handling:

| Field | Datatype | Description |
| --| --| --|
| `block ` | `uint256` | assigned block number returned from verification in `_block`|
| `epoch` | `uint256` | assigned the identifier of the epoch in which the accountability event `_block` occurred |
| `reportingBlock` | `uint256` | assigned the current block number |
| `messageHash` | `uint256` | assigned the hash of the main evidence for the accountability event returned from verification in `_messageHash` |

2. The event is added to the events queue and assigned an `_eventId` value reflecting its position in the event queue.
3. The record of validator faults is updated to add the new event ID.
4. The event is added to the slashing queue.
5. The slashing history of the validator for the epoch is updated to record the fault's severity.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_event` | `Event` | event data object |

### Response

None.

### Event

On success the function emits a `NewFaultProof` event for handling the fault proof, logging: round `_offender` validator address, `_severity` of the fault, and `_eventId`.


## _handleAccusation

The function validates the misbehaviour fault proof, passing the event's `rawProof` data to a precompiled `ACCUSATION_CONTRACT` for verification. The precompiled contract returns verification outcome to the method:

- `_success` - boolean flag indicating if proof verification succeeded or failed
- `_offender` - validator identifier address of the fault offender
- `_ruleId` - ID of the accountability rule tested
- `_block` - number of the block in which the fault occurred
- `_messageHash` - cryptographic hash of the main fault evidence

Constraint checks are applied:

- the raw proof verification passed: `_success` is `true`
- there are no mismatches between the event data and the verified raw proof data fields:
  - the returned `_offender` and event `offender` address values match
  - the returned `_ruleId` and event `rule` identifier values match
- the `_block` number returned by the verification is less than the current `block.number` - the proof is for a historical and not future event
- the severity of the fault event is greater than the severity of the offender's current slashing history for the epoch
- the validator has not already been slashed for a fault with a higher severity in the proof's epoch.
- the validator does not have a pending accusation being processed

The `event` data object is then updated using data returned by processing of the raw proof during proof verification processing:

On successful constraint checking:

1. Event data is updated to add the data fields assigned during event handling:

| Field | Datatype | Description |
| --| --| --|
| `block ` | `uint256` | assigned block number returned from verification in `_block`|
| `epoch` | `uint256` | assigned the identifier of the epoch in which the accountability event `_block` occurred |
| `reportingBlock` | `uint256` | assigned the current block number |
| `messageHash` | `uint256` | assigned the hash of the main evidence for the accountability event returned from verification in `_messageHash` |

2. The event is added to the events queue and assigned an `_eventId` value reflecting its position in the event queue.
3. The accusation is added to the queue of pending validator accusations.
4. The event is added to the accusation queue.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_event` | `Event` | event data object |

### Response

None.

### Event

On success the function emits a `NewAccusation` event for handling the accusation proof, logging: round `_offender` validator address, `_severity` of the fault, and `_eventId`.


## _handleInnocenceProof

The function validates the innocence proof, passing the event's `rawProof` data to a precompiled `INNOCENCE_CONTRACT` for verification. The precompiled contract returns verification outcome to the method:

- `_success` - boolean flag indicating if proof verification succeeded or failed
- `_offender` - validator identifier address of the fault offender
- `_ruleId` - ID of the accountability rule tested
- `_block` - number of the block in which the fault occurred
- `_messageHash` - cryptographic hash of the main fault evidence

Constraint checks are applied:

- the raw proof verification passed: `_success` is `true`
- there are no mismatches between the event data and the verified raw proof data fields:
  - the returned `_offender` and event `offender` address values match
  - the returned `_ruleId` and event `rule` identifier values match
- the`_block` number returned by the verification is less than the current `block.number` - the proof is for a historical and not future event
- the validator has an associated accusation already being processed
- the innocence proof and associated accusation proof have matching:
  - rule identifiers
  - block number
  - message hash.

The innocence proof is valid and the associated accusation is removed `event` data object is then updated using data returned by processing of the raw proof during proof verification processing:

On successful constraint checking the innocence proof is considered valid and:

1. The accusations queue is checked and the associated accusation is removed
2. The validator's pending accusation is reset to `0`, indicating the validator has no pending accusations (so a new accusation can now be submitted against the validator).

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_event` | `Event` | event data object |

### Response

None.

### Event

On success the function emits an `InnocenceProven` event for handling the innocence proof, logging: `_offender` validator address, `0` indicating there are no pending accusations against the validator.

