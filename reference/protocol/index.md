
---
title: "Protocol Parameters"

description: >
  Autonity protocol parameters - definitions, genesis configuration, update mechanism if modifiable 
---

# Overview

The protocol parameters are the configuration variables for the Autonity Network blockchain and Autonity Protocol Contracts. The parameterisation sets how the network will function by specifying economic, consensus, temporal, and governance settings.

Protocol parameter values for [public Autonity networks](/reference/genesis/#public-autonity-network-configuration) are set as network presets in the genesis configuration of the Autonity software - i.e. the Autonity Go Client, Protocol Contracts, and Autonity Oracle Server.

Protocol parameter values for a [local Autonity network](/reference/genesis/#local-autonity-network-configuration) are specified in the [`config` object](/reference/genesis/#config-object) of the local network's `genesis.json` file. The local network operator can choose to use default settings or specify their own custom settings in their `genesis.json` file as required by their use case.

A subset of the protocol parameters may be updated by the network's governance account after genesis.

## Protocol Constants

Protocol Constants are protocol parameter constant values that may be used in one or more Protocol Contracts. They are defined in `ProtocolConstants.sol`.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `SLASHING_RATE_DECIMALS` | The number of decimal points used for fixed-point arithmetic during computation of slashing penalties | `4` | None | 
| `SLASHING_RATE_SCALE_FACTOR` | The division precision used as the denominator when computing the slashing amount of a penalty | `10 ** SLASHING_RATE_DECIMALS` (`10^4 = 10_000`, i.e. 0.01%)| None |
| `CONVERSION_RATIO_DECIMALS` | The number of decimal points used for fixed-point arithmetic during computation of validator LNTN-NTN conversion ratio | `18` | None | 
| `CONVERSION_RATIO_SCALE_FACTOR` | The division precision used as the denominator when computing the LNTN-NTN conversion ratio of a validator | `10 ** CONVERSION_RATIO_DECIMALS` (`10^18 = 1_000_000_000_000_000_000`, i.e. 100%)| None |

::: {.callout-note title="Scale factor and decimals" collapse="false"}

Solidity doesn't natively support decimal fixed point arithmetic. Using the `DECIMALS` and `SCALE_FACTOR` method allows the protocol to define the % level of precision used when computing a value.

For example, `SLASHING_RATE_DECIMALS` and `SLASHING_RATE_SCALE_FACTOR` are used to allow for decimal slashing penalty values:

| Scale Factor | Slashing rate applied |
|:-------------|:----------------------|
| `10_000`     | 100% slash |
| `1_000`      | 10% slash |
| `100`        | 1% slash |
| `10`         | 0.1% slash |
| `1`          | 0.01% slash |

:::


## Protocol Contracts

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `autonity` contract address | The Autonity Protocol Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | None |
| `accountability` contract address | The Accountability Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setAccountabilityContract()`](/reference/api/aut/op-prot/#setaccountabilitycontract) |
| `oracle` contract address | The Oracle Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setOracleContract()`](/reference/api/aut/op-prot/#setoraclecontract) |
| `acu` contract address | The ASM ACU Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setAcuContract()`](/reference/api/aut/op-prot/#setacucontract) |
| `supplyControl` contract address | The ASM Supply Control Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setSupplyControlContract()`](/reference/api/aut/op-prot/#setsupplycontrolcontract) |
| `stabilisation` contract address | The ASM Stabilisation Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setStabilizationContract()`](/reference/api/aut/op-prot/#setstabilizationcontract) |
| `auctioneer` contract address | The ASM Auctioneer Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setAuctioneerContract()`](/reference/api/aut/op-prot/#setauctioneercontract) |
| `upgradeManagerContract` contract address | The Upgrade Manager Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setUpgradeManagerContract()`](/reference/api/aut/op-prot/#setupgrademanagercontract) |
| `inflationController` contract address | The Newton Inflation Controller Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setInflationControllerContract()`](/reference/api/aut/op-prot/#setinflationcontrollercontract) |
| `omissionAccountability` contract address | The Omission Accountability Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setOmissionAccountabilityContract()`](/reference/api/aut/op-prot/#setomissionaccountabilitycontract) |

## Chain Config Protocol Parameters

Protocol parameters are set in the Autonity Network's `ChainConfig`, the core configuration object for the protocol.

| Parameter object | Description | Configuration Setting |
|---------|-----------|-----|
| `chainId` | Autonity network identifier | See [Chain ID](/reference/protocol/#chain-id) |
| `autonity` | Autonity Protocol parameters | See [Autonity Config](/reference/protocol/#autonity-config) |
| `accountability` | Accountability Fault Detection protocol parameters | See [Accountability Config](/reference/protocol/#accountability-config) |
| `oracle` | Oracle protocol and Oracle Accountability Fault Detection protocol parameters | See [Oracle Config](/reference/protocol/#oracle-config) |
| `inflationController` | Newton inflation mechanism parameters | See [Inflation Controller Config](/reference/protocol/#inflation-controller-config) |
| `asm` | Auton Stabilization Mechanism parameters | See [ASM Config](/reference/protocol/#asm-config) |
| `omissionAccountability ` | Omission Fault Detection protocol parameters | See [Omission Accountability Config](/reference/protocol/#omission-accountability-config) |

### Chain ID

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `chainID` | Identifier for the Autonity blockchain network | Set in the genesis configuration using the format described in [`config.chainId`](/reference/genesis/#config-object) on the [Genesis](/reference/genesis/) Reference page | None |

::: {.callout-note title="Note" collapse="false"}

Autonity assigns the same value to Chain and Network identifiers `networkId` and `chainId`.

:::

### Autonity Config

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `minBaseFee` | The minimum gas price for computing a transaction on an Autonity network after genesis. A high minimum gas price setting incentivizes validators at genesis when transaction volumes are low | Set to `10000000000` (10 [gigaton](/glossary/#gigaton)) | See [`setEip1559Params()`](/reference/api/aut/op-prot/#seteip1559params) |
| `epochPeriod` | The period of time for which a consensus committee is elected, defined as a number of blocks. The `epochPeriod` must be shorter than the `unbondingPeriod` and must be greater than the [OFD](/concepts/ofd/) `[Delta](/concepts/ofd/#delta-delta)+[lookbackWindow](/concepts/ofd/#lookback-window)-1`. | Set to `1800` | See [`setEpochPeriod()`](/reference/api/aut/op-prot/#setepochperiod) |
| `unbondingPeriod` | The period of time bonded stake must wait before Newton can be redeemed after unbonding, defined as a number of blocks. The unbonding period can be any integer number `> 0`, but must be longer than the `epochPeriod`. | Set to `21600` | See [`setUnbondingPeriod()`](/reference/api/aut/op-prot/#setunbondingperiod) |
| `blockPeriod` | The minimum time interval between two consecutive blocks, measured in seconds. Also known as 'block time' or 'block interval'. | Set to `1` | None |
| `maxCommitteeSize` | The maximum number of validators that can be selected as members of a consensus committee | Set to `27`, the number of genesis validators. Increased post-genesis. | See [`setCommitteeSize()`](/reference/api/aut/op-prot/#setcommitteesize) |
| governance `operator` account | Address of the Autonity Protocol governance account. The governance account has the authority to mint Newton and change protocol parameters including specification of a new governance `operator` account address. A scenario for this would be migrating to a DAO form of governance. | Multisig account address | See [`setOperatorAccount()`](/reference/api/aut/op-prot/#setoperatoraccount) |
| `treasury` account | The Autonity Protocol’s treasury account for receiving treasury fees used for Autonity community funds. | Multisig account address | See [`setTreasuryAccount()`](/reference/api/aut/op-prot/#settreasuryaccount) |
| `withheldRewardsPool` account | The address of the Autonity Withheld Rewards account, the pool to which withheld Newton inflation rewards are sent for holding | Multisig account address. Set by default to the Autonity `treasury` account at genesis unless specified | See [`setWithheldRewardsPool()`](/reference/api/aut/op-prot/#setwithheldrewardspool) |
| `treasuryFee` | The percentage fee of staking rewards that is deducted by the protocol for Autonity community funds. The fee is sent to the Autonity Treasury account at epoch end on reward distribution. Specified as an integer value representing up to 18 decimal places of precision. | Set to `50000000000000000` (5%)  | See [`setTreasuryFee()`](/reference/api/aut/op-prot/#settreasuryfee) |
| `delegationRate` | The percentage fee of staking rewards that is deducted by validators as a commission from delegated stake. The fee is sent to the validator's [`treasury`](/concepts/validator/#treasury-account) account at epoch end on reward distribution. The rate can be specified to the precision of 1 basis point. Specified as an integer value representing up to 3 decimal places of precision. | Set to `1000` (10%) | See [`config.autonity.delegationRate`](/reference/genesis/#configautonity-object)  | None (Individual validators can reset their rate after registration. See [`changeCommissionRate()`](/reference/api/aut/#changecommissionrate)) |
| `withholdingThreshold` | The inactivity threshold at which committee member staking and Newton inflation rewards are withheld and sent to the Withheld Rewards Pool account by the Omission Fault Detection protocol | Set to `0` (0%, no tolerance) | See [`setWithholdingThreshold()`](/reference/api/aut/op-prot/#setwithholdingthreshold) |
| `proposerRewardRate` | The percentage of epoch staking rewards allocated for proposer rewarding by the Omission Fault Detection protocol  | Set to `500` (5%) | See [`setProposerRewardRate()`](/reference/api/aut/op-prot/#setproposerrewardrate) |
| `oracleRewardRate` | The percentage of epoch staking rewards deducted for oracles as a reward for correct price reporting by the Oracle Accountability Fault Detection protocol | Set to `500` (5%) | See [`setOracleRewardRate()`](/reference/api/aut/op-prot/#setoraclerewardrate) |
| `initialInflationReserve` | the amount of Newton held in reserve for Newton inflation rewards | Set to `40 Million` (40% of the total supply of 100 Million Newton) | None |
| `gasLimit` | The maximum amount of gas expenditure allowed for a block, placing a ceiling on transaction computations possible within a block. The value is specified as the number of gas units allowed in a block. The gas limit determines the amount of gas allowed to compute the genesis block; for subsequent blocks the gas limit is algorithmically adjusted by protocol and is a desired gas limit. The runtime block gas limit is a normal distribution around this target. | Value is set to: `30000000` (30M) |  See [`setGasLimit()`](/reference/api/aut/op-prot/#setgaslimit) |
| `gasLimitBoundDivisor` | The divisor that determines the change in the gas limit compared to the parent block's gas limit. | Set to `1024 ` | See [`setEip1559Params()`](/reference/api/aut/op-prot/#seteip1559params) |
| `baseFeeChangeDenominator` | Bounds the amount the base fee can change between blocks. | Set to `64` | See [`setEip1559Params()`](/reference/api/aut/op-prot/#seteip1559params) |
| `elasticityMultiplier` | Multiplier to compute the block gas target. Results in block gas target as a percentage of the parent block gas limit. | Set to `2` (targets 50% of the block gas limit) | See [`setEip1559Params()`](/reference/api/aut/op-prot/#seteip1559params) |
| `clusteringThreshold` | Sets the clustering threshold for consensus message routing. When committee size exceeds this threshold, network participants are grouped into deterministic clusters to optimize network propagation of gossiped consensus messages. | Set to `64` | See [`setClusteringThreshold()`](/reference/api/aut/op-prot/#setclusteringthreshold) |
| `skipGenesisVerification` | A boolean flag to skip or not verification checks that the amount of NTN minted and bonded at genesis matches the `tokenBond` and `tokenMint` parameter values. | Set to `false` | None |
| `tokenBond` | The amount of NTN stake token bonded to validators at network genesis. | Specific to network  genesis | None |
| `tokenMint` | The amount of NTN stake token minted at network genesis. | Set to `60 Million` (60% of the total supply of 100 Million Newton)  | None |
| `schedules` | Protocol schedules determine the amount of NTN to deduct from the total minted NTN amount to set the circulating supply (inflation base) to which the inflation rate is applied. | Specific to network genesis | None |
| `maxScheduleDuration` | The maximum allowed duration of a schedule. See `schedules`. | Set to 	`126230400` seconds (4+(1/365) years) | See [`setMaxScheduleDuration()`](/reference/api/aut/op-prot/#setmaxscheduleduration) |
| `validators` | Specify the genesis validator set. | Specific to network genesis | Post-genesis the genesis validators can `pause` and `reactivate` to enter and leave committee selection. New validators can register after genesis. |

::: {.callout-note title="NTN supply, protocol schedules and Newton inflation" collapse="false"}

The _total supply_ of NTN is capped at 100M NTN, 60M of which is minted at genesis (`tokenMint`) and 40M of which is in the Newton inflation reserve (`initialInflationReserve`. NTN in the inflation reserve is then minted by the Newton [inflation mechanism](/glossary/#inflation-mechanism) and emitted into circulation over time as [inflation rewards](/glossary/#inflation-rewards) awarded to [participating](/glossary/#participation-rate) NTN. Participating NTN is the amount of NTN in the _circulating supply_ that has been [delegated](/glossary/#delegated) ([bonded](/glossary/#bond)) to validators and so is securing the network (at genesis this is `tokenBond`). NTN inflation rewards are emitted epoch end and [autobonded](/glossary/#autobond) to the validator staked to. Autobonding simultaneously increases the NTN [participating stake](/glossary/#participation-rate) amount of a delegator and increases network security.

The _circulating supply_ of NTN at genesis is the amount of NTN minted at genesis (`tokenMint`) minus the amount of NTN in the protocol schedules (`schedules`). 

The protocol `schedules` record the amount of minted NTN that is out of circulation at genesis. Specifically, the protocol schedules record the amount of NTN locked in locking contract(s) that will unlock and release NTN in to the _circulating supply_ over time according to an unlocking schedule. An unlocking schedule can be no greater than the `maxScheduleDuration`.

The amount of NTN in the circulating supply at genesis (i.e. `tokenMint` amount minus protocol `schedules` amount) is the _inflation base_ to which the _inflation rate_ is applied by the Newton _inflation mechanism_. The protocol schedules are properties of the inflation mechanism, therefore. 

For detail on NTN supply, protocol schedules and Newton inflation see:

- Concepts, Protocol assets, Newton, [Total supply and Newton inflation](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation).
- Concepts, Architecture, [Newton Inflation Controller Contract](/concepts/architecture/#newton-inflation-controller-contract).
- Reference, Protocol Parameters, [Inflation Controller Config](/reference/protocol/#inflation-controller-config).
- Glossary: [circulating supply](/glossary/#circulating-supply), [total supply](/glossary/#total-supply), [inflation mechanism](/glossary/#inflation-mechanism), [inflation rewards](/glossary/#inflation-rewards), [participation rate](/glossary/#participation-rate), [autobond](/glossary/#autobond), [delegation](/glossary/#delegation).

To return current state data see the Autonity Contract Interfaces and:

- Autonity Contract Interface (for NTN supply and inflation reserve amounts):  [`circulatingSupply()`](/reference/api/aut/#circulatingsupply), [`getInflationReserve()`](/reference/api/aut/#get-inflation-reserve), [`totalSupply()`](/reference/api/aut/#totalsupply).
- Inflation Controller Contract Interface (for Newton inflation mechanism configuration): [`getParams`](/reference/api/inflation/#getparams).

:::

### Accountability Config

Parameters for the Accountability Contract and the Accountability Fault Detection (AFD) protocol.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `innocenceProofSubmissionWindow` | The number of blocks forming a window within which an accused offending validator has to submit a proof of innocence on-chain refuting an accusation | Set by default to `120` (120 blocks) | See [`setInnocenceProofSubmissionWindow()`](/reference/api/aut/op-prot/#setinnocenceproofsubmissionwindow-accountability-contract) |
| `delta` | The delta for the provable fault detector. It is the number of blocks that must elapse before running the fault detector on a certain height (e.g height $x$ gets scanned at block $x+delta$) | Set by default to `10` (10 blocks) | See [`setDelta()`](/reference/api/aut/op-prot/#setdelta-accountability-contract) |
| `range` | The height range for the provable fault detector. It is used for garbage collection of messages and to establish height boundaries for accusation validity | Set by default to `128` (128 blocks) | See [`setRange()`](/reference/api/aut/op-prot/#setrange-accountability-contract) |
| `gracePeriod` | The grace period for a validator to defend against an accusation; prevents the possibility of the protocol raising an indefensible accusation in the case of a `range` increase. | Set by default to `0` (blocks) | None; automatically adjusted by protocol |
| `baseSlashingRateLow` | The base slashing rate for a fault of _Low_ severity | Set by default to `50` (0.5%) | See [`setBaseSlashingRates()`](/reference/api/aut/op-prot/#setbaseslashingrates-accountability-contract) |
| `baseSlashingRateMid` | The base slashing rate for a fault of _Mid_ severity | Set by default to `100` (1%) | See [`setBaseSlashingRates()`](/reference/api/aut/op-prot/#setbaseslashingrates-accountability-contract) |
| `baseSlashingRateHigh` | The base slashing rate for a fault of _High_ severity | Set by default to `200` (2%) | See [`setBaseSlashingRates()`](/reference/api/aut/op-prot/#setbaseslashingrates-accountability-contract) |
| `collusionFactor` | The percentage factor applied to the total number of slashable offences committed during an epoch when computing the slashing amount of a penalty | Set by default to `24` (0.25%) | See [`setFactors()`](/reference/api/aut/op-prot/#setfactors-accountability-contract) |
| `historyFactor` | The percentage factor applied to the total number of proven faults committed by a validator used as a factor when computing the slashing amount of a penalty | Set by default to `150` (1.5%) | See [`setFactors()`](/reference/api/aut/op-prot/#setfactors-accountability-contract) |
| `jailFactor` | The number of epochs used as a factor when computing the jail period of an offending validator | Set by default to `48` (48 epochs, i.e. 1 day at a 30 mins epoch) | See [`setFactors()`](/reference/api/aut/op-prot/#setfactors-accountability-contract) |
| `SLASHING_RATE_SCALE_FACTOR` | Set as a [Protocol Constant](/reference/protocol/#protocol-constants) | See `SLASHING_RATE_SCALE_FACTOR` in [Protocol Constants](/reference/protocol/#protocol-constants) | None |


### Oracle Config

Parameters for the Oracle Contract of the Oracle protocol and Oracle Accountability Fault Detection (OAFD) protocol.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| Oracle `symbols` | The currency pairs that the oracle component collects data points for. The first listed currency of the pair is the base currency and the second the quote currency | Comma separated list of currency pairs. Set by default to `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD"]` | See [`setSymbols()`](/reference/api/aut/op-prot/#setsymbols-oracle-contract) |
| Oracle `votePeriod` | The interval at which the oracle network initiates a new oracle round for submitting and voting on oracle data, measured in blocks | Set by default to `600` (600 blocks) | None |
| `outlierDetectionThreshold` | Defines the threshold for flagging outliers | Set by default to `3` (3%) | None |
| `outlierSlashingThreshold` | Defines the threshold for outlier slashing penalties, controlling the sensitivity of the penalty model | Set by default to `225` (15%) | None |
| `baseSlashingRate` | Defines the base slashing rate for outlier slashing penalties | Set by default to `10` (0.1%) | None |
| `nonRevealThreshold` | Defines the threshold for missed reveals | Set by default to `5` (oracle voting rounds) | None |
| `revealResetInterval` | The number of oracle voting rounds after which the missed reveal counter is reset | Set by default to `10` | None |
| `slashingRateCap` | The maximum % slashing rate for oracle accountability slashing penalties | Set by default to `50` (0.5%) | None |
| `OracleRewardRate` | Set in the Autonity Protocol Contract configuration | See [`config.autonity.oracleRewardRate`](/reference/protocol/#autonity-config) | See [`setOracleRewardRate()`](/reference/api/aut/op-prot/#setoraclerewardrate) |

### Inflation Controller Config

Parameters for the Inflation Controller Contract of the Newton inflation mechanism. 

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `inflationRateInitial` | Initial inflation rate | Set by default to `7.5%` AR | None |
| `inflationRateTransition` | Transition inflation rate | Set by default to `5.5%` AR | None |
| `inflationReserveDecayRate` | Constant inflation rate | Set by default to `17.3168186793%` AR | None |
| `inflationTransitionPeriod` | Transition period | Set by default to `4.002739726027397` (4+1/365 years) | None |
| `inflationCurveConvexity` | Convexity parameter | Set by default to `2.7648007374` | None |
| `InitialInflationReserve` | Set in the Autonity Protocol Contract configuration | See [`config.autonity.InitialInflationReserve`](/reference/protocol/#autonity-contract-config) | None |


### ASM Config

Configuration of the Auton Stabilization Mechanism (ASM) ACU, Stabilization, Auctioneer, and Supply Control Contracts.

#### ACU Config

The ASM's Autonomous Currency Unit (ACU) currency basket configuration, an optimal currency basket of 7 free-floating fiat currencies.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------| 
| `symbols` | The [currency pair](/glossary/#currency-pair) symbols used to retrieve prices for the currencies in the basket | Set by default to `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "USD-USD"]` | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |
| `quantities` | The basket quantity corresponding to each symbol. | Set by default to `[1_826_272, 1_634_362, 1_023_622, 886_976, 177_065_877, 11_513_754, 1_192_007]` | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |
| `scale` | The scale used to represent the basket `quantities` and ACU value. | Set by default to `7` | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |

#### Stabilization Config

The ASM's Stabilization mechanism CDP configuration.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `borrowInterestRate` | The annual continuously-compounded interest rate for borrowing. | `0%` while [CDP Opening Restrictions](/concepts/asm/#asm-restrictions) are in force. Set by default to 5%, `50_000_000_000_000_000`, which applies on lifting of the CDP Opening Restrictions | See [`updateBorrowInterestRate()`](/reference/api/aut/op-prot/#updateborrowinterestrate-asm-stabilization-contract) |
| `announcementWindow` | The length of time in seconds before an update to ASM Stabilization config will take effect. | Set by default to 1 hour, `3600` seconds | See [`updateAnnouncementWindow()`](/reference/api/aut/op-prot/#updateannouncementwindow-asm-stabilization-contract) |
| `liquidationRatio` | The minimum ACU value of collateral required to maintain 1 ACU value of debt. | Set by default to 1.8, `1_800_000_000_000_000_000` | See [`updateRatios()`](/reference/api/aut/op-prot/#updateratios-asm-stabilization-contract) |
| `minCollateralizationRatio` | The minimum ACU value of collateral required to borrow 1 ACU value of debt. | Set by default to 2, `2_000_000_000_000_000_000` | See [`updateRatios()`](/reference/api/aut/op-prot/#updateratios-asm-stabilization-contract) |
| `minDebtRequirement` | The minimum amount of debt required to maintain a CDP. | Set by default to 1 [`megaton`](/concepts/protocol-assets/auton/#unit-measures-of-auton), `1_000_000` (i.e. `10^-12` ATN) | See  [`setMinDebtRequirement()`](/reference/api/aut/op-prot/#setmindebtrequirement-asm-stabilization-contract) |
| `targetPrice` | The ACU value of 1 unit of debt. | Set by default to the Golden Ratio rounded to 5 dp `1.61804`, `1_618_034_000_000_000_000` | None |
| `defaultNTNATNPrice` | Default NTN-ATN price for use at genesis (with Oracle decimals precision) | Set by default to `0.6666193` | See [`setDefaultNTNATNPrice()`](/reference/api/aut/op-prot/#setdefaultntnatnprice-asm-stabilization-contract) |
| `defaultNTNUSDPrice` | Default NTN-USD price for use at genesis (with Oracle decimals precision) | Set by default to `0.9` | See [`setDefaultNTNUSDPrice()`](/reference/api/aut/op-prot/#setdefaultntnusdprice-asm-stabilization-contract) |
| `defaultACUUSDPrice` | Optional ACU-USD price for use at genesis | Set by default to `0.8344052` | See [`setDefaultACUUSDPrice()`](/reference/api/aut/op-prot/#setdefaultacuusdprice-asm-stabilization-contract) |

::: {.callout-tip title="ASM restrictions" collapse="false"}

See the [ASM](/concepts/asm/) concept and [ASM restrictions](/concepts/asm/#asm-restrictions) for detail on CDP Opening Restrictions and the setting of default prices by Fixed Price Restrictions during network bootstrapping.

:::


#### Supply Control Config

Parameters for the ASM's Auton supply control configuration.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `initialAllocation` | The initial allocation of Auton to the ASM |   $2^{256} - 1 - GenesisATN$ (integer datatype minus the amount of ATN created by [allocation at genesis](/reference/genesis/#alloc-object) ($GenesisATN$)) | None |

#### Auctioneer Config

The ASM's CDP debt and interest Auction mechanism configuration.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------| 
| `liquidationAuctionDuration` | The number of blocks for a liquidation auction to move from the liquidation rate to the bankruptcy rate	| Set by default to `60` (60 blocks)| See [`setLiquidationAuctionDuration()`](/reference/api/aut/op-prot/#setliquidationauctionduration-asm-auctioneer-contract) |
| `interestAuctionDuration` | The number of blocks for an interest auction to move from the discount rate to the floor price | Set by default to `60` (60 blocks) | See [`setInterestAuctionDuration()`](/reference/api/aut/op-prot/#setinterestauctionduration-asm-auctioneer-contract) |
| `interestAuctionDiscount` | The fraction above market price that an interest auction starts at | Set by default to `0.1` (10%) | See [`setInterestAuctionDiscount()`](/reference/api/aut/op-prot/#setinterestauctiondiscount-asm-auctioneer-contract) |
| `interestAuctionThreshold` | The minimum amount of ATN paid in interest to trigger an interest auction | Set by default to `1` ATN | See [`setInterestAuctionThreshold()`](/reference/api/aut/op-prot/#setinterestauctionthreshold-asm-auctioneer-contract) |
| `proceedAddress` | The address to which interest auction proceeds are sent. (Proceeds accumulate in the Auctioneer Contract until a proceed address is set by governance.) | Set by default to the Auctioneer Contract address | See [`setProceedAddress()`](/reference/api/aut/op-prot/#setproceedaddress-asm-auctioneer-contract) |

### Omission Accountability Config

Parameters for the Omission Accountability Contract and the Omission Fault Detection (OFD) protocol.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `inactivityThreshold` | Defines the threshold for flagging validator inactivity | Set by default to `1500` (15%) | See [`setInactivityThreshold()`](/reference/api/aut/op-prot/#setinactivitythreshold-omission-accountability-contract) |
| `lookbackWindow` | The number of blocks over which the protocol will look for inactivity | Set by default to `60` (60 blocks) | See [`setLookbackWindow()`](/reference/api/aut/op-prot/#setlookbackwindow-omission-accountability-contract) |
| `pastPerformanceWeight` | Determines how much weight is given to past performance of the validator in the preceding epoch in the current epoch when computing the aggregated inactivity score | Set by default to `1000` (10%) | See [`setPastPerformanceWeight()`](/reference/api/aut/op-prot/#setpastperformanceweight-omission-accountability-contract) |
| `initialJailingPeriod` | The initial number of block(s) that a validator will be jailed for | Set by default to `10_000` (10000 blocks) | See [`setInitialJailingPeriod()`](/reference/api/aut/op-prot/#setinitialjailingperiod-omission-accountability-contract) |
| `initialProbationPeriod` | The initial number of epoch(s) that a validator will be set under probation for | Set by default to  `8` (8 epochs) | See [`setInitialProbationPeriod()`](/reference/api/aut/op-prot/#setinitialprobationperiod-omission-accountability-contract) |
| `initialSlashingRate` | The initial slashing rate used with the offence count and collusion degree when computing the slashing amount of a penalty | Set by default to `5` (0.05%) | See [`setInitialSlashingRate()`](/reference/api/aut/op-prot/#setinitialslashingrate-omission-accountability-contract) |
| `delta` | The number of blocks to wait before generating an activity proof | Set by default to `5` (5 blocks) | See [`setDelta()`](/reference/api/aut/op-prot/#setdelta-omission-accountability-contract) |
| `SCALE_FACTOR` | Used for fixed-point arithmetic during computation of inactivity score |  See `SCALE_FACTOR` in `OmissionAccountability.sol` | None |
| `SLASHING_RATE_SCALE_FACTOR` | Set as a [Protocol Constant](/reference/protocol/#protocol-constants) | See `SLASHING_RATE_SCALE_FACTOR` in [Protocol Constants](/reference/protocol/#protocol-constants) | None |
