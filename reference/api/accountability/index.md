---
title: "Accountability Contract Interface"
---

Interface for interacting with Autonity Accountability Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Accountability Contract's generated ABI and the `aut` tool's `contract` command to call the Accountability Contract address `0x5a443704dd4B594B382c22a083e2BD3090A6feF3`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Accountability.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Accountability.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::


## canAccuse

Called by a reporting validator to determine if (a) an offending validator can be accused of a rule infraction, and, (b) the number of blocks before which an accusation can be submitted.

Returns (a) a boolean flag specifying if the validator is accusable or not, and, (b) the number of blocks remaining in the innocence proof submission window before a new `Accusation` proof can be be submitted on-chain.

::: {.callout-note title="Note" collapse="false"}
A reporting validator can only submit an accusation against an offending validator if the offending validator:

- has not already been slashed in the epoch in which the accusation is being made for an offence with a higher severity. Slashing history is checked to determine this.
- is not currently already under accusation. In this case, a new accusation cannot be made until expiry of the innocence window during which an accused validator is able to submit an `Innocence` proof refuting the accusation. This creates a _deadline_ before which a new `Accusation` proof cannot be submitted. Pending validator accusations are checked to determine this.

Accusations do not automatically cause slashing. The _innocence proof window_ is measured in blocks and gives the accused offending validator a window to detect an accusation and prove innocence by submitting an `Innocence` proof on-chain. If the offending validator already has an accusation pending, the accountability protocol determines the offender is not currently accusable. Protocol has to wait to determine if the accusation has been defended or, if not, promoted to a fault. Until then, it cannot determine if the offending validator has committed a rule infraction with a higher severity or not.

:::

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_offender` | `address` | [identifier address](/concepts/validator/#validator-identifier) of the offending validator |
| `_rule` | `Rule` | enumerated value providing the ID for the protocol rule |
| `_block` | `uint256` | block number at which the rule infraction occurred |

### Response

| Field | Datatype | Description |
| --| --| --|
| `_result` | `bool` | a `boolean` value specifying whether the reported infraction is accusable (`true`) or not (`false`) |
| `_deadline` | `uint256` | the number of blocks before the validator becomes acusable. Returns (a) a `non zero` value indicating the block height at which a pending accusation's innocence window expires, or, (b) `0` indicating that there is no pending innocence window expiry |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 canAccuse _offender _rule _block
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 canAccuse 0x4B241e33CEFbeF5fFE87CF81C56f19D6321536c4 10 1245
```
```console
web3.exceptions.ContractLogicError: execution reverted
```
:::

::: {.callout-note title="Note" collapse="false"}
If the validator is not accusable, the transaction will simply revert.
:::


## canSlash

Called by a reporting validator to determine if the infraction of a protocol rule by a designated offending validator has a severity higher than any rule infraction committed by the offending validator in the current epoch.

Returns true if the severity of the reported rule infraction is higher than that of any already reported.

::: {.callout-note title="Note" collapse="false"}
Protocol only applies an accountability slashing for the fault with the highest severity committed in an epoch.

If the severity of the rule infraction reported is higher than any infraction faults committed by the offending validator in the current epoch, then it can lead to a slashing until a rule infraction with a higher severity is reported.
:::

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_offender` | `address` | [identifier address](/concepts/validator/#validator-identifier) of the offending validator |
| `_rule` | `Rule` | enumerated value providing the ID for the protocol rule |
| `_block` | `uint256` | block number at which the rule infraction occurred |

### Response

The method returns a `boolean` flag specifying whether the reported infraction is slashable (`true`) or not (`false`).

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 canSlash _offender _rule _block
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 canSlash 0x4B241e33CEFbeF5fFE87CF81C56f19D6321536c4 10 1245
```
```console
web3.exceptions.ContractLogicError: execution reverted
```
:::

::: {.callout-note title="Note" collapse="false"}
If the validator is not slashable, the transaction will simply revert.
:::


## getBeneficiary

Returns the address of the beneficiary (reporting validator) which will receive the slashed staking rewards of the offending validator.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_offender` | `address` | [identifier address](/concepts/validator/#validator-identifier) of the offending validator |

### Response

| Field | Datatype | Description |
| --| --| --|
| `beneficiary` | `address` | [identifier address](/concepts/validator/#validator-identifier) of the reporting validator |

If there is no beneficiary, then the zero address is returned.

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getBeneficiary _offender
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getBeneficiary 0xd7CB53dfBe18CEc2B84F711daDfDa904d91bC5F8
```
```console
"0x0000000000000000000000000000000000000000"
```
:::

## getConfig

Returns the Autonity Network configuration at the block height the call was submitted.

### Parameters

None.

### Response

Returns a `Config` object consisting of:

| Object | Field | Datatype | Description |
| --| --| --| --|
| | `innocenceProofSubmissionWindow` | `uint256` | the number of blocks forming a window within which an accused offending validator has to submit a proof of innocence on-chain refuting an accusation |
| | `delta` | `uint256` | the number of blocks that must elapse before running the fault detector on a certain height |
| | `range` | `uint256` | the number of blocks that establishes the height boundaries for accusation validity |
| `BaseSlashingRates ` | n/a | `struct` | the Accountability Contract's configuration of base slashing rates |
| | `low` | `uint256` | Low severity: `1` |
| | `mid` | `uint256` | Mid severity: `2` |
| | `high` | `uint256` | High severity: `s` |
| `Factors ` | n/a | `struct` | the Accountability Contract's configuration of base slashing rates for accountable rule infractions |
| | `collusion` | `uint256` | the percentage factor applied to the total number of slashable offences committed during an epoch when computing the slashing amount of a penalty |
| | `history` | `uint256` | the percentage factor applied to the total number of proven faults committed by a validator used as a factor when computing the slashing amount of a penalty |
| | `jail` | `uint256` | the number of epochs used as a factor when computing the jail period of an offending validator |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getConfig
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getConfig
```
```console
{"innocenceProofSubmissionWindow": 100, "delta": 10, "range": 256, "baseSlashingRates": {"low": 400, "mid": 600, "high": 800}, "factors": {"collusion": 200, "history": 500, "jail": 48}}
```
:::


## getEvent

Returns the accountability event for a designated accountability event ID.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_id` | `uint256` | the event identifier |

### Response

Returns an `Event` object. For the object fields see [Event structure](/concepts/afd/#event-structure) in the [AFD](/concepts/afd/) concept.

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getEvent _id
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getEvent 1
```
```console
{"eventType": 1, "rule": 2, "reporter": "0xa759BDd39eeD0d8CbCAB889D7002c0C99Cc7A9eB", "offender": "0x9564eb7b0D12C50114f2Eaf39ca08a2c15BB5BaE", "rawProof": "0xf8a3010227f89901f8960180830711cca03fdf890f74320297be999ccd845a30c02cffb42241c23e27e744a9a86027b8becc858200000822c50101010101b860b27952202d06f28c709f467ca2705b5ae49803ce8f8199681b6422d64563f2e6268fd22367265e2d2987f4f1a8a672d50c7f678c29cf7ec5282313d8b60e41404fa9eec183f7d3f90d36cfcc104f3678ec20d16bc63d0a3bc99870fb439fb8e3c0c380c080", "id": 1, "block": 463308, "epoch": 257, "reportingBlock": 463472, "messageHash": 46951917275171109801915475652663826606332598748190239073389408433879820473353}
```
:::

## getEventsLength

Returns the number of accountability events at the block height of the call.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `events.length` | `uint256` | the number of accountability events |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getEventsLength
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getEventsLength
```
```console
3
```
:::


## getGracePeriod

Returns the grace period from the Accountability Contract protocol configuration.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `gracePeriod` | `uint256` | the grace period number of blocks |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getGracePeriod
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getGracePeriod
```
```console
0
```
:::


## getHistory

Returns the number of times a validator has been punished in the past.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator ` | `address` | the validator [identifier address](/concepts/validator/#validator-identifier) |

### Response

| Field | Datatype | Description |
| --| --| --|
| `history` | `uint256` | returns the severity of the slashing |

::: {.callout-note title="Note" collapse="false"}
For a table of slashing rules and their severity see [rules](/concepts/afd/#rules) in the [AFD](https://docs.autonity.org/concepts/afd/) concept.
:::

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getHistory _validator
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getHistory 0x027C1592E8F7b9B3d0baC51A2ebf6980a3D04980
```
```console
1
```
:::

## getSlashingHistory

Returns the severity at which a validator was punished in a designated epoch.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator ` | `address` | the validator [identifier address](/concepts/validator/#validator-identifier) |
| `_epoch` | `uint256` | the epoch identifier |

### Response

| Field | Datatype | Description |
| --| --| --|
| `slashingHistory` | `uint256` | the severity of the slashing: Low `1`, Mid `2`, High `3` |

::: {.callout-note title="Note" collapse="false"}
For a table of slashing rules and their severity see [rules](/concepts/afd/#rules) in the [AFD](https://docs.autonity.org/concepts/afd/) concept.
:::

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getSlashingHistory _validator _epoch
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getSlashingHistory 0x027C1592E8F7b9B3d0baC51A2ebf6980a3D04980 257
```
```console
2
```
:::


## getValidatorAccusation

Returns the most recent pending accusation reported for a validator. The method response may be empty if there is no associated validator accusation event object for the address argument provided.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_val` | `address` | [identifier address](/concepts/validator/#validator-identifier) of the validator |

### Response

Returns an `Event` object of type `Accusation` consisting of:

| Field | Datatype | Description |
| --| --| --|
| `chunks` | `uint8` | counter of number of chunks in the event (for oversize accountability event) |
| `chunkId` | `uint8` | chunk index to construct the oversize accountability event |
| `eventType` | `EventType` | accountability event type: `Accusation` |
| `rule` | `Rule` | the identifier of the accountability Rule defined in the Accountability Fault Detector (AFD) rule engine. |
| `reporter` | `address` | the node address of the validator that reported this accountability event |
| `offender` | `address` | the node address of the validator accused of the accountability event. |
| `rawProof` | `bytes` | the rlp encoded bytes of the accountability proof object |
| `block ` | `uint256` | block number at which the accountability event occurred |
| `epoch` | `uint256` | identifier of the epoch in which the accountability event occurred |
| `reportingBlock` | `uint256` | block number at which the accountability event was reported |
| `messageHash` | `uint256` | hash of the main evidence for the accountability event |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getValidatorAccusation _val
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getValidatorAccusation 0x6558D2cEEb4a9Fe9c9cF19A3F6EBE7D45C30efaF
```
```console
web3.exceptions.ContractLogicError: execution reverted: no accusation
```
:::

::: {.callout-note title="Note" collapse="false"}
If there are no accusations, the transaction will simply revert with the revert reason: "no accusation".
:::

## getValidatorFaults

Returns proven misbehaviour faults reported for a validator. The method response may be empty if there are no associated validator `FaultProof` event object(s) for the address argument provided.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_val` | `address` | [identifier address](/concepts/validator/#validator-identifier) of the validator |

Returns an array of `Event` object(s) of type `FaultProof` consisting of:

| Field | Datatype | Description |
| --| --| --|
| `chunks` | `uint8` | counter of number of chunks in the event (for oversize accountability event) |
| `chunkId` | `uint8` | chunk index to construct the oversize accountability event |
| `eventType` | `EventType` | accountability event type: `FaultProof` |
| `rule` | `Rule` | the identifier of the accountability Rule defined in the Accountability Fault Detector (AFD) rule engine. |
| `reporter` | `address` | the node address of the validator that reported this accountability event |
| `offender` | `address` | the node address of the validator accused of the accountability event. |
| `rawProof` | `bytes` | the rlp encoded bytes of the accountability proof object |
| `block ` | `uint256` | block number at which the accountability event occurred |
| `epoch` | `uint256` | identifier of the epoch in which the accountability event occurred |
| `reportingBlock` | `uint256` | block number at which the accountability event was reported |
| `messageHash` | `uint256` | hash of the main evidence for the accountability event |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getValidatorFaults _val
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
autdev contract call --abi abi/Accountability.abi --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getValidatorFaults 0x027C1592E8F7b9B3d0baC51A2ebf6980a3D04980
```
```console
[{"eventType": 1, "rule": 2, "reporter": "0x163087D2119050BD8A656A1B50eA3343AF710BDb", "offender": "0x027C1592E8F7b9B3d0baC51A2ebf6980a3D04980", "rawProof": "0xf8a8010223f89e01f89b0180830711cca03fdf890f74320297be999ccd845a30c02cffb42241c23e27e744a9a86027b8bed1858a0822820aca02020102010202010101b860913c4eed4680e07517e56ebdae16db1679fd8c70f847e0a9d6d03985d5ea876ec446e06382deff52bf702a3ec2c8ea1b0b789f1cbca48ba30766f21f750d3c63c6b86e3d4be40d229f15913173fedb7fc20c7c88488216b1c8828e1a9e81ba5bc0c380c080", "id": 2, "block": 463308, "epoch": 257, "reportingBlock": 463492, "messageHash": 95749239210802124714124511173996749850922515771860302267718561569751513818632}]
```
:::
