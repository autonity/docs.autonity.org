
---
title: "Protocol Parameters"
linkTitle: "Protocol Parameters"

description: >
  Autonity protocol parameters - definitions, genesis configuration, update mechanism if modifiable 
---

Autonity Protocol parameters specify economic, consensus, temporal, and governance settings of an Autonity Network. They are specified as part of the `genesis.json` file at network genesis and may be updated by the network's governance account.


## Parameters

| Parameter | Description | Genesis Configuration | Post Genesis Update Mechanism |
|-----------|-------------|-----------------------|-------------------------------|
| `minBaseFee` | minimum price for a unit of gas used to compute a transaction on the network | See [`config.autonity.minBaseFee`](/reference/genesis/#configautonity-object) | See [`setMinimumBaseFee()`](/reference/api/aut/op-prot/#setminimumbasefee) |
| `gasLimit` | maximum amount of gas expenditure allowed for computing the genesis block, and then blocks thereafter  | See [`config.gasLimit`](/reference/genesis/#gaslimit) | None |
| `treasury` account | protocol’s treasury account for receiving treasury fees used for Autonity community funds | See [`config.autonity.treasury`](/reference/genesis/#configautonity-object) | See [`setTreasuryAccount()`](/reference/api/aut/op-prot/#settreasuryaccount) |
| `treasuryFee` | the percentage of staking rewards  deducted for community funds. | See [`config.autonity.treasuryFee`](/reference/genesis/#configautonity-object) | See [`setTreasuryFee()`](/reference/api/aut/op-prot/#settreasuryfee) |
| `maxCommitteeSize` | maximum number of consensus committee members| See [`config.autonity.maxCommitteeSize`](/reference/genesis/#configautonity-object) | See [`setCommitteeSize()`](/reference/api/aut/op-prot/#setcommitteesize) |
| `delegationRate` | the percentage of staking rewards deducted by validators as a commission from delegated stake | See [`config.autonity.delegationRate`](/reference/genesis/#configautonity-object)  | None (Individual validators can reset their rate after registration. See [`changeCommissionRate()`](/reference/api/aut/#changecommissionrate)) |
| `unbondingPeriod` | the period of time bonded stake must wait before Newton can be redeemed after unbonding, defined as a number of blocks. The unbonding period can be any integer number > 0, but must be longer than the epoch period.| See [`config.autonity.unbondingPeriod`](/reference/genesis/#configautonity-object)  | See [`setUnbondingPeriod()`](/reference/api/aut/op-prot/#setunbondingperiod) |
| `epochPeriod` | the period of time for which a consensus committee is elected, defined as a number of blocks| See [`config.autonity.epochPeriod`](/reference/genesis/#configautonity-object) | See [`setEpochPeriod()`](/reference/api/aut/op-prot/#setepochperiod) |
| `blockPeriod` | the minimum time interval between two consecutive blocks, measured in seconds | See [`config.autonity.blockPeriod`](/reference/genesis/#configautonity-object) | None |
| governance `operator` account | address of the Autonity Protocol, Autonity Oracle Contract, and ASM Contracts governance account| See [`config.autonity.operator`](/reference/genesis/#configautonity-object) | See [`setOperatorAccount()`](/reference/api/aut/op-prot/#setoperatoraccount) |
| Oracle `symbols` | the currency pairs that the oracle network provides data points for | See [`config.oracle.symbols`](/reference/genesis/#configoracle-object) | See [`setSymbols()`](/reference/api/aut/op-prot/#setsymbols-oracle-contract) |
| Oracle `votePeriod` | the time interval at which the oracle network initiates a new oracle round for submitting and voting on oracle data, measured in blocks | See [`config.oracle.votePeriod`](/reference/genesis/#configoracle-object) | None |
| ASM ACU `symbols`, `quantities`, `scale` | the ACU currency basket configuration | See [`config.asm.acu object`](/reference/genesis/#configasmacu-object) | See [`modifyBasket()`](/reference/api/aut/op-prot/#modifybasket-acu-contract) |
| ASM Stabilization `liquidationRatio` | the minimum ACU value of collateral required to maintain 1 ACU value of debt | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | See [`setLiquidationRatio()`](/reference/api/aut/op-prot/#setliquidationratio-asm-stabilization-contract) |
| ASM Stabilization `minCollateralizationRatio` | the minimum ACU value of collateral required to borrow 1 ACU value of debt | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | See [`setMinCollateralizationRatio()`](/reference/api/aut/op-prot/#setmincollateralizationratio-asm-stabilization-contract) |
| ASM Stabilization `minDebtRequirement` | the minimum amount of debt required to maintain a CDP | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | See  [`setMinDebtRequirement()`](/reference/api/aut/op-prot/#setmindebtrequirement-asm-stabilization-contract) |
| ASM Stabilization `minDebtRequirement` | the minimum amount of debt required to maintain a CDP | See [`config.asm.stabilization object`](/reference/genesis/#configasmstabilization-object) | See  [`setMinDebtRequirement()`](/reference/api/aut/op-prot/#setmindebtrequirement-asm-stabilization-contract) |
| ASM Stabilization `oracle` contract address | the Autonity Oracle Contract address | See Concept Architecture and [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract) | See [`setOracle()`](/reference/api/aut/op-prot/#setoracle-asm-stabilization-contract) |
| ASM Stabilization `supplyControl` contract address | the ASM Supply Control Contract address | See Concept Architecture and [ASM Supply Control Contract](/concepts/architecture/#asm-supply-control-contract) | See [`setSupplyControl()`](/reference/api/aut/op-prot/#setsupplycontrol-asm-stabilization-contract) |


<!-- 
| Protocol Contract upgrade: `bytecode`, `abi`  | Autonity Protocol Contract is provided as part of the codebase. An upgraded contract can be specified at or post genesis | To specify an upgraded contract at initialisation, see [`config.autonity.bytecode`](/reference/genesis/#configautonity-object) and [`config.autonity.abi`](/reference/genesis/#configautonity-object) | See [`upgradeContract()`](/reference/api/aut/op-prot/#upgradecontract) |
-->
