
---
title: "Auton Stabilization Mechanism (ASM)"
linkTitle: "Auton Stabilization Mechanism (ASM)"
weight: 10
description: >
  Auton Stabilization Mechanism: elements, the functions they perform, and the lifecycle for Auton and Newton supply.
---

## Overview

This section describes the [Auton Stabilization Mechanism (ASM)](/glossary/#asm) and protocol. It details the elements comprising the mechanism, the functions the mechanism provides to compute and maintain a stable price for [Auton (ATN)](/glossary/#auton), and the lifecycle for Auton and [Newton (NTN)](/glossary/#newton) supply.

For Auton stabilization control Autonity implements a [CDP](/glossary/#cdp)-based stabilization mechanism. Users take out CDP's, depositing Collateral Token (NTN) to borrow Auton at interest. As CDP's are taken out and repaid Collateral Token (NTN) and ATN are removed and returned to circulation, bringing equilibrium to supply and demand.

CDP are maintained according to collateralization and liquidation ratios that set collateral amount and collateral value thresholds to keep a CDP in good health.  Auton is minted and burned as CDP's pass through their lifecycle, i.e. are taken out, repaid, withdrawn, and liquidated.

Elasticity in supply and demand for Auton is absorbed by dynamically adjusting CDP incentives to increase and decrease Auton borrowing costs when Auton price moves above or below its Stabilization Target.

Auton price has the [Auton Currency Unit (ACU)](/glossary/#acu) as the Stabilization Target to which it mean-reverts. ACU is a basket of free-floating currencies. An index price is computed from the basket, weighted _pro rata_ to each currency's share i.e. _quantity_ in the basket, and an index value for ACU computed. Use of a currency basket minimises the Auton user's exposure to an individual currency's FX exchange risk.


## ASM identifiers and accounts

The ASM functions with two identities for cryptographic security: the CDP owner and the stabilization protocol contract.

Stabilization Contract calls to mint and burn Auton as CDP's are interacted with to borrow and repay Auton are  restricted to the Stabilization Contract address, the '`stabilizer`' protocol address.

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

The [Auton Currency Unit (ACU)](/glossary/#acu) is a currency basket from which an index value is computed. This index value is then used as the _stabilization target_ for Auton price.

The ACU currency basket is composed of 7 free-floating currencies:

- AUD - Australian Dollar
- CAD - Canadian Dollar
- EUR - Euro
- GBP - British Pound Sterling
- JPY - Japanese Yen
- SEK - Swedish Krona
- USD - United States Dollar

Each currency's quantity in the basket is computed to provide a currency basket with minimal variance. The index value then has minimal volatility with respect to variance from individual currency fluctuations.

ACU is used as the _stabilization target_ for Auton price, see _[Stabilization](/concepts/asm/#stabilization)_.

The value of ACU can be computed at any time in terms of exchange rates. ACU is computed based on the end-of-day time for the most recent 11 calendar years of data for each currency in the basket.

{{% alert title="Info" %}}
A 365 calendar day is used, end-of-day is 17:00 GMT. Price data is sourced from off-chain by the validator [oracle network](/concepts/oracle-network/) and retrieved from the [Oracle Contract](/concepts/architecture/#autonity-oracle-contract) on-chain.
{{% /alert %}}

USD is used as the numeraire over the data. The quantity of each currency in the basket is then computed based on a weighting that minimizes variance and using an initial target value of 1 USD for the total value of the basket. Basket quantities fixed over time. The value of SAC at any time can be computed in terms of exchange rates.
\end{enumerate}

To illustrate supposing the ACU is computed at 17:00 GMT today:

- Collect end-of-day (17:00 GMT) data for each ACU constituent currency for the preceding 11 calendar years to today.
- Compute minimization, weights, and basket quantities using the data
- Compute the ACU value for today using the data.

When the computed weights are determined to no longer be optimal, they are updated. The "recompute time" is then the close of the most recent calendar day in the past and again based on the preceding 11 years of calendar data from that time point the new basket quantities are computed.

Public functions can be called to return the ACU value, the currency pair symbols in the basket, and the basket quantities, see [ACU Contract Interface](/reference/api/asm/acu/).

Modifying the currency basket is restricted to the governance account. See the Governance and Protocol Only Reference, [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract).

#### Supply control

The Supply Control contract controls the supply of Auton in circulation on the network. The contract is called by the [Stabilization](/concepts/asm/#stabilization) contract to mint and burn Auton as CDP's are opened and Auton borrowed and repaid. See the Governance and Protocol Only Reference, [`mint()`](/reference/api/aut/op-prot/#mint-supply-control-contract) and [`burn()`](/reference/api/aut/op-prot/#burn-supply-control-contract).

Public functions to return the total supply of Auton and the amount of Auton available for minting can be called, see [Supply Control Contract Interface](/reference/api/asm/supplycontrol/).


#### Stabilization

Stabilization functions by dynamically adjusting CDP incentives.

Users post Collateral Token (NTN) to borrow ATN against collateral at the Borrow Rate. The Auton Borrow Rate goes up (down) depending on whether ATN/ACU is below (above) the target exchange rate for ATN/ACU to:
  - Increase ATN borrowing (more supply) when ATN/ACU is above target
  - Decrease ATN borrowing (less supply) when ATN/ACU is below target
 
CDP collateral token is currently restricted to the Autonity staking token NTN. A next generation of the ASM will also accept LNTN as collateral. In this future iteration, stakers who post LNTN collateral will continue to receive their staking awards, eliminating opportunity cost distortions. I.e. lending NTN collateral introduces an opportunity cost of paying interest and losing opportunity to earn staking rewards if bonded.

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

- CDP - CDP-based stabilization mechanism and the core attributes thereof - principal, etc
- Protocol Assets - Auton, Newton, Liquid Newton - Auton supply, price stability, collateral token
- ACU - ACU value derived from weighted currency basket, to minimize FX exposure for borderless markets.
- Oracle. Oracle data from oracle contract - or subsume this into ACU?
- CDP liquidation - of under collateralized debt positions

...

#### CDP

Collateralized Debt Position (CDP) attributes:

- `timestamp`: the timestamp of the last borrow or repayment.
- `collateral`: the collateral deposited with the Stabilization Contract.
- `principal`: the principal debt outstanding as of `timestamp`.
- `interest`: the interest debt that is due at the `timestamp`.


...

#### xyz

...

### CDP lifecycle

CDP lifecycle events.

    /// Collateral Token was deposited into a CDP
    /// @param account The CDP account address
    /// @param amount Collateral Token deposited
    event Deposit(address indexed account, uint256 amount);
    /// Collateral Token was withdrawn from a CDP
    /// @param account The CDP account address
    /// @param amount Collateral Token withdrawn
    event Withdraw(address indexed account, uint256 amount);
    /// Auton was borrowed from a CDP
    /// @param account The CDP account address
    /// @param amount Auton amount borrowed
    event Borrow(address indexed account, uint256 amount);
    /// Auton debt was paid into a CDP
    /// @param account The CDP account address
    /// @param amount Auton amount repaid
    event Repay(address indexed account, uint256 amount);
    /// A CDP was liquidated
    /// @param account The CDP account address
    /// @param liquidator The liquidator address
    event Liquidate(address indexed account, address liquidator);

...



### CDP ownership

...


### CDP liquidation

...


## ASM economics

- for protocol - Auton supply control
- for borrower - collateralized borrowing using protocol asset as collateral token; borrow interest payment, risk of liquidation
- for liquidator - returns from liquidation, remaining collateral after settlement of debt and interest outstanding