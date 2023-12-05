---
title: "Piccadilly Testnet"
linkTitle: "Piccadilly Testnet"
weight: 2
description: >
  The _bleeding-edge_ public Testnet running the latest deployable version of the Autonity protocol
---

Piccadilly is a public Testnet running the latest deployable version of the Autonity protocol. It is the testing environment used in the pre-MainNet [Piccadilly Circus Games Competition (PCGC) <i class='fas fa-external-link-alt'></i>](https://game.autonity.org) and may undergo re-genesis with the latest protocol implementation at the end of a game round. 

Piccadilly is for participants interested in:

- Taking part in the [Piccadilly Circus Games Competition <i class='fas fa-external-link-alt'></i>](https://game.autonity.org) and helping to develop the Autonity project.
- Helping find bugs in Autonity (See the game's [Bug Bounty<i class='fas fa-external-link-alt'></i>](https://game.autonity.org/#tasks--points)).
- Operating node infrastructure.
- Operating as a validator.
- Stake delegation.
- Developing and deploying dApp use cases.

## Piccadilly Testnet details

|**Field**|**Input**|
|------|----------|
|Network Name|`Autonity Piccadilly (Barada) Testnet`|
|New RPC URL|`https://rpc1.piccadilly.autonity.org/`|
|ChainID |`65100001`|
|Symbol|`ATN`|
|Block Explorer URL (optional)|`https://piccadilly.autonity.org/`|

(The above information can be used to connect an existing client such as [MetaMask <i class='fas fa-external-link-alt'></i>](https://metamask.zendesk.com/hc/en-us/articles/360043227612-How-to-add-a-custom-network-RPC))

## Genesis configuration

| Name                               | Piccadilly                    |
| ---------------------------------- | ----------------------------- |
| `chainId`                          | `65100001`                    |
| `gasLimit`                         | `30000000`(30M)               |
| `config.autonity.blockPeriod`      | `1` second                    |
| `config.autonity.epochPeriod`      | `1800`(30 min)                |
| `config.autonity.unbondingPeriod`  | `21600`(6 hours)              |
| `config.autonity.maxCommitteeSize` | `100`                         |
| `config.autonity.delegationRate`   | `1000` (10%)                  |
| `config.autonity.treasuryFee`      | `10000000000000000` (1%)      |
| `config.autonity.minBaseFee`       | `500000000` (0.5 GWei)        |
| `config.autonity.operator`         | `0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397` |
| `config.autonity.treasury`         | `0xF74c34Fed10cD9518293634C6f7C12638a808Ad5` |
| `config.autonity.validators`       | `enode://d4dc137f987e17155a69b31e566494c16edafd228912483cc519a48ce85864781faccc38141cc0eb1df8cdb28b9b3ccd10e1c298bac78ac43bbe5804021c1152@34.142.71.5:30303` |
|  | `enode://74a4f767ad2f3f607a2db06732b44e6c61a68cae1959b331c18aea6256aae16bded31ba40dd85dcc4d719baaeb29f918726d19fa51b5d8174b27da0d7593e19b@34.142.33.89:30303` |
|  | `enode://0ddc30943837f9416f563063ed5d409aca37780b8b8f939ef9f4b7901b9eb94c09d7ba2af27f70b33d76e74403d00021c13ebc4943ad46bc1e5051689cd862b8@35.234.131.29:30303` |
|  | `enode://9435658d26e5daf30261648504560f6375b24cdf0e4403613d44ebc4020489cc67ac82ababe7928d63d9f113c67b946845d18db935abe3d241e665114fc75e94@35.177.73.222:30303` |
|  | `enode://fe2c621f2b660725a3d529b3eefd780e90bb86e9eb4b7136c0b00a7365260a478b9b8941f1a65c6d4d77bff1b2e22eb6d781f5cc86401d60b373c6d4155c189a@3.10.195.56:30304` |
|  | `enode://6ab1e6bbf5897e1a24ccf8d8718615ec972ffd54d99c3e46f4517d5602e8bf7110e2e5e2c2e584795e45e2e842172de044b4df165a7082133c6697b632da8282@18.168.88.205:30305` |
| `config.oracle.symbols`       | `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD"]`        |
| `config.oracle.votePeriod`       | `30` (30 blocks)       |

Note:

- The client default setting for the `--miner.gaslimit` flag is set to `30000000` (30M), the EIP-1559 block gas limit of 30M per Ethereum upstream.


## Bootnodes

The network bootnode addresses are:

- "enode://3c7f26eb85a7fc37d5ea64c07598a28dd58f507477a88b2144179a4a162c6cba9407389d39c76386126f0604dd53141680d8075b6d210a22cc38c3a8dd877711@35.246.7.21:30303"
- "enode://08e2ed9ca80772ce32e3b56fba3469e33a034a66780e4852586e38db657658fdc610cfb7345543a01277eb53af458ef7cac0b66570ac1982011f24d3832d782c@34.100.165.124:30303"
- "enode://d820e4d53f1e47443c23f2db28b251ca8b8dc207a1b0a0e36ae1bbeb63d0cea4f00dabb61e5daf27468f022adc8780dfd181c57ce0db16a9668dd72e18ecac6b@159.203.156.236:30303"

## Release

- The current iteration of the Piccadilly network is built using this Autonity Release: [v0.12.2 <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity/releases/tag/v0.12.2)

- The nodes are running this docker image release: `ghcr.io/autonity/autonity:latest`

## Faucet

- There is currently no faucet for [auton](/concepts/protocol-assets/auton) or [newton](/concepts/protocol-assets/newton) on Piccadilly. Network participants access testnet auton and newton by participating in the [Piccadilly Circus Games Competition (PCGC) <i class='fas fa-external-link-alt'></i>](https://game.autonity.org).

## Public endpoints

Default rate limit on calls to `ws` and `http` public endpoints combined  is 250 requests per second per IP.

- RPC: https://rpc1.piccadilly.autonity.org
- WebSocket: wss://rpc1.piccadilly.autonity.org/ws

## Block explorer

- BlockScout explorer for searching and viewing ledger data: [https://piccadilly.autonity.org/ <i class='fas fa-external-link-alt'></i>](https://piccadilly.autonity.org/)
