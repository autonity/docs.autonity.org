---
title: "Autonity Mainnet"
description: >
 The live Autonity blockchain network for real-value transactions running the stable version of the Autonity Protocol
draft: false
---

Autonity Mainnet is the live Autonity blockchain network for transactions and decentralized application (dApp) operations using real value.

Mainnet is for participants interested in:

- The Autonity Futures Protocol
- Decentralized application (dApp) use cases
- Providing live validator and public RPC endpoint node infrastructure
- ...


## Mainnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity (Nile) Mainnet`|
|New RPC URL|Please select one from [Chainlist] ()|
|ChainID |`65000000`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|``|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

The network's genesis configuration is:

| Name                               | Mainnet                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65000000`                    |
| `gasLimit`                         | ` ` ( M)              |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | ``                          |
| `config.autonity.delegationRate`   | `` ( %)                  |                |
| `config.autonity.treasuryFee`      | `` ( %)      |
| `config.autonity.minBaseFee`       | `` ( GWei)        |
| `config.autonity.operator`         | `` |
| `config.autonity.treasury`         | `` |
| `config.autonity.validators`       |  See [`Validators`] ( ) object in the AGC `MainnetChainConfig` for details.  |
| `config.oracle.symbols`       | `[  ]`        |
| `config.oracle.votePeriod`       | `` ( blocks)       |


## Bootnodes

The network bootnode addresses are:

| enode |
| :-- |
| `enode://...` |


## Release

Mainnet is built using:

- Autonity Go Client (AGC) Release: [ ] ( ). The docker image release is: `ghcr.io/autonity/autonity:latest`

- Autonity Oracle Server (AOS) Release: [ ]( ). The docker image release is: `ghcr.io/autonity/autonity-oracle:latest`

## Faucet

- Faucet for [Auton](/concepts/protocol-assets/auton) ... TO DO
- ... [Newton](/concepts/protocol-assets/newton) ... TO DO

## Public endpoints

Please select one from [Chainlist] ( TO DO ). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [ TO DO ](https://bakerloo.autonity.org/)
