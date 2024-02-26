---
title: "Piccadilly Testnet"
description: >
  The _bleeding-edge_ public Testnet running the latest deployable version of the Autonity protocol
---

Piccadilly is a public Testnet running the latest deployable version of the Autonity protocol. It is the testing environment used in the pre-MainNet [Piccadilly Circus Games Competition (PCGC)](https://game.autonity.org) and may undergo re-genesis with the latest protocol implementation at the end of a game round. 

Piccadilly is for participants interested in:

- Taking part in the [Piccadilly Circus Games Competition](https://game.autonity.org) and helping to develop the Autonity project.
- Helping find bugs in Autonity (See the game's [Bug Bounty](https://game.autonity.org/#tasks--points)).
- Operating node infrastructure.
- Operating as a validator.
- Stake delegation.
- Developing and deploying dApp use cases.

## Piccadilly Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Piccadilly (Barada) Testnet`|
|New RPC URL|`https://rpc1.piccadilly.autonity.org/`|
|ChainID |`65100002`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://piccadilly.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

| Name                               | Piccadilly                    |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65100002`                    |
| `gasLimit`                         | `30000000`(30M)               |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `9` (increases to `100` after genesis, then oscillates in range `34` - `100`) |
| `config.autonity.delegationRate`   | `1000` (10%)                  |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 GWei)        |
| `config.autonity.operator`         | `0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397` |
| `config.autonity.treasury`         | `0xF74c34Fed10cD9518293634C6f7C12638a808Ad5` |
| `config.autonity.validators`       | `enode://772248dfe1af5f77e0efc0510e83364bfad55cbd6d3e276f3bd0b4ddec6472aa98645655fd80bbf049ba3da18d219ab30a68fcb98da8e06dd42863dd0356cc95@35.242.168.170:30303` |
|  | `enode:/22f696529d7874ca66d177c2c272600c3d1f2f7111d02140c462a8cbc789f5f8968c2ce57a5aac1373ef17bf3fc67d155b54691d1413516459824067e13750a4@34.92.27.46:30303` |
|  | `enode://24b2655b0434d1af4e2329cababf38963cab8a154e0b8c9748e75c85d10d7dab5032af7a41f3ec06dd1a7d3d306f1edee5dc46dad7a2858b80ebb56e5fa24925@34.233.111.193:30303` |
|  | `enode://a20e27effd92dc11e7340e96a6f2908124ea363e6b68af34cad2a46a9ffdc6f5d4f516acec7f98949cc25955269f7842dc513444902c21239155de7e70b86a87@65.109.160.27:30303` |
|  | `enode://a2ea938a325381c7b163e7a3ca1a63fcfd927a81cadcf86551ad29f2f3ed05ef06f0b3a5d10ca932d0b85b3cf9a7c7956bf5398a2c9322f941817c92f9f62105@37.252.184.235:30303` |
|  | `enode://46f4abe3aeca863ce3a1b4a2b2fce3112476ca75a20039ef4bad78e1a2171ae36404d74b08a0c5a8720e2548d296d37e0b92062c096801b3f6d2d86e4e9da2f2@46.4.32.57:30303` |
|  | `enode://84c9a23b75bcd0252e0b361f6962a9f360d38f4fe5206cfb2d907074de877edbb1b810fd9cecf2fa64aa6ec4f7816a7f238650d489eaa82d68e8660769c6763d@51.91.220.174:30303` |
|  | `enode://11dd1e9d4a68fb07e4cbd60d225c6ffea45852ac3d4e17df3a086a7d27ee05698922e7474db4dbcef14a11e3dd44bf66a52160610bd43a890fdc1bc8a2f51393@65.109.69.239:30303` |
|  | `enode://700ae526623b87a748acf278cee299d970ccde4e4d6e7aa7685f4a550500b6e53b84892e37c2c10516673f45253fcb824d8e1836ee91a92a16b66b85b8000642@93.115.25.90:30303` |
| `config.oracle.symbols`       | `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "ATN-NTN"]`        |
| `config.oracle.votePeriod`       | `30` (30 blocks)       |


## Bootnodes

The network bootnode addresses are:

| enode |
| :--:  |
| `enode://48a10db920251436ee1d7989db6cbab734157d5bd3ec9d534021e4903fdab51407ba4fd936bd6af1d188e3f464374c437accefa40f0312eac9bc9ae6fc0a2782@34.105.239.129:30303` |
| `enode://9379179c8c0f7fec28dd3cca64da5d85f843e3b05ba24f6ae4f8d1bb688b4581f92c10e84e166328499987cf2da18668446dd7353724cf691ad2a931a0cbd88d@34.93.237.13:30303` |
| `enode://c7e8619c09c85c47a2bbda720ecec449ab1207574cc60d8ec451b109b407d7542cabc2683eedcf326009532e3aea2b748256bac1d50bf877c73eea4d633e8913@54.241.251.216:30303` |

## Release

- The current iteration of the Piccadilly network is built using this Autonity Release: [v0.13.0](https://github.com/autonity/autonity/releases/tag/v0.13.0)

- The docker image release is: `ghcr.io/autonity/autonity:latest`

## Faucet

- There is currently no faucet for [auton](/concepts/protocol-assets/auton) or [newton](/concepts/protocol-assets/newton) on Piccadilly. Network participants access testnet auton and newton by participating in the [Piccadilly Circus Games Competition (PCGC)](https://game.autonity.org).

## Public endpoints

Default rate limit on calls to `wss` and `https` public endpoints combined  is 250 requests per second per IP.

- RPC: [https://rpc1.piccadilly.autonity.org](https://rpc1.piccadilly.autonity.org)
- WebSocket: [wss://rpc1.piccadilly.autonity.org/ws](wss://rpc1.piccadilly.autonity.org/ws)

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://piccadilly.autonity.org/](https://piccadilly.autonity.org/)
