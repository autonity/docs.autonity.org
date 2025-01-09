---
title: "Non Stakeable Vesting Contract Interface"

description: >
  Non Stakeable Vesting Contract functions
---

Interfaces for interacting with the Non Stakeable Vesting Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Non Stakeable Vesting Contract's generated ABI and the `aut` tool's `contract` command to call the Non Stakeable Vesting Contract address `0x6901F7206A34E441Ac5020b5fB53598A65547A23`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `NonStakeableVesting.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/NonStakeableVesting.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::

## CDP Owner
### deposit

Deposit Collateral Token to a CDP using the ERC20 allowance mechanism.

Before calling this function, the CDP owner must approve the Stabilization contract to spend Collateral Token on their behalf for the full amount to be deposited.

::: {.callout-note title="Note" collapse="false"}
You can approve the Stabilization Contract as a spender of Newton Collateral Token using the `aut` command `aut token approve [OPTIONS] SPENDER AMOUNT`.
:::

Constraint checks are applied:

- the `amount` deposited is a non-zero amount
- the `amount` deposited is `<` the `allowance` amount that the CDP owner has approved the CDP contract to transfer.

The CDP's collateral balance is then incremented by the deposited amount.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | Units of Collateral Token to deposit (non-zero) |

#### Response

None.

#### Event

On a successful call the function emits a `Deposit` event, logging: `msg.sender`, `amount`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f deposit amount
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --abi Stabilization.abi deposit 1000000000000000000 | aut tx sign - | aut tx send -
```
:::


