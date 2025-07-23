
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
| `minBaseFee` | The minimum gas price for computing a transaction on an Autonity network after genesis. A high minimum gas price setting incentivizes validators at genesis when transaction volumes are low | Set to `500000000` | See [`setMinimumBaseFee()`](/reference/api/aut/op-prot/#setminimumbasefee) |
| `epochPeriod` | The period of time for which a consensus committee is elected, defined as a number of blocks. The `epochPeriod` must be shorter than the `unbondingPeriod` | Set to `1800` | See [`setEpochPeriod()`](/reference/api/aut/op-prot/#setepochperiod) |
| `unbondingPeriod` | The period of time bonded stake must wait before Newton can be redeemed after unbonding, defined as a number of blocks. The unbonding period can be any integer number `> 0`, but must be longer than the `epochPeriod`. | See [`config.autonity.unbondingPeriod`](/reference/genesis/#configautonity-object)  | See [`setUnbondingPeriod()`](/reference/api/aut/op-prot/#setunbondingperiod) |
| `blockPeriod` | The minimum time interval between two consecutive blocks, measured in seconds. Also known as 'block time' or 'block interval'. | Set to `1` | None |
| `maxCommitteeSize` | The maximum number of validators that can be selected as members of a consensus committee | Set to `30`, the number of genesis validators. Increased post-genesis to `100` | See [`setCommitteeSize()`](/reference/api/aut/op-prot/#setcommitteesize) |
| `maxScheduleDuration` | The maximum allowed duration of a schedule | Set to `94608000` (1095 days) | See [`setMaxScheduleDuration()`](/reference/api/aut/op-prot/#setmaxscheduleduration) |
| governance `operator` account | Address of the Autonity Protocol governance account. The governance account has the authority to mint Newton and change protocol parameters including specification of a new governance `operator` account address. A scenario for this would be migrating to a DAO form of governance. | EOA account address | See [`setOperatorAccount()`](/reference/api/aut/op-prot/#setoperatoraccount) |
| `treasury` account | The Autonity Protocol’s treasury account for receiving treasury fees used for Autonity community funds. | EOA account address | See [`setTreasuryAccount()`](/reference/api/aut/op-prot/#settreasuryaccount) |
| `withheldRewardsPool` account | The address of the Autonity Withheld Rewards account, the pool to which withheld Newton inflation rewards are sent for holding | EOA account address. Set by default to the Autonity `treasury` account at genesis unless specified | See [`setWithheldRewardsPool()`](/reference/api/aut/op-prot/#setwithheldrewardspool) |
| `treasuryFee` | The percentage fee of staking rewards that is deducted by the protocol for Autonity community funds. The fee is sent to the Autonity Treasury account at epoch end on reward distribution. Specified as an integer value representing up to 18 decimal places of precision. | Set to `10000000000000000` (1%)  | See [`setTreasuryFee()`](/reference/api/aut/op-prot/#settreasuryfee) |
| `delegationRate` | The percentage fee of staking rewards that is deducted by validators as a commission from delegated stake. The fee is sent to the validator's [`treasury`](/concepts/validator/#treasury-account) account at epoch end on reward distribution. The rate can be specified to the precision of 1 basis point. Specified as an integer value representing up to 3 decimal places of precision. | Set to `1000` (10%) | See [`config.autonity.delegationRate`](/reference/genesis/#configautonity-object)  | None (Individual validators can reset their rate after registration. See [`changeCommissionRate()`](/reference/api/aut/#changecommissionrate)) |
| `withholdingThreshold` | The inactivity threshold at which committee member staking and Newton inflation rewards are withheld and sent to the Withheld Rewards Pool account by the Omission Fault Detection protocol | Set to `0` (0%, no tolerance) | See [`setWithholdingThreshold()`](/reference/api/aut/op-prot/#setwithholdingthreshold) |
| `proposerRewardRate` | The percentage of epoch staking rewards allocated for proposer rewarding by the Omission Fault Detection protocol  | Set to `1000` (10%) | See [`setProposerRewardRate()`](/reference/api/aut/op-prot/#setproposerrewardrate) |
| `oracleRewardRate` | The percentage of epoch staking rewards deducted for oracles as a reward for correct price reporting by the Oracle Accountability Fault Detection protocol | Set to `1000` (10%) | See [`setOracleRewardRate()`](/reference/api/aut/op-prot/#setoraclerewardrate) |
| `initialInflationReserve` | the amount of Newton held in reserve for Newton inflation rewards | Set to `40 Million` (40% of the total supply of 100 Million Newton) | None |


### Accountability Config

Parameters for the Accountability Contract and the Accountability Fault Detection (AFD) protocol.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `innocenceProofSubmissionWindow` | The number of blocks forming a window within which an accused offending validator has to submit a proof of innocence on-chain refuting an accusation | Set by default to `100` (100 blocks) | See [`setInnocenceProofSubmissionWindow()`](/reference/api/aut/op-prot/#setinnocenceproofsubmissionwindow-accountability-contract) |
| `baseSlashingRateLow` | The base slashing rate for a fault of _Low_ severity | Set by default to `400` (4%) | See [`setBaseSlashingRates()`](/reference/api/aut/op-prot/#setbaseslashingrates-accountability-contract) |
| `baseSlashingRateMid` | The base slashing rate for a fault of _Mid_ severity | Set by default to `600` (6%) | See [`setBaseSlashingRates()`](/reference/api/aut/op-prot/#setbaseslashingrates-accountability-contract) |
| `baseSlashingRateHigh` | The base slashing rate for a fault of _High_ severity | Set by default to `800` (8%) | See [`setBaseSlashingRates()`](/reference/api/aut/op-prot/#setbaseslashingrates-accountability-contract) |
| `collusionFactor` | The percentage factor applied to the total number of slashable offences committed during an epoch when computing the slashing amount of a penalty | Set by default to `200` (2%) | See [`setFactors()`](/reference/api/aut/op-prot/#setfactors-accountability-contract) |
| `historyFactor` | The percentage factor applied to the total number of proven faults committed by a validator used as a factor when computing the slashing amount of a penalty | Set by default to `500` (5%) | See [`setFactors()`](/reference/api/aut/op-prot/#setfactors-accountability-contract) |
| `jailFactor` | The number of epochs used as a factor when computing the jail period of an offending validator | Set by default to `48` (48 epochs, i.e. 1 day at a 30 mins epoch) | See [`setFactors()`](/reference/api/aut/op-prot/#setfactors-accountability-contract) |
| `SLASHING_RATE_SCALE_FACTOR` | Set as a [Protocol Constant](/reference/protocol/#protocol-constants) | See `SLASHING_RATE_SCALE_FACTOR` in [Protocol Constants](/reference/protocol/#protocol-constants) | None |


### Oracle Config

Parameters for the Oracle Contract of the Oracle protocol and Oracle Accountability Fault Detection (OAFD) protocol.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| Oracle `symbols` | The currency pairs that the oracle component collects data points for. The first listed currency of the pair is the base currency and the second the quote currency | Comma separated list of currency pairs. Set by default to `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "NTN-ATN"]` | See [`setSymbols()`](/reference/api/aut/op-prot/#setsymbols-oracle-contract) |
| Oracle `votePeriod` | The interval at which the oracle network initiates a new oracle round for submitting and voting on oracle data, measured in blocks | Set by default to `30` (30 blocks) | None |
| `outlierDetectionThreshold` | Defines the threshold for flagging outliers | Set by default to `10` (10%) | None |
| `outlierSlashingThreshold` | Defines the threshold for outlier slashing penalties, controlling the sensitivity of the penalty model | Set by default to `225` (15%) | None |
| `baseSlashingRate` | Defines the base slashing rate for outlier slashing penalties | Set by default to `10` (0.1%) | None |
| `nonRevealThreshold` | Defines the threshold for missed reveals | Set by default to `3` (oracle voting rounds) | None |
| `revealResetInterval` | The number of oracle voting rounds after which the missed reveal counter is reset | Set by default to `10` | None |
| `slashingRateCap` | The maximum % slashing rate for oracle accountability slashing penalties | Set by default to `1_000` (10%) | None |
| `OracleRewardRate` | Set in the Autonity Protocol Contract configuration | See [`config.autonity.oracleRewardRate`](/reference/protocol/#autonity-config) | See [`setOracleRewardRate()`](/reference/api/aut/op-prot/#setoraclerewardrate) |

### Inflation Controller Config

Parameters for the Inflation Controller Contract of the Newton inflation mechanism. 

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `inflationRateInitial` | Initial inflation rate | Set by default to `7.5%` AR | None |
| `inflationRateTransition` | Transition inflation rate | Set by default to `5.5%` AR | None |
| `inflationReserveDecayRate` | Constant inflation rate | Set by default to `17.3168186793%` AR | None |
| `inflationTransitionPeriod` | Transition period | Set by default to `(4+1/365)` years | None |
| `inflationCurveConvexity` | Convexity parameter | Set by default to `-1.7794797758` | None |
| `InitialInflationReserve` | Set in the Autonity Protocol Contract configuration | See [`config.autonity.InitialInflationReserve`](/reference/protocol/#autonity-contract-config) | None |



### ASM Config

Configuration of the Auton Stabilization Mechanism (ASM) ACU, Stabilization, Auctioneer, and Supply Control Contracts.

#### ACU Config

The ASM's Autonomous Currency Unit (ACU) currency basket configuration, an optimal currency basket of 7 free-floating fiat currencies.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------| 
| `symbols` | The [currency pair](/glossary/#currency-pair) symbols used to retrieve prices for the currencies in the basket | Set by default to `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "USD-USD"]` | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |
| `quantities` | The basket quantity corresponding to each symbol. | Set by default to `[1_744_583, 1_598_986, 1_058_522, 886_091, 175_605_573, 12_318_802, 1_148_285]` | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |
| `scale` | The scale used to represent the basket `quantities` and ACU value. | Set by default to `7` | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |

#### Stabilization Config

The ASM's Stabilization mechanism CDP configuration.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `borrowInterestRate` | The annual continuously-compounded interest rate for borrowing. | Set by default to 5%, `50_000_000_000_000_000` | See [`updateBorrowInterestRate()`](/reference/api/aut/op-prot/#updateborrowinterestrate-asm-stabilization-contract) |
| `announcementWindow` | The length of time in seconds before an update to ASM Stabilization config will take effect. | Set by default to 1 hour, `3600` | See [`updateAnnouncementWindow()`](/reference/api/aut/op-prot/#updateannouncementwindow-asm-stabilization-contract) |
| `liquidationRatio` | The minimum ACU value of collateral required to maintain 1 ACU value of debt. | Set by default to 1.8, `1_800_000_000_000_000_000` | See [`updateRatios()`](/reference/api/aut/op-prot/#updateratios-asm-stabilization-contract) |
| `minCollateralizationRatio` | The minimum ACU value of collateral required to borrow 1 ACU value of debt. | Set by default to 2, `2_000_000_000_000_000_000` | See [`updateRatios()`](/reference/api/aut/op-prot/#updateratios-asm-stabilization-contract) |
| `minDebtRequirement` | The minimum amount of debt required to maintain a CDP. | Set by default to a [`megaton`](/concepts/protocol-assets/auton/#unit-measures-of-auton), `1_000_000` | See  [`setMinDebtRequirement()`](/reference/api/aut/op-prot/#setmindebtrequirement-asm-stabilization-contract) |
| `targetPrice` | The ACU value of 1 unit of debt. | Set by default to the Golden Ratio rounded to 5 dp `1.61804`, `1_618_034_000_000_000_000` | None |
| `defaultNTNATNPrice` | Default NTN-ATN price for use at genesis (with Oracle decimals precision) | Set by default to 1.0, `1_000_000_000_000_000_000` | See [`setDefaultNTNATNPrice()`](/reference/api/aut/op-prot/#setdefaultntnatnprice-asm-stabilization-contract) |
| `defaultNTNUSDPrice` | Default NTN-USD price for use at genesis (with Oracle decimals precision) | Set by default to 1.6, `1_600_000_000_000_000_000` | See [`setDefaultNTNUSDPrice()`](/reference/api/aut/op-prot/#setdefaultntnusdprice-asm-stabilization-contract) |
| `defaultACUUSDPrice` | Optional ACU-USD price for use at genesis | Set by default to NULL, `0` | See [`setDefaultACUUSDPrice()`](/reference/api/aut/op-prot/#setdefaultacuusdprice-asm-stabilization-contract) |

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
| `inactivityThreshold` | Defines the threshold for flagging validator inactivity | Set by default to`1000` (10%) | See [`setInactivityThreshold()`](/reference/api/aut/op-prot/#setinactivitythreshold-omission-accountability-contract) |
| `lookbackWindow` | The number of blocks over which the protocol will look for inactivity | Set by default to `40` (40 blocks) | See [`setLookbackWindow()`](/reference/api/aut/op-prot/#setlookbackwindow-omission-accountability-contract) |
| `pastPerformanceWeight` | Determines how much weight is given to past performance of the validator in the preceding epoch in the current epoch when computing the aggregated inactivity score | Set by default to `1000` (10%) | See [`setPastPerformanceWeight()`](/reference/api/aut/op-prot/#setpastperformanceweight-omission-accountability-contract) |
| `initialJailingPeriod` | The initial number of block(s) that a validator will be jailed for | Set by default to `10_000` (10000 blocks) | See [`setInitialJailingPeriod()`](/reference/api/aut/op-prot/#setinitialjailingperiod-omission-accountability-contract) |
| `initialProbationPeriod` | The initial number of epoch(s) that a validator will be set under probation for | Set by default to  `24` (24 epochs) | See [`setInitialProbationPeriod()`](/reference/api/aut/op-prot/#setinitialprobationperiod-omission-accountability-contract) |
| `initialSlashingRate` | The initial slashing rate used with the offence count and collusion degree when computing the slashing amount of a penalty | Set by default to `25` (0.25%) | See [`setInitialSlashingRate()`](/reference/api/aut/op-prot/#setinitialslashingrate-omission-accountability-contract) |
| `delta` | The number of blocks to wait before generating an activity proof | Set by default to `5` (5 blocks) | See [`setDelta()`](/reference/api/aut/op-prot/#setdelta-omission-accountability-contract) |
| `SCALE_FACTOR` | Used for fixed-point arithmetic during computation of inactivity score |  See `SCALE_FACTOR` in `OmissionAccountability.sol` | None |
| `SLASHING_RATE_SCALE_FACTOR` | Set as a [Protocol Constant](/reference/protocol/#protocol-constants) | See `SLASHING_RATE_SCALE_FACTOR` in [Protocol Constants](/reference/protocol/#protocol-constants) | None |
