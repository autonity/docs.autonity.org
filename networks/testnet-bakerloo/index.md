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
|ChainID |`65010001`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://bakerloo.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

The network's genesis configuration is:

| Name                               | Bakerloo                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65010001`                    |
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
| `config.autonity.validators`       | `enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303` |
|  | `enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303` |
|  |`enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303` |
|  | `enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308` |
|  | `enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309` |
|  | `enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310` |
| `config.oracle.symbols`       | `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "ATN-NTN"]`        |
| `config.oracle.votePeriod`       | `30` (30 blocks)       |

Note:

- The client default setting for the `--miner.gaslimit` flag is set to `30000000` (30M), the EIP-1559 block gas limit of 30M per Ethereum upstream.

## Bootnodes

The network bootnode addresses are:

- "enode://46164e112b9a89641ca1cdb861fb7fefa6d5b111df1ec831601afdb6262a85af1865b4c53b378988c0b85e2d53b758c81322f86b5d3831ccf54d2e4e62c77ff6@34.142.78.108:30303"
- "enode://475b720eded83c95ba55648127cb861c1620482690bfb3aece61f0cad85a234d7b73e1d2b29b753af4e9c6f5a1ffd16a1da04e1185169366fe011ca81ef2ecf7@35.189.83.7:30303"

## Release

- The current iteration of the Bakerloo network is built using this Autonity Release: [v0.12.2](https://github.com/autonity/autonity/releases/tag/v0.12.2)

- The nodes are running this docker image release: `ghcr.io/autonity/autonity:latest`

## Faucet

- Faucet for [auton](/concepts/protocol-assets/auton) test funds: [https://faucet.autonity.org/](https://faucet.autonity.org/)
- There is currently no faucet for [newton](/concepts/protocol-assets/newton), as newton tokens will be made available to network participants in later phases of the testnet.

## Public endpoints

Default rate limit on calls to `ws` and `http` public endpoints combined  is 250 requests per second per IP.

- RPC: https://rpc1.bakerloo.autonity.org
- WebSocket: wss://rpc1.bakerloo.autonity.org/ws

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://bakerloo.autonity.org/](https://bakerloo.autonity.org/)
