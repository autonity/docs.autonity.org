---
title: "Piccadilly Testnet"
linkTitle: "Piccadilly Testnet"
weight: 1
description: >
  An open testnet for the Piccadilly Circus Game Competition
---

A public testnet for participants interested in:

- Helping find bugs in Autonity.
- Operating node infrastructure.
- Operating as a validator.
- Stake delegation.
- Developing and deploying dApp use cases.

For the goals of the Piccadilly Circus Competition Game and how to participate, see the game competition website at [https://game.autonity.org/](https://game.autonity.org/).

## Piccadilly Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Piccadilly Testnet`|
|New RPC URL|`https://rpc1.piccadilly.autonity.org/`|
|ChainID |`65100000`|
|Symbol|`XTN`|
|Block Explorer URL (optional)|`https://piccadilly.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

| Name                               | Piccadilly                    |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65100000`                    |
| `gasLimit`                         | `30000000`(30M)               |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `100`                         |
| `config.autonity.delegationRate`   | `1000` (10%)                  |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 GWei)        |
| `config.autonity.operator`         |  |  |
| `config.autonity.treasury`         |  |  |
| `config.autonity.validators`       |  |  |

Note:

- The client default setting for the `--miner.gaslimit` flag is set to `30000000` (30M), the EIP-1559 block gas limit of 30M per Ethereum upstream.


## Bootnodes

The network bootnode addresses are:

- "enode://3c7f26eb85a7fc37d5ea64c07598a28dd58f507477a88b2144179a4a162c6cba9407389d39c76386126f0604dd53141680d8075b6d210a22cc38c3a8dd877711@35.246.7.21:30303"
- "enode://08e2ed9ca80772ce32e3b56fba3469e33a034a66780e4852586e38db657658fdc610cfb7345543a01277eb53af458ef7cac0b66570ac1982011f24d3832d782c@34.100.165.124:30303"
- "enode://d820e4d53f1e47443c23f2db28b251ca8b8dc207a1b0a0e36ae1bbeb63d0cea4f00dabb61e5daf27468f022adc8780dfd181c57ce0db16a9668dd72e18ecac6b@159.203.156.236:30303"

## Release

- The current iteration of the Piccadilly network is built using this Autonity Release: [v0.9.0](https://github.com/autonity/autonity/releases/tag/v0.9.0)

- The nodes are running this docker image release: `ghcr.io/autonity/autonity/autonity:latest`

## Faucet

- Faucet for [auton](/autonity/protocol-assets/auton) test funds: [https://faucet.autonity.org/](https://faucet.autonity.org/)

## Public endpoints:

- RPC: https://rpc1.piccadilly.autonity.org
- WebSocket: wss://rpc1.piccadilly.autonity.org/ws

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://piccadilly.autonity.org/](https://piccadilly.autonity.org/)
