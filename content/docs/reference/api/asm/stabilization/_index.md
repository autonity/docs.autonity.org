---
title: "Stabilization Contract Interface"
linkTitle: "Stabilization Contract Interface"
weight: 30

description: >
  Stabilization Contract functions
---

Interfaces for interacting with the ASM Stabilization Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

{{% pageinfo %}}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Stabilization Contract's generated ABI and the `aut` tool's `contract` command to call the Stabilization Contract address `0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Stabilization.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Stabilization.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
{{% /pageinfo %}}

## CDP Owner
### deposit

Deposit Collateral Token to a CDP using the ERC20 allowance mechanism.

Before calling this function, the CDP owner must approve the Stabilization contract to spend Collateral Token on their behalf for the full amount to be deposited.

{{< alert title="Info" >}}
You can approve the Stabilization Contract as a spender of Newton Collateral Token using the `aut` command `aut token approve [OPTIONS] SPENDER AMOUNT`.
{{< /alert >}}

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

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f deposit amount
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f deposit 1000000000000000000 | aut tx sign - | aut tx send -
{{< /tab >}}
{{< /tabpane >}}


### withdraw

Request a withdrawal of Collateral Token from a CDP.

On method execution, state is inspected to retrieve:

- the CDP principal, collateral, and debt amounts
- the minimum collateralization and liquidation ratios from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- invalid amount: the `amount` withdrawn is `<` the CDP's collateral amount 
- insufficient collateral: the withdrawn `amount` must not reduce the remaining Collateral Token amount below the minimum collateral ratio.
- liquidatable: withdrawal does not make the CDP liquidatable. The withdrawn amount value must not reduce the CDP to an under collateralized state below the liquidation ratio.

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

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw amount
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw 1000000000000000000 | aut tx sign - | aut tx send -
{{< /tab >}}
{{< /tabpane >}}

### borrow

Borrow Auton against CDP Collateral.

On method execution, state is inspected to retrieve:

- the current CDP borrow limit, and debt and accrued interest amounts
- the minimum collateralization and liquidation ratios, and the minimum debt requirement from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- invalid debt position: the `debt` after borrowing must satisfy the minimum debt requirement.
- liquidatable: borrowing does not make the CDP liquidatable. The `debt` after borrowing amount value must not reduce the CDP to an under collateralized state below the liquidation ratio.
- insufficient collateral: the borrowed `amount` must not exceed the borrow `limit` for the CDP. The `debt` after borrowing must not reduce the CDP to an under collateralized state below the minimum collateral ratio.

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

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrow amount
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrow 1000000000000000000 | aut tx sign - | aut tx send -
{{< /tab >}}
{{< /tabpane >}}


### repay

Make a payment towards a CDP debt. The transaction value is the payment amount.

On method execution, state is inspected to retrieve:

- the current CDP principal amount, and debt and accrued interest amounts
- the minimum collateralization and liquidation ratios, and the minimum debt requirement from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- no debt position: there is a debt; the CDP `principal` is `> 0`.
- invalid debt position: the debt after payment must satisfy the minimum debt requirement. The payment amount is `<` the `debt` and the `debt` after the payment amount satisfies the minimum debt requirement.

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

{{< alert title="Info" >}}
Use the `aut tx` command, specifying the Stabilization Contract address as the `RECIPIENT` address.
{{< /alert >}}

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value amount repay
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value 1 repay | aut tx sign - | aut tx send -
{{< /tab >}}
{{< /tabpane >}}


## CDP Liquidator 

### isLiquidatable

Determines if a CDP is liquidatable at the block height of the call.

Constraint checks are applied:

- good time: the block `timestamp` at the time of the call must be equal to or later than the CDP's `timestamp` attribute, i.e. the time of the CDP's last borrow or repayment (ensuring current and future liquidability is tested). 
 

{{< alert title="Info" >}}
The function tests liquidatibility by calling [`underCollateralized()`](/reference/api/asm/stabilization/#undercollateralized).
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | The CDP account address |

#### Response

The function returns a `Boolean` flag indicating if the CDP is liquidatable (`True`) or not (`False`).

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f isLiquidatable account
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f isLiquidatable 0x1f790c60D974F5A8f88558CA90F743a71F009641
false
{{< /tab >}}
{{< /tabpane >}}


### liquidate

Liquidates a CDP that is undercollateralized.

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

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value amount liquidate account
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value 2500000000000000000 liquidate 0x1f790c60D974F5A8f88558CA90F743a71F009641 | aut tx sign - | aut tx send -
{{< /tab >}}
{{< /tabpane >}}


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

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f accounts
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f accounts
["0x1f790c60D974F5A8f88558CA90F743a71F009641"]
{{< /tab >}}
{{< /tabpane >}}


### borrowLimit

Calculates the maximum amount of Auton that can be borrowed for the given amount of Collateral Token.
    
Constraint checks are applied:

- invalid parameter: the `price` and `mcr` argument values are valid, i.e. are not equal to `0`.

{{< alert title="Info" >}}
The borrowing limit amount is calculated by `(collateral * price * targetPrice) / (mcr * SCALE_FACTOR)`.

Where:

- `SCALE_FACTOR` is the Stabilisation Contract multiplier for scaling numbers to the required scale of decimal places in fixed-point integer representation. `SCALE_FACTOR = 10 ** SCALE`.
- `SCALE` is the Stabilisation Contract setting for decimal places in fixed-point integer representation. `SCALE = 18`.
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `collateral` | `uint256` | Amount of Collateral Token backing the debt |
| `price` | `uint256` | The price of Collateral Token in Auton |
| `targetPrice` | `uint256` | The ACU value of 1 unit of debt |
| `mcr` | `uint256` | The minimum collateralization ratio |

{{< alert title="Info" >}}
For the default values set for `targetPrice` and `mcr` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object).

The current `price` value can be returned by calling [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice).
{{< /alert >}}

#### Response

The function returns the maximum amount of Auton that can be borrowed as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrowLimit collateral price targetPrice mcr
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrowLimit 4000000000000000000 9816500000000000000 1000000000000000000 2000000000000000000
19633000000000000000
{{< /tab >}}
{{< /tabpane >}}


### collateralPrice

Retrieves the Collateral Token price from the Oracle Contract and converts it to Auton.

The function reverts in case the price is invalid or unavailable.

Constraint checks are applied:

- price unavailable: the Oracle Contract is providing data computed in the oracle network's last completed voting round.

{{< alert title="Info" >}}
To get this data the Oracle Contract function [`latestRoundData()`](/reference/api/oracle/#latestrounddata) is called. This returns the latest available median price data for a currency pair symbol. If the last oracle voting round failed to successfully compute a new median price, then it will return the most recent median price for the requested symbol.
{{< /alert >}}

- invalid price: the `price` returned by the Oracle Contract is not equal to `0`.

On method execution, state is inspected to retrieve:

- the latest computed Collateral Token price data and the Oracle Contract scale precision from the Oracle Contract.

{{< alert title="Info" >}}
The function converts the Collateral Token price retrieved from the Oracle Contract to `SCALE` decimals used by the Stabilisation Contract.

Conversion is conditional upon the difference between the Stabilisation Contract and Oracle Contract scale and precision:

- if `(SCALE_FACTOR > precision)`, then collateral price = `price * (SCALE_FACTOR / precision`
- else collateral price = `price / (precision() / SCALE_FACTOR)`.

Where:

- `SCALE_FACTOR` is the Stabilisation Contract multiplier for scaling numbers to the required scale of decimal places in fixed-point integer representation. `SCALE_FACTOR = 10 ** SCALE`.
- `SCALE` is the Stabilisation Contract setting for decimal places in fixed-point integer representation. `SCALE = 18`.
- `price` is the aggregated median price for Collateral Token calculated by the Oracle Contract (returned by calling [`latestRoundData()`](/reference/api/oracle/#latestrounddata)).
- `precision` is the Oracle Contract setting for the multiplier applied to submitted data price reports before calculation of an aggregated median price for a symbol (returned by calling [`getPrecision()`](/reference/api/oracle/#getprecision)).
{{< /alert >}}

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| `price` | `uint256` | Price of Collateral Token |

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f collateralPrice
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f collateralPrice
10019717700000000000
{{< /tab >}}
{{< /tabpane >}}


### debtAmount

Calculates the current debt amount outstanding for a CDP at the block height of the call.

Constraint checks are applied:

- good time: the block `timestamp` at the time of the call must be equal to or later than the CDP's `timestamp` attribute, i.e. the time of the CDP's last borrow or repayment (ensuring current and future liquidability is tested).

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | the CDP account address |
| `timestamp` | `uint` | the timestamp to value the debt. The timestamp is provided as a [Unix time](/glossary/#unix-time) value |

#### Response

The function returns the debt amount as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount account timestamp
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount 0x1f790c60D974F5A8f88558CA90F743a71F009641 1695740525
300012369185855391
{{< /tab >}}
{{< /tabpane >}}


### interestDue

Calculates the interest due for a given amount of debt.

Constraint checks are applied:

- invalid parameter: the `timeBorrow` argument is not greater than the `timeDue` argument value.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `debt` | `uint256` | The debt amount |
| `rate` | `uint256` | The borrow interest rate |
| `timeBorrow` | `uint` | The borrow time. The timestamp is provided as a [Unix time](/glossary/#unix-time) value |
| `timeDue` | `uint` | The time the interest is due. The timestamp is provided as a [Unix time](/glossary/#unix-time) value |

{{< alert title="Info" >}}
For the default value set for `rate` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object).
{{< /alert >}}
  
#### Response

The function returns the amount of interest due as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f interestDue debt rate timeBorrow timeDue
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f interestDue 1000000000000000000 50000000000000000 1695308566 1697900566
4118044981651418
{{< /tab >}}
{{< /tabpane >}}


### minimumCollateral

Calculates the minimum amount of Collateral Token that must be deposited in the CDP in order to borrow the given amount of Autons.

Constraint checks are applied:

- invalid parameter: the `price` and `mcr` argument values are valid, i.e. are not equal to `0`.

{{< alert title="Info" >}}
The minimum collateral amount is calculated by `(principal * mcr) / price`.
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `principal` | `uint256` | Auton amount to borrow |
| `price` | `uint256` | The price of Collateral Token in Auton |
| `mcr` | `uint256` | The minimum collateralization ratio |

{{< alert title="Info" >}}
For the default value set for `mcr` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object).

The current `price` value can be returned by calling [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice).
{{< /alert >}}

#### Response

The function returns the minimum collateral required as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f minimumCollateral principal price mcr
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f minimumCollateral 1000000000000000000 9672000000000000000 2000000000000000000
206782464846980976
{{< /tab >}}
{{< /tabpane >}}


### underCollateralized

Determines if a debt position is undercollateralized or not.

Constraint checks are applied:

- invalid price: the value of the `price` argument is valid, i.e. it is not equal to `0`.

If the CDP is under collateralized, then it can be liquidated - see [`liquidate()`](/reference/api/asm/stabilization/#liquidate).

{{< alert title="Info" >}}
If a debt position is under collateralized or not is determined by calculating `(collateral * price) / debt`. If this returns a value `< liquidationRatio`, then the CDP is under collateralised and can be liquidated.
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `collateral` | `uint256` | Amount of Collateral Token backing the debt |
| `price` | `uint256` | The price of Collateral Token in Auton |
| `debt` | `uint256` | The debt amount |
| `liquidationRatio` | `uint256` | The liquidation ratio |

{{< alert title="Info" >}}
For the default value set for `liquidationRatio` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object).

The current `price` value can be returned by calling [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice).
{{< /alert >}}

#### Response

The method returns a boolean flag specifying whether the CDP is undercollateralized (true) or not (false).

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized collateral price debt liquidationRatio
{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized 206782464846980976 9672000000000000000 1000000000000000000 1800000000000000000
false
{{< /tab >}}
{{< /tabpane >}}


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

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}


### debtAmount

Calculates the current debt amount outstanding for a CDP at the block height of the call.

Constraint checks are applied:

- good time: the block `timestamp` at the time of the call must be equal to or later than the CDP's `timestamp` attribute, i.e. the time of the CDP's last borrow or repayment (ensuring current and future liquidability is tested).

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | The CDP account address to liquidate |

#### Response

The function returns the debt amount as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}


### isLiquidatable

Determines if a CDP is liquidatable at the block height of the call.

Constraint checks are applied:

- good time: the block `timestamp` at the time of the call must be equal to or later than the CDP's `timestamp` attribute, i.e. the time of the CDP's last borrow or repayment (ensuring current and future liquidability is tested). 
 

{{< alert title="Info" >}}
The function tests liquidatibility by calling [`underCollateralized()`](/reference/api/asm/stabilization/#undercollateralized).
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | The CDP account address |
<!--
| `timestamp` | `uint` | The timestamp at which the CDP liquidatability is being queried |
-->

#### Response

The function returns a `Boolean` flag indicating if the CDP is liquidatable (`True`) or not (`False`).

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

### collateralPrice

Retrieves the Collateral Token price from the Oracle Contract and converts it to Auton.

The function reverts in case the price is invalid or unavailable.

Constraint checks are applied:

- price unavailable: the Oracle Contract is providing data computed in the oracle network's last completed voting round.

{{< alert title="Info" >}}
To get this data the Oracle Contract function [`latestRoundData()`](/reference/api/oracle/#latestrounddata) is called. This returns the latest available median price data for a currency pair symbol. If the last oracle voting round failed to successfully compute a new median price, then it will return the most recent median price for the requested symbol.
{{< /alert >}}

- invalid price: the `price` returned by the Oracle Contract is not equal to `0`.

On method execution, state is inspected to retrieve:

- the latest computed Collateral Token price data and the Oracle Contract scale precision from the Oracle Contract.

{{< alert title="Info" >}}
The function converts the Collateral Token price retrieved from the Oracle Contract to `SCALE` decimals used by the Stabilisation Contract.

Conversion is conditional upon the difference between the Stabilisation Contract and Oracle Contract scale and precision:

- if `(SCALE_FACTOR > precision)`, then collateral price = `price * (SCALE_FACTOR / precision`
- else collateral price = `price / (precision() / SCALE_FACTOR)`.

Where:

- `SCALE_FACTOR` is the Stabilisation Contract multiplier for scaling numbers to the required scale of decimal places in fixed-point integer representation. `SCALE_FACTOR = 10 ** SCALE`.
- `SCALE` is the Stabilisation Contract setting for decimal places in fixed-point integer representation. `SCALE = 18`.
- `price` is the aggregated median price for Collateral Token calculated by the Oracle Contract (returned by calling [`latestRoundData()`](/reference/api/oracle/#latestrounddata)).
- `precision` is the Oracle Contract setting for the multiplier applied to submitted data price reports before calculation of an aggregated median price for a symbol (returned by calling [`getPrecision()`](/reference/api/oracle/#getprecision)).
{{< /alert >}}

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| `price` | `uint256` | Price of Collateral Token |

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

### borrowLimit

Calculates the maximum amount of Amount that can be borrowed for the given amount of Collateral Token.
    
Constraint checks are applied:

- invalid parameter: the `price` and `mcr` argument values are valid, i.e. are not equal to `0`.

{{< alert title="Info" >}}
The borrowing limit amount is calculated by `(collateral * price * targetPrice) / (mcr * SCALE_FACTOR)`.

Where:

- `SCALE_FACTOR` is the Stabilisation Contract multiplier for scaling numbers to the required scale of decimal places in fixed-point integer representation. `SCALE_FACTOR = 10 ** SCALE`.
- `SCALE` is the Stabilisation Contract setting for decimal places in fixed-point integer representation. `SCALE = 18`.
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `collateral` | `uint256` | Amount of Collateral Token backing the debt |
| `price` | `uint256` | The price of Collateral Token in Auton |
| `targetPrice` | `uint256` | The ACU value of 1 unit of debt |
| `mcr` | `uint256` | The minimum collateralization ratio |

#### Response

The function returns the maximum amount of Auton that can be borrowed as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

### minimumCollateral

Calculates the minimum amount of Collateral Token that must be deposited in the CDP in order to borrow the given amount of Autons.

Constraint checks are applied:

- invalid parameter: the `price` and `mcr` argument values are valid, i.e. are not equal to `0`.

{{< alert title="Info" >}}
The minimum collateral amount is calculated by `(principal * mcr) / price`.
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `principal` | `uint256` | Auton amount to borrow |
| `price` | `uint256` | The price of Collateral Token in Auton |
| `mcr` | `uint256` | The minimum collateralization ratio |


#### Response

The function returns the minimum collateral required as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

### interestDue

Calculates the interest due for a given amount of debt.

Constraint checks are applied:

- invalid parameter: the `timeBorrow` argument is not greater than the `timeDue` argument value.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `debt` | `uint256` | The debt amount |
| `rate` | `uint256` | The borrow interest rate |
| `timeBorrow` | `uint` | The borrow time |
| `timeDue` | `uint` | The time the interest is due |
  
#### Response

The function returns the amount of interest due as an `uint256` integer value.

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

### underCollateralized

Determines if a debt position is undercollateralized or not.

Constraint checks are applied:

- invalid price: the value of the `price` argument is valid, i.e. it is not equal to `0`.

If the CDP is under collateralized, then it can be liquidated - see [`liquidate()`](/reference/api/asm/stabilization/#liquidate).

{{< alert title="Info" >}}
If a debt position is under collateralized or not is determined by calculating `(collateral * price) / debt`. If this returns a value `< liquidationRatio`, then the CDP is under collateralised and can be liquidated.
{{< /alert >}}

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `collateral` | `uint256` | Amount of Collateral Token backing the debt |
| `price` | `uint256` | The price of Collateral Token in Auton |
| `debt` | `uint256` | The debt amount |
| `liquidationRatio` | `uint256` | The liquidation ratio |

#### Response

The method returns a boolean flag specifying whether the CDP is undercollateralized (true) or not (false).

#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}
