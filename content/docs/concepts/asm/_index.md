
---
title: "Auton Stabilization Mechanism (ASM)"
linkTitle: "Auton Stabilization Mechanism (ASM)"
weight: 10
description: >
  Auton Stabilization Mechanism: elements, the functions they perform, and the lifecycle for Auton and Newton supply.
---

## Overview

This section describes the [Auton Stabilization Mechanism (ASM)](/glossary/#asm) and protocol. It details the elements comprising the mechanism, the functions the mechanism provides to compute and maintain a stable price for [Auton (ATN)](/glossary/#auton), and the lifecycle for Auton and [Newton (NTN)](/glossary/#newton) supply.

For Auton stabilization control Autonity implements a [CDP](/glossary/#cdp)-based stabilization mechanism. Users take out CDPs, depositing Collateral Token (NTN) to borrow Auton at interest. As CDPs are taken out and repaid Collateral Token (NTN) and ATN are removed and returned to circulation, bringing equilibrium to supply and demand.

CDP are maintained according to collateralization and liquidation ratios that set debt to collateral ratio to keep a CDP in good health. Auton is minted and burned as CDPs pass through their lifecycle, i.e. are taken out, repaid, withdrawn, and liquidated.

Elasticity in supply and demand for Auton is absorbed by dynamically adjusting CDP incentives to increase and decrease Auton borrowing costs when Auton price moves above or below its Stabilization Target the [Auton Currency Unit (ACU)](/glossary/#acu).

## ASM identifiers and accounts

The ASM functions with two identities for cryptographic security: the CDP owner and the stabilization protocol contract.

Stabilization Contract calls to mint and burn Auton as CDPs are interacted with to borrow and repay Auton are  restricted to the Stabilization Contract address, the '`stabilizer`' protocol address.

### CDP identifiers

The CDP owner's account address is used as a unique identifier for the CDP itself as well as the CDP owner.

The identity is in the form of an ethereum format account address and is used to:

- unambiguously identify the CDP on-chain
- by the CDP owner as the `msg.sender` address in all CDP interactions: to open, repay debt, and withdraw collateral from the CDP
- by a Liquidator to identify the CDP being liquidated in a liquidation scenario.


## Stabilization protocol

ASM roles, core concepts, and the lifecycle of a CDP from opening to closure.

### Stabilization roles

There are three roles in the ASM:

- *Borrower (CDP owner)*: a user taking out a CDP to borrow Auton, deposing collateral in return. There is no limit on the number of open CDP's a _borrower_ can own at any one time. Borrower's must have an [account](/glossary/#account) on the Autonity network.
- *Liquidator (Keeper)*: a user or agent that liquidates a CDP that has brobecome under collateralized, repaying the CDP's outstanding debt and receiving remaining collateral token in return. Liquidator's must have an [account](/glossary/#account) on the Autonity network.
- *Stabilizer (ASM Protocol)*: the `stabilizer` is the protocol account address used for Auton `mint` and `burn` operations by the Stabilization Contract)

### ASM elements

The ASM is composed of 3 system elements implemented as smart contract logic: ACU, Supply Control, Stabilization. ASM contracts are deployed by the protocol at genesis.

#### ACU

The [Auton Currency Unit (ACU)](/glossary/#acu) is a currency basket from which an index value is computed. This index value is then used as the _stabilization target_ for Auton price, see _[Stabilization](/concepts/asm/#stabilization)_.

The ACU currency basket is composed of 7 free-floating currencies:

- AUD - Australian Dollar
- CAD - Canadian Dollar
- EUR - Euro
- GBP - British Pound Sterling
- JPY - Japanese Yen
- SEK - Swedish Krona
- USD - United States Dollar

Each currency's quantity in the basket is computed to provide a currency basket with minimal total variance with respect to its underlying currencies. The index value then has minimal volatility with respect to variance from individual currency fluctuations.

The index value of ACU can be computed at any time in terms of exchange rates. The index value is computed from price data for each of the basket currencies. Price data is sourced from off-chain by the validator [oracle network](/concepts/oracle-network/) and retrieved from the [Oracle Contract](/concepts/architecture/#autonity-oracle-contract) on-chain.

The value is recomputed at the end of each [oracle voting round](/concepts/oracle-network/#voting-rounds) after new price data for the basket currencies has been computed by the [oracle network](/concepts/oracle-network/).

Public functions can be called to return the ACU value, the currency pair symbols in the basket, and the basket quantities, see [ACU Contract Interface](/reference/api/asm/acu/).

Modifying the currency basket is restricted to the governance account. See the Governance and Protocol Only Reference, [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract).

<!--

{{% alert title="A note on ACU basket quantities" color="info" %}}
The quantity of each currency in the basket is computed based on the end-of-day time for the most recent 11 calendar years of rate data for each currency. A 365 calendar day is used, end-of-day is 17:00 GMT.

USD is used as the numeraire over the data. The quantity of each currency in the basket is then computed based on a weighting that aims to minimize its variance with respect to the basket and using an initial target value of 1 USD for the total value of the basket. Basket quantities fixed over time. The value of ACU at any time can be computed in terms of exchange rates.

When the computed weights are determined to no longer be optimal, the basket quantities are recomputed. The "recompute time" is then the close of the most recent calendar day in the past and again based on the preceding 11 years of calendar data from that time point.

The new basket quantities are computed by:

- Collecting end-of-day (17:00 GMT) data for each ACU constituent currency for the preceding 11 calendar years to today.
- Compute minimization, weights, and basket quantities using the data.
{{% /alert %}}

-->

#### Supply control

The Supply Control contract controls the supply of Auton in circulation on the network. The contract is called by the [Stabilization](/concepts/asm/#stabilization) contract to mint and burn Auton as CDP's are opened and Auton borrowed and repaid. See the Governance and Protocol Only Reference, [`mint()`](/reference/api/aut/op-prot/#mint-supply-control-contract) and [`burn()`](/reference/api/aut/op-prot/#burn-supply-control-contract).

Public functions to return the total supply of Auton and the amount of Auton available for minting can be called, see [Supply Control Contract Interface](/reference/api/asm/supplycontrol/).


#### Stabilization

The Stabilization Contract maintains a record of CDPs and calls the Supply Control Contract to mint and burn Auton as collateral token is deposited or withdrawn and borrowing repaid. For each CDP, the Stabilization Contract records:

- `timestamp`: the timestamp of the last borrow or repayment.
- `collateral`: the collateral deposited with the Stabilization Contract.
- `principal`: the principal debt outstanding as of `timestamp`.
- `interest`: the interest debt that is due at the `timestamp`.

The stabilization mechanism operates by dynamically adjusting CDP incentives.

Users post Collateral Token to borrow ATN against collateral at the Borrow Rate. The Auton Borrow Rate goes up (down) depending on whether ATN/ACU is below (above) the target exchange rate for ATN/ACU to:

  - Increase ATN borrowing (more supply) when ATN/ACU is above target
  - Decrease ATN borrowing (less supply) when ATN/ACU is below target.

CDP collateral token is currently restricted to the Autonity staking token NTN but may be extended to other protocol assets.

Modifying the stabilization configuration for CDP collateral and debt thresholds is restricted to the governance account. See the Governance and Protocol Only Reference, [`setLiquidationRatio()`](/reference/api/aut/op-prot/#setliquidationratio-asm-stabilization-contract), [`setMinCollateralizationRatio()`](/reference/api/aut/op-prot/#setmincollateralizationratio-asm-stabilization-contract), and [`setMinDebtRequirement()`](/reference/api/aut/op-prot/#setmindebtrequirement-asm-stabilization-contract).

Public functions can be called for:

- CDP ownership - borrow and repay Auton, withdraw and deposit Collateral Token
- CDP cost discovery - collateral price, borrow limit, minimum debt requirement, and interest due
- CDP liquidation - if a CDP is liquidatable and to liquidate.

See [Stabilization Contract Interface](/reference/api/asm/stabilization/).


### ASM configuration

ASM parameter settings:

- ACU:
  - _quantities_  = `[21_300, 18_700, 14_300, 10_400, 1_760_000, 18_000, 141_000]`, the basket quantity corresponding to each symbol.
  - _scale_  = `5`, the scale used to represent _quantities_ and the ACU value as a fixed-point integer.
  - _symbols_  = `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "USD-USD", "SEK-USD"]`, the symbols comprising the currency basket.

- Supply Control:
  - _initial allocation_  = 2^<sup>256</sup> - 1, the total supply of Auton available for minting.

- Stabilization:
  - _borrow interest rate_ = `50_000_000_000_000_000` (`0.05e18`), the annual continuously-compounded interest rate for borrowing.
  - _liquidation ratio_ = `1_800_000_000_000_000_000` (`1.8e18`): the minimum ACU value of collateral required to maintain 1 ACU value of debt.
  - _min collateralization ratio_ = `2_000_000_000_000_000_000` (`2.0e18`): the minimum ACU value of collateral required to borrow 1 ACU value of debt.
  - _min debt requirement_ = `1_000_000` ([_megaton_](/concepts/protocol-assets/auton/#unit-measures-of-auton)) : the minimum amount of debt required to maintain a CDP.
  - _target price_ = `1_000_000_000_000_000_000` (`1.0e18`): the ACU value of 1 unit of debt.
 
 <!--
 - _SCALE_ = `18`, the decimal places in fixed-point integer representation.
- _SCALE_FACTOR_ = `10 ** SCALE`, the multiplier for scaling numbers to the required scale.
- _SECONDS_IN_YEAR_ = `365 days`, a year is assumed to have 365 days for interest rate calculations.   
-->

### Protocol primitives

Essential primitives of ASM are: collateral, exchange rate price data, ACU, and the CDP.

#### Collateral

Auton borrowing is collateralized by depositing collateral token into a CDP. The amount and value of collateral backing a CDP is determined by collateralization and liquidation ratios set in the [ASM configuration](/concepts/asm/#asm-configuration). Failure by a [borrower](/concepts/asm/#stabilization-roles) to maintain these ratios results in a CDP becoming liquidatable. In a liquidation scenario a [liquidator](/concepts/asm/#stabilization-roles) is able to assume the debt position, repay outstanding debt, and receive the position's remaining collateral in return.

Autonity's native protocol asset [Newton (NTN)](/concepts/protocol-assets/newton/) is used as the collateral token.

#### Exchange rate price data
ASM sources price data via Autonity's [oracle network](/concepts/oracle-network/), retrieving the data on-chain by contract interactions with the [Oracle Contract](/concepts/architecture/#autonity-oracle-contract).

Oracle price data is used for two purposes:

- for the ACU currency basket symbols to compute the ACU _value_
- for CDP borrowing to compute the value of Collateral Token (NTN) in ATN and determine the _borrow limit_.

Oracle price data is computed per the [Oracle protocol](/concepts/oracle-network/#oracle-protocol), updated periodically in [voting rounds](/glossary/#voting-round).

#### ACU

Auton price has the [Auton Currency Unit (ACU)](/glossary/#acu) as the Stabilization Target to which it _mean-reverts_. ACU is an index value computed from a basket of free-floating currencies. Use of a currency basket minimises exposure to an individual currency's FX exchange risk. The index value is computed from the basket, weighted _pro rata_ to each currency's share i.e. _quantity_ in the basket. Basket quantities are set at network genesis and may be modified by governance.

ASM then functions to maintain Auton-to-ACU value, '_mean reverting_' to this value by the CDP stabilization mechanism. 

ACU value is kept current by protocol recomputing the value at the end of each oracle voting round when price data for all the basket currencies is available. See the Protocol Only Reference functions [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) [`update()`](/reference/api/aut/op-prot/#update-acu-contract) for more detail.

#### CDP

The CDP functions to manage Auton borrowing and stabilize Auton price by adjusting the CDP borrowing cost. CDP's are operated within strict parameterization constraints:

- CDP Ownership:
  - A borrower (CDP Owner) can have only `1` open CDP at a time.
  - A borrower opens a CDP by depositing collateral `>=` the _minimum debt requirement_ for a CDP. A borrower can then within CDP constraints:
  - borrow ATN against collateral
  - repay ATN to partially or completely repay the CDP
  - withdraw collateral

- Minimum debt requirement:
  - A CDP must be `>=` a minimum amount of debt. This ensures the position is economically viable, i.e. the transaction and interest costs of opening and servicing, or liquidating, a position is viable.

- Borrow interest rate:
  - Interest on debt is charged at an annual continuously-compounded interest rate.
  - Adjusting the borrow rate is the primary economic lever by which the CDP-based stabilization mechanism incentivises increase or decrease in ATN borrowing and '_mean-revert_' ATN to ACU value.
  - Repayments to a CDP are used to cover accrued interest before debt principal.

- Borrow limit:
  - The amount of Auton that can be borrowed against collateral deposited to a CDP is determined by the ATN value of that deposited collateral, forming a _borrow limit_.
  - The CDP Owner can borrow Auton to an amount `<=` the  _borrow limit_.
  - The amount of Auton borrowed in a CDP is the _principal_ of the debt position. _Principal_ cannot exceed the _borrow limit_. 

- Collateralization:
  - A CDP must maintain adequate collateral value at all times. A _minimum collateralization ratio_ sets the minimum ACU value of collateral required to _borrow_ 1 ACU value of debt. This ratio must be strictly greater than `1.0`.
  - Collateral must be an ERC 20 token. The accepted collateral token is the protocol asset Newton.

- Liquidation ratio:
  - A CDP must maintain adequate collateral value at all times. A _liquidation ratio_ sets the minimum ACU value of collateral required to _maintain_ 1 ACU value of debt. 
  - The liquidation ratio must be strictly less than the _minimum collateralization ratio_.

- Liquidation Condition:
  - A CDP is _liquidatable_ when the CDP's _collateralisation ratio_ falls below the _liquidation ratio_:
  - If the _liquidation condition_ is met, the only permitted operations on the CDP are:
    - For the _Borrower_, the CDP Owner, to pay back Auton until and repay the CDP or bring the position back within the _liquidation ratio_
    - For a _Liquidator_ to liquidate the position.


### CDP lifecycle

The sequence of lifecycle events for a CDP is:

- CDP is opened.
  - Borrower determines their borrowing and collateral requirements. To do this, the borrower can call Stabilization Contract functions, see [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice), [`minimumCollateral()`](/reference/api/asm/stabilization/#minimumcollateral).
  - Borrower opts to open a CDP, becoming a CDP Owner. The CDP Owner then approves the Stabilization Contract to spend Collateral Token (NTN) on their behalf for the amount of collateral to be deposited:
    - Calls the Collateral Token Contract (i.e. Autonity Protocol Contract) to [`approve()`](/reference/api/aut/#approve) the [Stabilization Contract address](/concepts/architecture/#protocol-contract-account-addresses) as a spender on their behalf and set the [`allowance()`](/reference/api/aut/#allowance) of collateral token that the Stabilization Contract can spend.
    - Calls the Stabilization Contract to deposit Collateral Token to a CDP, calling the contract's [`deposit()`(/reference/api/asm/stabilization/#deposit) to deposit collateral.
  - Stabilization Contract creates the CDP, using the ERC20 allowance mechanism to execute the collateral deposit. A CDP object is created, and the [CDP attributes](/concepts/asm/#stabilization) are populated.

- CDP is maintained and serviced. The CDP Owner maintains the CDP, opting to increase or decrease borrowing and deposited collateral within [CDP primitive constraints](/concepts/asm/#cdp). The CDP Owner may:

  - _Borrow_: CDP Owner borrows Auton from CDP against collateral. Constraint checks are applied:
    - the amount borrowed must not exceed the _borrow limit_ for the deposited collateral value
    - the _principal_ debt must meet the _minimum debt requirement_
    - the borrowing does not decrease the CDP collateralization ratio below the _minimum collateralization ratio_.
    
      The Stabilization Contract calls the Supply Control Contract to mint the borrowed Auton amount to the CDP Owner.

  - _Repay_: CDP Owner pays back some or all borrowed Auton in a CDP to (a) service the debt, or (b) maintain the CDP within constraints and prevent a CDP becoming _liquidatable_. Constraint checks are applied:
    - Payment is only accepted if outstanding debt after the payment meets the _minimum debt requirement_
    
      The Stabilization Contract uses the payment to cover outstanding accrued _interest_ before outstanding debt _principal_, transfering the interest proceeds to the contract's _Internal Balance Sheet_. If a payment surplus remains after covering outstanding interest, then the contract reduces the CDP _principal_ and calls the Supply Control Contract to burn the amount of Auton _principal_ debt paid back.

  - _Withdraw_: CDP Owner withdraws _collateral token_ from the CDP. Constraint checks are applied:
    - the withdrawal must not reduce collateral below the CDP's _liquidation ratio_, making the CDP meet the _liquidation condition_ and so become _liquidatable_
    - the withdrawal must not reduce the remaining collateral below the CDP's _minimum collateralization ratio_.
    
      The Stabilization Contract transfers the withdrawn amount of collateral to the CDP Owner account address.

- CDP is liquidated.
  - A Liquidator determines that a CDP has or will meet the _liquidation condition_ and so become _liquidatable_. To do this, the liquidator can call Stabilization Contract [CDP View functions](/reference/api/asm/stabilization/#cdp-view-functions) to view CDP state.
  - Liquidator opts to liquidate a CDP. The liquidator calls the Stabilization Contract [`liquidate()`](/reference/api/asm/stabilization/#liquidate) function to repay the CDP and claim the collateral. Constraint checks are applied:
  - The liquidate transaction payment amount will pay all the CDP debt outstanding, _principal_ and accrued _interest_. 

    As a reward, the liquidator will receive the collateral that is held in the CDP. Any payment surplus remaining after covering the CDP's debt is refunded to the liquidator.


## ASM economics

ASM economics are multi-dimensional:

- For the protocol:
  - Protocol asset price stability: the stabilization mechanism mean-reverts Auton to the ACU stabilization target over time, smoothing Auton price movement.
  - Supply and demand elasticity: Auton supply increases and decreases according to demand, the CDP _borrow rate_ providing the economic lever to adjust CDP incentives.
  - Protocol revenue from _borrow interest_ earned on CDP's.
- For the borrower:
  - CDP's give access to collateralized borrowing for Auton with  flexibility to increase and decrease borrowing and collateral amounts within constraints. Borrowers can offset flexibility against opportunity costs of borrow interest, staking reward potential if deposited Newton collateral were earning staking rewards, and liquidation risk.
- For the liquidator:
  - Liquidation returns from remaining collateral after settlement of debt and interest outstanding.