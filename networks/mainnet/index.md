---
title: "Autonity Mainnet"
description: >
 The live Autonity blockchain network for real-value transactions running the stable version of the Autonity Protocol
draft: false
---

Autonity Mainnet is the live Autonity blockchain network for transactions and decentralized application (dApp) operations using real value.

Mainnet is for participants interested in:

- The [Autonity Futures Protocol](https://afp.autonity.org/)
- Decentralized application (dApp) use cases
- Providing live validator and public RPC endpoint node infrastructure
- The Autonity community!


## Mainnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity (Nile) Mainnet`|
|New RPC URL|Please select one from [Chainlist](https://chainlist.org/?search=autonity)|
|ChainID |`65000000`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://autonityscan.org`|

::: {.callout-tip title="Adding Autonity as a custom network to your wallet" collapse="false"}

The above information can be used to add Autonity as a custom network to to an existing client such as [MetaMask](https://support.metamask.io/configure/networks/how-to-add-a-custom-network-rpc/).

:::

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
| `config.autonity.validators`       |  See `MainnetValidators` in the AGC [`Mainnet Config`](https://github.com/autonity/autonity/blob/release/v1.1.2/params/mainnet_config.go#L158)) for details.  |
| `config.oracle.symbols`            | `['AUD-USD','CAD-USD','EUR-USD','GBP-USD','JPY-USD','SEK-USD']`        |
| `config.oracle.votePeriod`         | `600` (600  blocks)          |


## Node discovery

Bootnode addresses must be specified explicitly for peer node discovery when joining and syncing with the network. For configuration details, see the Development guide page [Setting up custom networks](/developer/custom-networks/) and **How to identify and configure bootnodes for a custom network**.

## Release

Mainnet is built using:

- Autonity Go Client (AGC) Release: [v1.1.2](https://github.com/autonity/autonity/releases/tag/v1.1.2). The docker image release is: [`ghcr.io/autonity/autonity:v1.1.2`](https://github.com/autonity/autonity/pkgs/container/autonity/480778709?tag=v1.1.2).

- Autonity Oracle Server (AOS) Release: [v0.2.6](https://github.com/autonity/autonity-oracle/releases/tag/v0.2.6). The docker image release is: [`ghcr.io/autonity/autonity-oracle:v0.2.6`](https://github.com/orgs/autonity/packages/container/autonity-oracle/483926882?tag=v0.2.6).

## Bridge and ATN funding

There is a third-party operated Bridge available at [https://autonity.protousd.com/](https://autonity.protousd.com/) to transfer USDC from many popular networks to Autonity Mainnet. 

When doing so, an additional small amount of ATN 0.01 is provided for free to the recipient account, to support the account holder with covering gas fees for follow on transactions.

<!--
[Auton (ATN)](/concepts/protocol-assets/auton) is available on-chain from the Decentralized Auton Exchange (DAX) ATN-USDC market.

DAX is a Uniswap V2 clone AMM. Bridge USDC to Autonity from Polygon Mainnet using the VIA Labs bridge and trade in the DAX to purchase ATN.
-->

<!-- 
To bridge see [Use the Bridge](/networks/mainnet/bridge.md)

To trade see [Use the DAX](/networks/mainnet/dax.md)
-->

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?search=autonity). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://autonityscan.org](https://autonityscan.org).
