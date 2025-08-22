---
title: "AFP Smart Contract Python Bindings Reference"
---

## afp.bindings

Typed bindings around the smart contracts of the Autonomous Futures System.

**Classes:**

- [**AuctionConfig**](#afp.bindings.AuctionConfig) – Port of `struct AuctionConfig` on the IAuctioneer contract.
- [**AuctionData**](#afp.bindings.AuctionData) – Port of `struct AuctionData` on the IAuctioneer contract.
- [**BidData**](#afp.bindings.BidData) – Port of `struct BidData` on the IAuctioneer contract.
- [**ClearingConfig**](#afp.bindings.ClearingConfig) – Port of `struct ClearingConfig` on the IClearing contract.
- [**ClearingDiamond**](#afp.bindings.ClearingDiamond) – ClearingDiamond contract binding.
- [**Config**](#afp.bindings.Config) – Port of `struct Config` on the IClearing contract.
- [**Intent**](#afp.bindings.Intent) – Port of `struct Intent` on the IClearing contract.
- [**IntentData**](#afp.bindings.IntentData) – Port of `struct IntentData` on the IClearing contract.
- [**LAAData**](#afp.bindings.LAAData) – Port of `struct LAAData` on the IBankruptcy contract.
- [**MarginAccount**](#afp.bindings.MarginAccount) – MarginAccount contract binding.
- [**MarginAccountRegistry**](#afp.bindings.MarginAccountRegistry) – MarginAccountRegistry contract binding.
- [**OracleProvider**](#afp.bindings.OracleProvider) – OracleProvider contract binding.
- [**OracleSpecification**](#afp.bindings.OracleSpecification) – Port of `struct OracleSpecification` on the IProductRegistry contract.
- [**PositionData**](#afp.bindings.PositionData) – Port of `struct PositionData` on the IMarginAccount contract.
- [**PositionLossData**](#afp.bindings.PositionLossData) – Port of `struct PositionLossData` on the IBankruptcy contract.
- [**Product**](#afp.bindings.Product) – Port of `struct Product` on the IProductRegistry contract.
- [**ProductMetadata**](#afp.bindings.ProductMetadata) – Port of `struct ProductMetadata` on the IProductRegistry contract.
- [**ProductRegistry**](#afp.bindings.ProductRegistry) – ProductRegistry contract binding.
- [**ProductState**](#afp.bindings.ProductState) – Port of `enum ProductState` on the ProductRegistry contract.
- [**Settlement**](#afp.bindings.Settlement) – Port of `struct Settlement` on the IMarginAccount contract.
- [**Side**](#afp.bindings.Side) – Port of `enum Side` on the ClearingFacet contract.
- [**Trade**](#afp.bindings.Trade) – Port of `struct Trade` on the IClearing contract.
- [**TradingProtocol**](#afp.bindings.TradingProtocol) – TradingProtocol contract binding.

### afp.bindings.AuctionConfig

```python
AuctionConfig(restoration_buffer, liquidation_duration)
```

Port of `struct AuctionConfig` on the IAuctioneer contract.

**Attributes:**

- [**liquidation_duration**](#afp.bindings.AuctionConfig.liquidation_duration) (<code>[int](#int)</code>) –
- [**restoration_buffer**](#afp.bindings.AuctionConfig.restoration_buffer) (<code>[int](#int)</code>) –

#### afp.bindings.AuctionConfig.liquidation_duration

```python
liquidation_duration: int
```

#### afp.bindings.AuctionConfig.restoration_buffer

```python
restoration_buffer: int
```

### afp.bindings.AuctionData

```python
AuctionData(start_block, mae_at_initiation, mmu_at_initiation, mae_now, mmu_now)
```

Port of `struct AuctionData` on the IAuctioneer contract.

**Attributes:**

- [**mae_at_initiation**](#afp.bindings.AuctionData.mae_at_initiation) (<code>[int](#int)</code>) –
- [**mae_now**](#afp.bindings.AuctionData.mae_now) (<code>[int](#int)</code>) –
- [**mmu_at_initiation**](#afp.bindings.AuctionData.mmu_at_initiation) (<code>[int](#int)</code>) –
- [**mmu_now**](#afp.bindings.AuctionData.mmu_now) (<code>[int](#int)</code>) –
- [**start_block**](#afp.bindings.AuctionData.start_block) (<code>[int](#int)</code>) –

#### afp.bindings.AuctionData.mae_at_initiation

```python
mae_at_initiation: int
```

#### afp.bindings.AuctionData.mae_now

```python
mae_now: int
```

#### afp.bindings.AuctionData.mmu_at_initiation

```python
mmu_at_initiation: int
```

#### afp.bindings.AuctionData.mmu_now

```python
mmu_now: int
```

#### afp.bindings.AuctionData.start_block

```python
start_block: int
```

### afp.bindings.BidData

```python
BidData(product_id, price, quantity, side)
```

Port of `struct BidData` on the IAuctioneer contract.

**Attributes:**

- [**price**](#afp.bindings.BidData.price) (<code>[int](#int)</code>) –
- [**product_id**](#afp.bindings.BidData.product_id) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**quantity**](#afp.bindings.BidData.quantity) (<code>[int](#int)</code>) –
- [**side**](#afp.bindings.BidData.side) (<code>[Side](#afp.bindings.auctioneer_facet.Side)</code>) –

#### afp.bindings.BidData.price

```python
price: int
```

#### afp.bindings.BidData.product_id

```python
product_id: hexbytes.HexBytes
```

#### afp.bindings.BidData.quantity

```python
quantity: int
```

#### afp.bindings.BidData.side

```python
side: Side
```

### afp.bindings.ClearingConfig

```python
ClearingConfig(clearing_fee_rate)
```

Port of `struct ClearingConfig` on the IClearing contract.

**Attributes:**

- [**clearing_fee_rate**](#afp.bindings.ClearingConfig.clearing_fee_rate) (<code>[int](#int)</code>) –

#### afp.bindings.ClearingConfig.clearing_fee_rate

```python
clearing_fee_rate: int
```

### afp.bindings.ClearingDiamond

```python
ClearingDiamond(w3)
```

Bases: <code>[AuctioneerFacet](#afp.bindings.auctioneer_facet.AuctioneerFacet)</code>, <code>[BankruptcyFacet](#afp.bindings.bankruptcy_facet.BankruptcyFacet)</code>, <code>[ClearingFacet](#afp.bindings.clearing_facet.ClearingFacet)</code>, <code>[FinalSettlementFacet](#afp.bindings.final_settlement_facet.FinalSettlementFacet)</code>, <code>[MarkPriceTrackerFacet](#afp.bindings.mark_price_tracker_facet.MarkPriceTrackerFacet)</code>

ClearingDiamond contract binding.

Includes all functions inherited from various facets.

**Parameters:**

- **w3** (<code>[Web3](#web3.Web3)</code>) –

**Functions:**

- [**auction_config**](#afp.bindings.ClearingDiamond.auction_config) – Binding for `auctionConfig` on the AuctioneerFacet contract.
- [**auction_data**](#afp.bindings.ClearingDiamond.auction_data) – Binding for `auctionData` on the AuctioneerFacet contract.
- [**bid_auction**](#afp.bindings.ClearingDiamond.bid_auction) – Binding for `bidAuction` on the AuctioneerFacet contract.
- [**can_terminate_auctions**](#afp.bindings.ClearingDiamond.can_terminate_auctions) – Binding for `canTerminateAuctions` on the AuctioneerFacet contract.
- [**clearing_fee_rate**](#afp.bindings.ClearingDiamond.clearing_fee_rate) – Binding for `clearingFeeRate` on the ClearingFacet contract.
- [**closeout_fee_rate**](#afp.bindings.ClearingDiamond.closeout_fee_rate) – Binding for `CLOSEOUT_FEE_RATE` on the FinalSettlementFacet contract.
- [**closeout_reward_rate**](#afp.bindings.ClearingDiamond.closeout_reward_rate) – Binding for `CLOSEOUT_REWARD_RATE` on the FinalSettlementFacet contract.
- [**config**](#afp.bindings.ClearingDiamond.config) – Binding for `config` on the ClearingFacet contract.
- [**estimate_fees**](#afp.bindings.ClearingDiamond.estimate_fees) – Binding for `estimateFees` on the ClearingFacet contract.
- [**execute**](#afp.bindings.ClearingDiamond.execute) – Binding for `execute` on the ClearingFacet contract.
- [**finalize_fsp**](#afp.bindings.ClearingDiamond.finalize_fsp) – Binding for `finalizeFsp` on the FinalSettlementFacet contract.
- [**finalize_initialization**](#afp.bindings.ClearingDiamond.finalize_initialization) – Binding for `finalizeInitialization` on the ClearingFacet contract.
- [**get_admin**](#afp.bindings.ClearingDiamond.get_admin) – Binding for `getAdmin` on the ClearingFacet contract.
- [**get_fsp**](#afp.bindings.ClearingDiamond.get_fsp) – Binding for `getFsp` on the FinalSettlementFacet contract.
- [**get_margin_account_registry**](#afp.bindings.ClearingDiamond.get_margin_account_registry) – Binding for `getMarginAccountRegistry` on the ClearingFacet contract.
- [**get_product_registry**](#afp.bindings.ClearingDiamond.get_product_registry) – Binding for `getProductRegistry` on the ClearingFacet contract.
- [**get_treasury**](#afp.bindings.ClearingDiamond.get_treasury) – Binding for `getTreasury` on the ClearingFacet contract.
- [**hash_intent**](#afp.bindings.ClearingDiamond.hash_intent) – Binding for `hashIntent` on the ClearingFacet contract.
- [**initialize**](#afp.bindings.ClearingDiamond.initialize) – Binding for `initialize` on the ClearingFacet contract.
- [**initiate_final_settlement**](#afp.bindings.ClearingDiamond.initiate_final_settlement) – Binding for `initiateFinalSettlement` on the FinalSettlementFacet contract.
- [**is_admin_active**](#afp.bindings.ClearingDiamond.is_admin_active) – Binding for `isAdminActive` on the ClearingFacet contract.
- [**is_liquidatable**](#afp.bindings.ClearingDiamond.is_liquidatable) – Binding for `isLiquidatable` on the AuctioneerFacet contract.
- [**is_liquidating**](#afp.bindings.ClearingDiamond.is_liquidating) – Binding for `isLiquidating` on the AuctioneerFacet contract.
- [**last_traded_timestamp**](#afp.bindings.ClearingDiamond.last_traded_timestamp) – Binding for `lastTradedTimestamp` on the BankruptcyFacet contract.
- [**mae_check_on_bid**](#afp.bindings.ClearingDiamond.mae_check_on_bid) – Binding for `maeCheckOnBid` on the AuctioneerFacet contract.
- [**max_mae_offered**](#afp.bindings.ClearingDiamond.max_mae_offered) – Binding for `maxMaeOffered` on the AuctioneerFacet contract.
- [**max_trading_fee_rate**](#afp.bindings.ClearingDiamond.max_trading_fee_rate) – Binding for `MAX_TRADING_FEE_RATE` on the ClearingFacet contract.
- [**mutualize_losses**](#afp.bindings.ClearingDiamond.mutualize_losses) – Binding for `mutualizeLosses` on the BankruptcyFacet contract.
- [**open_interest**](#afp.bindings.ClearingDiamond.open_interest) – Binding for `openInterest` on the FinalSettlementFacet contract.
- [**request_liquidation**](#afp.bindings.ClearingDiamond.request_liquidation) – Binding for `requestLiquidation` on the AuctioneerFacet contract.
- [**set_active**](#afp.bindings.ClearingDiamond.set_active) – Binding for `setActive` on the ClearingFacet contract.
- [**set_admin**](#afp.bindings.ClearingDiamond.set_admin) – Binding for `setAdmin` on the ClearingFacet contract.
- [**set_config**](#afp.bindings.ClearingDiamond.set_config) – Binding for `setConfig` on the ClearingFacet contract.
- [**terminate_auctions**](#afp.bindings.ClearingDiamond.terminate_auctions) – Binding for `terminateAuctions` on the AuctioneerFacet contract.
- [**unique_trader_count**](#afp.bindings.ClearingDiamond.unique_trader_count) – Binding for `uniqueTraderCount` on the BankruptcyFacet contract.
- [**validate_auctions**](#afp.bindings.ClearingDiamond.validate_auctions) – Binding for `validateAuctions` on the AuctioneerFacet contract.
- [**validate_la_as**](#afp.bindings.ClearingDiamond.validate_la_as) – Binding for `validateLAAs` on the BankruptcyFacet contract.
- [**valuation**](#afp.bindings.ClearingDiamond.valuation) – Binding for `valuation` on the MarkPriceTrackerFacet contract.
- [**valuation_after_trade**](#afp.bindings.ClearingDiamond.valuation_after_trade) – Binding for `valuationAfterTrade` on the MarkPriceTrackerFacet contract.
- [**version**](#afp.bindings.ClearingDiamond.version) – Binding for `version` on the ClearingFacet contract.

**Attributes:**

- [**Auctioned**](#afp.bindings.ClearingDiamond.Auctioned) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Auctioned` on the AuctioneerFacet contract.
- [**LiquidationStarted**](#afp.bindings.ClearingDiamond.LiquidationStarted) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event LiquidationStarted` on the AuctioneerFacet contract.
- [**LiquidationTerminated**](#afp.bindings.ClearingDiamond.LiquidationTerminated) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event LiquidationTerminated` on the AuctioneerFacet contract.
- [**TradeExecuted**](#afp.bindings.ClearingDiamond.TradeExecuted) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event TradeExecuted` on the ClearingFacet contract.

#### afp.bindings.ClearingDiamond.Auctioned

```python
Auctioned: contract.ContractEvent
```

Binding for `event Auctioned` on the AuctioneerFacet contract.

#### afp.bindings.ClearingDiamond.LiquidationStarted

```python
LiquidationStarted: contract.ContractEvent
```

Binding for `event LiquidationStarted` on the AuctioneerFacet contract.

#### afp.bindings.ClearingDiamond.LiquidationTerminated

```python
LiquidationTerminated: contract.ContractEvent
```

Binding for `event LiquidationTerminated` on the AuctioneerFacet contract.

#### afp.bindings.ClearingDiamond.TradeExecuted

```python
TradeExecuted: contract.ContractEvent
```

Binding for `event TradeExecuted` on the ClearingFacet contract.

#### afp.bindings.ClearingDiamond.auction_config

```python
auction_config()
```

Binding for `auctionConfig` on the AuctioneerFacet contract.

**Returns:**

- <code>[AuctionConfig](#afp.bindings.auctioneer_facet.AuctionConfig)</code> –

#### afp.bindings.ClearingDiamond.auction_data

```python
auction_data(margin_account_id, collateral)
```

Binding for `auctionData` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[AuctionData](#afp.bindings.auctioneer_facet.AuctionData)</code> –

#### afp.bindings.ClearingDiamond.bid_auction

```python
bid_auction(margin_account_id, collateral_token, bids)
```

Binding for `bidAuction` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral_token** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **bids** (<code>[List](#typing.List)\[[BidData](#afp.bindings.auctioneer_facet.BidData)\]</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.can_terminate_auctions

```python
can_terminate_auctions(margin_account_id, collateral)
```

Binding for `canTerminateAuctions` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.ClearingDiamond.clearing_fee_rate

```python
clearing_fee_rate()
```

Binding for `clearingFeeRate` on the ClearingFacet contract.

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.closeout_fee_rate

```python
closeout_fee_rate()
```

Binding for `CLOSEOUT_FEE_RATE` on the FinalSettlementFacet contract.

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.closeout_reward_rate

```python
closeout_reward_rate()
```

Binding for `CLOSEOUT_REWARD_RATE` on the FinalSettlementFacet contract.

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.config

```python
config()
```

Binding for `config` on the ClearingFacet contract.

**Returns:**

- <code>[Config](#afp.bindings.clearing_facet.Config)</code> –

#### afp.bindings.ClearingDiamond.estimate_fees

```python
estimate_fees(product_id, price, quantity, trading_fee_rate)
```

Binding for `estimateFees` on the ClearingFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **price** (<code>[int](#int)</code>) –
- **quantity** (<code>[int](#int)</code>) –
- **trading_fee_rate** (<code>[int](#int)</code>) –

**Returns:**

- <code>[int](#int)</code> –
- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.execute

```python
execute(trade, fallback_on_failure)
```

Binding for `execute` on the ClearingFacet contract.

**Parameters:**

- **trade** (<code>[Trade](#afp.bindings.clearing_facet.Trade)</code>) –
- **fallback_on_failure** (<code>[bool](#bool)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.finalize_fsp

```python
finalize_fsp(product_id)
```

Binding for `finalizeFsp` on the FinalSettlementFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.finalize_initialization

```python
finalize_initialization(margin_account_registry)
```

Binding for `finalizeInitialization` on the ClearingFacet contract.

**Parameters:**

- **margin_account_registry** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.get_admin

```python
get_admin()
```

Binding for `getAdmin` on the ClearingFacet contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.ClearingDiamond.get_fsp

```python
get_fsp(product_id)
```

Binding for `getFsp` on the FinalSettlementFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –
- <code>[bool](#bool)</code> –

#### afp.bindings.ClearingDiamond.get_margin_account_registry

```python
get_margin_account_registry()
```

Binding for `getMarginAccountRegistry` on the ClearingFacet contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.ClearingDiamond.get_product_registry

```python
get_product_registry()
```

Binding for `getProductRegistry` on the ClearingFacet contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.ClearingDiamond.get_treasury

```python
get_treasury()
```

Binding for `getTreasury` on the ClearingFacet contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.ClearingDiamond.hash_intent

```python
hash_intent(intent)
```

Binding for `hashIntent` on the ClearingFacet contract.

**Parameters:**

- **intent** (<code>[Intent](#afp.bindings.clearing_facet.Intent)</code>) –

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.ClearingDiamond.initialize

```python
initialize(_product_registry, _treasury)
```

Binding for `initialize` on the ClearingFacet contract.

**Parameters:**

- **\_product_registry** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **\_treasury** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.initiate_final_settlement

```python
initiate_final_settlement(product_id, accounts)
```

Binding for `initiateFinalSettlement` on the FinalSettlementFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **accounts** (<code>[List](#typing.List)\[[ChecksumAddress](#eth_typing.ChecksumAddress)\]</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.is_admin_active

```python
is_admin_active()
```

Binding for `isAdminActive` on the ClearingFacet contract.

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.ClearingDiamond.is_liquidatable

```python
is_liquidatable(margin_account_id, collateral_token)
```

Binding for `isLiquidatable` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral_token** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.ClearingDiamond.is_liquidating

```python
is_liquidating(margin_account_id, collateral_token)
```

Binding for `isLiquidating` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral_token** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.ClearingDiamond.last_traded_timestamp

```python
last_traded_timestamp(product_id, trader)
```

Binding for `lastTradedTimestamp` on the BankruptcyFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **trader** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.mae_check_on_bid

```python
mae_check_on_bid(liquidator_margin_account_id, liquidating_margin_account_id, collateral, bids)
```

Binding for `maeCheckOnBid` on the AuctioneerFacet contract.

**Parameters:**

- **liquidator_margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **liquidating_margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **bids** (<code>[List](#typing.List)\[[BidData](#afp.bindings.auctioneer_facet.BidData)\]</code>) –

**Returns:**

- <code>[bool](#bool)</code> –
- <code>[bool](#bool)</code> –

#### afp.bindings.ClearingDiamond.max_mae_offered

```python
max_mae_offered(margin_account_id, collateral, mmu_decreased)
```

Binding for `maxMaeOffered` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **mmu_decreased** (<code>[int](#int)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.max_trading_fee_rate

```python
max_trading_fee_rate()
```

Binding for `MAX_TRADING_FEE_RATE` on the ClearingFacet contract.

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.mutualize_losses

```python
mutualize_losses(bankrupt_account_id, collateral_token, product_ids, laas)
```

Binding for `mutualizeLosses` on the BankruptcyFacet contract.

**Parameters:**

- **bankrupt_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral_token** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **product_ids** (<code>[List](#typing.List)\[[HexBytes](#hexbytes.HexBytes)\]</code>) –
- **laas** (<code>[List](#typing.List)\[[ChecksumAddress](#eth_typing.ChecksumAddress)\]</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.open_interest

```python
open_interest(product_id)
```

Binding for `openInterest` on the FinalSettlementFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.request_liquidation

```python
request_liquidation(margin_account_id, collateral_token)
```

Binding for `requestLiquidation` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral_token** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.set_active

```python
set_active(active)
```

Binding for `setActive` on the ClearingFacet contract.

**Parameters:**

- **active** (<code>[bool](#bool)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.set_admin

```python
set_admin(new_admin)
```

Binding for `setAdmin` on the ClearingFacet contract.

**Parameters:**

- **new_admin** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.set_config

```python
set_config(_config)
```

Binding for `setConfig` on the ClearingFacet contract.

**Parameters:**

- **\_config** (<code>[Config](#afp.bindings.clearing_facet.Config)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.terminate_auctions

```python
terminate_auctions(margin_account_id, collateral)
```

Binding for `terminateAuctions` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ClearingDiamond.unique_trader_count

```python
unique_trader_count(product_id)
```

Binding for `uniqueTraderCount` on the BankruptcyFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.validate_auctions

```python
validate_auctions(margin_account_id, collateral_token, bids)
```

Binding for `validateAuctions` on the AuctioneerFacet contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **collateral_token** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **bids** (<code>[List](#typing.List)\[[BidData](#afp.bindings.auctioneer_facet.BidData)\]</code>) –

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.ClearingDiamond.validate_la_as

```python
validate_la_as(margin_account, bankrupt_account, product_id, product_owners)
```

Binding for `validateLAAs` on the BankruptcyFacet contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **bankrupt_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **product_owners** (<code>[List](#typing.List)\[[ChecksumAddress](#eth_typing.ChecksumAddress)\]</code>) –

**Returns:**

- <code>[PositionLossData](#afp.bindings.bankruptcy_facet.PositionLossData)</code> –

#### afp.bindings.ClearingDiamond.valuation

```python
valuation(product_id)
```

Binding for `valuation` on the MarkPriceTrackerFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.valuation_after_trade

```python
valuation_after_trade(product_id, price, quantity)
```

Binding for `valuationAfterTrade` on the MarkPriceTrackerFacet contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **price** (<code>[int](#int)</code>) –
- **quantity** (<code>[int](#int)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ClearingDiamond.version

```python
version()
```

Binding for `version` on the ClearingFacet contract.

**Returns:**

- <code>[str](#str)</code> –

### afp.bindings.Config

```python
Config(auction_config, clearing_config)
```

Port of `struct Config` on the IClearing contract.

**Attributes:**

- [**auction_config**](#afp.bindings.Config.auction_config) (<code>[AuctionConfig](#afp.bindings.clearing_facet.AuctionConfig)</code>) –
- [**clearing_config**](#afp.bindings.Config.clearing_config) (<code>[ClearingConfig](#afp.bindings.clearing_facet.ClearingConfig)</code>) –

#### afp.bindings.Config.auction_config

```python
auction_config: AuctionConfig
```

#### afp.bindings.Config.clearing_config

```python
clearing_config: ClearingConfig
```

### afp.bindings.Intent

```python
Intent(margin_account_id, intent_account_id, hash, data, signature)
```

Port of `struct Intent` on the IClearing contract.

**Attributes:**

- [**data**](#afp.bindings.Intent.data) (<code>[IntentData](#afp.bindings.clearing_facet.IntentData)</code>) –
- [**hash**](#afp.bindings.Intent.hash) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**intent_account_id**](#afp.bindings.Intent.intent_account_id) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- [**margin_account_id**](#afp.bindings.Intent.margin_account_id) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- [**signature**](#afp.bindings.Intent.signature) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

#### afp.bindings.Intent.data

```python
data: IntentData
```

#### afp.bindings.Intent.hash

```python
hash: hexbytes.HexBytes
```

#### afp.bindings.Intent.intent_account_id

```python
intent_account_id: eth_typing.ChecksumAddress
```

#### afp.bindings.Intent.margin_account_id

```python
margin_account_id: eth_typing.ChecksumAddress
```

#### afp.bindings.Intent.signature

```python
signature: hexbytes.HexBytes
```

### afp.bindings.IntentData

```python
IntentData(nonce, trading_protocol_id, product_id, limit_price, quantity, max_trading_fee_rate, good_until, side)
```

Port of `struct IntentData` on the IClearing contract.

**Attributes:**

- [**good_until**](#afp.bindings.IntentData.good_until) (<code>[int](#int)</code>) –
- [**limit_price**](#afp.bindings.IntentData.limit_price) (<code>[int](#int)</code>) –
- [**max_trading_fee_rate**](#afp.bindings.IntentData.max_trading_fee_rate) (<code>[int](#int)</code>) –
- [**nonce**](#afp.bindings.IntentData.nonce) (<code>[int](#int)</code>) –
- [**product_id**](#afp.bindings.IntentData.product_id) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**quantity**](#afp.bindings.IntentData.quantity) (<code>[int](#int)</code>) –
- [**side**](#afp.bindings.IntentData.side) (<code>[Side](#afp.bindings.clearing_facet.Side)</code>) –
- [**trading_protocol_id**](#afp.bindings.IntentData.trading_protocol_id) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

#### afp.bindings.IntentData.good_until

```python
good_until: int
```

#### afp.bindings.IntentData.limit_price

```python
limit_price: int
```

#### afp.bindings.IntentData.max_trading_fee_rate

```python
max_trading_fee_rate: int
```

#### afp.bindings.IntentData.nonce

```python
nonce: int
```

#### afp.bindings.IntentData.product_id

```python
product_id: hexbytes.HexBytes
```

#### afp.bindings.IntentData.quantity

```python
quantity: int
```

#### afp.bindings.IntentData.side

```python
side: Side
```

#### afp.bindings.IntentData.trading_protocol_id

```python
trading_protocol_id: eth_typing.ChecksumAddress
```

### afp.bindings.LAAData

```python
LAAData(owner, quantity, last_traded_timestamp, position_age)
```

Port of `struct LAAData` on the IBankruptcy contract.

**Attributes:**

- [**last_traded_timestamp**](#afp.bindings.LAAData.last_traded_timestamp) (<code>[int](#int)</code>) –
- [**owner**](#afp.bindings.LAAData.owner) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- [**position_age**](#afp.bindings.LAAData.position_age) (<code>[int](#int)</code>) –
- [**quantity**](#afp.bindings.LAAData.quantity) (<code>[int](#int)</code>) –

#### afp.bindings.LAAData.last_traded_timestamp

```python
last_traded_timestamp: int
```

#### afp.bindings.LAAData.owner

```python
owner: eth_typing.ChecksumAddress
```

#### afp.bindings.LAAData.position_age

```python
position_age: int
```

#### afp.bindings.LAAData.quantity

```python
quantity: int
```

### afp.bindings.MarginAccount

```python
MarginAccount(w3, address)
```

MarginAccount contract binding.

**Parameters:**

- **w3** (<code>[Web3](#web3.Web3)</code>) –
- **address** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) – The address of a deployed MarginAccount contract.

**Functions:**

- [**authorize**](#afp.bindings.MarginAccount.authorize) – Binding for `authorize` on the MarginAccount contract.
- [**authorized**](#afp.bindings.MarginAccount.authorized) – Binding for `authorized` on the MarginAccount contract.
- [**batch_mae_check**](#afp.bindings.MarginAccount.batch_mae_check) – Binding for `batchMaeCheck` on the MarginAccount contract.
- [**batch_settle**](#afp.bindings.MarginAccount.batch_settle) – Binding for `batchSettle` on the MarginAccount contract.
- [**capital**](#afp.bindings.MarginAccount.capital) – Binding for `capital` on the MarginAccount contract.
- [**clearing**](#afp.bindings.MarginAccount.clearing) – Binding for `clearing` on the MarginAccount contract.
- [**collateral_asset**](#afp.bindings.MarginAccount.collateral_asset) – Binding for `collateralAsset` on the MarginAccount contract.
- [**collateral_token**](#afp.bindings.MarginAccount.collateral_token) – Binding for `collateralToken` on the MarginAccount contract.
- [**collect_fee**](#afp.bindings.MarginAccount.collect_fee) – Binding for `collectFee` on the MarginAccount contract.
- [**deposit**](#afp.bindings.MarginAccount.deposit) – Binding for `deposit` on the MarginAccount contract.
- [**disperse_fees**](#afp.bindings.MarginAccount.disperse_fees) – Binding for `disperseFees` on the MarginAccount contract.
- [**estimate_liquidation_price**](#afp.bindings.MarginAccount.estimate_liquidation_price) – Binding for `estimateLiquidationPrice` on the MarginAccount contract.
- [**estimate_liquidation_price_for_position**](#afp.bindings.MarginAccount.estimate_liquidation_price_for_position) – Binding for `estimateLiquidationPriceForPosition` on the MarginAccount contract.
- [**initialize**](#afp.bindings.MarginAccount.initialize) – Binding for `initialize` on the MarginAccount contract.
- [**mae**](#afp.bindings.MarginAccount.mae) – Binding for `mae` on the MarginAccount contract.
- [**mae_and_mmu_after_batch_trade**](#afp.bindings.MarginAccount.mae_and_mmu_after_batch_trade) – Binding for `maeAndMmuAfterBatchTrade` on the MarginAccount contract.
- [**mae_check**](#afp.bindings.MarginAccount.mae_check) – Binding for `maeCheck` on the MarginAccount contract.
- [**mma**](#afp.bindings.MarginAccount.mma) – Binding for `mma` on the MarginAccount contract.
- [**mmu**](#afp.bindings.MarginAccount.mmu) – Binding for `mmu` on the MarginAccount contract.
- [**pnl**](#afp.bindings.MarginAccount.pnl) – Binding for `pnl` on the MarginAccount contract.
- [**position_age**](#afp.bindings.MarginAccount.position_age) – Binding for `positionAge` on the MarginAccount contract.
- [**position_count**](#afp.bindings.MarginAccount.position_count) – Binding for `positionCount` on the MarginAccount contract.
- [**position_data**](#afp.bindings.MarginAccount.position_data) – Binding for `positionData` on the MarginAccount contract.
- [**position_pn_l**](#afp.bindings.MarginAccount.position_pn_l) – Binding for `positionPnL` on the MarginAccount contract.
- [**position_quantity**](#afp.bindings.MarginAccount.position_quantity) – Binding for `positionQuantity` on the MarginAccount contract.
- [**positions**](#afp.bindings.MarginAccount.positions) – Binding for `positions` on the MarginAccount contract.
- [**product_registry**](#afp.bindings.MarginAccount.product_registry) – Binding for `productRegistry` on the MarginAccount contract.
- [**revoke_authorization**](#afp.bindings.MarginAccount.revoke_authorization) – Binding for `revokeAuthorization` on the MarginAccount contract.
- [**settle**](#afp.bindings.MarginAccount.settle) – Binding for `settle` on the MarginAccount contract.
- [**valuation**](#afp.bindings.MarginAccount.valuation) – Binding for `valuation` on the MarginAccount contract.
- [**withdraw**](#afp.bindings.MarginAccount.withdraw) – Binding for `withdraw` on the MarginAccount contract.
- [**withdrawable**](#afp.bindings.MarginAccount.withdrawable) – Binding for `withdrawable` on the MarginAccount contract.

**Attributes:**

- [**FeeCollected**](#afp.bindings.MarginAccount.FeeCollected) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event FeeCollected` on the MarginAccount contract.
- [**FeeDispersed**](#afp.bindings.MarginAccount.FeeDispersed) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event FeeDispersed` on the MarginAccount contract.
- [**Initialized**](#afp.bindings.MarginAccount.Initialized) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Initialized` on the MarginAccount contract.
- [**PositionUpdated**](#afp.bindings.MarginAccount.PositionUpdated) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event PositionUpdated` on the MarginAccount contract.

#### afp.bindings.MarginAccount.FeeCollected

```python
FeeCollected: contract.ContractEvent
```

Binding for `event FeeCollected` on the MarginAccount contract.

#### afp.bindings.MarginAccount.FeeDispersed

```python
FeeDispersed: contract.ContractEvent
```

Binding for `event FeeDispersed` on the MarginAccount contract.

#### afp.bindings.MarginAccount.Initialized

```python
Initialized: contract.ContractEvent
```

Binding for `event Initialized` on the MarginAccount contract.

#### afp.bindings.MarginAccount.PositionUpdated

```python
PositionUpdated: contract.ContractEvent
```

Binding for `event PositionUpdated` on the MarginAccount contract.

#### afp.bindings.MarginAccount.authorize

```python
authorize(intent_account)
```

Binding for `authorize` on the MarginAccount contract.

**Parameters:**

- **intent_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.authorized

```python
authorized(margin_account, intent_account)
```

Binding for `authorized` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **intent_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.MarginAccount.batch_mae_check

```python
batch_mae_check(margin_account, settlements, mark_price_if_settled)
```

Binding for `batchMaeCheck` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **settlements** (<code>[List](#typing.List)\[[Settlement](#afp.bindings.margin_account.Settlement)\]</code>) –
- **mark_price_if_settled** (<code>[List](#typing.List)\[[int](#int)\]</code>) –

**Returns:**

- <code>[bool](#bool)</code> –
- <code>[int](#int)</code> –
- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.batch_settle

```python
batch_settle(margin_account_id, settlements)
```

Binding for `batchSettle` on the MarginAccount contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **settlements** (<code>[List](#typing.List)\[[Settlement](#afp.bindings.margin_account.Settlement)\]</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.capital

```python
capital(margin_account)
```

Binding for `capital` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.clearing

```python
clearing()
```

Binding for `clearing` on the MarginAccount contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccount.collateral_asset

```python
collateral_asset()
```

Binding for `collateralAsset` on the MarginAccount contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccount.collateral_token

```python
collateral_token()
```

Binding for `collateralToken` on the MarginAccount contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccount.collect_fee

```python
collect_fee(margin_account, capital_amount)
```

Binding for `collectFee` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **capital_amount** (<code>[int](#int)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.deposit

```python
deposit(amount)
```

Binding for `deposit` on the MarginAccount contract.

**Parameters:**

- **amount** (<code>[int](#int)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.disperse_fees

```python
disperse_fees(recipients, capital_amounts)
```

Binding for `disperseFees` on the MarginAccount contract.

**Parameters:**

- **recipients** (<code>[List](#typing.List)\[[ChecksumAddress](#eth_typing.ChecksumAddress)\]</code>) –
- **capital_amounts** (<code>[List](#typing.List)\[[int](#int)\]</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.estimate_liquidation_price

```python
estimate_liquidation_price(margin_account_id, product_id, price, quantity)
```

Binding for `estimateLiquidationPrice` on the MarginAccount contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **price** (<code>[int](#int)</code>) –
- **quantity** (<code>[int](#int)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.estimate_liquidation_price_for_position

```python
estimate_liquidation_price_for_position(margin_account_id, position_id)
```

Binding for `estimateLiquidationPriceForPosition` on the MarginAccount contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **position_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.initialize

```python
initialize(_collateral_token, _valuation, _product_registry, _clearing)
```

Binding for `initialize` on the MarginAccount contract.

**Parameters:**

- **\_collateral_token** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **\_valuation** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **\_product_registry** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **\_clearing** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.mae

```python
mae(margin_account)
```

Binding for `mae` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.mae_and_mmu_after_batch_trade

```python
mae_and_mmu_after_batch_trade(margin_account, settlements, mark_price_if_settled)
```

Binding for `maeAndMmuAfterBatchTrade` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **settlements** (<code>[List](#typing.List)\[[Settlement](#afp.bindings.margin_account.Settlement)\]</code>) –
- **mark_price_if_settled** (<code>[List](#typing.List)\[[int](#int)\]</code>) –

**Returns:**

- <code>[int](#int)</code> –
- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.mae_check

```python
mae_check(margin_account, settlement, mark_price_if_settled)
```

Binding for `maeCheck` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **settlement** (<code>[Settlement](#afp.bindings.margin_account.Settlement)</code>) –
- **mark_price_if_settled** (<code>[int](#int)</code>) –

**Returns:**

- <code>[bool](#bool)</code> –
- <code>[int](#int)</code> –
- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.mma

```python
mma(margin_account)
```

Binding for `mma` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.mmu

```python
mmu(margin_account)
```

Binding for `mmu` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.pnl

```python
pnl(margin_account)
```

Binding for `pnl` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.position_age

```python
position_age(margin_account_id, position_id)
```

Binding for `positionAge` on the MarginAccount contract.

**Parameters:**

- **margin_account_id** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **position_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.position_count

```python
position_count(margin_account)
```

Binding for `positionCount` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.position_data

```python
position_data(margin_account, position_id)
```

Binding for `positionData` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **position_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[PositionData](#afp.bindings.margin_account.PositionData)</code> –

#### afp.bindings.MarginAccount.position_pn_l

```python
position_pn_l(margin_account, position_id)
```

Binding for `positionPnL` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **position_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.position_quantity

```python
position_quantity(margin_account, position_id)
```

Binding for `positionQuantity` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **position_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.MarginAccount.positions

```python
positions(margin_account)
```

Binding for `positions` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[List](#typing.List)\[[HexBytes](#hexbytes.HexBytes)\]</code> –

#### afp.bindings.MarginAccount.product_registry

```python
product_registry()
```

Binding for `productRegistry` on the MarginAccount contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccount.revoke_authorization

```python
revoke_authorization(intent_account)
```

Binding for `revokeAuthorization` on the MarginAccount contract.

**Parameters:**

- **intent_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.settle

```python
settle(margin_account, intent_account, settlement)
```

Binding for `settle` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **intent_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **settlement** (<code>[Settlement](#afp.bindings.margin_account.Settlement)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.valuation

```python
valuation()
```

Binding for `valuation` on the MarginAccount contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccount.withdraw

```python
withdraw(amount)
```

Binding for `withdraw` on the MarginAccount contract.

**Parameters:**

- **amount** (<code>[int](#int)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccount.withdrawable

```python
withdrawable(margin_account)
```

Binding for `withdrawable` on the MarginAccount contract.

**Parameters:**

- **margin_account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[int](#int)</code> –

### afp.bindings.MarginAccountRegistry

```python
MarginAccountRegistry(w3)
```

Bases: <code>[MarginAccountRegistry](#afp.bindings.margin_account_registry.MarginAccountRegistry)</code>

MarginAccountRegistry contract binding.

**Parameters:**

- **w3** (<code>[Web3](#web3.Web3)</code>) –

**Functions:**

- [**clearing**](#afp.bindings.MarginAccountRegistry.clearing) – Binding for `clearing` on the MarginAccountRegistry contract.
- [**get_admin**](#afp.bindings.MarginAccountRegistry.get_admin) – Binding for `getAdmin` on the MarginAccountRegistry contract.
- [**get_margin_account**](#afp.bindings.MarginAccountRegistry.get_margin_account) – Binding for `getMarginAccount` on the MarginAccountRegistry contract.
- [**initialize**](#afp.bindings.MarginAccountRegistry.initialize) – Binding for `initialize` on the MarginAccountRegistry contract.
- [**initialize_margin_account**](#afp.bindings.MarginAccountRegistry.initialize_margin_account) – Binding for `initializeMarginAccount` on the MarginAccountRegistry contract.
- [**is_admin_active**](#afp.bindings.MarginAccountRegistry.is_admin_active) – Binding for `isAdminActive` on the MarginAccountRegistry contract.
- [**margin_accounts**](#afp.bindings.MarginAccountRegistry.margin_accounts) – Binding for `marginAccounts` on the MarginAccountRegistry contract.
- [**owner**](#afp.bindings.MarginAccountRegistry.owner) – Binding for `owner` on the MarginAccountRegistry contract.
- [**product_registry**](#afp.bindings.MarginAccountRegistry.product_registry) – Binding for `productRegistry` on the MarginAccountRegistry contract.
- [**proxiable_uuid**](#afp.bindings.MarginAccountRegistry.proxiable_uuid) – Binding for `proxiableUUID` on the MarginAccountRegistry contract.
- [**renounce_ownership**](#afp.bindings.MarginAccountRegistry.renounce_ownership) – Binding for `renounceOwnership` on the MarginAccountRegistry contract.
- [**set_active**](#afp.bindings.MarginAccountRegistry.set_active) – Binding for `setActive` on the MarginAccountRegistry contract.
- [**set_admin**](#afp.bindings.MarginAccountRegistry.set_admin) – Binding for `setAdmin` on the MarginAccountRegistry contract.
- [**transfer_ownership**](#afp.bindings.MarginAccountRegistry.transfer_ownership) – Binding for `transferOwnership` on the MarginAccountRegistry contract.
- [**upgrade_interface_version**](#afp.bindings.MarginAccountRegistry.upgrade_interface_version) – Binding for `UPGRADE_INTERFACE_VERSION` on the MarginAccountRegistry contract.
- [**upgrade_to_and_call**](#afp.bindings.MarginAccountRegistry.upgrade_to_and_call) – Binding for `upgradeToAndCall` on the MarginAccountRegistry contract.
- [**valuation**](#afp.bindings.MarginAccountRegistry.valuation) – Binding for `valuation` on the MarginAccountRegistry contract.

**Attributes:**

- [**Initialized**](#afp.bindings.MarginAccountRegistry.Initialized) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Initialized` on the MarginAccountRegistry contract.
- [**MarginAccountCreated**](#afp.bindings.MarginAccountRegistry.MarginAccountCreated) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event MarginAccountCreated` on the MarginAccountRegistry contract.
- [**OwnershipTransferred**](#afp.bindings.MarginAccountRegistry.OwnershipTransferred) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event OwnershipTransferred` on the MarginAccountRegistry contract.
- [**Upgraded**](#afp.bindings.MarginAccountRegistry.Upgraded) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Upgraded` on the MarginAccountRegistry contract.

#### afp.bindings.MarginAccountRegistry.Initialized

```python
Initialized: contract.ContractEvent
```

Binding for `event Initialized` on the MarginAccountRegistry contract.

#### afp.bindings.MarginAccountRegistry.MarginAccountCreated

```python
MarginAccountCreated: contract.ContractEvent
```

Binding for `event MarginAccountCreated` on the MarginAccountRegistry contract.

#### afp.bindings.MarginAccountRegistry.OwnershipTransferred

```python
OwnershipTransferred: contract.ContractEvent
```

Binding for `event OwnershipTransferred` on the MarginAccountRegistry contract.

#### afp.bindings.MarginAccountRegistry.Upgraded

```python
Upgraded: contract.ContractEvent
```

Binding for `event Upgraded` on the MarginAccountRegistry contract.

#### afp.bindings.MarginAccountRegistry.clearing

```python
clearing()
```

Binding for `clearing` on the MarginAccountRegistry contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccountRegistry.get_admin

```python
get_admin()
```

Binding for `getAdmin` on the MarginAccountRegistry contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccountRegistry.get_margin_account

```python
get_margin_account(collateral_asset)
```

Binding for `getMarginAccount` on the MarginAccountRegistry contract.

**Parameters:**

- **collateral_asset** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccountRegistry.initialize

```python
initialize(_clearing, _valuation, _product_registry, beacon_)
```

Binding for `initialize` on the MarginAccountRegistry contract.

**Parameters:**

- **\_clearing** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **\_valuation** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **\_product_registry** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **beacon\_** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccountRegistry.initialize_margin_account

```python
initialize_margin_account(collateral_asset)
```

Binding for `initializeMarginAccount` on the MarginAccountRegistry contract.

**Parameters:**

- **collateral_asset** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccountRegistry.is_admin_active

```python
is_admin_active()
```

Binding for `isAdminActive` on the MarginAccountRegistry contract.

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.MarginAccountRegistry.margin_accounts

```python
margin_accounts(key0)
```

Binding for `marginAccounts` on the MarginAccountRegistry contract.

**Parameters:**

- **key0** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccountRegistry.owner

```python
owner()
```

Binding for `owner` on the MarginAccountRegistry contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccountRegistry.product_registry

```python
product_registry()
```

Binding for `productRegistry` on the MarginAccountRegistry contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.MarginAccountRegistry.proxiable_uuid

```python
proxiable_uuid()
```

Binding for `proxiableUUID` on the MarginAccountRegistry contract.

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.MarginAccountRegistry.renounce_ownership

```python
renounce_ownership()
```

Binding for `renounceOwnership` on the MarginAccountRegistry contract.

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccountRegistry.set_active

```python
set_active(active)
```

Binding for `setActive` on the MarginAccountRegistry contract.

**Parameters:**

- **active** (<code>[bool](#bool)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccountRegistry.set_admin

```python
set_admin(new_admin)
```

Binding for `setAdmin` on the MarginAccountRegistry contract.

**Parameters:**

- **new_admin** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccountRegistry.transfer_ownership

```python
transfer_ownership(new_owner)
```

Binding for `transferOwnership` on the MarginAccountRegistry contract.

**Parameters:**

- **new_owner** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccountRegistry.upgrade_interface_version

```python
upgrade_interface_version()
```

Binding for `UPGRADE_INTERFACE_VERSION` on the MarginAccountRegistry contract.

**Returns:**

- <code>[str](#str)</code> –

#### afp.bindings.MarginAccountRegistry.upgrade_to_and_call

```python
upgrade_to_and_call(new_implementation, data)
```

Binding for `upgradeToAndCall` on the MarginAccountRegistry contract.

**Parameters:**

- **new_implementation** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **data** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.MarginAccountRegistry.valuation

```python
valuation()
```

Binding for `valuation` on the MarginAccountRegistry contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

### afp.bindings.OracleProvider

```python
OracleProvider(w3)
```

Bases: <code>[OracleProvider](#afp.bindings.oracle_provider.OracleProvider)</code>

OracleProvider contract binding.

**Parameters:**

- **w3** (<code>[Web3](#web3.Web3)</code>) –

**Functions:**

- [**get_admin**](#afp.bindings.OracleProvider.get_admin) – Binding for `getAdmin` on the OracleProvider contract.
- [**initialize**](#afp.bindings.OracleProvider.initialize) – Binding for `initialize` on the OracleProvider contract.
- [**is_admin_active**](#afp.bindings.OracleProvider.is_admin_active) – Binding for `isAdminActive` on the OracleProvider contract.
- [**owner**](#afp.bindings.OracleProvider.owner) – Binding for `owner` on the OracleProvider contract.
- [**product_registry**](#afp.bindings.OracleProvider.product_registry) – Binding for `productRegistry` on the OracleProvider contract.
- [**proxiable_uuid**](#afp.bindings.OracleProvider.proxiable_uuid) – Binding for `proxiableUUID` on the OracleProvider contract.
- [**renounce_ownership**](#afp.bindings.OracleProvider.renounce_ownership) – Binding for `renounceOwnership` on the OracleProvider contract.
- [**resolve**](#afp.bindings.OracleProvider.resolve) – Binding for `resolve` on the OracleProvider contract.
- [**set_active**](#afp.bindings.OracleProvider.set_active) – Binding for `setActive` on the OracleProvider contract.
- [**set_admin**](#afp.bindings.OracleProvider.set_admin) – Binding for `setAdmin` on the OracleProvider contract.
- [**submit**](#afp.bindings.OracleProvider.submit) – Binding for `submit` on the OracleProvider contract.
- [**transfer_ownership**](#afp.bindings.OracleProvider.transfer_ownership) – Binding for `transferOwnership` on the OracleProvider contract.
- [**upgrade_interface_version**](#afp.bindings.OracleProvider.upgrade_interface_version) – Binding for `UPGRADE_INTERFACE_VERSION` on the OracleProvider contract.
- [**upgrade_to_and_call**](#afp.bindings.OracleProvider.upgrade_to_and_call) – Binding for `upgradeToAndCall` on the OracleProvider contract.

**Attributes:**

- [**Initialized**](#afp.bindings.OracleProvider.Initialized) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Initialized` on the OracleProvider contract.
- [**OwnershipTransferred**](#afp.bindings.OracleProvider.OwnershipTransferred) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event OwnershipTransferred` on the OracleProvider contract.
- [**PriceSubmitted**](#afp.bindings.OracleProvider.PriceSubmitted) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event PriceSubmitted` on the OracleProvider contract.
- [**Upgraded**](#afp.bindings.OracleProvider.Upgraded) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Upgraded` on the OracleProvider contract.

#### afp.bindings.OracleProvider.Initialized

```python
Initialized: contract.ContractEvent
```

Binding for `event Initialized` on the OracleProvider contract.

#### afp.bindings.OracleProvider.OwnershipTransferred

```python
OwnershipTransferred: contract.ContractEvent
```

Binding for `event OwnershipTransferred` on the OracleProvider contract.

#### afp.bindings.OracleProvider.PriceSubmitted

```python
PriceSubmitted: contract.ContractEvent
```

Binding for `event PriceSubmitted` on the OracleProvider contract.

#### afp.bindings.OracleProvider.Upgraded

```python
Upgraded: contract.ContractEvent
```

Binding for `event Upgraded` on the OracleProvider contract.

#### afp.bindings.OracleProvider.get_admin

```python
get_admin()
```

Binding for `getAdmin` on the OracleProvider contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.OracleProvider.initialize

```python
initialize(_product_registry)
```

Binding for `initialize` on the OracleProvider contract.

**Parameters:**

- **\_product_registry** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.OracleProvider.is_admin_active

```python
is_admin_active()
```

Binding for `isAdminActive` on the OracleProvider contract.

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.OracleProvider.owner

```python
owner()
```

Binding for `owner` on the OracleProvider contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.OracleProvider.product_registry

```python
product_registry()
```

Binding for `productRegistry` on the OracleProvider contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.OracleProvider.proxiable_uuid

```python
proxiable_uuid()
```

Binding for `proxiableUUID` on the OracleProvider contract.

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.OracleProvider.renounce_ownership

```python
renounce_ownership()
```

Binding for `renounceOwnership` on the OracleProvider contract.

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.OracleProvider.resolve

```python
resolve(product_id, key1)
```

Binding for `resolve` on the OracleProvider contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **key1** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.OracleProvider.set_active

```python
set_active(active)
```

Binding for `setActive` on the OracleProvider contract.

**Parameters:**

- **active** (<code>[bool](#bool)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.OracleProvider.set_admin

```python
set_admin(admin)
```

Binding for `setAdmin` on the OracleProvider contract.

**Parameters:**

- **admin** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.OracleProvider.submit

```python
submit(key, fsp)
```

Binding for `submit` on the OracleProvider contract.

**Parameters:**

- **key** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **fsp** (<code>[int](#int)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.OracleProvider.transfer_ownership

```python
transfer_ownership(new_owner)
```

Binding for `transferOwnership` on the OracleProvider contract.

**Parameters:**

- **new_owner** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.OracleProvider.upgrade_interface_version

```python
upgrade_interface_version()
```

Binding for `UPGRADE_INTERFACE_VERSION` on the OracleProvider contract.

**Returns:**

- <code>[str](#str)</code> –

#### afp.bindings.OracleProvider.upgrade_to_and_call

```python
upgrade_to_and_call(new_implementation, data)
```

Binding for `upgradeToAndCall` on the OracleProvider contract.

**Parameters:**

- **new_implementation** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **data** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

### afp.bindings.OracleSpecification

```python
OracleSpecification(oracle_address, fsv_decimals, fsp_alpha, fsp_beta, fsv_calldata)
```

Port of `struct OracleSpecification` on the IProductRegistry contract.

**Attributes:**

- [**fsp_alpha**](#afp.bindings.OracleSpecification.fsp_alpha) (<code>[int](#int)</code>) –
- [**fsp_beta**](#afp.bindings.OracleSpecification.fsp_beta) (<code>[int](#int)</code>) –
- [**fsv_calldata**](#afp.bindings.OracleSpecification.fsv_calldata) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**fsv_decimals**](#afp.bindings.OracleSpecification.fsv_decimals) (<code>[int](#int)</code>) –
- [**oracle_address**](#afp.bindings.OracleSpecification.oracle_address) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

#### afp.bindings.OracleSpecification.fsp_alpha

```python
fsp_alpha: int
```

#### afp.bindings.OracleSpecification.fsp_beta

```python
fsp_beta: int
```

#### afp.bindings.OracleSpecification.fsv_calldata

```python
fsv_calldata: hexbytes.HexBytes
```

#### afp.bindings.OracleSpecification.fsv_decimals

```python
fsv_decimals: int
```

#### afp.bindings.OracleSpecification.oracle_address

```python
oracle_address: eth_typing.ChecksumAddress
```

### afp.bindings.PositionData

```python
PositionData(position_id, quantity, cost_basis, maintenance_margin, pnl)
```

Port of `struct PositionData` on the IMarginAccount contract.

**Attributes:**

- [**cost_basis**](#afp.bindings.PositionData.cost_basis) (<code>[int](#int)</code>) –
- [**maintenance_margin**](#afp.bindings.PositionData.maintenance_margin) (<code>[int](#int)</code>) –
- [**pnl**](#afp.bindings.PositionData.pnl) (<code>[int](#int)</code>) –
- [**position_id**](#afp.bindings.PositionData.position_id) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**quantity**](#afp.bindings.PositionData.quantity) (<code>[int](#int)</code>) –

#### afp.bindings.PositionData.cost_basis

```python
cost_basis: int
```

#### afp.bindings.PositionData.maintenance_margin

```python
maintenance_margin: int
```

#### afp.bindings.PositionData.pnl

```python
pnl: int
```

#### afp.bindings.PositionData.position_id

```python
position_id: hexbytes.HexBytes
```

#### afp.bindings.PositionData.quantity

```python
quantity: int
```

### afp.bindings.PositionLossData

```python
PositionLossData(position_id, bankrupt_account_u_pn_l, bankrupt_account_quantity, mark_price, point_value, tick_size, laa_data)
```

Port of `struct PositionLossData` on the IBankruptcy contract.

**Attributes:**

- [**bankrupt_account_quantity**](#afp.bindings.PositionLossData.bankrupt_account_quantity) (<code>[int](#int)</code>) –
- [**bankrupt_account_u_pn_l**](#afp.bindings.PositionLossData.bankrupt_account_u_pn_l) (<code>[int](#int)</code>) –
- [**laa_data**](#afp.bindings.PositionLossData.laa_data) (<code>[List](#typing.List)\[[LAAData](#afp.bindings.bankruptcy_facet.LAAData)\]</code>) –
- [**mark_price**](#afp.bindings.PositionLossData.mark_price) (<code>[int](#int)</code>) –
- [**point_value**](#afp.bindings.PositionLossData.point_value) (<code>[int](#int)</code>) –
- [**position_id**](#afp.bindings.PositionLossData.position_id) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**tick_size**](#afp.bindings.PositionLossData.tick_size) (<code>[int](#int)</code>) –

#### afp.bindings.PositionLossData.bankrupt_account_quantity

```python
bankrupt_account_quantity: int
```

#### afp.bindings.PositionLossData.bankrupt_account_u_pn_l

```python
bankrupt_account_u_pn_l: int
```

#### afp.bindings.PositionLossData.laa_data

```python
laa_data: typing.List[LAAData]
```

#### afp.bindings.PositionLossData.mark_price

```python
mark_price: int
```

#### afp.bindings.PositionLossData.point_value

```python
point_value: int
```

#### afp.bindings.PositionLossData.position_id

```python
position_id: hexbytes.HexBytes
```

#### afp.bindings.PositionLossData.tick_size

```python
tick_size: int
```

### afp.bindings.Product

```python
Product(metadata, oracle_spec, price_quotation, collateral_asset, start_time, earliest_fsp_submission_time, unit_value, initial_margin_requirement, maintenance_margin_requirement, offer_price_buffer, auction_bounty, tradeout_interval, tick_size, extended_metadata)
```

Port of `struct Product` on the IProductRegistry contract.

**Attributes:**

- [**auction_bounty**](#afp.bindings.Product.auction_bounty) (<code>[int](#int)</code>) –
- [**collateral_asset**](#afp.bindings.Product.collateral_asset) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- [**earliest_fsp_submission_time**](#afp.bindings.Product.earliest_fsp_submission_time) (<code>[int](#int)</code>) –
- [**extended_metadata**](#afp.bindings.Product.extended_metadata) (<code>[str](#str)</code>) –
- [**initial_margin_requirement**](#afp.bindings.Product.initial_margin_requirement) (<code>[int](#int)</code>) –
- [**maintenance_margin_requirement**](#afp.bindings.Product.maintenance_margin_requirement) (<code>[int](#int)</code>) –
- [**metadata**](#afp.bindings.Product.metadata) (<code>[ProductMetadata](#afp.bindings.product_registry.ProductMetadata)</code>) –
- [**offer_price_buffer**](#afp.bindings.Product.offer_price_buffer) (<code>[int](#int)</code>) –
- [**oracle_spec**](#afp.bindings.Product.oracle_spec) (<code>[OracleSpecification](#afp.bindings.product_registry.OracleSpecification)</code>) –
- [**price_quotation**](#afp.bindings.Product.price_quotation) (<code>[str](#str)</code>) –
- [**start_time**](#afp.bindings.Product.start_time) (<code>[int](#int)</code>) –
- [**tick_size**](#afp.bindings.Product.tick_size) (<code>[int](#int)</code>) –
- [**tradeout_interval**](#afp.bindings.Product.tradeout_interval) (<code>[int](#int)</code>) –
- [**unit_value**](#afp.bindings.Product.unit_value) (<code>[int](#int)</code>) –

#### afp.bindings.Product.auction_bounty

```python
auction_bounty: int
```

#### afp.bindings.Product.collateral_asset

```python
collateral_asset: eth_typing.ChecksumAddress
```

#### afp.bindings.Product.earliest_fsp_submission_time

```python
earliest_fsp_submission_time: int
```

#### afp.bindings.Product.extended_metadata

```python
extended_metadata: str
```

#### afp.bindings.Product.initial_margin_requirement

```python
initial_margin_requirement: int
```

#### afp.bindings.Product.maintenance_margin_requirement

```python
maintenance_margin_requirement: int
```

#### afp.bindings.Product.metadata

```python
metadata: ProductMetadata
```

#### afp.bindings.Product.offer_price_buffer

```python
offer_price_buffer: int
```

#### afp.bindings.Product.oracle_spec

```python
oracle_spec: OracleSpecification
```

#### afp.bindings.Product.price_quotation

```python
price_quotation: str
```

#### afp.bindings.Product.start_time

```python
start_time: int
```

#### afp.bindings.Product.tick_size

```python
tick_size: int
```

#### afp.bindings.Product.tradeout_interval

```python
tradeout_interval: int
```

#### afp.bindings.Product.unit_value

```python
unit_value: int
```

### afp.bindings.ProductMetadata

```python
ProductMetadata(builder, symbol, description)
```

Port of `struct ProductMetadata` on the IProductRegistry contract.

**Attributes:**

- [**builder**](#afp.bindings.ProductMetadata.builder) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- [**description**](#afp.bindings.ProductMetadata.description) (<code>[str](#str)</code>) –
- [**symbol**](#afp.bindings.ProductMetadata.symbol) (<code>[str](#str)</code>) –

#### afp.bindings.ProductMetadata.builder

```python
builder: eth_typing.ChecksumAddress
```

#### afp.bindings.ProductMetadata.description

```python
description: str
```

#### afp.bindings.ProductMetadata.symbol

```python
symbol: str
```

### afp.bindings.ProductRegistry

```python
ProductRegistry(w3)
```

Bases: <code>[ProductRegistry](#afp.bindings.product_registry.ProductRegistry)</code>

ProductRegistry contract binding.

**Parameters:**

- **w3** (<code>[Web3](#web3.Web3)</code>) –

**Functions:**

- [**auction_bounty**](#afp.bindings.ProductRegistry.auction_bounty) – Binding for `auctionBounty` on the ProductRegistry contract.
- [**clearing**](#afp.bindings.ProductRegistry.clearing) – Binding for `clearing` on the ProductRegistry contract.
- [**collateral_asset**](#afp.bindings.ProductRegistry.collateral_asset) – Binding for `collateralAsset` on the ProductRegistry contract.
- [**earliest_fsp_submission_time**](#afp.bindings.ProductRegistry.earliest_fsp_submission_time) – Binding for `earliestFSPSubmissionTime` on the ProductRegistry contract.
- [**id**](#afp.bindings.ProductRegistry.id) – Binding for `id` on the ProductRegistry contract.
- [**imr**](#afp.bindings.ProductRegistry.imr) – Binding for `imr` on the ProductRegistry contract.
- [**initialize**](#afp.bindings.ProductRegistry.initialize) – Binding for `initialize` on the ProductRegistry contract.
- [**mmr**](#afp.bindings.ProductRegistry.mmr) – Binding for `mmr` on the ProductRegistry contract.
- [**offer_price_buffer**](#afp.bindings.ProductRegistry.offer_price_buffer) – Binding for `offerPriceBuffer` on the ProductRegistry contract.
- [**oracle_specification**](#afp.bindings.ProductRegistry.oracle_specification) – Binding for `oracleSpecification` on the ProductRegistry contract.
- [**owner**](#afp.bindings.ProductRegistry.owner) – Binding for `owner` on the ProductRegistry contract.
- [**point_value**](#afp.bindings.ProductRegistry.point_value) – Binding for `pointValue` on the ProductRegistry contract.
- [**products**](#afp.bindings.ProductRegistry.products) – Binding for `products` on the ProductRegistry contract.
- [**proxiable_uuid**](#afp.bindings.ProductRegistry.proxiable_uuid) – Binding for `proxiableUUID` on the ProductRegistry contract.
- [**register**](#afp.bindings.ProductRegistry.register) – Binding for `register` on the ProductRegistry contract.
- [**renounce_ownership**](#afp.bindings.ProductRegistry.renounce_ownership) – Binding for `renounceOwnership` on the ProductRegistry contract.
- [**set_clearing**](#afp.bindings.ProductRegistry.set_clearing) – Binding for `setClearing` on the ProductRegistry contract.
- [**state**](#afp.bindings.ProductRegistry.state) – Binding for `state` on the ProductRegistry contract.
- [**tick_size**](#afp.bindings.ProductRegistry.tick_size) – Binding for `tickSize` on the ProductRegistry contract.
- [**transfer_ownership**](#afp.bindings.ProductRegistry.transfer_ownership) – Binding for `transferOwnership` on the ProductRegistry contract.
- [**upgrade_interface_version**](#afp.bindings.ProductRegistry.upgrade_interface_version) – Binding for `UPGRADE_INTERFACE_VERSION` on the ProductRegistry contract.
- [**upgrade_to_and_call**](#afp.bindings.ProductRegistry.upgrade_to_and_call) – Binding for `upgradeToAndCall` on the ProductRegistry contract.

**Attributes:**

- [**Initialized**](#afp.bindings.ProductRegistry.Initialized) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Initialized` on the ProductRegistry contract.
- [**OwnershipTransferred**](#afp.bindings.ProductRegistry.OwnershipTransferred) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event OwnershipTransferred` on the ProductRegistry contract.
- [**ProductRegistered**](#afp.bindings.ProductRegistry.ProductRegistered) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event ProductRegistered` on the ProductRegistry contract.
- [**Upgraded**](#afp.bindings.ProductRegistry.Upgraded) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Upgraded` on the ProductRegistry contract.

#### afp.bindings.ProductRegistry.Initialized

```python
Initialized: contract.ContractEvent
```

Binding for `event Initialized` on the ProductRegistry contract.

#### afp.bindings.ProductRegistry.OwnershipTransferred

```python
OwnershipTransferred: contract.ContractEvent
```

Binding for `event OwnershipTransferred` on the ProductRegistry contract.

#### afp.bindings.ProductRegistry.ProductRegistered

```python
ProductRegistered: contract.ContractEvent
```

Binding for `event ProductRegistered` on the ProductRegistry contract.

#### afp.bindings.ProductRegistry.Upgraded

```python
Upgraded: contract.ContractEvent
```

Binding for `event Upgraded` on the ProductRegistry contract.

#### afp.bindings.ProductRegistry.auction_bounty

```python
auction_bounty(product_id)
```

Binding for `auctionBounty` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ProductRegistry.clearing

```python
clearing()
```

Binding for `clearing` on the ProductRegistry contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.ProductRegistry.collateral_asset

```python
collateral_asset(product_id)
```

Binding for `collateralAsset` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.ProductRegistry.earliest_fsp_submission_time

```python
earliest_fsp_submission_time(product_id)
```

Binding for `earliestFSPSubmissionTime` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ProductRegistry.id

```python
id(product)
```

Binding for `id` on the ProductRegistry contract.

**Parameters:**

- **product** (<code>[Product](#afp.bindings.product_registry.Product)</code>) –

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.ProductRegistry.imr

```python
imr(product_id)
```

Binding for `imr` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ProductRegistry.initialize

```python
initialize()
```

Binding for `initialize` on the ProductRegistry contract.

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ProductRegistry.mmr

```python
mmr(product_id)
```

Binding for `mmr` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ProductRegistry.offer_price_buffer

```python
offer_price_buffer(product_id)
```

Binding for `offerPriceBuffer` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ProductRegistry.oracle_specification

```python
oracle_specification(product_id)
```

Binding for `oracleSpecification` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[OracleSpecification](#afp.bindings.product_registry.OracleSpecification)</code> –

#### afp.bindings.ProductRegistry.owner

```python
owner()
```

Binding for `owner` on the ProductRegistry contract.

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.ProductRegistry.point_value

```python
point_value(product_id)
```

Binding for `pointValue` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ProductRegistry.products

```python
products(product_id)
```

Binding for `products` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[Product](#afp.bindings.product_registry.Product)</code> –

#### afp.bindings.ProductRegistry.proxiable_uuid

```python
proxiable_uuid()
```

Binding for `proxiableUUID` on the ProductRegistry contract.

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.ProductRegistry.register

```python
register(product)
```

Binding for `register` on the ProductRegistry contract.

**Parameters:**

- **product** (<code>[Product](#afp.bindings.product_registry.Product)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ProductRegistry.renounce_ownership

```python
renounce_ownership()
```

Binding for `renounceOwnership` on the ProductRegistry contract.

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ProductRegistry.set_clearing

```python
set_clearing(clearing_)
```

Binding for `setClearing` on the ProductRegistry contract.

**Parameters:**

- **clearing\_** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ProductRegistry.state

```python
state(product_id)
```

Binding for `state` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[ProductState](#afp.bindings.product_registry.ProductState)</code> –

#### afp.bindings.ProductRegistry.tick_size

```python
tick_size(product_id)
```

Binding for `tickSize` on the ProductRegistry contract.

**Parameters:**

- **product_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.ProductRegistry.transfer_ownership

```python
transfer_ownership(new_owner)
```

Binding for `transferOwnership` on the ProductRegistry contract.

**Parameters:**

- **new_owner** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.ProductRegistry.upgrade_interface_version

```python
upgrade_interface_version()
```

Binding for `UPGRADE_INTERFACE_VERSION` on the ProductRegistry contract.

**Returns:**

- <code>[str](#str)</code> –

#### afp.bindings.ProductRegistry.upgrade_to_and_call

```python
upgrade_to_and_call(new_implementation, data)
```

Binding for `upgradeToAndCall` on the ProductRegistry contract.

**Parameters:**

- **new_implementation** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **data** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

### afp.bindings.ProductState

Bases: <code>[IntEnum](#enum.IntEnum)</code>

Port of `enum ProductState` on the ProductRegistry contract.

**Attributes:**

- [**EXPIRED**](#afp.bindings.ProductState.EXPIRED) –
- [**FINAL_SETTLEMENT**](#afp.bindings.ProductState.FINAL_SETTLEMENT) –
- [**LIVE**](#afp.bindings.ProductState.LIVE) –
- [**NOT_EXIST**](#afp.bindings.ProductState.NOT_EXIST) –
- [**PENDING**](#afp.bindings.ProductState.PENDING) –
- [**TRADEOUT**](#afp.bindings.ProductState.TRADEOUT) –

#### afp.bindings.ProductState.EXPIRED

```python
EXPIRED = 5
```

#### afp.bindings.ProductState.FINAL_SETTLEMENT

```python
FINAL_SETTLEMENT = 4
```

#### afp.bindings.ProductState.LIVE

```python
LIVE = 2
```

#### afp.bindings.ProductState.NOT_EXIST

```python
NOT_EXIST = 0
```

#### afp.bindings.ProductState.PENDING

```python
PENDING = 1
```

#### afp.bindings.ProductState.TRADEOUT

```python
TRADEOUT = 3
```

### afp.bindings.Settlement

```python
Settlement(position_id, quantity, price)
```

Port of `struct Settlement` on the IMarginAccount contract.

**Attributes:**

- [**position_id**](#afp.bindings.Settlement.position_id) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**price**](#afp.bindings.Settlement.price) (<code>[int](#int)</code>) –
- [**quantity**](#afp.bindings.Settlement.quantity) (<code>[int](#int)</code>) –

#### afp.bindings.Settlement.position_id

```python
position_id: hexbytes.HexBytes
```

#### afp.bindings.Settlement.price

```python
price: int
```

#### afp.bindings.Settlement.quantity

```python
quantity: int
```

### afp.bindings.Side

Bases: <code>[IntEnum](#enum.IntEnum)</code>

Port of `enum Side` on the ClearingFacet contract.

**Attributes:**

- [**ASK**](#afp.bindings.Side.ASK) –
- [**BID**](#afp.bindings.Side.BID) –

#### afp.bindings.Side.ASK

```python
ASK = 1
```

#### afp.bindings.Side.BID

```python
BID = 0
```

### afp.bindings.Trade

```python
Trade(product_id, protocol_id, trade_id, price, timestamp, accounts, quantities, fee_rates, intents)
```

Port of `struct Trade` on the IClearing contract.

**Attributes:**

- [**accounts**](#afp.bindings.Trade.accounts) (<code>[List](#typing.List)\[[ChecksumAddress](#eth_typing.ChecksumAddress)\]</code>) –
- [**fee_rates**](#afp.bindings.Trade.fee_rates) (<code>[List](#typing.List)\[[int](#int)\]</code>) –
- [**intents**](#afp.bindings.Trade.intents) (<code>[List](#typing.List)\[[Intent](#afp.bindings.clearing_facet.Intent)\]</code>) –
- [**price**](#afp.bindings.Trade.price) (<code>[int](#int)</code>) –
- [**product_id**](#afp.bindings.Trade.product_id) (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- [**protocol_id**](#afp.bindings.Trade.protocol_id) (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- [**quantities**](#afp.bindings.Trade.quantities) (<code>[List](#typing.List)\[[int](#int)\]</code>) –
- [**timestamp**](#afp.bindings.Trade.timestamp) (<code>[int](#int)</code>) –
- [**trade_id**](#afp.bindings.Trade.trade_id) (<code>[int](#int)</code>) –

#### afp.bindings.Trade.accounts

```python
accounts: typing.List[eth_typing.ChecksumAddress]
```

#### afp.bindings.Trade.fee_rates

```python
fee_rates: typing.List[int]
```

#### afp.bindings.Trade.intents

```python
intents: typing.List[Intent]
```

#### afp.bindings.Trade.price

```python
price: int
```

#### afp.bindings.Trade.product_id

```python
product_id: hexbytes.HexBytes
```

#### afp.bindings.Trade.protocol_id

```python
protocol_id: eth_typing.ChecksumAddress
```

#### afp.bindings.Trade.quantities

```python
quantities: typing.List[int]
```

#### afp.bindings.Trade.timestamp

```python
timestamp: int
```

#### afp.bindings.Trade.trade_id

```python
trade_id: int
```

### afp.bindings.TradingProtocol

```python
TradingProtocol(w3, address)
```

TradingProtocol contract binding.

**Parameters:**

- **w3** (<code>[Web3](#web3.Web3)</code>) –
- **address** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) – The address of a deployed TradingProtocol contract.

**Functions:**

- [**add_trade_submitter**](#afp.bindings.TradingProtocol.add_trade_submitter) – Binding for `addTradeSubmitter` on the TradingProtocol contract.
- [**change_owner**](#afp.bindings.TradingProtocol.change_owner) – Binding for `changeOwner` on the TradingProtocol contract.
- [**default_admin_role**](#afp.bindings.TradingProtocol.default_admin_role) – Binding for `DEFAULT_ADMIN_ROLE` on the TradingProtocol contract.
- [**deposit**](#afp.bindings.TradingProtocol.deposit) – Binding for `deposit` on the TradingProtocol contract.
- [**execute**](#afp.bindings.TradingProtocol.execute) – Binding for `execute` on the TradingProtocol contract.
- [**execute_sequence**](#afp.bindings.TradingProtocol.execute_sequence) – Binding for `executeSequence` on the TradingProtocol contract.
- [**get_role_admin**](#afp.bindings.TradingProtocol.get_role_admin) – Binding for `getRoleAdmin` on the TradingProtocol contract.
- [**get_role_member**](#afp.bindings.TradingProtocol.get_role_member) – Binding for `getRoleMember` on the TradingProtocol contract.
- [**get_role_member_count**](#afp.bindings.TradingProtocol.get_role_member_count) – Binding for `getRoleMemberCount` on the TradingProtocol contract.
- [**get_role_members**](#afp.bindings.TradingProtocol.get_role_members) – Binding for `getRoleMembers` on the TradingProtocol contract.
- [**grant_role**](#afp.bindings.TradingProtocol.grant_role) – Binding for `grantRole` on the TradingProtocol contract.
- [**has_role**](#afp.bindings.TradingProtocol.has_role) – Binding for `hasRole` on the TradingProtocol contract.
- [**initialize**](#afp.bindings.TradingProtocol.initialize) – Binding for `initialize` on the TradingProtocol contract.
- [**proxiable_uuid**](#afp.bindings.TradingProtocol.proxiable_uuid) – Binding for `proxiableUUID` on the TradingProtocol contract.
- [**remove_trade_submitter**](#afp.bindings.TradingProtocol.remove_trade_submitter) – Binding for `removeTradeSubmitter` on the TradingProtocol contract.
- [**renounce_role**](#afp.bindings.TradingProtocol.renounce_role) – Binding for `renounceRole` on the TradingProtocol contract.
- [**revoke_role**](#afp.bindings.TradingProtocol.revoke_role) – Binding for `revokeRole` on the TradingProtocol contract.
- [**supports_interface**](#afp.bindings.TradingProtocol.supports_interface) – Binding for `supportsInterface` on the TradingProtocol contract.
- [**trade_submitter_role**](#afp.bindings.TradingProtocol.trade_submitter_role) – Binding for `TRADE_SUBMITTER_ROLE` on the TradingProtocol contract.
- [**upgrade_interface_version**](#afp.bindings.TradingProtocol.upgrade_interface_version) – Binding for `UPGRADE_INTERFACE_VERSION` on the TradingProtocol contract.
- [**upgrade_to_and_call**](#afp.bindings.TradingProtocol.upgrade_to_and_call) – Binding for `upgradeToAndCall` on the TradingProtocol contract.
- [**withdraw**](#afp.bindings.TradingProtocol.withdraw) – Binding for `withdraw` on the TradingProtocol contract.

**Attributes:**

- [**Initialized**](#afp.bindings.TradingProtocol.Initialized) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Initialized` on the TradingProtocol contract.
- [**RoleAdminChanged**](#afp.bindings.TradingProtocol.RoleAdminChanged) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event RoleAdminChanged` on the TradingProtocol contract.
- [**RoleGranted**](#afp.bindings.TradingProtocol.RoleGranted) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event RoleGranted` on the TradingProtocol contract.
- [**RoleRevoked**](#afp.bindings.TradingProtocol.RoleRevoked) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event RoleRevoked` on the TradingProtocol contract.
- [**Upgraded**](#afp.bindings.TradingProtocol.Upgraded) (<code>[ContractEvent](#web3.contract.contract.ContractEvent)</code>) – Binding for `event Upgraded` on the TradingProtocol contract.

#### afp.bindings.TradingProtocol.Initialized

```python
Initialized: contract.ContractEvent
```

Binding for `event Initialized` on the TradingProtocol contract.

#### afp.bindings.TradingProtocol.RoleAdminChanged

```python
RoleAdminChanged: contract.ContractEvent
```

Binding for `event RoleAdminChanged` on the TradingProtocol contract.

#### afp.bindings.TradingProtocol.RoleGranted

```python
RoleGranted: contract.ContractEvent
```

Binding for `event RoleGranted` on the TradingProtocol contract.

#### afp.bindings.TradingProtocol.RoleRevoked

```python
RoleRevoked: contract.ContractEvent
```

Binding for `event RoleRevoked` on the TradingProtocol contract.

#### afp.bindings.TradingProtocol.Upgraded

```python
Upgraded: contract.ContractEvent
```

Binding for `event Upgraded` on the TradingProtocol contract.

#### afp.bindings.TradingProtocol.add_trade_submitter

```python
add_trade_submitter(submitter)
```

Binding for `addTradeSubmitter` on the TradingProtocol contract.

**Parameters:**

- **submitter** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.change_owner

```python
change_owner(new_owner)
```

Binding for `changeOwner` on the TradingProtocol contract.

**Parameters:**

- **new_owner** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.default_admin_role

```python
default_admin_role()
```

Binding for `DEFAULT_ADMIN_ROLE` on the TradingProtocol contract.

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.TradingProtocol.deposit

```python
deposit(margin_account_contract, amount)
```

Binding for `deposit` on the TradingProtocol contract.

**Parameters:**

- **margin_account_contract** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **amount** (<code>[int](#int)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.execute

```python
execute(trade, fallback_on_failure)
```

Binding for `execute` on the TradingProtocol contract.

**Parameters:**

- **trade** (<code>[Trade](#afp.bindings.trading_protocol.Trade)</code>) –
- **fallback_on_failure** (<code>[bool](#bool)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.execute_sequence

```python
execute_sequence(trades, fallback_on_failure)
```

Binding for `executeSequence` on the TradingProtocol contract.

**Parameters:**

- **trades** (<code>[List](#typing.List)\[[Trade](#afp.bindings.trading_protocol.Trade)\]</code>) –
- **fallback_on_failure** (<code>[bool](#bool)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.get_role_admin

```python
get_role_admin(role)
```

Binding for `getRoleAdmin` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.TradingProtocol.get_role_member

```python
get_role_member(role, index)
```

Binding for `getRoleMember` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **index** (<code>[int](#int)</code>) –

**Returns:**

- <code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code> –

#### afp.bindings.TradingProtocol.get_role_member_count

```python
get_role_member_count(role)
```

Binding for `getRoleMemberCount` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[int](#int)</code> –

#### afp.bindings.TradingProtocol.get_role_members

```python
get_role_members(role)
```

Binding for `getRoleMembers` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[List](#typing.List)\[[ChecksumAddress](#eth_typing.ChecksumAddress)\]</code> –

#### afp.bindings.TradingProtocol.grant_role

```python
grant_role(role, account)
```

Binding for `grantRole` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.has_role

```python
has_role(role, account)
```

Binding for `hasRole` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.TradingProtocol.initialize

```python
initialize(clearing_address)
```

Binding for `initialize` on the TradingProtocol contract.

**Parameters:**

- **clearing_address** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.proxiable_uuid

```python
proxiable_uuid()
```

Binding for `proxiableUUID` on the TradingProtocol contract.

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.TradingProtocol.remove_trade_submitter

```python
remove_trade_submitter(submitter)
```

Binding for `removeTradeSubmitter` on the TradingProtocol contract.

**Parameters:**

- **submitter** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.renounce_role

```python
renounce_role(role, caller_confirmation)
```

Binding for `renounceRole` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **caller_confirmation** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.revoke_role

```python
revoke_role(role, account)
```

Binding for `revokeRole` on the TradingProtocol contract.

**Parameters:**

- **role** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –
- **account** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.supports_interface

```python
supports_interface(interface_id)
```

Binding for `supportsInterface` on the TradingProtocol contract.

**Parameters:**

- **interface_id** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[bool](#bool)</code> –

#### afp.bindings.TradingProtocol.trade_submitter_role

```python
trade_submitter_role()
```

Binding for `TRADE_SUBMITTER_ROLE` on the TradingProtocol contract.

**Returns:**

- <code>[HexBytes](#hexbytes.HexBytes)</code> –

#### afp.bindings.TradingProtocol.upgrade_interface_version

```python
upgrade_interface_version()
```

Binding for `UPGRADE_INTERFACE_VERSION` on the TradingProtocol contract.

**Returns:**

- <code>[str](#str)</code> –

#### afp.bindings.TradingProtocol.upgrade_to_and_call

```python
upgrade_to_and_call(new_implementation, data)
```

Binding for `upgradeToAndCall` on the TradingProtocol contract.

**Parameters:**

- **new_implementation** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **data** (<code>[HexBytes](#hexbytes.HexBytes)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.

#### afp.bindings.TradingProtocol.withdraw

```python
withdraw(margin_account_contract, amount)
```

Binding for `withdraw` on the TradingProtocol contract.

**Parameters:**

- **margin_account_contract** (<code>[ChecksumAddress](#eth_typing.ChecksumAddress)</code>) –
- **amount** (<code>[int](#int)</code>) –

**Returns:**

- <code>[ContractFunction](#web3.contract.contract.ContractFunction)</code> – A contract function instance to be sent in a transaction.
