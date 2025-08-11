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

::: {.callout-tip title="Mainnet is on the way!" collapse="false"}

Watch this space, coming soon! 🚀

:::


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
| `config.autonity.validators`       |  See `MainnetValidators` in the AGC [`Mainnet Config`](https://github.com/autonity/autonity/blob/release/v1.1.2/params/mainnet_config.go#L158)) for details.  |
| `config.oracle.symbols`            | `['AUD-USD','CAD-USD','EUR-USD','GBP-USD','JPY-USD','SEK-USD']`        |
| `config.oracle.votePeriod`         | `600` (600  blocks)          |


## Bootnodes

The network bootnode addresses are:

| enode | region |
| :-- | :--      |
| `enode://bba73a4252e64fa23e11bcfc9c0c03e912fc8c17374a637bbc9cb42351a22624f463b0e774a0ab06141690d4499f686e2446fc96cb76fd7c842a191bce047f8a@34.147.142.153:30303` | europe-west2 |
| `enode://87dd0697db1a6a434cdc1813b45396a8aa2003ca65a9cbb7d8fc82e5fb608b561af012a91aef827979ffa973ddb0df7c7dc43e0778729cd067d91554b1138413@35.200.148.179:30303` | asia-south1b|
| `enode://d295a022386c51f52b7630586304eac18fc2a299276fcea31771ec0c20bf967e772d90467f18d6b7fe3e7dfbcfd896db2192a3e9556eecbfdae43eab6c097ee0@34.102.61.248:30303` | us-west2 |


## Release

Mainnet is built using:

- Autonity Go Client (AGC) Release: [v1.1.2](https://github.com/autonity/autonity/releases/tag/v1.1.2). The docker image release is: [`ghcr.io/autonity/autonity:v1.1.2`](https://github.com/autonity/autonity/pkgs/container/autonity/480778709?tag=v1.1.2).

- Autonity Oracle Server (AOS) Release: [v0.2.6](https://github.com/autonity/autonity-oracle/releases/tag/v0.2.6). The docker image release is: [`ghcr.io/autonity/autonity-oracle:v0.2.6`](https://github.com/orgs/autonity/packages/container/autonity-oracle/483926882?tag=v0.2.6).

## ATN funding

[Auton (ATN)](/concepts/protocol-assets/auton) is available on-chain from the Decentralized Auton Exchange (DAX) ATN-USDC market.

DAX is a Uniswap V2 clone AMM. Bridge USDC to Autonity from Polygon Mainnet using the VIA Labs bridge and trade in the DAX to purchase ATN.

<!-- -->
::: {.callout-tip title="Mainnet is on the way!" collapse="false"}
Watch this space, coming soon! 🚀

Mainnet launch is 12th August!

:::

To bridge see [Use the Bridge](/networks/mainnet/bridge.md)

To trade see [Use the DAX](/networks/mainnet/dax.md)
<!-- -->

## Public endpoints

Please select one from [Chainlist](https://chainlist.org/?search=autonity). For questions related to rate limits or other usage questions, please speak to the owner of the RPC endpoint directly.

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://autonityscan.org](https://autonityscan.org).
