---
title: "ACU Contract Interface"

description: >
  Autonomous Currency Unit (ACU) Contract functions

---

Interfaces for interacting with the ASM Autonomous Currency Unit Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the ACU Contract's generated ABI and the `aut` tool's `contract` command to call the ACU Contract address `0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `ACU.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/ACU.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::


## getRound

Returns the Oracle round of the current ACU index value.
    
### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `round` | `uint256` | the oracle voting round number for the latest successfully computed ACU index value |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA getRound
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA getRound
```
```console
33400
```
:::


## getScale

Returns the decimal places used to represent the ACU as a fixed-point integer.

Note this is also the scale used to represent the basket quantities. See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract).
    
### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `scale` | `uint256` | the decimal places used to represent the ACU as a fixed-point integer |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA getScale
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA getScale
```
```console
7
```
:::


## getScaleFactor

Returns the multiplier for scaling numbers to the ACU scaled representation.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `scaleFactor` | `uint256` | the scale factor for ACU index values |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA getScaleFactor
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA getScaleFactor
```
```console
10000000
```
:::


## multiplier

Returns the quantity multiplier that is used to compute the ACU index value.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `quantityMultiplier` | `uint256` | the ACU  quantity multiplier |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA multiplier
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA multiplier
```
```console
10000000
```
:::


## quantities

Returns the basket quantities used to compute the ACU index value.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `_quantities` | `uint256` array | an array of the quantities |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA quantities
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA quantities
```
```console
[1744583, 1598986, 1058522, 886091, 175605573, 12318802, 1148285]
```
:::


## scaledQuantities

Returns the scaled quantities used to compute the ACU index value.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `scaled` | `uint256` array | an array of the scaled quantities |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA scaledQuantities
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA scaledQuantities
```
```console
[1744583, 1598986, 1058522, 886091, 175605573, 12318802, 1148285]
```
:::


## symbols

Returns the currency pair symbols used to compute the ACU index.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `_symbols` | `string` array | a comma-separated list of the currency pair symbols used to compute the ACU index value |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA symbols
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA symbols
["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "USD-USD"]
```
:::


## value

Returns the latest value for the ACU index that was computed.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `_value ` | `int256` | the ACU value in fixed-point integer representation rescaled by the quantity multiplier |

If there is no value the function reverts with the error `NoACUValue`.

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA value
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA value
```
```console
8307395
```
:::
