---
title: "Bakerloo Testnet"
description: >
 The _stable_ public Testnet running the stable version of the Autonity protocol
draft: false
---

Bakerloo is a general purpose public Testnet providing a stable testing environment for those developing a project on top of Autonity.

Bakerloo is for participants interested in:

- Operating node infrastructure.
- Developing and deploying dApp use cases.

## Bakerloo Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Bakerloo (Nile) Testnet`|
|New RPC URL|Please select one from [Chainlist](https://chainlist.org/?search=autonity&testnets=true)|
|ChainID |`65010004`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://bakerloo.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

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
| `config.autonity.validators`       |  See `Validators` in the AGC [`BakerlooChainConfig`](https://github.com/autonity/autonity/blob/release/v1.1.0/params/config.go)) for details.  |
| `config.oracle.symbols`       | `['AUD-USD','CAD-USD','EUR-USD','GBP-USD','JPY-USD','SEK-USD']`        |
| `config.oracle.votePeriod`       | `600` (600  blocks)       |


## Bootnodes

The network bootnode addresses are:

| enode | region |
| :-- | :--      |
| `enode://aa56696a131d2cfac1cfaa18dba06f5dc32ef57cf8c8b3548ab1f74227987c5656c2c0eecba61dfdd0754030c23d433e4db554f6b677eb900c05b98792b1d7fb@34.39.58.139:30303` | europe-west2 |
| `enode://feb31d821a92db0c7a6260c1eff9539bde1db5d947f319b7f761ea99479b5b31a95209153c9c910c8f94e8f557541a7ffa72a4a1ff0602944df2b0e6611be4ce@35.200.221.60:30303` | asia-south1 |
| `enode://b6e18b34019e70d32bfd43bcf66b71a127117f3402c29f857337b9dd3ccc45c4a9d441d211ca2a201bd46d003cfbf84a2b0721cf9b939ae6abd66dfe698700fc@35.235.121.67:30303` | us-west2 |


## Release TO DO

The current iteration of the Bakerloo network is built using:

- Autonity Go Client (AGC) Release: [ ]( ). The docker image release is: `ghcr.io/autonity/autonity:latest`

- Autonity Oracle Server (AOS) Release: [ ]( ). The docker image release is: `ghcr.io/autonity/autonity-oracle-bakerloo:latest`

## Faucet

- Faucet for [Auton](/concepts/protocol-assets/auton) test funds: [https://autonity.faucetme.pro/](https://autonity.faucetme.pro/) 

There is currently no faucet for [Newton](/concepts/protocol-assets/newton), as newton tokens will be made available to network participants in later phases of the testnet by request on Autonity [Discord Server](https://discord.gg/autonity).

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?search=autonity&testnets=true). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://bakerloo.autonity.org/](https://bakerloo.autonity.org/)
