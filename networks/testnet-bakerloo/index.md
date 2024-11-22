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
|New RPC URL|Please select one from [Chainlist](https://chainlist.org/?testnets=true&search=bakerloo)|
|ChainID |`65010003`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://bakerloo.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

The network's genesis configuration is:

| Name                               | Bakerloo                      |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65010003`                    |
| `gasLimit`                         | `20000000` (20M)              |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `50`                          |
| `config.autonity.delegationRate`   | `1000` (10%)                  |                |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 GWei)        |
| `config.autonity.operator`         | `0x293039dDC627B1dF9562380c0E5377848F94325A` |
| `config.autonity.treasury`         | `0x7f1B212dcDc119a395Ec2B245ce86e9eE551043E` |
| `config.autonity.validators`       |  See [`Validators`](https://github.com/autonity/autonity/blob/release/v0.14.0/params/config.go#L206) object in the AGC `BakerlooChainConfig` for details.  |
| `config.oracle.symbols`       | `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "ATN-NTN"]`        |
| `config.oracle.votePeriod`       | `30` (30 blocks)       |


## Bootnodes

The network bootnode addresses are:

| enode |
| :-- |
| `enode://63ba7876187203163d093c63e8bbeaf9c4c385ad9b37dc64aa9407e90b98d6678cf1caa9d810829730986966fd0e056c49bdac10eb3389756e3d457580ee0687@34.142.78.108:30303` |
| `enode://ec317b7ae32d55620f37edc9c8af649e6e649f806ba8c3e53ab5407537b13c7a0b00719bb5518d9518978631765fb21a1620f4c32d97a5be0ed9672d8ff4d1a0@35.189.83.7:30303` |


## Release

The current iteration of the Bakerloo network is built using:

- Autonity Go Client (AGC) Release: [v0.14.0](https://github.com/autonity/autonity/releases/tag/v0.14.0). The docker image release is: `ghcr.io/autonity/autonity:latest`

- Autonity Oracle Server (AOS) Release: [v0.1.9](https://github.com/autonity/autonity-oracle/releases/tag/v0.1.9). The docker image release is: `ghcr.io/autonity/autonity-oracle-bakerloo:latest`

## Faucet

- Faucet for [auton](/concepts/protocol-assets/auton) test funds: [https://faucet.autonity.org/](https://faucet.autonity.org/)
- There is currently no faucet for [newton](/concepts/protocol-assets/newton), as newton tokens will be made available to network participants in later phases of the testnet.

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?testnets=true&search=piccadilly. For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://bakerloo.autonity.org/](https://bakerloo.autonity.org/)
