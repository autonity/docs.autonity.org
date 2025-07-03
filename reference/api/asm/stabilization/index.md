---
title: "Stabilization Contract Interface"

description: >
  Stabilization Contract functions
---

Interfaces for interacting with the ASM Stabilization Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Stabilization Contract's generated ABI and the `aut` tool's `contract` command to call the Stabilization Contract address `0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Stabilization.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Stabilization.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
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
- `InsufficientAllowance`: the `amount` deposited is `<` the `allowance` amount that the CDP owner has approved the CDP contract to transfer.
- `Liquidatable`: if the CDP is in a liquidatable state, the deposited amount is large enough to make the CDP non-liquidatable.

::: {.callout-note title="`Liquidatable` check" collapse="false"}
This constraint prevents a CDP Owner trying to update their CDP's timestamp to influence a liquidation auction. So if you deposit while liquidatable, the deposit must be big enough to make you non-liquidatable.
:::

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


### withdraw

Request a withdrawal of Collateral Token from a CDP.

On method execution, state is inspected to retrieve:

- the CDP principal, collateral, and debt amounts
- the minimum collateralization and liquidation ratios from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- `InvalidAmount`: the `amount` withdrawn is `<` the CDP's collateral amount 
- `Insufficient Collateral`: the withdrawn `amount` must not reduce the remaining Collateral Token amount below the minimum collateral ratio.
- `Liquidatable`: withdrawal does not make the CDP liquidatable. The withdrawn amount value must not reduce the CDP to an under collateralized state below the liquidation ratio.

The CDP's collateral balance is then decremented by the withdrawn amount and Collateral Token is transferred to the CDP owner.


#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | Units of Collateral Token to withdraw (non-zero) |

#### Response

None.

#### Event

On a successful call the function emits a `Withdraw` event, logging: `msg.sender`, `amount`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw amount
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw 1000000000000000000 | aut tx sign - | aut tx send -
```
:::


### borrow

Borrow Auton against CDP Collateral.

On method execution, state is inspected to retrieve:

- the current CDP borrow limit, and debt and accrued interest amounts
- the minimum collateralization and liquidation ratios, and the minimum debt requirement from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- `InvalidDebtPosition`: the `debt` after borrowing must satisfy the minimum debt requirement.
- `Liquidatable`: borrowing does not make the CDP liquidatable. The `debt` after borrowing amount value must not reduce the CDP to an under collateralized state below the liquidation ratio.
- `InsufficientCollateral`: the borrowed `amount` must not exceed the borrow `limit` for the CDP. The `debt` after borrowing must not reduce the CDP to an under collateralized state below the minimum collateral ratio.

The CDP's debt is then incremented by the borrowed amount and Auton is minted to the CDP owner.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | Amount of Auton to borrow (non-zero) |

#### Response

None.

#### Event

On a successful call the function emits a `Borrow` event, logging: `msg.sender`, `amount`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrow amount
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrow 1000000000000000000 | aut tx sign - | aut tx send -
```
:::


### repay

Make a payment towards a CDP debt. The transaction value is the payment amount.

On method execution, state is inspected to retrieve:

- the current CDP principal amount, and debt and accrued interest amounts
- the minimum collateralization and liquidation ratios, and the minimum debt requirement from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- `NoDebtPosition`: there is a debt; the CDP `principal` is `> 0`.
- `InvalidDebtPosition`: the debt after payment must satisfy the minimum debt requirement. The payment amount is `<` the `debt` and the `debt` after the payment amount satisfies the minimum debt requirement.

The payment is allocated to first cover outstanding interest debt on the CDP, and then repay CDP principal debt. If there is a surplus after principal repayment, then the surplus is returned to the CDP Owner.


#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `msg.value` | `uint256` | The payment amount |


#### Response

None.

#### Event

On a successful call the function emits a `Repay` event, logging: `msg.sender`, `msg.value`.


#### Usage

::: {.callout-note title="Note" collapse="false"}
Use the `aut tx` command, specifying the Stabilization Contract address as the `RECIPIENT` address.
:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value amount repay
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value 1 repay | aut tx sign - | aut tx send -
```
:::


## CDP Keeper functions (Auctioneer Contract Only)


### liquidate

Liquidates a CDP that is undercollateralized. Invoked by the Auctioneer Contract's [`bidDebt()`](/reference/api/asm/auctioneer/#biddebt) function when a liquidator bids for the debt of a liquidatable CDP.

The liquidator must pay all the CDP debt outstanding. As a reward, the liquidator will receive the collateral that is held in the CDP. The transaction value is the payment amount.

On method execution, state is inspected to retrieve:

- the current CDP debt, collateral, and accrued interest amounts
- the liquidation ratio from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- no debt position: there is a debt to liquidate; the CDP `principal` is `> 0`.
- not liquidatable: the CDP is under collateralized and eligible for liquidation.
- insufficient payment: the payment amount is sufficient to pay off the CDP debt (principal and  accrued interest). After covering the debt the surplus remaining from the payment is `>= 0`.

On processing the payment:

- the CDP's debt is paid off and any payment surplus is refunded to the liquidator
- the CDP's Collateral Token is transferred to the liquidator
- Auton to the value of the CDP's debt is burnt.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | The CDP account address to liquidate |
| `msg.value` | `uint256` | The payment amount |

#### Response

None.

#### Event

On a successful call the function emits a `Liquidate ` event, logging: `account`, `msg.sender`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value amount liquidate account
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value 2500000000000000000 liquidate 0x1f790c60D974F5A8f88558CA90F743a71F009641 | aut tx sign - | aut tx send -
```
:::


## CDP View functions

### accounts

Retrieve all the accounts that have opened a CDP.

#### Parameters

None.

#### Response
Returns an `_accounts` array of CDP account addresses:


| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | The CDP account address |

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f accounts
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f accounts
["0x1f790c60D974F5A8f88558CA90F743a71F009641"]
```
:::


### acuPrice

Returns a USD price for the [ACU](/concepts/asm/#acu) value in `SCALE_FACTOR` precision used by the Stabilization Contract.

If a default fixed price has been set for ACU-USD, then that price is returned from config (See [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract)).

Else, the function retrieves the ACU index value and scale factor from the ACU Contract, and converts it to a USD value scaled to the precision used by the Stabilization Contract.

If an ACU-USD price cannot be computed the function reverts with a `PriceUnavailable` error.

::: {.callout-note title="How the price is scaled and computed" collapse="true"}
The function converts the ACU index value retrieved from the ACU Contract to `SCALE` decimals used by the Stabilisation Contract.

Conversion is conditional upon the difference between the Stabilization Contract and ACU Contract scale and precision:

  `(value * SCALE_FACTOR) / valueScaleFactor`

Where:

- `value` is the ACU index value
- `SCALE_FACTOR` is the Stabilisation Contract multiplier for scaling numbers to the required scale of decimal places in fixed-point integer representation. `SCALE_FACTOR = 10 ** SCALE`
- `SCALE` is the Stabilisation Contract setting for decimal places in fixed-point integer representation. `SCALE = 18`.
- `valueScaleFactor` is the ACU Contract scale factor.
:::

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| `price` | `uint256` | Price of ACU index value in USD |

#### Event

None.

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


### borrowLimit

Calculates the maximum amount of Auton that can be borrowed for the given amount of Collateral Token.
    
Constraint checks are applied:

- invalid parameter: the `price` and `mcr` argument values are valid, i.e. are not equal to `0`.

::: {.callout-note title="Note" collapse="false"}
The borrowing limit amount is calculated by `(collateral * price * targetPrice) / (mcr * SCALE_FACTOR)`.

Where:

- `SCALE_FACTOR` is the Stabilisation Contract multiplier for scaling numbers to the required scale of decimal places in fixed-point integer representation. `SCALE_FACTOR = 10 ** SCALE`.
- `SCALE` is the Stabilisation Contract setting for decimal places in fixed-point integer representation. `SCALE = 18`.
:::

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `collateral` | `uint256` | Amount of Collateral Token backing the debt |
| `collateralPriceACU` | `uint256` | The price of Collateral Token in ACU |
| `targetPriceACU` | `uint256` | The ACU value of 1 unit of debt |
| `mcr` | `uint256` | The minimum collateralization ratio |
    
::: {.callout-note title="Note" collapse="false"}
For the default values set for `targetPrice` and `mcr` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object).

The current `price` value can be returned by calling [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice).
:::

#### Response

The function returns the maximum amount of Auton that can be borrowed as an `uint256` integer value.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrowLimit collateral price targetPrice mcr
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrowLimit 4000000000000000000 9816500000000000000 1000000000000000000 2000000000000000000
19633000000000000000
```
:::


### cdps

Retrieve the state for a CDP account.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `owner` | `address` | The CDP account address |

#### Response
Returns a `_cdps` Collateralized Debt Position (CDP) account object:

| Field | Datatype | Description |
| --| --| --|
| `timestamp` | `uint` | The timestamp of the last borrow or repayment. The timestamp is provided as a [Unix time](/glossary/#unix-time) value  |
| `collateral` | `uint256` | The collateral deposited with the Stabilization Contract |
| `principal` | `uint256` | The principal debt outstanding as of `timestamp` |
| `interest` | `uint256` | The interest debt that is due at the `timestamp` |
| `lastAggregatedInterestExponent` | `uint256` |  The aggregated interest exponent till last update |    
    
#### Event

None.

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


### collateralPrice

Returns the NTN Collateral Token price in ATN.

If a default fixed price has been set for NTN-ATN, then that price is returned from config (See [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract)).

Else, the function retrieves the aggregated median NTN-ATN price from the Oracle Contract.

Constraint checks are applied:

- `InvalidPrice`: the NTN-ATN `price` returned by the Oracle Contract is not `<= 0`.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| `price` | `uint256` | Price of NTN Collateral Token in ATN|

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f collateralPrice
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f collateralPrice
10019717700000000000
```
:::


### collateralPriceACU

Returns the NTN Collateral Token price in [ACU](/glossary/#acu).

Constraint checks are applied:

- `InvalidPrice`: the NTN-USD `price` returned by the Oracle Contract is not `<= 0`.

::: {.callout-note title="How the price is scaled and computed" collapse="true"}
The function computes the NTN-ACU price by:

  `ntnUsdPrice * SCALE_FACTOR / acuUsd`

Where:

- `ntnUsdPrice` is the NTN-USD price, either:
  - a default fixed price from config if set (See [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract))
  - else, the aggregated median price calculated by the Oracle Contract (returned by calling [`latestRoundData()`](/reference/api/oracle/#latestrounddata)).
- `SCALE_FACTOR` is the Stabilisation Contract multiplier for scaling numbers to the required scale of decimal places in fixed-point integer representation. `SCALE_FACTOR = 10 ** SCALE`.
- `SCALE` is the Stabilisation Contract setting for decimal places in fixed-point integer representation. `SCALE = 18`.
- `acuUsd` is the ACU-USD price, either:
  - a default fixed price from config if set (See [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract))
  - else, the ACU-USD price calculated by the Stabilisation Contract (as described in [`acuPrice()`](/reference/api/asm/stabilization/#acuprice)), see note **How the price is scaled and computed**.)

:::

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| `price` | `uint256` | Price of NTN Collateral Token in ACU |

#### Event

None.

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


### config

Returns the Stabilization Contract configuration at the block height the call was submitted.

#### Parameters

None.

#### Response

Returns a `Config` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `borrowInterestRate` | `uint256` | The annual continuously-compounded interest rate for borrowing |
| `announcementWindow` | `uint256` | The minimum ACU value of collateral required to maintain 1 ACU value of debt |
| `liquidationRatio` | `uint256` |  |
| `minCollateralizationRatio` | `uint256` | The minimum ACU value of collateral required to borrow 1 ACU value of debt |
| `minDebtRequirement` | `uint256` | The minimum amount of debt required to maintain a CDP |
| `targetPrice` | `uint256` | The ACU value of 1 unit of debt |
| `defaultNTNATNPrice` | `uint256` | The default NTN-ATN price for use at genesis if fixed prices are enabled |
| `defaultNTNUSDPrice` | `uint256` | The default NTN-USD price for use at genesis if fixed prices are enabled |
| `defaultACUUSDPrice` | `uint256` | the default ACU-USD price for use if fixed prices are enabled |

For enabling fixed prices see the governance function  [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract).

#### Event

None.

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


### debtAmount

Calculates the current debt amount outstanding for a CDP at the block height of the call.

Constraint checks are applied:

- good time: the block `timestamp` at the time of the call must be equal to or later than the CDP's `timestamp` attribute, i.e. the time of the CDP's last borrow or repayment (ensuring current and future liquidability is tested).

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | the CDP account address |

#### Response

| Field | Datatype | Description |
| --| --| --|
| `debt` | `uint256` | The debt amount |

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount account timestamp
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount 0x1f790c60D974F5A8f88558CA90F743a71F009641 1695740525
300012369185855391
```
:::

### debtAmountAtTime

Calculates the current debt amount outstanding for a CDP at the given timestamp.

Constraint checks are applied:

- good time: the block `timestamp` at the time of the call must be equal to or later than the CDP's `timestamp` attribute, i.e. the time of the CDP's last borrow or repayment (ensuring current and future liquidability is tested).

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | the CDP account address |
| `timestamp` | `uint` | the timestamp to value the debt. The timestamp is provided as a [Unix time](/glossary/#unix-time) value |

#### Response

| Field | Datatype | Description |
| --| --| --|
| `debt` | `uint256` | The debt amount |

#### Event

None.

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

### getAggregatedInterestExponent

Return the aggregated interest exponent.

This is calculated as the summation of all interest rates multiplied by their respective time window (in years) up to the timestamp of the last committed block.
 
#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| aggregated interest exponent | `uint256` | The aggregated interest exponent value |

#### Event

None.

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


### getAnnouncementWindow

Return the current active announcement window.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| current announcement window  | `uint256` | The current announcement window value in seconds |

#### Event

None.

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


### getCurrentRate

Return the current active borrow interest rate.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| current rate  | `uint256` | The current interest rate value |

#### Event

None.

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


### getCurrentRateActiveTimestamp

Return the timestamp since when the current borrow interest rate is active.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| current rate active timestamp | `uint256` | The timestamp since when the current interest rate is active |

#### Event

None.

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


### getPendingAnnouncementWindowInfo

Return the pending announcement window and the time it will become active.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| pending announcement window | `uint256` | The pending borrow interest rate value |
| pending announcement window active timestamp | `uint256` | The timestamp since when the pending announcement window will be active |

#### Event

None.

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


### getPendingInterestRateInfo

Return the pending borrow interest rate and the time it will become active.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| pending rate | `uint256` | The pending borrow interest rate value |
| pending rate active timestamp | `uint256` | The timestamp since when the pending interest rate will be active |

#### Event

None.

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


### getPendingLiquidationRatioInfo

Return the pending liquidation ratio and the time it will become active.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| pending liquidation ratio | `uint256` | The pending liquidation ratio value|
| pending liquidation n ratio active timestamp | `uint256` | The timestamp since when the pending liquidation ratio will be active |

#### Event

None.

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


### getPendingMinCollateralizationRatioInfo

Return the pending minimum collateralization ratio and the time it will become active.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| pending minimum collateralization ratio | `uint256` | The pending minimum collateralization ratio value |
| pending minimum collateralization ratio active timestamp | `uint256` | The timestamp since when the pending minimum collateralization ratio will be active |

#### Event

None.

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


### interestDue

Calculates the interest due for a given amount of debt.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `debt` | `uint256` | The debt amount |
| `rateExponent` | `uint256` | The summation of the interest rates multiplied by their respective time window |

::: {.callout-note title="Note" collapse="false"}

Users can also determine their interest owed by `debtAmount(account) - cdps(account).principal`.

See [`debtAmount()`](/reference/api/asm/stabilization/#debtAmount) and [`cdps()`](/reference/api/asm/stabilization/#cdps).

For how to get the rate exponent for a given interest rate see  [`interestExponent()`](/reference/api/asm/stabilization/#interestexponent).

:::
  
#### Response

The function returns the amount of interest due as an `uint256` integer value.

#### Event

None.

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


### interestExponent

Calculates the interest exponent for the given rate in the given time window.

Constraint checks are applied:

- `InvalidParameter`: the `endTimestamp` must be `>` than the `startTimestamp`.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `interestRate ` | `uint256` | The interest rate |
| `startTimestamp` | `uint256` | The start timestamp of the window in seconds |
| `endTimestamp` | `uint256` | The end timestamp of the window in seconds |

::: {.callout-note title="Note" collapse="false"}

Users can also determine their interest owed by `debtAmount(account) - cdps(account).principal`.

See [`debtAmount()`](/reference/api/asm/stabilization/#debtAmount) and [`cdps()`](/reference/api/asm/stabilization/#cdps).
:::
  
#### Response

The function returns the interest exponent as an `uint256` integer value.

#### Event

None.

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


### isLiquidatable

Determines if a CDP is liquidatable at the block height of the call.

Constraint checks are applied:

- good time: the block `timestamp` at the time of the call must be equal to or later than the CDP's `timestamp` attribute, i.e. the time of the CDP's last borrow or repayment (ensuring current and future liquidability is tested). 
 

::: {.callout-note title="Note" collapse="false"}
The function tests liquidatibility by calling [`underCollateralized()`](/reference/api/asm/stabilization/#undercollateralized).
:::

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | The CDP account address |

#### Response

The function returns a `Boolean` flag indicating if the CDP is liquidatable (`True`) or not (`False`).

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f isLiquidatable account
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f isLiquidatable 0x1f790c60D974F5A8f88558CA90F743a71F009641
false
```
:::


### lastUpdated

Return the last updated timestamps of the Stabilization Contract's updatable config parameters `borrowInterestRate`, `announcementWindow`, `liquidationRatio`, `minCollateralizationRatio`.
            
#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| borrow interest rate active timestamp | `uint256` | The timestamp since when the current interest rate value is active |
| announcement window active timestamp | `uint256` | The timestamp since when the current announcement window value is active |
| liquidation ratio active timestamp | `uint256` | The timestamp since when the current liquidation ratio is active |
| minimum collateralization ratio active timestamp | `uint256` | The timestamp since when the current minimum collateralization ratio is active |

#### Event

None.

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


### liquidationRatio

Return the current liquidation ratio.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| liquidation ratio  | `uint256` | The current liquidation ratio value |

#### Event

None.

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


### maxBorrow

Calculates the maximum amount of Auton that can be borrowed for the given amount of Collateral Token.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `collateral` | `uint256` | Amount of Collateral Token backing the borrowing |

#### Response

The function returns the maximum amount of Auton that can be borrowed as an `uint256` integer value.

#### Event

None.

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


### minCollateralizationRatio

Return the minimum collateralization ratio.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| minimum collateralization ratio  | `uint256` | The current minimum collateralization ratio value |

#### Event

None.

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


### minimumCollateral

Calculates the minimum amount of Collateral Token that must be deposited in the CDP in order to borrow the given amount of Autons.

Constraint checks are applied:

- invalid parameter: the `price` and `mcr` argument values are valid, i.e. are not equal to `0`.

::: {.callout-note title="Note" collapse="false"}
The minimum collateral amount is calculated by `(principal * mcr) / price`.
:::

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `principal` | `uint256` | Auton amount to borrow |
| `collateralPriceACU ` | `uint256` | The price of Collateral Token in ACU |
| `targetPriceACU` | `uint256` | The ACU value of 1 unit of debt |
| `mcr` | `uint256` | The minimum collateralization ratio |

::: {.callout-note title="Note" collapse="false"}
For the default value set for `mcr` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object).

The current `price` value can be returned by calling [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice).
:::

#### Response

The function returns the minimum collateral required as an `uint256` integer value.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f minimumCollateral principal price mcr
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f minimumCollateral 1000000000000000000 9672000000000000000 2000000000000000000
206782464846980976
```
:::


### underCollateralized

Determine if a debt position is undercollateralized.

Constraint checks are applied:

- invalid price: the value of the `price` argument is valid, i.e. it is not equal to `0`.

If the CDP is under collateralized, then it can be liquidated - see [`liquidate()`](/reference/api/asm/stabilization/#liquidate).

::: {.callout-note title="Note" collapse="false"}
If a debt position is under collateralized or not is determined by calculating `(collateral * price) / debt`. If this returns a value `< liquidationRatio`, then the CDP is under collateralised and can be liquidated.
:::

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `collateral` | `uint256` | Amount of Collateral Token backing the debt |
| `price` | `uint256` | The price of Collateral Token in Auton |
| `debt` | `uint256` | The debt amount |
| `liquidationRatio` | `uint256` | The liquidation ratio |

::: {.callout-note title="Note" collapse="false"}
For the default value set for `liquidationRatio` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object).

The current `price` value can be returned by calling [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice).
:::

#### Response

The method returns a boolean flag specifying whether the CDP is undercollateralized (`true`) or not (`false`).

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized collateral price debt liquidationRatio
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized 206782464846980976 9672000000000000000 1000000000000000000 1800000000000000000
false
```
:::
