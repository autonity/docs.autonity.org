
---
title: "Auton Stabilization Mechanism (ASM)"
description: >
  Auton Stabilization Mechanism: elements, the functions they perform, and the lifecycle for Auton and Newton supply.
---

## Overview

This section describes the [Auton Stabilization Mechanism (ASM)](/glossary/#asm) and protocol. The Auton Stabilization Mechanism provides functions to compute the target value for the [Auton (ATN)](/glossary/#auton), a [Collateralized Debt Position (CDP)](/glossary/#cdp)-based stabilization mechanism to borrow Auton for [Newton (NTN)](/glossary/#newton) collateral at interest, and an auction mechanism to maintain CDP health by debt and interest auctions.

Auton price stability is maintained by targeting Auton market value to a Stabilization Target the [Autonomous Currency Unit (ACU)](/glossary/#acu). 

Auton borrowing and repayment via a [CDP](/glossary/#cdp)-based stabilization mechanism acts to mean-revert the Auton's actual market price towards the target through the supply of Auton and [Newton (NTN)](/glossary/#newton). CDP integrity is maintained by CDP owners managing their CDPs and an auction mechanism introducing market incentives by means of interest auctions for CDP loan interest and debt auctions for liquidatable CDP collateral.

Auton tokens are minted and burned exclusively as a result of changing Collateralized Debt Positions.

Users open [CDP](/glossary/#cdp)s by depositing collateral in the form of NTN to borrow Auton at interest. Autons are minted when borrowed and interest then begins to accrue against the loan debt. 

Autons are burned when a CDP is repaid by depositing ATN to the ASM's Stabilization smart contract. NTN is removed and returned to circulation by CDP owners as they deposit and withdraw NTN collateral to their CDP. 

CDPs are created with defined collateralization and liquidation ratios which limit the risk that the debt cannot be adequately covered by the sale of the collateral.

Borrowers maintain their CDP throughout its lifecycle, depositing and withdrawing collateral, paying interest, and increasing or decreasing borrowing to maintain their CDP within the required collateral and liquidation ratios.

An Auction Mechanism is utilised to maintain CDP health and Auton and Newton supply by auction-based market incentives. CDP interest payments accumulate until a threshold amount is crossed, triggering an interest auction where bidders bid NTN for the paid ATN interest. If a CDP becomes liquidatable, then a debt auction is triggered where bidders bid ATN for CDP NTN collateral.

Changes in supply and demand for Auton are absorbed by dynamically adjusting CDP incentives to increase and decrease Auton borrowing costs when Auton price moves above or below its Stabilization Target the [Autonomous Currency Unit (ACU)](/glossary/#acu).

## ASM identifiers and accounts

The ASM functions with three identities for cryptographic security: the CDP owner, and the Stabilization and Auctioneer protocol contracts.

Stabilization Contract calls to mint and burn Auton as CDPs are interacted with to borrow and repay Auton are restricted to the Stabilization Contract, the '`stabilizer`' address.

Stabilization Contract calls to liquidate CDPs are restricted to the Auctioneer Contract, the '`auctioneer`' address.

### CDP identifiers

The CDP owner's account address is used as a unique identifier for the CDP itself as well as the CDP owner.

The identity is in the form of an Ethereum formatted account address and is used to:

- unambiguously identify the CDP on-chain
- by the CDP owner as the `msg.sender` address in all CDP interactions: to open, repay debt, and withdraw collateral from the CDP
- by a Liquidator to identify the CDP being liquidated in a liquidation scenario.


## Stabilization protocol

ASM roles, core concepts, and the lifecycle of a CDP from opening to closure.

### Stabilization roles

There are five roles in the ASM:

- *Borrower (CDP owner)*: a user taking out a CDP to borrow Auton, deposing collateral in return. There is no limit on the number of open CDP's a _borrower_ can own at any one time. Borrower's must have an [account](/glossary/#account) on the Autonity network.

- *Bidder (debt, interest auctions)*: a user or agent that bids in auctions for: 
  - *debt*: bidding ATN for NTN. A debt auction liquidates and is triggered by a CDP that has become under collateralized, repaying the CDP's outstanding ATN debt and receiving remaining NTN collateral token in return.
  - *interest*: bidding NTN for ATN. An interest auction is triggered when the accumulated amount of ATN the ASM has received from CDP interest repayments crosses a threshold.
  
  Bidders must have an [account](/glossary/#account) on the Autonity network.

- *Stabilizer (ASM Protocol)*: the `stabilizer` is the protocol account address used for Auton `mint` and `burn` operations by the Stabilization Contract

- *Auctioneer (ASM Protocol Liquidator (Keeper))*: the `auctioneer` is the Auctioneer Protocol Contract used to initiate and manage debt and interest auctions. Interest auctions are managed purely by the Auctioneer Contract. In debt auctions the `auctioneer` address is used to call the Stabilization Contract [`liquidate()`](/reference/api/asm/stabilization/#liquidate) function and trigger CDP liquidation.

### ASM elements

The ASM is composed of 4 system elements implemented as smart contract logic: ACU, Supply Control, Stabilization, Auctioneer. ASM contracts are deployed by the protocol at genesis.

#### ACU

The [Autonomous Currency Unit (ACU)](/glossary/#acu) is a currency basket from which an index value is computed. This index value is then used as the _stabilization target_ for Auton price, see _[Stabilization](/concepts/asm/#stabilization)_.

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

Public functions can be called to return the ACU value, scaling, the currency pair symbols in the basket, and the basket quantities. See [ACU Contract Interface](/reference/api/asm/acu/).

Modifying the currency basket is restricted to the governance account. See the Governance and Protocol Only Reference, [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract).

::: {.callout-note title="A note on ACU basket quantities and ACU index value" collapse="false"}
The quantity of each currency in the basket is computed based on the end-of-day time for the most recent 11 calendar years of rate data for each currency. A 365 calendar day is used, end-of-day is 17:00 GMT.

$\text{USD}$ is used as the numeraire over the data. The quantity of each currency in the basket is then computed based on a weighting that aims to minimize its variance with respect to the basket and using an initial target value of $\text{1 USD}$ for the total value of the basket. Basket quantities fixed over time. The index value of ACU at any time can be computed in terms of exchange rates.

When the computed weights are determined to no longer be optimal, the basket quantities are recomputed. The "recompute time" is then the close of the most recent calendar day in the past and again based on the preceding 11 years of calendar data from that time point.

The new basket quantities are computed by:

- Collecting end-of-day (17:00 GMT) data for each ACU constituent currency for the preceding 11 calendar years to today.
- Compute minimization, weights, and basket quantities using the data.
:::


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
- CDP liquidation - if a CDP is liquidatable and to liquidate. Liquidation is invoked by ASM debt auctions. See ASM element [Auctioneer](/concepts/asm/#auctioneer) and ASM protocol primitive [auction](/concepts/asm/#auction).

See [Stabilization Contract Interface](/reference/api/asm/stabilization/).

#### Auctioneer

The Auctioneer Contract initiates and manages debt and interest auctions for illiquid CDPs and accumulated CDP interest payments respectively.

ASM's auction mechanism is complementary to the Stabilization mechanism and contributes to lending market equilibrium. Auctions introduce market incentives that bring NTN and ATN in and out of open circulation by means of bidding NTN for CDP ATN loan interest in *interest auctions* and repaying ATN debt for NTN collateral in CDP *debt auctions* for liquidatable CDP collateral.

Auctions open with a *start* price which decreases over the auction's duration to a *floor* price as a function of time.

For interest auctions the *start* price is set at a premium to the collateral price and *floor* at a discount to the collateral price. For debt auctions the *start* price is set at the liquidation price and *floor* at the bankruptcy price.

Participants with sufficient funds can place *bids* at or above the *reserve*  price and the auction ends when the first *bid* $>=$ the *reserve* price is received. If no bids are received within the auction duration, the auction remains at the *floor* price until a willing bidder is found. An auction will always end with a single, successful *bid*.
 
A debt auction is triggered by a bidder identifying a CDP that has become under collateralized and submitting a bid to repay the CDP's outstanding ATN debt in return for the remaining CDP collateral. A successful debt bid then trigger CDP liquidation: ATN debt is repaid and burnt; NTN is released into open circulation.

::: {.callout-note title="A note on CDP liquidation" collapse="false"}
Debt bids trigger liquidation by the Auctioneer Contract invoking the Stabilization Contract [`liquidate()`](/reference/api/asm/stabilization/#liquidate) function.
:::

An interest auction is triggered when the accumulated amount of ATN that the ASM has received from CDP interest repayments crosses a configured *threshold* amount. For each new interest auction triggered, the Auctioneer Contract emits a `NewInterestAuction` event logging:

- `auctionId`: the unique identifier for the auction.
- `amount`: the amount of ATN in the auction.
- `startRound`: the timestamp when the auction will begin; this is the timestamp of the interest payment that triggered the interest auction.

::: {.callout-note title="A note on CDP interest repayments" collapse="false"}
See the Stabilization Contract [`repay()`](/reference/api/asm/stabilization/#repay) for how CDP loan interest repayments are processed and the order in which a repayment settles interest before reducing loan principal, with surplus from over repayment returned to the borrower.
:::

The Auctioneer Contract records for an interest auction:

- `id`: the unique identifier for the auction.
- `amount`: the amount of ATN received from interest payments that triggered the auction.
- `startPrice`: the reserve price for the auction. Start price is set at a fraction above market price that an interest auction starts at
- `startTimestamp`: the timestamp at which the auction was triggered.

Bidders discover interest auctions by querying Auctioneer Contract state for open auctions (see Auctioneer Contract Interface, [Auction View functions](/reference/api/asm/auctioneer/#openauctions)) and listening for `NewInterestAuction` events. Multiple interest auctions can be open concurrently. The actual duration of an individual interest auction is the delta between the auction `startTimestamp` and the first successful bid.

Successful interest auctions then result in ATN returning to open circulation and NTN transferring to the protocol interest auction proceeds address.

See [Auctioneer Contract Interface](/reference/api/asm/auctioneer/).

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
  - _announcement window_ = `` (), the length of time in seconds before an update to ASM Stabilization config will take effect.
  - _liquidation ratio_ = `1_800_000_000_000_000_000` (`1.8e18`): the minimum ACU value of collateral required to maintain 1 ACU value of debt.
  - _min collateralization ratio_ = `2_000_000_000_000_000_000` (`2.0e18`): the minimum ACU value of collateral required to borrow 1 ACU value of debt.
  - _min debt requirement_ = `1_000_000` ([_megaton_](/concepts/protocol-assets/auton/#unit-measures-of-auton)) : the minimum amount of debt required to maintain a CDP.
  - _target price_ = `1_618_034_000_000_000_000` (`1.6180340e18`): the ACU value of 1 unit of debt.
  - _default NTN ATN price_ = `` (), default NTN-ATN price for use at genesis.
  - _default NTN USD price_ = `` (), default NTN-USD price for use at genesis.
  - _default ACU USD Price_ `` (), optional default ACU-USD price for use at genesis.


::: {.callout-note title="A note on target price and ATN price" collapse="false"}

Target price is the ATN to ACU conversion rate, which is set to the [Golden ratio](https://en.wikipedia.org/wiki/Golden_ratio)  ${\displaystyle {\frac {1+{\sqrt {5}}}{2}}}$ i.e. $1.6180340$.

ATN value is targeting $\text{ACU index value} \times \text{target price}$.

For example if at today’s exchange rates the $\text{ACU index value}$ is $079 \dots$ then it would give an ATN price of ca $1.28 \dots$.

:::

- Auctioneer:
  - _liquidation auction duration_ = `` ( blocks), the number of blocks for a liquidation auction to move from the liquidation rate to the bankruptcy rate.
  - _interest auction duration_ = `` ( blocks), the number of blocks for an interest auction to move from the discount rate to the floor price.
  - _interest auction discount_ = `` ( %), the fraction above market price that an interest auction starts at.
  - _interest auction threshold_ = `` ATN, the minimum amount of ATN paid in interest to trigger an interest auction.

::: {.callout-note title="Auction price and rate terminology" collapse="false"}

For auction rate terminology see the notebox "**Deep dive into auction price and rate terminology**" in [Protocol primitives, auction](/concepts/asm/#auction) on this page.

:::

### ASM restrictions

ASM may be configured with temporary restrictions to facilitate genesis bootstrapping of an [Autonity network](/glossary/#autonity-network).

There are two types of temporary restriction that can be set and lifted:

- CDP Opening Restrictions. Restricts CDP opening to an `atnSupplyoperator` account set by network governance. The rationale is limiting the supply of ATN at genesis until there is sufficient market liquidity in ATN and NTN for ASM to work effectively.
- CDP Opening Price Restrictions. Sets NTN and ATN [protocol asset](/concepts/protocol-assets/) prices used by the ASM to default fixed price values. The rationale is ATN and NTN market prices are not available from public market sources at network genesis. Without these 'opening prices' ASM cannot compute a collateral price and enable CDP borrowing to bring ATN into circulation. Post genesis network bootstrapping can therefore use default prices until public NTN and ATN market price availability.

Restrictions are subject to network governance and can be set and removed by the governance `operator` account. For details see [Autonity Contract Interface, Governance and Protocol Only Reference](/reference/api/aut/op-prot/) and [`useFixedGenesisPrices()`]( /reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract), [`setAtnSupplyOperator()`](/reference/api/aut/op-prot/#setatnsupplyoperator-asm-stabilization-contract), and [`removeCDPRestrictions()`](/reference/api/aut/op-prot/#setatnsupplyoperator-asm-stabilization-contract).

### Protocol primitives

Essential primitives of ASM are: ACU, auction, CDP, collateral, and exchange rate price data..

#### ACU

Auton price has the [Autonomous Currency Unit (ACU)](/glossary/#acu) as the Stabilization Target to which it _mean-reverts_. ACU is an index value computed from a basket of free-floating currencies. Use of a currency basket minimises exposure to an individual currency's FX exchange risk. The index value is computed from the basket, weighted _pro rata_ to each currency's share i.e. _quantity_ in the basket. Basket quantities are set at network genesis and may be modified by governance.

ASM then functions to maintain Auton-to-ACU value, '_mean reverting_' to this value by the CDP stabilization mechanism. 

ACU value is kept current by protocol recomputing the value at the end of each oracle voting round when price data for all the basket currencies is available. See the Protocol Only Reference functions [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) [`update()`](/reference/api/aut/op-prot/#update-acu-contract) for more detail.

#### Auction

Auctions introduce market incentives that bring NTN and ATN in and out of open circulation on the network. There are two types of auction: *debt* and *interest*. In *interest auctions* NTN is bid for CDP ATN loan interest, bringing ATN out of the ASM into open circulation on the network and moving NTN into the ASM. In *debt auctions* ATN debt is repaid in return for NTN collateral in liquidatable CDPs. CDP liquidation results in moving ATN into the ASM and burning it as the ATN borrowing debt is repaid, and moving NTN out of the ASM and returning it into open circulation on the network.

Auctions have *start*, *floor*, and *bid* ('hammer') prices. The *start* price is the auction opening price and *floor* the lowest price accepted in an auction. Price evolves throughout the auction's maximum *duration* from *start* to *floor* price. Start and floor prices are, therefore, a *reserve* or *minimum bid* price for the auction that adjusts automatically as a function of time after the auction starts.

Auction *bidders* place *bids* at or above the *reserve*  price and the auction ends when the first *bid* $>=$ the *reserve* price is received. If no bids are received within the auction duration, the auction remains at the *floor* price until a successful *bid* is made. An auction will always end with a single, successful *bid*.

::: {.callout-note title="Deep dive into auction price and rate terminology" collapse="false"}

- **Collateral Rate**
  The market rate of NTN in ATN.

- **Liquidation Rate**
  The rate of NTN in ATN which makes a CDP's collateral value times the CDP's liquidation ratio equal to its total debt value.

- **Bankruptcy Rate**
  The rate of NTN in ATN which makes a CDP's collateral value equal to its total debt value.

- **Discount Rate**
  The discount to _Collateral Rate_ applied to the _Starting Price_ of an interest auction.

- **Lot**
  The asset and amount being offered for sale (or offered as collateral) as a single unit, in which the asset is called the _Lot Asset_ and the amount is called the _Lot Amount_.

- **Bid**
  The asset and amount a bidder is willing to offer at any point in the auction, in which the asset is called the _Bid Asset_, the amount is called the _Bid Amount_ and the bid amount times the collateral price is called the _Bid Price_.

- **Reserve Price**
  The minimum bid price an auctioneer is willing to accept at any point in the auction.

- **Starting Price**
  The reserve price when the auction starts, in which the starting price divided by the lot amount is called the _Starting Rate_.

- **Floor Price**
  The minimum reserve price for the whole duration of the auction, in which the floor price divided by the lot amount is called the _Floor Rate_.

- **Bid Price**
  The bid price at which the auctioneer closes the sale, in which the bid price divided by the lot amount is called the _Bid Rate_.

- **Price Evolution Function**
  A function $P(t)$ mapping the time since the auction started to the price of the lot. The price evolution function must start at the starting price at $t = 0$ and end at the floor price at $t = T$ (the auction duration).

- **Auction Duration**
  The duration $T$, in seconds, after which the auction will reach the _Floor Price_.

- **Auctioneer**
  The individual or entity that conducts the auction.

- **Seller**
  The individual or entity that offers the lot for auction.

- **Bidder**
  The participant in the auction who places bids.

:::


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

#### Collateral

Auton borrowing is collateralized by depositing collateral token into a CDP. The amount and value of collateral backing a CDP is determined by collateralization and liquidation ratios set in the [ASM configuration](/concepts/asm/#asm-configuration). Failure by a [borrower](/concepts/asm/#stabilization-roles) to maintain these ratios results in a CDP becoming liquidatable. In a liquidation scenario a [liquidator](/concepts/asm/#stabilization-roles) is able to assume the debt position, repay outstanding debt, and receive the position's remaining collateral in return.

Autonity's native protocol asset [Newton (NTN)](/concepts/protocol-assets/newton/) is used as the collateral token.

#### Exchange rate price data
ASM sources price data via Autonity's [oracle network](/concepts/oracle-network/), retrieving the data on-chain by contract interactions with the [Oracle Contract](/concepts/architecture/#autonity-oracle-contract).

Oracle price data is used for two purposes:

- for the ACU currency basket symbols to compute the ACU _value_
- for CDP borrowing to compute the value of Collateral Token (NTN) in ATN and determine the _borrow limit_.

Oracle price data is computed per the [Oracle protocol](/concepts/oracle-network/#oracle-protocol), updated periodically in [voting rounds](/glossary/#voting-round).


### CDP lifecycle

The sequence of lifecycle events for a CDP is:

- CDP is opened.
  - Borrower determines their borrowing and collateral requirements. To do this, the borrower can call Stabilization Contract functions, see [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice), [`minimumCollateral()`](/reference/api/asm/stabilization/#minimumcollateral).
  - Borrower opts to open a CDP, becoming a CDP Owner. The CDP Owner then approves the Stabilization Contract to spend Collateral Token (NTN) on their behalf for the amount of collateral to be deposited:
    - Calls the Collateral Token Contract (i.e. Autonity Protocol Contract) to [`approve()`](/reference/api/aut/#approve) the [Stabilization Contract address](/concepts/architecture/#protocol-contract-account-addresses) as a spender on their behalf and set the [`allowance()`](/reference/api/aut/#allowance) of collateral token that the Stabilization Contract can spend.
    - Calls the Stabilization Contract to deposit Collateral Token to a CDP, calling the contract's [`deposit()`](/reference/api/asm/stabilization/#deposit) to deposit collateral.
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

- CDP debt auction (liquidation).
  - A bidder determines that a CDP has or will meet the _liquidation condition_ and so become _liquidatable_. To do this, the liquidator can call Stabilization Contract [CDP View functions](/reference/api/asm/stabilization/#cdp-view-functions) to view CDP state.
  - Liquidator opts to liquidate a CDP by submitting a bid for CDP collateral. The liquidator calls the Auctioneer Contract [`bidDebt()`](/reference/api/asm/auctioneer/#bidDebt) function to submit an ATN bid for a specific amount `<=` the CDP's remaining NTN collateral. 

    As a reward, the liquidator will receive the collateral that is held in the CDP. Any payment surplus remaining after covering the CDP's debt is refunded to the liquidator.

- CDP interest auction.
  - Accrued CDP loan interest payments cross the interest auction threshold, triggering a new interest auction.
  - Bidder detects that a CDP interest auction has opened. To do this the bidder can listen for `NewInterestAuction` events or can call Auctioneer Contract [Auction View functions](/reference/api/asm/auctioneer/#auction-view-functions) to view auction state.
  - Bidder opts to submit a bid for the auctioned loan interest. The liquidator calls the Auctioneer Contract [`bidInterest()`](/reference/api/asm/auctioneer/#bidInterest) function to submit an NTN bid for the auctioned amount of ATN loan interest.


## ASM economics

ASM economics are multi-dimensional:

- For the protocol:
  - Protocol asset price stability: the stabilization mechanism mean-reverts Auton to the ACU stabilization target over time, smoothing Auton price movement.
  - Supply and demand elasticity: Auton supply increases and decreases according to demand, the CDP _borrow rate_ providing the economic lever to adjust CDP incentives.
  - Protocol revenue from _borrow interest_ earned on CDP's.
- For the borrower:
  - CDP's give access to collateralized borrowing for Auton with  flexibility to increase and decrease borrowing and collateral amounts within constraints. Borrowers can offset flexibility against opportunity costs of borrow interest, staking reward potential if deposited Newton collateral were earning staking rewards, and liquidation risk.
- For auction bidders:
  - Liquidation returns from NTN collateral after bidding for CDP collateral in ASM debt (i.e. liquidation) auctions.
  - Interest returns from ATN interest after bidding for CDP interest payments in ASM interest auctions.
