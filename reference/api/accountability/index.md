---
title: "Accountability Contract Interface"
  Autonity Accountability Contract functions
---

Interface for interacting with Autonity Accountability Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

{{pageinfo}}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Accountability Contract's generated ABI and the `aut` tool's `contract` command to call the Accountability Contract address `0x5a443704dd4B594B382c22a083e2BD3090A6feF3`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Accountability.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Accountability.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
{{/pageinfo}}


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

<!--
{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}
-->
::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
:::

### Example

<!--
{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}
-->
::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
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

<!--
{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}
-->

::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
:::

### Example

<!--
{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}
-->

::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
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

::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
:::

### Example

::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
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

<!--
{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}
-->
::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
:::

### Example

<!--
{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}
-->
::: {.callout-note title="Note" collapse="false"}
To add - see Issue [Accountability Contract Interface: add Usage and Examples to canAccuse, canSlash, getValidatorAccusation #103](https://github.com/autonity/docs.autonity.org/issues/103).
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

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getValidatorFaults _val
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x5a443704dd4B594B382c22a083e2BD3090A6feF3 getValidatorFaults 0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C
[]
{{< /tab >}}
{{< /tabpane >}}
