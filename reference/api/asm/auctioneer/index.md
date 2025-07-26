---
title: "Auctioneer Contract Interface"

description: >
  Auctioneer Contract functions
---

Interfaces for interacting with the ASM Auctioneer Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Auctioneer Contract's generated ABI and the `aut` tool's `contract` command to call the Auctioneer Contract address `0x6901F7206A34E441Ac5020b5fB53598A65547A23`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Auctioneer.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Stabilization.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::

## Auction Bidder

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

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
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
| `auction` | `uint256` | The ID of the auction |
| `ntnAmount` | `uint256` | The amount of NTN to pay for the interest (must be greater than or equal to the minimum interest payment) |
    
#### Response

None.

#### Event

On a successful call the function emits an `AuctionedInterest` event, logging: `msg.sender`, `atnToReceive`, `ntnToPay`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


## Auction View functions

### openAuctions

Returns all open interest auctions.

#### Parameters

None.
    
#### Response

Returns an array of `auction` objects consisting of:

| Field | Datatype | Description |
|:-- |:-- |:-- |
| `id` | `uint256` | the unique identifier of the auction |
| `amount` | `uint256` | the amount of ATN received from interest payments that is being auctioned |
| `startPrice` | `uint256` | the reserve price for the auction |
| `startTimestamp` | `uint256` | the opening time for the auction |

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### getAuction

Get an interest auction by ID.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `auction` | `uint256` | The ID of the auction |
    
#### Response

Returns an `auction` object consisting of:

| Field | Datatype | Description |
|:-- |:-- |:-- |
| `id` | `uint256` | the unique identifier of the auction |
| `amount` | `uint256` | the amount of ATN received from interest payments that is being auctioned |
| `startPrice` | `uint256` | the reserve price for the auction |
| `startTimestamp` | `uint256` | the opening time for the auction |

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### maxLiquidationReturn

Get the maximum amount of NTN that can be returned to a liquidator for a given CDP.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `debtor` | `address` | the address of the CDP owner |
| `liquidatableRound` | `uint256` | the earliest round in which the CDP was liquidatable |
    
#### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the maximum amount of NTN that can be received |

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### minInterestPayment

Get the minimum amount of NTN that can be paid for an interest auction.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `id` | `uint256` | the unique identifier of the auction |
    
#### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the minimum amount of NTN that can be paid |

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### getConfig

Returns the current Auctioneer Contract configuration.

#### Parameters

None.
    
#### Response

Returns a `config` object consisting of:

| Field | Datatype | Description |
|:-- |:-- |:-- |
| `liquidationAuctionDuration` | `uint256` | defines the number of blocks for an interest auction to move from the starting price to the floor price |
| `interestAuctionDuration` | `uint256` | the duration of an interest auction in seconds |
| `interestAuctionDiscount` | `uint256` | defines the discount rate for the starting price of an interest auction (set as a value between $[0,1)$ with $10 \hat{\ } 18$ precision) |
| `interestAuctionThreshold` | `uint256` | defines the total amount of accumulated ATN from interest payments required for triggering an auction for CDP interest proceeds |

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

### getCollateralToken

Returns the address of the CDP collateral token.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| `collateralToken` | `address` | the collateral token contract account address |

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### getProceedAddress

Returns the proceed address of the ASM auction.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| `proceedAddress` | `address` | the collateral token contract account address |

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::
