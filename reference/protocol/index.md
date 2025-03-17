
---
title: "Protocol Parameters"

description: >
  Autonity protocol parameters - definitions, genesis configuration, update mechanism if modifiable 
---

# Overview

The protocol parameters are the configuration variables for the Autonity Network blockchain and Autonity Protocol Contracts. The parameterisation sets how the network will function by specifying economic, consensus, temporal, and governance settings. Protocol parameters are specified as part of the `genesis.json` file at network genesis and/or set in the Autonity software's default configuration.

The values for [public Autonity networks](/reference/genesis/#public-autonity-network-configuration) are set as network presets in the genesis configuration of the Autonity software - i.e. the Autonity Go Client, Protocol Contracts, and Autonity Oracle Server.

If specifying the values for a [local Autonity network](/reference/genesis/#local-autonity-network-configuration), the values are specified in the [`config` object](/reference/genesis/#config-object) of the local network's `genesis.json` file. In the [local Autonity network](/reference/genesis/#local-autonity-network-configuration) scenario then the local network operator can choose to use default settings or specify their own settings in place of those defaults in their `genesis.json` file as required by their use case.

A subset of the protocol parameters may be updated by the network's governance account after genesis.

## WIP NOTES / TO DO

Above in parameters does this clearly state the params are:

- the core blockchain settings (epoch, block, gas etc)?
- the protocol contract settings (which includes the protocol contract addresses)?
- that they are set in the core codebase genesis and protocol contract config, in Solidity contracts?

Should the section protocol contract addresses be removed and move the set
REVIEW CHECKS FOR THE DRAFT:

- consistency of use of "None" vs "Contract upgrade" for the "Post Genesis Update Mechanism" column.
- consistency of including for each protocolcontract config:
  - parameters set in protocol constants contract
  - parameters hard-coded in protocol contracts
  - parameters set as protocol constants
  - parameters set in autonity config - namely OFD and OAFD - rewards and accounts:  setOracleRewardRate, setProposerRewardRate,

Chain Config:

- add the EIP-1559 TFM parameters?

Protocol Contracts

- change row ordering to reflect order in [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses)?
- should this be moved before Protocol constants?

Scale factor notebox

- remove second para as redundant or remove 1st para?


## Protocol Constants

Protocol Constants are protocol parameter constant values that may be used in one or more Protocol Contracts. They are defined in `ProtocolConstants.sol`.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `SLASHING_RATE_DECIMALS` | The number of decimal points used for fixed-point arithmetic during computation of slashing penalties | `4` | Contract upgrade | 
| `SLASHING_RATE_SCALE_FACTOR` | The division precision used as the denominator when computing the slashing amount of a penalty | `10 ** SLASHING_RATE_DECIMALS` (`10^4 = 10_000`, i.e. 0.01%)| Contract upgrade |
| `ORACLE_SLASHING_RATE_CAP` | The % slashing rate for oracle accountability slashing penalties | `1_000` (10%) | Contract upgrade |

::: {.callout-note title="Scale factor" collapse="false"}

`SLASHING_RATE_DECIMALS` and `SLASHING_RATE_SCALE_FACTOR` are used to allow for decimal slashing values. Solidity doesn't natively support decimal fixed point arithmetic. Using the scale factor method allows the protocol to define the % level of precision used when computing a slashing penalty.

For example:

| Scale Factor | Slashing rate applied |
|:-------------|:----------------------|
| `10_000`     | 100% slash |
| `1_000`       | 10% slash |
| `100`        | 1% slash |
| `10`         | 0.01% slash |
| `1`          | 0.001% slash |

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
| `upgradeManagerContract` contract address | The Upgrade Manager Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setUpgradeManagerContract()`](/reference/api/aut/op-prot/#setupgrademanagercontract) |
| `inflationController` contract address | The Newton Inflation Controller Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setInflationControllerContract()`](/reference/api/aut/op-prot/#setinflationcontrollercontract) |
| `omissionAccountability` contract address | The Omission Accountability Contract address | Deterministic - see [Protocol Contract addresses](/concepts/architecture/#protocol-contract-addresses) | See [`setOmissionAccountabilityContract()`](/reference/api/aut/op-prot/#setomissionaccountabilitycontract) |


## Chain Config

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
| `withholdingThreshold` account | The inactivity threshold at which committee member staking and Newton inflation rewards are withheld and sent to the Withheld Rewards Pool account by the Omission Fault Detection protocol | Set to `0` (0%, no tolerance) | See [`setWithholdingThreshold()`](/reference/api/aut/op-prot/#setwithholdingthreshold) |
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
| `SLASHING_RATE_SCALE_FACTOR` | Set as a [Protocol Constant](/reference/protocol/#protocol-constants) | See `SLASHING_RATE_SCALE_FACTOR` in [Protocol Constants](/reference/protocol/#protocol-constants) | Contract upgrade |


### Oracle Config DRAFT

Parameters for the Oracle Contract of the Oracle protocol and Oracle Accountability Fault Detection (OAFD) protocol.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| Oracle `symbols` | the currency pairs that the oracle network provides data points for | See [`config.oracle object`](/reference/genesis/#configoracle-object) | See [`setSymbols()`](/reference/api/aut/op-prot/#setsymbols-oracle-contract) |
| Oracle `votePeriod` | the time interval at which the oracle network initiates a new oracle round for submitting and voting on oracle data, measured in blocks | See [`config.oracle object`](/reference/genesis/#config.oracle-object) | None |
| `outlierDetectionThreshold` | Defines the threshold for flagging outliers | See [`config.oracle object`](/reference/genesis/#config.oracle-object) | None |
| `outlierSlashingThreshold` | Defines the threshold for slashing penalties, controlling the sensitivity of the penalty model | See [`config.oracle object`](/reference/genesis/#config.oracle-object) | None |
| `baseSlashingRate` | Defines the base slashing rate for penalising outliers | See [`config.oracle object`](/reference/genesis/#config.oracle-object) | None |
| `OracleRewardRate` | Set in the Autonity Protocol Contract configuration | See [`config.autonity.oracleRewardRate`](/#autonity-contract-config) | Contract upgrade |
| `ORACLE_SLASHING_RATE_CAP` | Set as a [Protocol Constant](/reference/protocol/#protocol-constants) | See `ORACLE_SLASHING_RATE_CAP` in [Protocol Constants](/reference/protocol/#protocol-constants) | Contract upgrade |
 


### Inflation Controller Config DRAFT

Parameters for the Inflation Controller Contract of the Newton inflation mechanism. 

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `inflationRateInitial` | Initial inflation rate | See [`config.InflationController object`](/reference/genesis/#configinflationcontroller-object) | None |
| `inflationRateTransition` | Transition inflation rate | See [`config.InflationController object`](/reference/genesis/#configinflationcontroller-object) | None |
| `inflationReserveDecayRate` | | Constant inflation rate | See [`config.InflationController object`](/reference/genesis/#configinflationcontroller-object) | None |
| `inflationTransitionPeriod` | Transition period | See [`config.InflationController object`](/reference/genesis/#configinflationcontroller-object) | None |
| `inflationCurveConvexity` | Convexity parameter | See [`config.InflationController object`](/reference/genesis/#configinflationcontroller-object) | None |
| `InitialInflationReserve` | Set in the Autonity Protocol Contract configuration | See [`config.autonity.InitialInflationReserve`](/reference/protocol/#autonity-contract-config) | None |



### ASM Config DRAFT

Configuration of the Auton Stabilization Mechanism's (ASM) ACU, Stabilization, and Supply Control Contracts.



#### ACU Config DRAFT

The ASM's Autonomous Currency Unit (ACU) currency basket configuration, an optimal currency basket of 7 free-floating fiat currencies.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------| 
| `symbols` | the [currency pair](/glossary/#currency-pair) symbols of the currencies in the basket | See [`config.asm.acu object`](/reference/genesis/#configasmacu-object) | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |
| `quantities` | the basket quantity corresponding to each of the `symbols` in the basket | See [`config.asm.acu object`](/reference/genesis/#configasmacu-object) | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |
| `scale` | the scale used to represent the basket `quantities` and ACU value | See [`config.asm.acu object`](/reference/genesis/#configasmacu-object) | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |



#### Stabilization Config DRAFT

The ASM's Stabilization mechanism CDP configuration.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `borrowInterestRate` | the annual continuously-compounded interest rate for borrowing | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | None |
| `liquidationRatio` | the minimum ACU value of collateral required to maintain 1 ACU value of debt | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | See [`setLiquidationRatio()`](/reference/api/aut/op-prot/#setliquidationratio-asm-stabilization-contract) |
| `minCollateralizationRatio` | the minimum ACU value of collateral required to borrow 1 ACU value of debt | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | See [`setMinCollateralizationRatio()`](/reference/api/aut/op-prot/#setmincollateralizationratio-asm-stabilization-contract) |
| `minDebtRequirement` | the minimum amount of debt required to maintain a CDP | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | See  [`setMinDebtRequirement()`](/reference/api/aut/op-prot/#setmindebtrequirement-asm-stabilization-contract) |
| `targetPrice` | the ACU value of 1 unit of debt | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | None |



#### Supply Control Config DRAFT

Parameters for the ASM's Auton supply control configuration.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `initialAllocation` | The initial allocation of Auton to the ASM | See [`config.asm.supplyControl object`](reference/genesis/#config.asm.supplycontrol-object) | None |



### Omission Accountability Config DRAFT

Parameters for the Omission Accountability Contract and the Omission Fault Detection (OFD) protocol.

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `inactivityThreshold` | Defines the threshold for flagging validator inactivity | See [`config.omissionAccountability object`](/reference/genesis/#config.omissionaccountability-object) | See [`setInactivityThreshold()`](/reference/api/aut/op-prot/#setinactivitythreshold-omission-accountability-contract) |
| `lookbackWindow` | The number of blocks over which the protocol will look for inactivity | See [`config.omissionAccountability object`](/reference/genesis/#config.omissionaccountability-object) | See [`setLookbackWindow()`](/reference/api/aut/op-prot/#setlookbackwindow-omission-accountability-contract) |
| `pastPerformanceWeight` | Determines how much weight is given to past performance of the validator in the preceding epoch in the current epoch when computing the aggregated inactivity score | See [`config.omissionAccountability object`](/reference/genesis/#config.omissionaccountability-object) | See [`setPastPerformanceWeight()`](/reference/api/aut/op-prot/#setpastperformanceweight-omission-accountability-contract) |
| `initialJailingPeriod` | The initial number of epoch(s) that a validator will be jailed for | See [`config.omissionAccountability object`](/reference/genesis/#config.omissionaccountability-object) | See [`setInitialJailingPeriod()`](/reference/api/aut/op-prot/#setinitialjailingperiod-omission-accountability-contract) |
| `initialProbationPeriod` | the initial number of epoch(s) that a validator will be set under probation for | See [`config.omissionAccountability object`](/reference/genesis/#config.omissionaccountability-object) | See [`setInitialProbationPeriod()`](/reference/api/aut/op-prot/#setinitialprobationperiod-omission-accountability-contract) |
| `initialSlashingRate` | the division precision used as the denominator when computing the slashing amount of a penalty | See [`config.omissionAccountability object`](/reference/genesis/#config.omissionaccountability-object) | See [`setDelta()`](/reference/api/aut/op-prot/#setdelta-omission-accountability-contract) |
| `delta` | the number of blocks to wait before generating an activity proof | See [`config.omissionAccountability object`](/reference/genesis/#config.omissionaccountability-object) | See [`setPastPerformanceWeight()`](/reference/api/aut/op-prot/#setinactivitythreshold-omission-accountability-contract) |
| `SCALE_FACTOR` | Used for fixed-point arithmetic during computation of inactivity score |  See `SCALE_FACTOR` in `OmissionAccountability.sol` | Contract upgrade |
| `SLASHING_RATE_SCALE_FACTOR` | Set as a [Protocol Constant](/reference/protocol/#protocol-constants) | See `SLASHING_RATE_SCALE_FACTOR` in [Protocol Constants](/reference/protocol/#protocol-constants) | Contract upgrade |
