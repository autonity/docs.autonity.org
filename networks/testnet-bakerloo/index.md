---
title: "Bakerloo Testnet"
description: >
 The _stable_ public Testnet running the current or an earlier version of the Autonity protocol
---

Bakerloo is a public Testnet providing a stable testing environment for those developing a project on top of Autonity.

Bakerloo is for participants interested in:

- Operating node infrastructure.
- Developing and deploying dApp use cases.

## Bakerloo Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Bakerloo (Barada) Testnet`|
|New RPC URL|`https://rpc1.bakerloo.autonity.org`|
|ChainID |`65010002`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://bakerloo.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

The network's genesis configuration is:

| Name                               | Bakerloo                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65010002`                    |
| `gasLimit`                         | `30000000` (30M)              |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `50`                          |
| `config.autonity.delegationRate`   | `1000` (10%)                  |                |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 GWei)        |
| `config.autonity.operator`         | `0x293039dDC627B1dF9562380c0E5377848F94325A` |
| `config.autonity.treasury`         | `0x7f1B212dcDc119a395Ec2B245ce86e9eE551043E` |
| `config.autonity.validators`       | `enode://ebd47c61fa3b0125240654f7b73abeb188dd8c954385e2b75dd0b46efc341b801ae4593be77a954120bcff97a5282ff8f9485306976f8541b2fa971066cd37be@35.246.21.247:30303` |
|  | `enode://1cbd580027a2d21c114c75720115c4c04524952231f66607514fd6bcb5979f20181066383a7a15f1382aa637f6470170c67f74bf1f95271f2abc4ae08c8a11fb@35.189.64.207:30303` |
|  | `enode://28136dd78f976e8fbcbd2c8222cee3f6ac45ac01ceea4a43946d476c03f4971cea23d8c30f0e1a2cbcfde5310a0117ae36ba15c6028e036f637141f330040f62@34.105.163.137:30303` |
|  | `enode://e4dacdb0170bc1baaf7a90935c8d35e75aeec639087320b19ffdd6eb8e6f3b967dd696b1c2f3f99a6a1fea003f7c2a0bb9d8228c06b31ae6c5fec863b8745a2d@35.177.8.113:30303` |
|  | `enode://07ea9eaa469d07695d6855089ad1e0fda35933b779f5907c6edbb77365eef2297b56039fa021e31183675c201855bd95275852d4b1ff9251cce558d1a3611240@35.179.46.181:30303` |
|  | `enode://fb6f5556df35da18c1ecac878fd44a84a0cc302952e1172871dfc48c996c9940b182df374586722212ecb92a8771cafcf48b21657832316423e33f7dbc0b4e7f@3.9.98.39:30303` |
| `config.oracle.symbols`       | `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "ATN-NTN"]`        |
| `config.oracle.votePeriod`       | `30` (30 blocks)       |


## Bootnodes

The network bootnode addresses are:

| enode |
| :-- |
| `enode://63ba7876187203163d093c63e8bbeaf9c4c385ad9b37dc64aa9407e90b98d6678cf1caa9d810829730986966fd0e056c49bdac10eb3389756e3d457580ee0687@34.142.78.108:30303` |
| `enode://ec317b7ae32d55620f37edc9c8af649e6e649f806ba8c3e53ab5407537b13c7a0b00719bb5518d9518978631765fb21a1620f4c32d97a5be0ed9672d8ff4d1a0@35.189.83.7:30303` |


## Release

- The current iteration of the Bakerloo network is built using this Autonity Release: [v0.13.0](https://github.com/autonity/autonity/releases/tag/v0.13.0)

- The docker image release is: `ghcr.io/autonity/autonity:latest`

## Faucet

- Faucet for [auton](/concepts/protocol-assets/auton) test funds: [https://faucet.autonity.org/](https://faucet.autonity.org/)
- There is currently no faucet for [newton](/concepts/protocol-assets/newton), as newton tokens will be made available to network participants in later phases of the testnet.

## Public endpoints

Default rate limit on calls to `wss` and `https` public endpoints combined  is 250 requests per second per IP.

- RPC: [https://rpc1.bakerloo.autonity.org](https://rpc1.bakerloo.autonity.org)
- WebSocket: [wss://rpc1.bakerloo.autonity.org/ws](wss://rpc1.bakerloo.autonity.org/ws)

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://bakerloo.autonity.org/](https://bakerloo.autonity.org/)
