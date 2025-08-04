---
title: "Oracle Contract Interface"
description: >
  Autonity Oracle Contract functions
---

Interface for interacting with Autonity Oracle Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Oracle Contract's generated ABI and the `aut` tool's `contract` command to call the Oracle Contract address `0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Oracle.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Oracle.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::


## getConfig

Returns the current Oracle Contract configuration.

### Parameters

None.
    
### Response

Returns a `config` object consisting of:

| Field | Datatype | Description |
|:-- |:-- |:-- |
| `votePeriod` | `uint` | Duration of the voting period |
| `outlierDetectionThreshold` | `int256` | Threshold for outlier detection |
| `outlierSlashingThreshold` | `int256` | Threshold for slashing outliers |
| `baseSlashingRate` | `uint256` | Base rate for slashing |
| `nonRevealThreshold` | `uint256` | Threshold for missed reveals | 
| `revealResetInterval` | `uint256` | Number of rounds after which the missed reveal counter is reset |
| `slashingRateCap` | `uint256` | Maximum slashing rate for oracle penalties |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi abi/Oracle.abi --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getConfig
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi abi/Oracle.abi --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getConfig
```
```console
{"autonity": "0xBd770416a3345F91E4B34576cb804a576fa48EB1", "operator": "0x2f3BcE2d6C2602de594d9a6662f0b93416cfB4d7", "votePeriod": 30, "outlierDetectionThreshold": 10, "outlierSlashingThreshold": 225, "baseSlashingRate": 10, "nonRevealThreshold": 3, "revealResetInterval": 10, "slashingRateCap": 1000}
```
:::


## getDecimals

Returns the decimal places to be used with price reports.

The number of decimal places is set as a constant to the integer value `18`.

::: {.callout-tip title="Conversion to decimal places" collapse="true"}
Prices for currency symbols in oracle server price data reports are aggregated off-chain and computed to a price precision determined by the [Oracle protocol](/concepts/oracle-network/#oracle-protocol) decimal places configuration (i.e. `18`). However, the price reports are submitted on-chain for price aggregation in the Oracle Contract as integer values. When requesting the price of a symbol on-chain from the Oracle Contract, therefore, the price point is returned as an integer value without precision.

A data consumer can convert the on-chain aggregation value to decimal precision for their use case by applying the number of decimal places as the precision.

For example:

`aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D latestRoundData "SEK-USD"
{"round": 22936, "price": 90540157841600943, "timestamp": 1734622607, "success": true}`

The  median price of `90540157841600943` converts to `0.090540157841600943`.
:::

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `ORACLE_DECIMALS` | `uint8` | the decimal precision multiplier applied to currency pair symbol price reports before aggregation. Set as a constant in the Oracle Contract to `18` |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getDecimals
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getDecimals
```
```console
10000000
```
:::


## getLastRoundBlock

Returns the block height at which the last completed oracle voting round ended.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `lastRoundBlock` | `uint256` | the block number at which the oracle voting round completed |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getLastRoundBlock
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getLastRoundBlock
```
```console
982200
```
:::


## getNewVotePeriod

Returns the new vote period that is going to be applied at the end of the current voting round.

To return the current vote period see [`getVotePeriod()`](/reference/api/oracle/#getvoteperiod). 

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `newVotePeriod` | `uint256` | integer value expressing the duration of an oracle round, measured in blocks |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getNewVotePeriod
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getNewVotePeriod
```
```console
30
```
:::


## getNewVoters

Returns the new voters in the committee.

The response is returned as a list of oracle identifier addresses, sorted in descending dictionary order.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `newVoters` | `address` array | a comma-separated list of oracle addresses for new participants in the oracle voting process |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getNewVoters
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}

aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getNewVoters
```
```console
["0x037b9420CA2983dc3EF87dF1C4994A2BDF6FF8BF", "0x0804A922ba6B7c0965928a8d9A10ecdeA0b3c41A",...]

```
:::


## getNonRevealThreshold

Returns the tolerance for the missed reveal count before the voter gets punished.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `nonRevealThreshold` | `uint256` | the `nonRevealThreshold` from the Oracle Contract config |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getNonRevealThreshold
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getNonRevealThreshold
```
```console
3
```
:::


## getReports

Returns the latest report from an oracle voter for a symbol.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_symbol` | `string` | the target symbol |
| `_voter` | `address` | the oracle address of the target voter, an oracle server in the [oracle network](/concepts/oracle-network/). |
    
### Response

Returns the latest report of that voter for that symbol.
        
### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getReports _symbol _voter
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getReports JPY-USD 0xEDE0Da16Cb4Bf5dd14907d4CdF6cfA1bEbDD5943
```
```console
{"price": 6765159877488300, "confidence": 50}
```
:::


## getRewardPeriodPerformance

Returns the epoch performance score for a voter at the block height of the call.

::: {.callout-note title="Note" collapse="false"}

Confidence scores for the price reports submitted by a validator in an epoch are summed to create the validator's [epoch performance score](/concepts/oafd/#epoch-performance-score). The performance score is used as a weighting factor in the OAFD [Oracle reward calculation](/concepts/oafd/#oracle-reward-calculation) end of epoch.

:::
 

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_voter` | `address` | the oracle address of the target voter, an oracle server in the [oracle network](/concepts/oracle-network/). |

### Response

| Field | Datatype | Description |
| --| --| --|
| `rewardPeriodPerformance ` | `uint256` | integer value expressing the reward performance of a voter in the current epoch |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRewardPeriodPerformance _voter
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRewardPeriodPerformance 0xEDE0Da16Cb4Bf5dd14907d4CdF6cfA1bEbDD5943
```
```console
16200
```
:::


## getRound

Returns the index number of the current oracle contract voting round.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `round` | `uint256` | the number of the current oracle voting round |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRound
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRound
```
```console
32758
```
:::


## getRoundData

Returns the median price data for a [currency pair](/glossary/#currency-pair) symbol at a given oracle voting round.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_round` | `uint256` | the oracle voting round index number for which the price should be returned |
| `_symbol` | `string` | the currency pair symbol for which the current price should be returned |

### Response

| Field | Datatype | Description |
| --| --| --|
| `round` | `uint256` | the index number of the oracle voting round in which the price was generated |
| `_p.price` | `uint256` | the median price for the requested currency pair symbol |
| `_p.timestamp` | `string` | the timestamp of the block height at which the returned price was calculated; the  timestamp is in Unix Timestamp format |
| `_p.sucess` | `bool` | status value indicating if the median price was calculated successfully or not in the requested `round`; value of `False` (FAILURE) or `True` (SUCCESS). If a price was not successfully calculated in the requested `round`, then the price returned is the most recently generated price for the requested symbol and was generated at the returned block timestamp.|

::: {.callout-note title="Note" collapse="false"}
Note that median price calculation happens when the last block of a round is finalised. If `getRoundData()` is called with the current `round` number, then it will return zero because the price aggregation hasn't been executed yet.
:::

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRoundData _round _symbol
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRoundData 32758 JPY-USD
```
```console
{"round": 32758, "price": 6767376852175925, "timestamp": 1754304838, "success": true}
```
:::


## getSymbols

Returns the [currency pair](/glossary/#currency-pair) symbols for which the oracle generates price reports.

Note that if the symbols supported by the oracle are changed that there is a delay of 2 voting rounds before prices are reported for the new symbols. This is because if symbols are updated at round number `r` then:

- oracles submit price data commits for the new symbols the following round in `r + 1`
- prices for the new symbols are computed by the oracle network in `r + 2` when the commits are revealed and prices voted on by the oracle voters.

If the `getSymbols` call is made at `r + 1`, then it will return the updated symbols for which prices will be generated at `r + 2`.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `symbols` | `string` array | a comma-separated list of the currency pair symbols for which price reports are generated |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getSymbols
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getSymbols
```
```console
["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD"]
```
:::


## getSymbolUpdatedRound

Returns the oracle voting round number in which the oracle [currency pair](/glossary/#currency-pair) symbols were last updated.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `symbolUpdatedRound` | `int256` | the voting round index number in which the currency pair symbols were last updated |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getSymbolUpdatedRound
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getSymbolUpdatedRound
```
```console
1676
```
:::


## getVotePeriod

Returns the current vote period from Oracle Contract config.

Vote period is the oracle contract setting for the interval at which the oracle network initiates a new oracle round for submitting, voting, and aggregating data points for oracle price reports. The interval is measured in blocks. Vote period is set at network genesis, see Reference, Genesis,[`oracle`](/reference/genesis/#configautonityoracle-object) config. 

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `votePeriod` | `uint256` | integer value expressing the duration of an oracle round, measured in blocks |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVotePeriod
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVotePeriod
```
```console
30
```
:::


## getVoterInfo

Returns information about the voting state of a validator's oracle at the block height of the call.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_voter` | `address` | the oracle address of the target voter (i.e. of a validator node's connected oracle server in the [oracle network](/concepts/oracle-network/). |
    
### Response

Returns a `voterInfo` object consisting of:

| Field | Datatype | Description |
|:-- |:-- |:-- |
| `round` | `uint256` | The last round the voter participated in |
| `commit` | `uint256` | The commit hash of the voter's last report |
| `performance` | `uint256` | The epoch performance score of the voter |
| `nonRevealCount` | `uint256` | Number of commits that were not revealed
| `isVoter` | `bool` | Indicates if the address is a registered voter |
| `reportAvailable` | `bool` | Indicates if the last report is available for the voter |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoterInfo 0xEDE0Da16Cb4Bf5dd14907d4CdF6cfA1bEbDD5943 _voter
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoterInfo 0xEDE0Da16Cb4Bf5dd14907d4CdF6cfA1bEbDD5943
```
```console
{"round": 32766, "commit": 37778611136603675814142104625773441195535314465281403930869093834500228128468, "performance": 0, "nonRevealCount": 0, "isVoter": true, "reportAvailable": true}
```
:::

## getVoters

Returns the list of participants in the oracle voting process, i.e. all voters in the current consensus committee.

The response is returned as a list of oracle identifier addresses, sorted in descending dictionary order.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `address` | `address` array | a comma-separated list of oracle addresses for current participants in the oracle voting process |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoters
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoters
```
```console   
["0x00bb781AE6bAf8B8a75eb52A7D07ba8f7684AD11", "0x0CE8253044ad3b0714D8d17DE32CBA7eAd520DE8", "0x0F667a719EAEc488c32C9460284BAb791B6D19c1", "0x134d4d57E2e35Bb0c86090844efDE6B59613d2a0", "0x1a78b8B9169cE5557e7778e72f8719432C942749", "0x3726a000d594038E69cBe907a4e58C5678BB2B5b", "0x39d08926b0FfC3BeBBc16206C3f9cbb21A02cd25", "0x39E0620D2184c087e6287c0d9FE3C1476C59cce1", "0x4C39f10efC7B3935b05AdE8aa5fcB93d344d58F0", "0x4CF037EA7451B715130631489bd1436dca180644", "0x516cFCd57aeBC0c34C886D0864bD9529a0af1776", "0x577Ae106D48D58A2d57cf5a3d6cbc12C906AdEe8", "0x5Befa3cD56Aaba59d7f9071EA92b0DA81E29dA1a", "0x5fCcE08030B80fcC3420D6f8f8431F627CcF603C", "0x66FB67bCF4021eDA62dcA32019B4A0625CCa2533", "0x70651F5b85fF8D8a4404b5f2ee3Bc0fc530E5097", "0x851326AA92FFe669F429452495672a390Bc2595F", "0x85B473CB48a465c94Af434861F116f54b6D5A0b0", "0x91462B6DfF1Cf49BDE2B1C7Df469612DceA165a8", "0x9eFA61be707a233c2BfEFDAF2D6b7eF4740fa105", "0xb01808820d243879675e67B46212Fc79A7E92405", "0xBD91F83C107AE4541207AA58837E75839946B89B", "0xc375A2eeB1914F660B23af6d408d77AE5f43ED8F", "0xC50144CC8b0F08AbFb1e8a26D3ec7350DE071c63", "0xc92e18c47eCCe34cEe55f86647f40b2824DEc64E", "0xc9f7D364CC131b2354342BD19507F217f9b57E61", "0xCB5a76Ed937511Af3B8F4814020A97eE142CA720", "0xD0caCb0C14862F8c57E3C2CfBa5A3E9a7e19B76a", "0xd5CaAa802B26C05930aff046B4Cb4275891729fb", "0xd85c0183679746C3A1AE468Ec99C4d2aCFbBA4c2", "0xDA3dd488e6cD991ae570b2A34e78f81CEBea9731", "0xDD9453561167727D347F961f0B27f5bD71C9C757", "0xdf29C6439512De8302E43FD1Ac800745d8CE079a", "0xDfe533635cd6aD40D0B996f344c667bFA0371183", "0xE1d55Ce8f12E8c2767f062b9152Ab695d6726d26", "0xe632C0B09F4894B5096AE0B9E61D18BD8f60f9c6", "0xEDE0Da16Cb4Bf5dd14907d4CdF6cfA1bEbDD5943", "0xefd5eA8c1bDC577E7e3F8172f52B42dC860a16E5", "0xf3718A3047224182579f4eBd3008E6578bDA03FA", "0xf6F4B060E03FA323d65d6EfBA5A613F9330E8096"]
```
:::


## getVoterTreasuries

Returns the validator `treasury` address for an oracle server address.

::: {.callout-note title="Note" collapse="false"}

The validator treasury account address is used by a validator operator to submit transactions for validator lifecycle management transactions and to receive its share of staking rewards. See Concepts [treasury account](/concepts/validator/#treasury-account).

:::

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_oracleAddress` | `address` | the oracle address of an oracle server in the [oracle network](/concepts/oracle-network/). |

### Response

| Field | Datatype | Description |
| --| --| --|
| `voterTreasuries` | `address` | the `treasury` account address of the validator the oracle server is connected to |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoterTreasuries _oracleAddress
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoterTreasuries 0xEDE0Da16Cb4Bf5dd14907d4CdF6cfA1bEbDD5943
```
```console
"0x64cfD13fe992ce03516A104274432Ef6E925bBc1"
```
:::


## getVoterValidators

Returns the validator address for an oracle server address.

::: {.callout-note title="Note" collapse="false"}

The validator node address and the oracle server address provide the unique cryptographic identity of an [AGC](/concepts/client/) [validator](/concepts/validator/) node and its connected [AOS](/concepts/oracle-server/) [oracle server](/concepts/oracle-network/) in an [Autonity network](/glossary/#autonity-network). See Concepts [validator identifier](/concepts/validator/#validator-identifier) and [oracle identifier](/concepts/oracle-network/#oracle-identifier).

:::

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_oracleAddress` | `address` | the oracle address of an oracle server in the [oracle network](/concepts/oracle-network/). |

### Response

| Field | Datatype | Description |
| --| --| --|
| `address` | `address` | the node address of the validator the oracle server is connected to |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoterValidators _oracleAddress
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getVoterValidators 0xEDE0Da16Cb4Bf5dd14907d4CdF6cfA1bEbDD5943
```
```console
"0xaEDf3d78e012F81E352295b25730bdAf0868AA9A"
```
:::


## latestRoundData

Returns the latest available median price data for a [currency pair](/glossary/#currency-pair) symbol.  The price returned is the one generated in the last successfully completed oracle voting round.

If the last oracle voting round failed to successfully compute a new median price, then it will return the most recent median price for the requested symbol.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_symbol` | `string` | the currency pair symbol for which the current oracle price is requested |

### Response

| Field | Datatype | Description |
| --| --| --|
| `round-1` | `uint256` | the index number of the oracle voting round in which the price was generated. This is always `1` less than the number of the oracle's voting round at the time of the call |
| `_p.price` | `uint256` | the latest median price for the requested currency pair symbol |
| `_p.timestamp` | `string` | the timestamp of the block height at which the returned price was calculated; the  timestamp is in Unix Timestamp format |
| `_p.status` | `uint` | status value indicating if the median price was calculated successfully or not in `round-1`, represented by a value of `0` (SUCCESS) or `1` (FAILURE).  If a price was not successfully calculated, then the price returned is the most recently generated price for the requested symbol and was generated at the returned block timestamp.|

::: {.callout-note title="Note" collapse="false"}
Unix time represents time as an integer value recording the number of seconds since 1 January 1970 00:00:00 UTC.

This can easily be converted to a human-readable form, for example:

- programmatically, using the Python `datetime` library `fromtimestamp()` function
- on the web, using online converters like https://www.unixtimestamp.com/index.php <i class='fas fa-external-link-alt'></i>.
:::

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D latestRoundData _symbol
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D latestRoundData JPY-USD
```
```console
{"round": 32779, "price": 6769938952206428, "timestamp": 1754305468, "success": true}
```
:::
