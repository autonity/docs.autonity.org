---
title: "Piccadilly Testnet"
description: >
  The _bleeding-edge_ public Testnet running the latest deployable version of the Autonity protocol
---

Piccadilly is a public Testnet running the latest deployable version of the Autonity protocol. It is the testing environment used in the pre-MainNet [Piccadilly Tiber Challenge](https://autonity.org/tiber). 

Piccadilly is for participants interested in:

- Taking part in the [Piccadilly Tiber Challenge](https://autonity.org/tiber) and helping to develop the Autonity project.
- Helping find bugs in Autonity software.
- Operating node infrastructure.
- Operating as a validator.
- Stake delegation.
- Developing and deploying dApp use cases.

## Piccadilly Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Piccadilly (Tiber) Testnet`|
|New RPC URL|Please select one from [Chainlist](https://chainlist.org/?testnets=true&search=piccadilly)|
|ChainID |`65100004`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://piccadilly.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

| Name                               | Piccadilly                    |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65100004`                    |
| `gasLimit`                         | `20000000`(20M)               |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `30` (increases to `100` after genesis) |
| `config.autonity.delegationRate`   | `1000` (10%)                  |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 [gton](/concepts/protocol-assets/auton/#unit-measures-of-auton))        |
| `config.autonity.operator`         | `0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397` |
| `config.autonity.treasury`         | `0xF74c34Fed10cD9518293634C6f7C12638a808Ad5` |
| `config.autonity.validators`       |  See [`PiccadillyGenesisValidators`](https://github.com/autonity/autonity/blob/release/v1.0.2-alpha/params/gen_piccadilly_config.go#L227-L505) in the AGC configuration code for details.  |
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

- Autonity Go Client (AGC) Release: [v1.0.2-alpha](https://github.com/autonity/autonity/releases/tag/v1.0.2-alpha). The docker image release is: [`ghcr.io/autonity/autonity:v1.0.2-alpha`](https://github.com/autonity/autonity/pkgs/container/autonity)

- Autonity Oracle Server (AOS) Release: [v0.2.3](https://github.com/autonity/autonity-oracle/releases/tag/v0.2.3). The docker image release is: [`ghcr.io/autonity/autonity-oracle:v0.2.3`](https://github.com/orgs/autonity/packages/container/package/autonity-oracle)

## Faucet

- There is currently no faucet for [auton](/concepts/protocol-assets/auton) or [newton](/concepts/protocol-assets/newton) on Piccadilly. Network participants access testnet auton and newton by participating in the [Piccadilly Tiber Challenge](https://autonity.org/tiber).

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?testnets=true&search=piccadilly). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.


## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://piccadilly.autonity.org/](https://piccadilly.autonity.org/)
