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

## CDP Liquidator - DRAFT - sage/Example TO DO

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


### bidInterest

Place a bid in an interest auction to purchase ATN interest for NTN.

The caller sends an amount of NTN to bid for interest in an interest auction.

Constraint checks are applied:

- `BidTooLow` check: the amount of NTN specified in the function call's `ntnAmount` parameter is `>` `ntnToPay`, where `ntnToPay` is the minimum interest payment, i.e. the minimum amount of NTN that the auction accepts as paymentl for the available interest
- `InsufficientAllowance` check: the bidder (i.e. the `msg.sender`) is approved with an allowance to transfer NTN that is `>` the bid `ntnAmount`.
- `TransferFailed`: the transfer of the specified `ntnAmount` to the Auctioneer contract is successful.

If constraint checks pass, and the auction bid is successful an `AuctionedInterest` event is emitted and the auction closed.
If a `proccedsAddress` has not been set for the Auctioneer contract then the auction NTN proceeds will accumulate in the Auctioneer contract until a proceeds address is set and will not be disbursed until the next successful auction bid.

If the transfer of ATN interest to the bidder fails, the ATN will remain in the contract and a `TransferFailed` event is emitted.    

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| | | |
| `auction` | `uint256` | The ID of the auction |
| `ntnAmount` | `uint256` | The amount of NTN to pay for the interest (must be greater than or equal to the minimum interest payment) |
    
#### Response

None.

#### Event

On a successful call the function emits an `AuctionedInterest` event, logging: `msg.sender`, `atnToReceive`, `ntnToPay`.

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

## Operator only WIP - MOVE TO OP-PROT REFERENCE

Functions with the `onlyOperator` access constraint that can only be called by the governance operator account.

### setLiquidationAuctionDuration (Auctioneer Contract) WIP - usage/Example TO DO

Sets a new value for the `liquidationAuctionDuration` protocol parameter. The new value will be used for auctions created after the new value was set.

The `liquidationAuctionDuration` value is set as a number of blocks.

Constraint checks are applied:

- `InvalidParameter`: the new liquidation auction `duration` value cannot be `0`.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `duration ` | `uint256` | a positive integer value specifying the number of blocks defining the duration of a liquidation auction |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `liquidationAuctionDuration` event, logging: configuration parameter `name`, `oldValue`, `newValue`.

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

### setInterestAuctionDuration (Auctioneer Contract) WIP - usage/Example TO DO

Sets a new value for the `interestAuctionDuration` protocol parameter. The new value will be used for auctions created after the new value was set.

The `liquidationAuctionDuration` value is set as a number of blocks.

Constraint checks are applied:

- `InvalidParameter`: the new interest auction `duration` value cannot be `0`.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `duration ` | `uint256` | a positive integer value specifying the number of blocks defining the duration of an interest auction |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits an `interestAuctionDuration` event, logging: configuration parameter `name`, `oldValue`, `newValue`.

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

### GOT TO HERE - NEXT

https://github.com/autonity/autonity/blob/f05aa9b476048daa5ad3a15bce6367d4424db761/autonity/solidity/contracts/asm/Auctioneer.sol#L262


### setInterestAuctionDiscount (Auctioneer Contract) TO DO
### setInterestAuctionThreshold (Auctioneer Contract) TO DO
### setProceedAddress (Auctioneer Contract) TO DO


## Auction View functions TO DO

Then back to public get functions:




And then back to public view / pure functions to get state data.
