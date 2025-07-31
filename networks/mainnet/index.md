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
- The Autonity community!


## Mainnet details

::: {.callout-tip title="Delegated staking" collapse="false"}

Watch this space, coming soon! 🚀

:::

<!--
|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity (Nile) Mainnet`|
|New RPC URL|Please select one from [Chainlist](https://chainlist.org/?search=autonity)|
|ChainID |`65000000`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://autonityscan.org`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

The network's genesis configuration is:

| Name                               | Mainnet                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65000000`                    |
| `gasLimit`                         | `30000000` (30M)              |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `27`                          |
| `config.autonity.delegationRate`   | `1000` (10%)                  |
| `config.autonity.treasuryFee`      | `50000000000000000` (5%)      |
| `config.autonity.minBaseFee`       | `10_000_000_000` (10 GWei)    |
| `config.autonity.operator`         | `0x83e5e0eab996Bb894814fa8F0AC96a0D314f06F3` |
| `config.autonity.treasury`         | `0xd735174cf1d0D9150cb57750C45B6e8095160f6A` |
| `config.autonity.validators`       |  See `Validators` in the AGC [`MainnetChainConfig`](https://github.com/autonity/autonity/blob/release/v1.1.0/params/config.go)) for details.  |
| `config.oracle.symbols`            | `['AUD-USD','CAD-USD','EUR-USD','GBP-USD','JPY-USD','SEK-USD']`        |
| `config.oracle.votePeriod`         | `600` (600  blocks)          |


## Bootnodes TO DO

The network bootnode addresses are:

| enode | region |
| :-- | :--      |
| `enode://...` |   |


## Release TO DO

Mainnet is built using:

- Autonity Go Client (AGC) Release: [ ] ( ). The docker image release is: `ghcr.io/autonity/autonity:latest`

- Autonity Oracle Server (AOS) Release: [ ]( ). The docker image release is: `ghcr.io/autonity/autonity-oracle:latest`

## ATN and NTN funding TO DO

- ... for [Auton](/concepts/protocol-assets/auton) ... TO DO
- ... [Newton](/concepts/protocol-assets/newton) ... TO DO

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?search=autonity). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://autonityscan.org](https://autonityscan.org)

-->