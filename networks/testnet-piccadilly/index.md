---
title: "Piccadilly Testnet"
description: >
  The _bleeding-edge_ public Testnet running the latest deployable version of the Autonity protocol
---

Piccadilly is a public Testnet running the latest deployable version of the Autonity protocol. It is the testing environment used in the pre-MainNet [Piccadilly Circus Games Competition (PCGC)](https://game.autonity.org) and may undergo re-genesis with the latest protocol implementation at the end of a game round. 

Piccadilly is for participants interested in:

- Taking part in the [Piccadilly Circus Games Competition](https://game.autonity.org) and helping to develop the Autonity project.
- Helping find bugs in Autonity (See the game's [Bug Bounty](https://game.autonity.org/#tasks-points)).
- Operating node infrastructure.
- Operating as a validator.
- Stake delegation.
- Developing and deploying dApp use cases.

## Piccadilly Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Piccadilly (Barada) Testnet`|
|New RPC URL|`https://rpc1.piccadilly.autonity.org/`|
|ChainID |`65100003`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://piccadilly.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

| Name                               | Piccadilly                    |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65100003`                    |
| `gasLimit`                         | `20000000`(20M)               |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `28` (increases to `100` after genesis) |
| `config.autonity.delegationRate`   | `1000` (10%)                  |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 GWei)        |
| `config.autonity.operator`         | `0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397` |
| `config.autonity.treasury`         | `0xF74c34Fed10cD9518293634C6f7C12638a808Ad5` |
| `config.autonity.validators`       |  See [`Validators`](https://github.com/autonity/autonity/blob/release/v0.14.1/params/config.go#L100) object in the AGC `PiccadillyChainConfig` for details.  |
| `config.oracle.symbols`       | `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "ATN-NTN"]`        |
| `config.oracle.votePeriod`       | `30` (30 blocks)       |


## Bootnodes

The network bootnode addresses are:

| enode |
| :--  |
| `enode://48a10db920251436ee1d7989db6cbab734157d5bd3ec9d534021e4903fdab51407ba4fd936bd6af1d188e3f464374c437accefa40f0312eac9bc9ae6fc0a2782@34.105.239.129:30303` |
| `enode://9379179c8c0f7fec28dd3cca64da5d85f843e3b05ba24f6ae4f8d1bb688b4581f92c10e84e166328499987cf2da18668446dd7353724cf691ad2a931a0cbd88d@34.93.237.13:30303` |
| `enode://c7e8619c09c85c47a2bbda720ecec449ab1207574cc60d8ec451b109b407d7542cabc2683eedcf326009532e3aea2b748256bac1d50bf877c73eea4d633e8913@54.241.251.216:30303` |

## Release

The current iteration of the Piccadilly network is built using:

- Autonity Go Client (AGC) Release: [v0.14.1](https://github.com/autonity/autonity/releases/tag/v0.14.1). The docker image release is: `ghcr.io/autonity/autonity:v0.14.1`

- Autonity Oracle Server (AOS) Release: [v0.1.9](https://github.com/autonity/autonity-oracle/releases/tag/v0.1.9). The docker image release is: `ghcr.io/autonity/autonity-oracle-piccadilly:latest`

## Faucet

- There is currently no faucet for [auton](/concepts/protocol-assets/auton) or [newton](/concepts/protocol-assets/newton) on Piccadilly. Network participants access testnet auton and newton by participating in the [Piccadilly Circus Games Competition (PCGC)](https://game.autonity.org).

## Public endpoints

Default rate limit on calls to `wss` and `https` public endpoints combined  is 250 requests per second per IP.

- RPC: [https://rpc1.piccadilly.autonity.org](https://rpc1.piccadilly.autonity.org)
- WebSocket: [wss://rpc1.piccadilly.autonity.org/ws](wss://rpc1.piccadilly.autonity.org/ws)

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://piccadilly.autonity.org/](https://piccadilly.autonity.org/)
