---
title: "Auctioneer Contract Interface"

description: >
  Auctioneer Contract functions
---

Interfaces for interacting with the ASM Auctioneer Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Auctioneer Contract's generated ABI and the `aut` tool's `contract` command to call the Auctioneer Contract address `TO ADD`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Auctioneer.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Stabilization.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::

## CDP Liquidator

### bidDebt

Place a bid to liquidate a CDP that is undercollateralized.

The caller sends an amount of ATN (via `msg.value`) to bid for a specified amount of NTN collateral. The NTN amount must be less than or equal to the amount of NTN in the CDP for the caller to successfully execute a liquidation.

Constraint checks are applied:

- `InvalidRound` check: the Round provided in the function call's `liquidatableRound` parameter does not have a timestamp `<` the timestamp of the last change to the ASM protocol's `liquidationRatio` parameter (Previous ratio settings are not tracked so a round with a timestamp before the `liquidationRatio` parameter last updated timestamp cannot be checked to determine if the CDP was undercollateralized or not.)
- `InvalidAmount` check: the amount of ATN bid (via `msg.value`) is not `<` the debt amount specified in the function call's `ntnAmount` parameter
- `InvalidRound` check: the CDP was liquidatable during the oracle round provided in the function call's `liquidatableRound` parameter (i.e. the liquidation ratio for the CDP was not met and the CDP was in an undercollateralized state)
- `BidTooLow` check: the amount of NTN specified in the function call's `ntnAmount` parameter is `>` the maximum amount of NTN that can be returned to a liquidator for the CDP

If constraint checks pass, the bid is successful and an `AuctionedDebt` event emitted. Else, if any constraint check fails, the bid fails with the error `NotLiquidatable`.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `debtor ` | `address` | The address of the CDP owner |
| `liquidatableRound` | `uint256` | The earliest round in which the CDP was liquidatable |
| `ntnAmount` | `uint256` | The amount of NTN to receive in exchange for paying off the debt |
    
#### Response

None.

#### Event

On a successful call the function emits an `AuctionedDebt` event, logging: `debtor`, `msg.sender`, `msg.value`, `debtAmount`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}

```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}

```
:::


### bidInterest WIP TO DO

TO DO

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| | | |

TO DO
    
#### Response

None.

#### Event

TO DO

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}

```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}

```
:::

