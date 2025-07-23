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

::: {.callout-note title="Note" collapse="false"}
The Oracle Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

## getDecimals

Returns the decimal places to be used with price reports.

The number of decimal places is set as a constant to the integer value `18`.

::: {.callout-note title="Conversion to decimal places" collapse="false"}
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
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getPrecision
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getPrecision
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
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
TO DO
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
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}

TO DO

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

::: {.callout-note title="Note" collapse="false"}
The Oracle Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


## getRewardPeriodPerformance

Returns the voting performance for a voter in the current reward (epoch) period.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `rewardPeriodPerformance ` | `uint256` | integer value expressing the reward performance of a voter in the current epoch |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRewardPeriodPerformance
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRewardPeriodPerformance
10
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
1809
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
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D getRoundData 1809 "SEK-USD"
{"round": 1809, "price": 899334, "timestamp": 1694668219, "success": True}
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
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
TO DO
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
| `voters` | `address` array | a comma-separated list of oracle addresses for participants in the oracle voting process |

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
["0x037b9420CA2983dc3EF87dF1C4994A2BDF6FF8BF", "0x0804A922ba6B7c0965928a8d9A10ecdeA0b3c41A",...]

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
30
```
:::


## getVoterInfo

Returns information about an oracle voter, i.e. of a validator node's connected oracle server.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_voter` | `address` | the oracle address of the target voter, an oracle server in the [oracle network](/concepts/oracle-network/). |
    
### Response

Returns a `voterInfo` object consisting of:

| Field | Datatype | Description |
|:-- |:-- |:-- |
| `round` | `uint256` | The last round the voter participated in |
| `commit` | `uint256` | The commit hash of the voter's last report |
| `performance` | `uint256` | The performance score of the voter |
| `nonRevealCount` | `uint256` | Number of commits that were not revealed
| `isVoter` | `bool` | Indicates if the address is a registered voter |
| `reportAvailable` | `bool` | Indicates if the last report is available for the voter |
        
        
### Usage

::: {.callout-note title="Note" collapse="false"}
The Oracle Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


## getVoters

Returns the current voters in the committee.

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
["0xf8D8c4818Fd21B4be57a0ACD619fdD88ec7A858c", "0xd4d2874450a21f1Bf5E1C12260773d8716b526B8", ...]
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
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}

TO DO

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
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}

TO DO

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
aut contract call --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D latestRoundData "SEK-USD"
{"round": 47631, "price": 963459, "timestamp": 1688390007, "status": 0}
```
:::
