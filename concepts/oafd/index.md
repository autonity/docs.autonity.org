
---
title: "Oracle accountability and fault detection (OAFD)"
description: >
  Autonity's Oracle Accountability Fault Detection model -- reporting mechanism, temporal constraints, and economics for reporting offences and penalties for failures while participating in oracle voting rounds.

from: markdown+emoji

---

## Overview

This section describes the Autonity oracle accountability fault detection protocol. It covers the role of the validator [oracle network](/concepts/oracle-network/) in fetching and submitting price data to the Oracle protocol contract on-chain for computation of median price data on chain by the Autonity oracle protocol, and the incentives and disincentives applied to consensus committee validators to incentivise accurate and timely price reporting by validators and their oracle servers.

Autonity implements an _oracle accountability fault detection (OAFD)_ protocol for detecting if _consensus committee members_ are participating in the Autonity [_oracle protocol_](/concepts/oracle-network/#oracle-protocol) in a timely manner.

Autonity provides consensus-computed median price data for a designated set of [_currency pair_](/glossary/#currency-pair) (AKA _symbols_) as an L1 platform feature for primary and secondary consumer use cases:

- The primary consumer of the data is the [Auton Stabilisation Mechanism (ASM)](/concepts/asm/):

  - FX price data: for the _currency pairs_ used as the FX currency basket in the [ACU](/concepts/asm/#acu) index, and,
  - Autonity NTN and ATN [protocol assets](/concepts/protocol-assets/) price data: for ATN borrowing against NTN collateral by the [CDP](/concepts/asm/#stabilization) mechanism.

- The secondary consumer of the data is use cases deployed on the Autonity L1.

A median price for the supported _currency pair_ _symbols_ is computed according to the Autonity [_oracle protocol_](/concepts/oracle-network/#oracle-protocol).

The _oracle protocol_ functions by a continuous cycle of discrete oracle _voting rounds_ in which raw price data for each of the supported _symbols_ is collected from external off-chain data sources and submitted to an Oracle Protocol Contract on-chain by [_consensus committee_](/glossary/#consensus-committee) _members_. An _aggregated median price_ for each _currency pair_ _symbol_ is then [consensus](/glossary/#consensus) computed resulting in a price feed cyclically refreshed at _voting round_ intervals.

Provision of the raw price data is a validator responsibility and only validators that are _consensus committee members_ participate in the _oracle protocol_. Each registered validator node operates an [Autonity Oracle Server (AOS)](/concepts/oracle-server/) as adjunct software to the [Autonity main client (AGC)](/concepts/client/) software. Validator operators configure their [oracle server](/concepts/oracle-server/) to collect price data from external data sources for each _currency pair_ _symbol_ the _oracle protocol_ supports. This forms a logical validator [_oracle network_](/concepts/oracle-network/) responsible for reporting price data in cyclical _voting rounds_. 

For each _voting round_ the _validator node_ retrieves raw price data from its connected _oracle server_ and submits a _price report_ to the Oracle contract on-chain. The Oracle contract _aggregates_ the submitted _price reports_ to  compute an _aggregated median price_ for each supported _currency pair_ _symbol_. That _aggregated median price_ data is then emitted each [_voting round_](/concepts/oracle-network/#voting-rounds) as _round data_ on-chain. The duration of a _voting round_ is measured in [blocks](/glossary/#block) and set as the [_vote period_](/reference/genesis/#config.oracle-object) parameter of the Oracle protocol configuration. If a validator does not submit a price for a symbol in a _voting round_, then its _last submitted price_ for that _symbol_ will be used instead.

To ensure the maximum accuracy of price reporting _committee members_ should be submitting _current_ (i.e. "_fresh_" and not out-of-date "_stale_" prices) and participating in each oracle _voting round_. OAFD detects failures to do this as an _accountable fault_ and applies penalties to validators for  these _faults_. For example:

| Fault | Description | Scenario |
|:--|:--|:--|
| _voting_ fault | failing to submit a _price report_ i.e. '_vote_ in an oracle _voting round_ | "Missing a voting round". The cause could be Byzantine (e.g. intentional failure to send), a technical accident (e.g. network glitch, vote arrives too late for the round) |
| _inaccurate price reporting_ fault | submitting a _price report_ that is considered inaccurate | An "outlier" price report falling outside tolerance of the median price reported by the oracle network as a whole. The cause could be Byzantine (e.g. attempt to manipulate the price) or technical accident (e.g. poor quality data source results in submission of "_stale_" out of date price data). |
| _incomplete price reporting_ fault | submitting a _price report_ with prices for some but not all of the supported _symbols_ | The cause could be technical - e.g. the oracle could not source with confidence a price for a _symbol_ for that _voting round_ so opted not to submit one. In this scenario, the oracle's _last submitted price_ for the _symbol_ would be used by the _oracle protocol_ . |

The OAFD protocol is based upon the processing of _price reports_ submitted by committee members to the Oracle contract each _voting round_, and functions to maximise the _currency_ and _accuracy_ properties of the submitted price data:

- _currency_: the price data is the latest available for the _voting round_ and is not "stale" and out of date
- _accuracy_: data reported by individual oracles varies within an acceptable tolerance range. I.e. price "_outliers_" outside that range are accounted for and so not allowed to "skew" computation of the final _aggregated median price_.

OAFD focuses on the risk from _outliers_, which addresses both _currency_ and _accuracy_ properties. This makes intuitive sense: the more current a price is, the less likely it is to be an _outlier_. 

Oracles submit _price reports_ with a _confidence score_ for each _symbol_ price reported that represents the _reporting validator's_ level of trust in the accuracy of the price data it is submitting. If a _reporting validator_ fails to submit a price report for a _symbol_ or _symbols_ in a _voting round_, then its _last submitted price_ for the _symbol(s)_ will be taken as the validator's submission for that _voting round_.

::: {.callout-caution title="What if that _last submitted price_ was an _outlier_?" collapse="false"}

If a validator oracle does not submit a price for a _symbol_ in a _voting round_, then the oracle's _last submitted price_ for that _symbol_ will be carried forward and used as the submission for the current _round_. 

The only exception to this is if the _last submitted price_ was detected as an _outlier_. **In this case no votes for any _symbols_ from that oracle will be included in the [final price calculation](/concepts/oafd/#final-price-calculation) for the _voting round_.** I.e. the validator oracle’s entire _price report_ for the round is ignored. Accordingly, the validator is punished by the opportunity cost of earning no incentive rewards for that _round_.

Note that this also addresses the price "freshness" i.e. the _currency_ property of price data, and incentivises timely price reporting in _voting rounds_. If the _last submitted price_ is not get detected as an _outlier_, then there is no punishment for not submitting a new price. However,  the _last submitted price_ will become "stale" and eventually become an _outlier_ as the market moves. Therefore, oracles that are not providing timely prices will ultimately be punished as well.
:::

OAFD detects _outliers_ by a _threshold_ mechanism. A configured _outlier detection threshold_ sets the percentage range that a reported price can differ  from a given _median price_. The _median price_ is computed by creating a sorted index of all reported prices for a _currency pair_  _symbol_ and finding the mid index. The _median price_ is then compared against for _outlier_ detection. If the submitted price for a _symbol_ is determined to be an _outlier_, then it is excluded from the [final price calculation](/concepts/oafd/#final-price-calculation) computing the _aggregated median price_ for that _symbol_.

The _confidence score_ is further used as a weight to influence the OAFD economic incentives and disincentives for price reporting.

OAFD applies an NTN stake slashing penalty to _reporting validators_ determined to have submitted _outlier_ price(s). OAFD makes use of a _threshold_ mechanism to determine if slashing is applied. The [maximum slashing amount is capped](/concepts/oafd/#oracle-accountability-protocol-configuration) by the protocol configuration.

The size of the penalty is proportional to  the _confidence score_ submitted with the _price report_ for a _symbol_: the higher the _confidence score_, the higher the penalty.

Oracle voting incentives are similarly influenced by the _confidence score_. Each _reporting validator_ is assigned an _epoch performance score_. This is a summation of the _confidence scores_ for each _symbol_ price they have submitted in an epoch that has been included in the final price calculations for _symbols_  in _voting rounds_ during the epoch. (The _epoch performance score_ naturally excludes any _outliers_ submitted during the epoch.) 

### Oracle accountability prerequisites 

To participate in OAFD a [validator](/glossary/#validator) must be a [consensus committee](/glossary/#consensus-committee) member.

## Oracle Accountability Fault Detection protocol

OAFD roles, core concepts, and the lifecycle of omission accountability processing from detection to applying penalties at epoch end.

### Roles

As a consensus committee member the validator may play the roles in the table beneath during OAFD processing.

| Role | Description |
|:--|:--|
| _committee member_ | as a validator in the consensus committee executing Autonity's consensus protocol. For OAFD submitting and validating oracle _price reports_, maintaining system state for epoch performance scores, and computing and applying slashing penalties |
| _reporting validator_ | as a _committee member_ operating an _oracle server_ and submitting valid oracle _price reports_ for _symbol(s)_ to the Oracle contract on-chain to participate in oracle protocol _voting rounds_  |
| _offending validator_ | as a _committee member_ that OAFD has detected as submitting an _outlier_ price report for _symbol(s)_ in an epoch and the object of slashing penalties |

The economic impact of the OAFD protocol on a validator depends on their role.

| Role | Economic impact |
|:--|:--|
| _offending validator_ | loss of oracle rewards, validator reputation, slash staking for self-bonded stake slashed per [Autonity’s Penalty-Absorbing Stake (PAS) model](/glossary/#penalty-absorbing-stake-pas) |
| _reporting validator_  | gain of OAFD oracle rewards for submitting valid  _price reports_ for _symbol(s)_ |

The Autonity community is also a _beneficiary_ of OAFD processing. Slashed stake token will be used for community funds.

### Protocol primitives

Essential primitives of OAFD are: oracle price report, confidence score, outlier detection threshold, epoch performance score.

#### Price report

The _price report_ is the raw price data input sourced off-chain and used to compute an _aggregated median price_ for each supported _currency pair_ _symbol_ on-chain by the Autonity [Oracle Protocol](/concepts/oracle-network/#oracle-protocol).

The _price report_ is generated by _consensus committee members_, i.e.  _validator nodes_ in the current _consensus committee_.

Raw price data is collected from external data providers by oracle servers connected to _consensus committee_ _validator nodes_.

The oracle server generates a _price report_:

- performing an off-chain data aggregation to compute a median price for each _currency pair_ _symbol_ it has sourced (i.e. allowing for the scenario of sourcing price data for an individual _symbol_ from multiple sources).
- assigning a _confidence score_ rating to its price for a _symbol_
- generating a _price report_ containing the price data for all _currency pair_ _symbols_ it has sourced.

The _price report_ is then taken by the connected _validator node_ and submitted to the Oracle protocol contract on-chain for computation of an _aggregated median price_ for each _symbol_.

The aggregated median price is continually refreshed in a cycle of _voting rounds_. Each _voting round_ the newly computed price is emitted on-chain and recorded in [system state]() as _round data_.

#### Outlier

An _outlier_ is a price for a _currency pair_ _symbol_ submitted in a _voting round_ that is found to be outside the acceptable % range of variance from the median index value of all other prices submitted for that _symbol_ in the  _voting round_.

See protocol primitives [price report](/concepts/oafd/#price-report) and [thresholds](/concepts/oafd/#thresholds).

#### Confidence score

The _confidence score_ represents a validator oracle's level of trust in the accuracy of the data it is submitting for a _currency pair_ _symbol_ in  a _price report_.

For each _currency pair_ _symbol_ in the _price report_ submission there will be a separate _confidence score_.

See [Confidence score calculation](/concepts/oafd/#confidence-score-calculation).

#### Epoch performance score

The _epoch performance score_ is the sum of the _confidence scores_ for valid prices submitted by a validator in an epoch.

This confidence summation accounts only for the $w_{i,j}$ values that contributed to the price calculations during the past epoch, excluding _outliers_ but including any past submissions if they are being re-used.

See [Epoch performance score calculation](/concepts/oafd/#epoch-performance-score-calculation).

See [Confidence score calculation](/concepts/oafd/#confidence-score-calculation) for $w_{i,j}$.

#### Thresholds

The _threshold_ sets a floor which if broken triggers oracle accountability penalties. OAFD has outlier thresholds:

- The _outlier detection threshold_ how far from the median price a report for a _symbol_ can be before it is flagges as an _outlier_.
- The _outlier slashing threshold_ how far from the median price a report for a _symbol_ needs to be before the reporting validator gets slashed. For example, if a price reported satisfies the inequality `((price - median)/median)^2 > outlierSlashingThreshold`, then it's eligible for slashing.

See protocol primitive [outlier](/concepts/oafd/#outlier).

## Slashing

### Oracle accountability protocol configuration

OAFD protocol parameters are set by default to:

| Protocol parameter | Description | Value |
|:--:|:--|:--:|
| `OutlierDetectionThreshold` | defines the threshold for flagging outliers | `10` (10%) |
| `OutlierSlashingThreshold` | defines the threshold for slashing penalties, controlling the sensitivity of the penalty model | `225` (15%) |
| `BaseSlashingRate` | defines the base slashing rate for penalizing outliers | `10 ` (0.1%) |
| `OracleRewardRate` | defines the percentage of epoch ATN staking and NTN inflation rewards allocated for Oracle voting incentivisation | `1000` (10%) |
| `ORACLE_SLASHING_RATE_CAP` | the maximum amount of stake that can be slashed for oracle accountability | `1_000` (10%) |


### Confidence score calculation

The _confidence score_ is computed and assigned to price data by the validator according to the validator's trust in the quality of the data they are submitting to the oracle protocol on-chain.

Formally, for each reporting validator $j$ and each price $i$, the submission of a reported price $p_{i,j}$  should come with a confidence score $w_{i,j}$ such that $0<w_i \leq 100$.

The management and the assignment of the _confidence score_ value is not prescribed and is left to the reporting validator's Oracle Server implementation. For example, it could be manually set in a configuration file or automatically adjusted based on factors such as:

- the number of data sources used to calculate the submitted price.
- the calculated variance of prices from various publishers (e.g. a higher variance could reduce confidence, while lower variance would increase it).

### Outlier detection calculation

An _outlier_ is a price determined to be outside an acceptable % range from the median index value of all prices submitted for that _symbol_ in a _voting round_.

_Outliers_ are detected by means of an _outlier detection threshold_ configuration parameter ( $O_t$ ) the value of which is in the range $(0,100)$.

If $m_i$ the median value of all prices submitted by reporting validators $p_{j,i}$ for a specific symbol price $p$, then a price submission is deemed as _outlier_ if it satisfies the condition:

$$
\mid p_{j,i}/m_i - 1 \mid > O_t/100
$$

Detected _outliers_ are excluded from the set of prices used to compute the _aggregated median price_ for the symbol by the [final price calculation](/concepts/oafd/#final-price-calculation).

### Slashing amount calculation

The _slashing_ amount is calculated by the formula:

<!-- markdownlint-disable-next-line line-length -->

$$
max(0, ( \frac{p_{j,i} - m_i}{m_i} )^2 - S_t ) * w_i*R
$$

Where,

- $p_{j,i}$ means the reported price $p$ for each reporting validator $j$ and each price $i$.
- $m_i$ means the median value of all prices $p$ submitted by all reporting validators for a specific _symbol_.
- $S_t$ means the `OutlierSlashingThreshold`, which defines the threshold for slashing penalties and controls the sensitivity of the penalty model. Setting the threshold to $0$ would mean that any detected _outlier_ would be penalized.
- $w_i$ means the confidence score $w$ price for each reported price $i$.
- $R$ means the `BaseSlashingRate`, which defines the % of bonded stake that will be slashed to penalise _outliers_.

The NTN slashing penalty is applied proportionally to the _confidence score_ provided for the _outlier_, discouraging inaccurate submissions with high confidence. To prevent excessively harsh penalties, the maximum
slashing rate for a single penalty is capped by the `ORACLE_SLASHING_RATE_CAP`.

### Final price calculation

The final price $P_i$ is calculated as a weighted average of
the submitted prices excluding any detected _outliers_.

The _aggregated median price_ is calculated by the formula:

<!-- markdownlint-disable-next-line line-length -->

$$
P_i=\frac{\sum_j{w_{j,i}p_{j,i}}}{\sum_j{w_{j,i}}}
$$

Where,

- $P_i$ means the final price for a _symbol_, calculated as the median value of all _non-outlier_ prices $p$ submitted by reporting validators and weighted by _confidence score_.
- $w_j,i$ means the _confidence score_ $w$ for a reported price for each reporting validator $j$ and each price $i$.
- $p_j,i$ means the reported price $p$ for a _symbol_ for each reporting validator $j$ and each price $i$.

In the edge case where no _price reports_ have been submitted in the current _voting round_, the aggregated price of the past _round_ is re-used as the current _round_ price.

### Epoch performance score calculation

Each reporting validator $v$ is assigned an _epoch performance score_ that is a summation of the _confidence scores_ for the _price reports_  submitted by $v$ in an epoch.

The _epoch performance score_ amount is calculated by the formula:

<!-- markdownlint-disable-next-line line-length -->

$$
P_v =  \sum_{i,j}{w_{i,j}}
$$

Where,

- $P_v$ means the _epoch performance score_ of the validator $v$
- ${i,j}$ means the index of summation, i.e. each price $i$ submitted by each validator $j$.
- $w_i,j$ means the _confidence score_ $w$ for each reporting validator $j$ and each reported price $i$.

This confidence summation accounts only for the $w_{i,j}$ values
that contributed to the price calculations during the past epoch,
excluding _outliers_, but including any past submissions if they
are being re-used.


### Oracle reward calculation

The _oracle reward_ for a validator is a percentage of the ATN staking rewards and NTN inflation rewards earned by stake delegated to a validator for an epoch. The reward originates from ATN [staking rewards](/glossary/#staking-rewards) earned on transactions processed during the epoch, and [NTN inflation rewards](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) earned from the Newton inflation mechanism for [delegated](/glossary/#delegated) [stake](/glossary/#staking). The amount is dependent upon:

- transactions processed in the epoch: how many transactions were processed and committed to blocks during the epoch
- total stake bonded in the epoch: the total amount of stake delegated to *all* validators during the epoch
- oracle performance in the epoch: the _epoch performance score_ of an oracle and how accurately the oracle has been reporting prices. See [Epoch performance score calculation](/concepts/oafd/#epoch-performance-score-calculation).


The reward amount is then calculated based on the validator's _epoch performance score_ for an epoch and the `OracleRewardRate` configuration parameter. The reward is deducted from the rewards before they are distributed to stake delegation.

The _oracle reward_ amount is calculated by the formula:

<!-- markdownlint-disable-next-line line-length -->

$$
B_v = \frac{P_v}{ \sum_j{P_j}} * \text{ORACLE\_REWARD\_RATE} * \text{TOTAL\_EPOCH\_REWARD}
$$

Where,

- $B_v$ means the _oracle reward_ for validator $v$ in an epoch.
- $P_v$ means the _epoch performance score_ for the validator $v$ in an epoch.
- ${\sum_j{P_j}}$ means the summation of the _epoch performance score_ for each validator $j$ in the epoch.
- $\text{ORACLE\_REWARD\_RATE}$ means the `OracleRewardRate`, the % of `TOTAL\_EPOCH\_REWARD`s that is deducted and allocated for Oracle voting incentivisation.
- $\text{TOTAL\_EPOCH\_REWARD}$ means the total amount of ATN staking rewards and NTN inflation rewards earned during an epoch.


::: {.callout-note title="A note on total rewards and an analogy" collapse="false"}

The oracle rewards are a portion of the total rewards earned during the epoch - from transaction fees and from Newton inflation. This reward amount is then distributed to the validators in the consensus committee, each validator's final reward amount influenced by their own oracle reporting performance.

On distributing the rewards:

- :pie: a big slice gets redistributed based on stake-based logic
- :pie: a small slice gets redistributed based on omission accountability performance
- :pie: a small slice gets redistributed based on oracle performance

:::

## OAFD economics

There are two aspects to oracle accountability fault detection economics of slashing: outlier penalties for _offending validators_ and oracle rewards for _honest validators_.

| Role | Economic impact |
|:--|:--|
| _offending validator_ | loss of oracle rewards, validator reputation, slash staking for detected outliers per [Autonity’s Penalty-Absorbing Stake (PAS) model](/glossary/#penalty-absorbing-stake-pas) |
| _reporting validator_  | gain of OAFD oracle rewards for submitting valid _price reports_ for _symbol(s)_ |

### Outlier penalties

The economic loss to consensus committee members and their delegators from reporting outlier prices covers stake slashing, and per the PAS model potential loss of staking rewards due to PAS slashing self-bonded stake in first priority.

| Economic loss | Receiving account | Distribution | Description |
|:-- |:--|:--|:--|
| Loss of current epoch _oracle rewards_ | n/a  | epoch end | The _offending validator_ loses the opportunity to earn oracle rewards for prices flagged as _outliers_. Oracles earn oracle rewards for reported prices included in the [Final price  calculation](/concepts/oafd/#final-price-calculation). _Outlier_ prices are excluded from that calculation and from the oracle's _epoch performance score_, which influences the amount of the validator's _oracle rewards_. See [Epoch performance score calculation](/concepts/oafd/#epoch-performance-score-calculation) and [Oracle reward calculation](/concepts/oafd/#oracle-reward-calculation). |
| Slashing of stake token | Autonity Protocol [`treasury`](/reference/genesis/#config.autonity-object) account | epoch end | The _offending validator's_ bonded stake is slashed for the oracle outlier penalty amount. Slashing is applied at epoch end according to the protocol's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model. Amount determined by the [Slashing amount calculation](/concepts/oafd/#slashing-amount-calculation). |

### Rewards

Economic rewards are provided to _reporting validators_ as an economic incentive to submit prices in an epoch.

_Oracle rewards_ comprise ATN and NTN: ATN staking rewards from transaction fees, and NTN inflation rewards from the [Newton inflation mechanism](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation).

The reward amount is influenced by the accuracy and confidence of prices reported by the validator's oracle in the epoch.

| Economic gain | Receiving account | Distribution | Description |
|:-- |:--|:--|:--|
| oracle rewards | [`treasury`](/concepts/validator/#treasury-account) account | epoch end | The ATN staking rewards and NTN inflation rewards earned for price reporting by the validator for the epoch. ATN is transferred to the validator's [`treasury`](/concepts/validator/#treasury-account) account and NTN inflation rewards are auto-bonded to the validator's [`treasury`](/concepts/validator/#treasury-account) account becoming self-gonded stake. Amount determined by the [Oracle reward calculation](/concepts/oafd/#oracle-reward-calculation) formula. |
