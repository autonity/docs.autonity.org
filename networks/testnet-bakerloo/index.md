---
title: "Bakerloo Testnet"
description: >
 The _stable_ public Testnet running the stable version of the Autonity protocol
draft: true
---

Bakerloo is a public Testnet providing a stable testing environment for those developing a project on top of Autonity.

Bakerloo is for participants interested in:

- Operating node infrastructure.
- Developing and deploying dApp use cases.

## Bakerloo Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Bakerloo (Nile) Testnet`|
|New RPC URL|Please select one from [Chainlist](https://chainlist.org/?testnets=true&search=bakerloo)|
|ChainID |`65010004`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://bakerloo.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

The network's genesis configuration is:

| Name                               | Bakerloo                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65010004`                    |
| `gasLimit`                         | `20000000` (20M)              |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | ` `                          |
| `config.autonity.delegationRate`   | ` ` ( %)                  |                |
| `config.autonity.treasuryFee`      | ` ` ( %)      |
| `config.autonity.minBaseFee`       | ` ` (  GWei)        |
| `config.autonity.operator`         | ` ` |
| `config.autonity.treasury`         | ` ` |
| `config.autonity.validators`       |  See [`Validators`](https://github.com/autonity/autonity/blob/release/v0.14.0/params/config.go#L206) object in the AGC `BakerlooChainConfig` for details.  |
| `config.oracle.symbols`       | `[ ]`        |
| `config.oracle.votePeriod`       | ` ` (  blocks)       |


## Bootnodes

The network bootnode addresses are:

| enode |
| :-- |
| `enode://... |


## Release

The current iteration of the Bakerloo network is built using:

- Autonity Go Client (AGC) Release: [ ]( ). The docker image release is: `ghcr.io/autonity/autonity:latest`

- Autonity Oracle Server (AOS) Release: [ ]( ). The docker image release is: `ghcr.io/autonity/autonity-oracle-bakerloo:latest`

## Faucet

- Faucet for [Auton](/concepts/protocol-assets/auton) test funds: [https://faucet.autonity.org/](https://faucet.autonity.org/)
- There is currently no faucet for [newton](/concepts/protocol-assets/newton), as newton tokens will be made available to network participants in later phases of the testnet.

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?testnets=true&search=bakerloo). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://bakerloo.autonity.org/](https://bakerloo.autonity.org/)
