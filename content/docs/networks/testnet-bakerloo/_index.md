---
title: "Bakerloo Testnet"
linkTitle: "Bakerloo Testnet"
weight: 1
description: >
  An open testnet for node operators, validators and developers
---

A public testnet for participants interested in:

- Operating node infrastructure.
- Operating as a validator.
- Stake delegation.
- Developing and deploying dApp use cases.

## Bakerloo Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Bakerloo Testnet`|
|New RPC URL|`https://rpc1.bakerloo.autonity.org`|
|ChainID |`65010000`|
|Symbol|`XTN`|
|Block Explorer URL (optional)|`https://bakerloo.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

The network's genesis configuration is:

| Name                               | Bakerloo                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65010000`                    |
| `gasLimit`                         | `30000000` (30M)              |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `50`                          |
| `config.autonity.delegationRate`   | `1000` (10%)                  |                |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 GWei)        |
| `config.autonity.operator`         |  |
| `config.autonity.treasury`         |  |
| `config.autonity.validators`       |  |

Note:

- The client default setting for the `--miner.gaslimit` flag is set to `30000000` (30M), the EIP-1559 block gas limit of 30M per Ethereum upstream.

## Bootnodes

The network bootnode addresses are:

- "enode://46164e112b9a89641ca1cdb861fb7fefa6d5b111df1ec831601afdb6262a85af1865b4c53b378988c0b85e2d53b758c81322f86b5d3831ccf54d2e4e62c77ff6@34.142.78.108:30303"
- "enode://475b720eded83c95ba55648127cb861c1620482690bfb3aece61f0cad85a234d7b73e1d2b29b753af4e9c6f5a1ffd16a1da04e1185169366fe011ca81ef2ecf7@35.189.83.7:30303"

## Release

- The current iteration of the Bakerloo network is built using this Autonity Release: [v0.9.0](https://github.com/autonity/autonity/releases/tag/v0.9.0)

- The nodes are running this docker image release: `ghcr.io/autonity/autonity/autonity:latest`

## Faucet

- Faucet for [auton](/concepts/protocol-assets/auton) test funds: [https://faucet.autonity.org/](https://faucet.autonity.org/)
- There is currently no faucet for [newton](/concepts/protocol-assets/newton), as newton tokens will be made available to network participants in later phases of the testnet.

## Public endpoints:

- RPC: https://rpc1.bakerloo.autonity.org
- WebSocket: wss://rpc1.bakerloo.autonity.org/ws

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://bakerloo.autonity.org/](https://bakerloo.autonity.org/)
