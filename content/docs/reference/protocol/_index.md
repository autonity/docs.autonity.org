
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
| `minBaseFee` | minimum price for a unit of gas used to compute a transaction on the network | See [`config.autonity.minBaseFee`](/reference/genesis/#configautonity-object) | See [`setMinimumBaseFee`](/reference/api/aut/op-prot/#setminimumbasefee) |
| `gasLimit` | maximum amount of gas expenditure allowed for computing the genesis block, and then blocks thereafter  | See [`config.gasLimit`](/reference/genesis/#gaslimit) | None |
| `treasury` account | protocol’s treasury account for receiving treasury fees used for Autonity community funds | See [`config.autonity.treasury`](/reference/genesis/#configautonity-object) | See [`setTreasuryAccount`](/reference/api/aut/op-prot/#settreasuryaccount) |
| `treasuryFee` | the percentage of staking rewards  deducted for community funds. | See [`config.autonity.treasuryFee`](/reference/genesis/#configautonity-object) | See [`setTreasuryFee`](/reference/api/aut/op-prot/#settreasuryfee) |
| `maxCommitteeSize` | maximum number of consensus committee members| See [`config.autonity.maxCommitteeSize`](/reference/genesis/#configautonity-object) | See [`setCommitteeSize`](/reference/api/aut/op-prot/#setcommitteesize) |
| `delegationRate` | the percentage of staking rewards deducted by validators as a commission from delegated stake | See [`config.autonity.delegationRate`](/reference/genesis/#configautonity-object)  | None |
| `unbondingPeriod` | the period of time bonded stake must wait before Newton can be redeemed after unbonding, defined as a number of blocks. The unbonding period can be any integer number > 0, but must be longer than the epoch period.| See [`config.autonity.unbondingPeriod`](/reference/genesis/#configautonity-object)  | See [`setUnbondingPeriod`](/reference/api/aut/op-prot/#setunbondingperiod) |
| `epochPeriod` | the period of time for which a consensus committee is elected, defined as a number of blocks| See [`config.autonity.epochPeriod`](/reference/genesis/#configautonity-object) | See [`setEpochPeriod`](/reference/api/aut/op-prot/#setepochperiod) |
| `blockPeriod` | the minimum time interval between two consecutive blocks, measured in seconds | See [`config.autonity.blockPeriod`](/reference/genesis/#configautonity-object) | See [`setBlockPeriod`](/reference/api/aut/op-prot/#setblockperiod) |
| governance `operator` account | address of the Autonity Protocol governance account| See [`config.autonity.operator`](/reference/genesis/#configautonity-object) | See [`setOperatorAccount`](/reference/api/aut/op-prot/#setoperatoraccount) |
| Protocol Contract upgrade: `bytecode`, `abi`  | Autonity Protocol Contract is provided as part of the codebase. An upgraded contract can be specified at or post genesis | To specify an upgraded contract at initialisation, see [`config.autonity.bytecode`](/reference/genesis/#configautonity-object) and [`config.autonity.abi`](/reference/genesis/#configautonity-object) | See [`upgradeContract`](/reference/api/aut/op-prot/#upgradecontract) |
