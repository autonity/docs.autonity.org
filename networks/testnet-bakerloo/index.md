---
title: "Bakerloo Testnet"
description: >
 Public Autonity Testnet for test and development
draft: false
---

Bakerloo is a general purpose public testnet that simulates the mainnet protocol configuration.

Testnet provides a stable environment for community developers, node operators, and infrastructure providers to:

- test protocol upgrades before rollout to Mainnet
- test tooling, software and operational practices
- work in a safe sandbox environment to build, test, and debug before deployment to mainnet without transaction cost
- innovate and develop new protocols, ideas, and projects for Autonity.

## Bakerloo Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Bakerloo (Nile) Testnet`|
|New RPC URL|Please select one from [Chainlist](https://chainlist.org/?search=autonity&testnets=true)|
|ChainID |`65010004`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://bakerloo.autonity.org/`|

::: {.callout-tip title="Adding Autonity as a custom network to your wallet" collapse="false"}

The above information can be used to add Autonity as a custom network to to an existing client such as [MetaMask](https://support.metamask.io/configure/networks/how-to-add-a-custom-network-rpc/).

:::

## Genesis configuration

The network's genesis configuration is:

| Name                               | Bakerloo                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65010004`                    |
| `gasLimit`                         | `30000000` (30M)              |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `27`                          |
| `config.autonity.delegationRate`   | `1000` (10%)                  |                |
| `config.autonity.treasuryFee`      | `50000000000000000` (5%)      |
| `config.autonity.minBaseFee`       | `10_000_000_000` (10 GWei)        |
| `config.autonity.operator`         | `0x83e5e0eab996Bb894814fa8F0AC96a0D314f06F3` |
| `config.autonity.treasury`         | `0xd735174cf1d0D9150cb57750C45B6e8095160f6A` |
| `config.autonity.validators`       |  See `BakerlooValidators` in the AGC [`Bakerloo Config`](https://github.com/autonity/autonity/blob/release/v1.1.1/params/bakerloo_config.go#L163) for details.  |
| `config.oracle.symbols`       | `['AUD-USD','CAD-USD','EUR-USD','GBP-USD','JPY-USD','SEK-USD']`        |
| `config.oracle.votePeriod`       | `600` (600  blocks)       |


## Node discovery

Bootnode addresses must be specified explicitly for peer node discovery when joining and syncing with the network. For configuration details, see the Development guide page [Setting up custom networks](/developer/custom-networks/) and **How to identify and configure bootnodes for a custom network**.

## Release

The current iteration of the Bakerloo network is built using:

- Autonity Go Client (AGC) Release: [v1.1.1](https://github.com/autonity/autonity/releases/tag/v1.1.1). The docker image release is: [`ghcr.io/autonity/autonity:v1.1.1`](https://github.com/autonity/autonity/pkgs/container/autonity/476121691?tag=v1.1.1).

- Autonity Oracle Server (AOS) Release: [v0.2.6](https://github.com/autonity/autonity-oracle/releases/tag/v0.2.6). The docker image release is: [`ghcr.io/autonity/autonity-oracle-bakerloo:v0.2.6`](https://github.com/orgs/autonity/packages/container/autonity-oracle-bakerloo/483918507?tag=v0.2.6).

## Faucet

- Faucet for [Auton](/concepts/protocol-assets/auton) test funds: [https://autonity.faucetme.pro/](https://autonity.faucetme.pro/) 

There is currently no faucet for [Newton](/concepts/protocol-assets/newton), as newton tokens will be made available to network participants in later phases of the testnet by request on Autonity [Discord Server](https://discord.gg/autonity).

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?search=autonity&testnets=true). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://bakerloo.autonity.org/](https://bakerloo.autonity.org/)
