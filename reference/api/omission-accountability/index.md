---
title: "Omission Accountability Contract Interface"
---

Interface for interacting with Autonity Omission Accountability Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Accountability Contract's generated ABI and the `aut` tool's `contract` command to call the Omission Accountability Contract address `0x684c903c66D69777377f0945052160C9f778d689`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `OmissionAccountability.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/OmissionAccountability.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::


## getAbsenteesLastHeight

Returns an array of consensus committee members absent from consensus at the last block height.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `newDelta` | `address[]` | an array of [validator identifier](/concepts/validator/#validator-identifier) addresses that were absentees of last height |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getAbsenteesLastHeight
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getAbsenteesLastHeight
["0x3597d2D42f8Fbbc82E8b1046048773aD6DDB717E", "0xBBf36374eb23968F25aecAEbb97BF3118f3c2fEC", "0xe877FcB4b26036Baa44d3E037117b9e428B1Aa65"]
```
:::


## getDelta

Returns the delta used to determine how many blocks to wait before generating the activity proof. If the delta will change at epoch end, the new value will be returned.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `newDelta` | `uint256` | the delta number of blocks to wait before generating the activity proof |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getDelta
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getDelta
5
```
:::


## getInactivityScore

Returns the inactivity score of a validator for the last finalized epoch.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `node` | `address` | [identifier address](/concepts/validator/#validator-identifier) of the offending validator |

### Response

| Field | Datatype | Description |
| --| --| --|
| `inactivityScores` | `uint256` | the inactivity score of the validator in the last finalized epoch |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getInactivityScore _validator
```
:::


### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getInactivityScore 0x9C7dAABb5101623340C925CFD6fF74088ff5672e
2419
```
:::


## getScaleFactor

Returns the scale factor used for fixed point computation of the inactivity score in the Omission Accountability contract.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| scale factor | `uint256` | the scale factor used for fixed point computations |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getScaleFactor
```
:::


### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getScaleFactor
10000
```
:::


## getLookbackWindow

Returns the lookback window value and whether an update of it is in progress. If the lookback window will change at epoch end, the new value will be returned.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `newLookbackWindow` | `uint256` | the lookback window current value |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getLookbackWindow
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getLookbackWindow
40
```
:::


## getTotalEffort

Returns the total proposer effort accumulated up to this block.

::: {.callout-note title="What is proposer effort?"}
Total effort is a cumulative sum of the effort of each Activity Proof over the epoch. The effort of an individual Activity Proof is defined as the voting power included in it minus the value of the Quorum voting power for that epoch.
:::

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `totalEffort` | `uint256` | the total proposer effort accumulated up to this block |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getTotalEffort
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x684c903c66D69777377f0945052160C9f778d689 getTotalEffort
598671823864170391110623510
```
:::
