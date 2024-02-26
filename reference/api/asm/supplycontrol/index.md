---
title: "Supply Control Contract Interface"

description: >
  Supply Control Contract functions
---

Interfaces for interacting with the ASM Supply Control Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Supply Control Contract's generated ABI and the `aut` tool's `contract` command to call the Supply Control Contract address `0x47c5e40890bcE4a473A49D7501808b9633F29782`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `SupplyControl.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/SupplyControl.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::


## availableSupply

Returns the supply of Auton available for minting.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `availableSupply` | `uint` | the amount of Auton available for minting as an integer value |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47c5e40890bcE4a473A49D7501808b9633F29782 availableSupply
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47c5e40890bcE4a473A49D7501808b9633F29782 availableSupply
115792089237316195423570985008687907853269984665640564039457584007913129639935
```
:::


## stabilizer

Returns the Stabilization Contract address, the `stabilizer` account that is authorized to mint and burn Auton.
    
### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| `address` | `address` | the Stabilization Contract address |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47c5e40890bcE4a473A49D7501808b9633F29782 stabilizer
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47c5e40890bcE4a473A49D7501808b9633F29782 stabilizer
"0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f"
```
:::


## totalSupply

Returns the total supply of Auton under management.

### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| Auton Supply | `uint256` | the total supply of Auton under management |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47c5e40890bcE4a473A49D7501808b9633F29782 totalSupply
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47c5e40890bcE4a473A49D7501808b9633F29782 --abi SupplyControl.abi totalSupply
115792089237316195423570985008687907853269984665640564039457584007913129639935
```
:::
