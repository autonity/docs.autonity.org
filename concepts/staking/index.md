
---
title: "Staking "
description: >
  Autonity's Liquid Staking and Penalty-Absorbing Stake (PAS) model, staking and staking rewards, temporal constraints governing staking transitions, and economic penalties for Byzantine behaviour.
---


## Overview

Autonity implements the Tendermint Proof of Stake consensus protocol, enhanced by a [liquid staking](/concepts/staking/#liquid-staking) and [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model. PoS consensus secures the network by an economic incentivisation scheme that rewards honest behaviour with revenue from transaction fees and punishes dishonest behaviour by slashing penalties that may confiscate a portion of bonded stake or otherwise impact the staking rewards a [validator](/glossary/#validator) would earn while participating in consensus.

Stake in an Autonity network is represented as the [Newton](/concepts/protocol-assets/newton/) stake token. Any network participant holding Newton becomes a [stakeholder](/glossary/#stakeholder) and is able to participate in securing the network and earn a share of [staking rewards](/glossary/#staking-rewards) proportionate to their stake in return. As default, Newton is in an unbonded state and can be transferred to other stakeholders. On bonding the Newton stake token is burned. Autonity implements a liquid staking model and Liquid Newton is minted for [delegated](/glossary/#delegated) stake. In this liquid staking model the Liquid Newton receives the staking reward entitlements due to the bonded stake it represents. Liquid Newton is transferrable. To redeem Liquid Newton for Newton, it is unbonded. Liquid Newton for [delegated](/glossary/#delegated) stake is locked on unbonding (so it is no longer tradable) and after the expiry of an [unbonding period](/concepts/staking/#unbondingperiod) Newton is redeemed.

Staking is open - any network participant is able to purchase stake token and bond stake by [delegation](/glossary/#delegation) to validators. 

Stakers are financially rewarded by Auton [staking rewards](/concepts/staking/#staking-rewards) and [Newton inflation rewards](/concepts/staking/#newton-inflation-rewards).

Staking rewards are distributed to [delegated](/glossary/#delegated) stake that is actively backing consensus. That is, to the subset of validator nodes participating in the [consensus committee](/glossary/#consensus-committee). Stake delegators to committee member validators receive a share of those rewards in proportion _pro rata_ to their share of the stake bonded to the committee.

Newton inflation rewards are distributed to [participating](/glossary/#participation-rate) stake at the end of each epoch by the Newton [inflation mechanism](/glossary/#inflation-mechanism). The newton inflation reward is [automatically bonded](/glossary/#autobond) by the protocol to the validator nodes where [participating](/glossary/#participation-rate) Newton is staked. Stake delegators receive a reward in proportion to the amount of Newton they have staked. Newton [inflation rewards](/glossary/#inflation-rewards) accrue to all bonded stake irrespective of whether it is active in the current committee or not.

::: {.callout-note title="Note" collapse="false"}

Note that in Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model, validator [self-bonded](/glossary/#self-bonded) stake does _not_ result in minting of liquid newton. Validator revenue is derived from commission, block proposal, staking rewards on self-bonded stake, and accountability protocol rewards. See [validator economics](/concepts/validator/#validator-economics).

:::

## Liquid staking

Autonity implements a liquid staking model, bringing benefits of:

- Capital efficiency: rewards from staking combined with the liquidity benefits of bonded stake that is transferable
- Composability: liquid stake tokens can be used in other protocols (e.g., as collateral)

### Liquid Newton

Liquid Newton is minted for [delegated](/glossary/#delegated) Newton stake bonded to a validator. On registration each validator has an ERC20 Liquid Newton contract created and deployed autonomously by the Autonity Protocol Contract (which maintains a registry of all Liquid Newton token contracts deployed).

It is important to note that stake bonded by the validator operator to its own validator - [self-bonded](/glossary/#self-bonded) stake - does _not_ result in minting of Liquid Newton. This is part of Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model.

Liquid Newton is validator-specific because there is a separate ERC20 token for each registered validator. Liquid Newton for a given validator is fungible, but Liquid Newton tokens of different validators are _not_ fungible with each other.

When [delegated](/glossary/#delegated) stake is bonded to a validator, the Newton is burned and Liquid Newton is minted for the Newton staked. The amount of Liquid Newton minted is subject to the amount of bonded Newton the validator has at the time the bonding is applied. Accountability penalties may apply stake [slashing](/concepts/staking/#slashing) to a validator. To keep Newton and Liquid Newton fungible a conversion rate is maintained by a validator's Liquid Newton contract as the reference price for Newton bonding and unbonding operations. The rate is determined by the ratio of issued liquid tokens over the total amount of stake tokens bonded to the validator.
             
As consequence, the amount of Liquid Newton minted is subject to any accountability and omissions penalties applied to the validator resulting in a stake slashing event:

- If at the time of bonding a validator's bonded stake amount _has not_ been reduced by a stake slashing event, then Liquid Newton is minted `1:1` for the Newton staked.
- However, if a validator has been slashed and the validator's existing bonded stake amount is less than the supply of issued Liquid Newton, then Liquid Newton is minted in proportion to the validator's bonded stake amounbt remaining, resulting in a `>1:1` issuance of Liquid Newton for Newton staked.

::: {.callout-note title="Info" collapse="false"}

For a worked example of how slashing affects the LNTN-NTN conversion rate, see [Slashing, Consequences for stake redemption](/concepts/staking/#consequences-for-stake-redemption) on this page.
:::

This tokenomic mechanism ensures that a validator's Liquid Newton tokens remain fungible as they are issued over time: the amount of Liquid Newton issued on bonding has a value matching that of the Newton being bonded.

::: {.callout-note title="Note that autobonding does not mint Liquid Newton" collapse="false"}

[Newton inflation](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) emissions for delegated stake are [autobonded](/glossary/#autobond) by protocol.

Note that Liquid Newton is not minted for [autobonded](/glossary/#autobond) stake delegations. The autobond process increases the Newton amount of the delegated stake of the validator without issuing new Liquid Newton tokens. This results in an increase in the LNTN/NTN conversion rate of delegations to the validator.

:::

The Liquid Newton has staking reward entitlement rights, is freely transferable, and represents the Liquid Newton holder's share of the total stake bonded to the validator (i.e. the holder's share of the validator's Liquid Newton pool).

When stake is unbonded it is subject to an unbonding period and the holder's Liquid Newton is redeemed in proportion to its share of the Liquid Newton pool minus any slashing penalties applied. 

For example, if a validator had suffered a slashing penalty equivalent to 1% of its stake pool, then stake redemption value after slashing would be 99% of the original stake amount.


### Fundamental operations

Liquid Newton has fundamental operations to _transfer ownership_ and _redeem_ for Newton stake token.

The Liquid Newton holder can transfer ownership of the token by sending to another network participant using the Liquid Newton contract's ERC20 `transfer()` function. Upon receipt of Liquid Newton the holder becomes a delegator to the associated validator and has a claim to staked Newton.

Redemption of Liquid Newton for Newton stake token is by unbonding. The Liquid Newton holder can unbond stake from a validator and redeem Newton at any time subject to the [unbonding period](/glossary/#unbonding-period) set for the chain. On mining of the unbonding tx in block $T$ of epoch $e$ , the Liquid Newton is locked. At $T+1$ the unbonding period begins. At the end of epoch $e$, the Liquid Newton is unlocked and burned, and unbonding shares are computed. At the end of the epoch in which the unbonding period expires, Newton is minted to the stake holder based on the unbonding shares. The unbonding Liquid Newton stake remains subject to any [slashing penalties](/glossary/#slashing-penalty) applied to the validator before unbonding completes and stake redemption occurs.
 
::: {.callout-note title="Note" collapse="false"}

It's important to note that Liquid Newton is validator-specific and as such is not $1:1$ fungible with Liquid Newton bonded to a different validator. A validator may or may not have had [slashing penalties](/glossary/#slashing-penalty) applied and the redemption value of Liquid Newton may vary across validators according to their fault slashing history.

:::

### Transferring Liquid Newton

For how to transfer Liquid Newton from a stake delegation to another account see the guide [Transfer Liquid Newton](/delegators/transfer-lntn/).

## Penalty-Absorbing Stake (PAS)

Autonity implements a [_penalty absorbing stake (PAS)_](/glossary/#penalty-absorbing-stake-pas) model where a validator's [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake when applying [slashing penalties](/glossary/#slashing-penalty) for accountability events.

Slashing priority is simply:

- [Self-bonded](/glossary/#self-bonded) stake is slashed as first priority until exhausted. If the validator has unbonding stake, then the unbonding stake is slashed before bonded stake.
- [Delegated](/glossary/#delegated) stake is slashed as second priority when the slashing amount exceeds the amount of self-bonded stake available. If the delegator has unbonding stake, then the unbonding stake and bonded stake are slashed _pro rata_ with equal priority.

In the PAS model self-bonded stake has a different risk profile to delegated stake _because it provides loss absorbing capital in the case of a slashing event_. For this reason, Liquid Newton is only minted for delegated stake to ensure validator Liquid Newton has a uniform risk profile.

::: {.callout-note title="Note" collapse="false"}
By self-bonding stake, a validator puts "skin in the game" because this constitutes a public commitment to the operational integrity of the validator node by its operator. Potential stake delegators can use the amount of self-bonded stake of a validator as a decision factor when conducting due diligence before staking.
:::

## Staking rewards
[Staking rewards](/glossary/#staking-rewards) are a distribution of fee revenue entitlement to all holders of bonded stake actively backing consensus. Reward distribution takes place _pro-rata_ to the share of total stake bonded to validators in the consensus committee. The fee revenue comes from the _base fees_ charged for computing transactions included in blocks committed to the system ledger. The optional _priority fee_ of a transaction is not included in the rewards pool but awarded to the block proposer according to the EIP 1559 transaction fee mechanism.

::: {.callout-note title="Note" collapse="false"}
For more detail on EIP 1559 and the distinction between _base fee_ and _priority fee_, see [Transaction fees](/concepts/system-model/#transaction-fees) in the System model.
:::

Staking rewards are collected by the protocol and accumulate in a protocol account as blocks are processed throughout a block epoch. The fees are out of circulation until epoch end, at which point the protocol distributes them to validator committee members. Rewards are then distributed to validator self-bonded and delegated stake holders _pro rata_ to their share of the validator's total bonded stake. After this distribution, the rewards become _claimable_ by stake delegators. Delegators then [claim rewards](/concepts/staking/#claiming-rewards) in a "pull" model, at the frequency they choose. 

As rewards are distributed, due fees are deducted from fee revenue by the protocol:

- Protocol treasury fee. A percentage of staking rewards is deducted for community funding. The fee goes to the Autonity Treasury account (See below), sent at epoch end when the epoch rewards are distributed to committee validators. The percentage value is set at genesis.  See `treasuryFee` parameter of the `config.autonity` object in the [Protocol](/reference/protocol#configautonity-object) section.

- Validator commission fees. The percentage commission rate charged by a validator to stakers delegating to the validator; essentially, the validator's service fee for providing a staking service to delegators. The fee is deducted from the validator's portion of the fee revenue before staking rewards are apportioned to the stake delegators _pro rata_ to their share of bonded stake. The percentage value is set at validator registration. See the `delegationRate` parameter of the `config.autonity` object in the [Protocol](/reference/protocol#configautonity-object) section.

The remaining fee revenue is then distributed to stake delegators. 

### Reward distribution
Stake delegation rewards are distributed to validator committee members at the end of each epoch. On finalization of the last block in the epoch rewards become claimable by stake delegators.

The _priority fee_ reward is distributed to the block proposer when the block is finalized. It is sent to the validator node's [`validator identifier`](/concepts/validator/#validator-identifier) account.

### Claiming rewards

Fees accumulate until claimed by delegators in a pull-based model. Staking rewards are manually retrieved by calling the validator specific Liquid Newton contract. This incurs transaction costs, so stake delegators should allow fees to accumulate until they exceed the gas cost of claiming them. 

For details on how to claim and the functionality for claiming staking rewards, see:

- How to [Claim Staking Rewards](/delegators/claim-rewards/).

## Newton inflation rewards
Newton [inflation rewards](/glossary/#inflation-rewards) are a distribution of newly minted newton by the Newton [inflation mechanism](/glossary/#inflation-mechanism) to all holders of bonded stake [participating](/glossary/#participation-rate) in securing the [Autonity network](/glossary/#autonity-network).

For more detail see the [Newton](/concepts/protocol-assets/newton/) concept and [Total supply and newton inflation](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation).

### Reward distribution
Newton [inflation rewards](/glossary/#inflation-rewards) are minted and distributed to stakers at the end of each epoch by the Newton [inflation mechanism](/glossary/#inflation-mechanism). On emission the newton inflation reward is [automatically bonded](/glossary/#autobond) by the protocol to the validator nodes where [participating](/glossary/#participation-rate) Newton is staked. The bonded stake balances of the individual stake delegators (i.e. for [delegated](/glossary/#delegated) and [self-bonded](/glossary/#self-bonded) stake) is incremented accordingly to reflect the inflation received.

## Staking accounts

The protocol makes use of different accounts for fee revenue collection and distribution.

### Staker account

The `account` address submitting a bond or unbonding request. A staker can bond stake across as many validators as it chooses. The `msg.sender` address of the request is the account that receives the staker's due share of staking reward entitlements, and determines if the stake is [delegated](/glossary/#delegated) or [self-bonded](/glossary/#self-bonded):

| Stake Delegation Type | Sending Address |
|:--|:--|
| [delegated](/glossary/#delegated) | `msg.sender` can be any network [account](/glossary/#account) _except_ the validator `treasury` account |
| [self-bonded](/glossary/#self-bonded) | `msg.sender` is a [validator `treasury` account](/concepts/staking/#validator-treasury-account) |

### Validator treasury account

The validator operator's account address. The `treasury` is used as the account:

- Identifying the validator operator entity itself.
- For submitting transactions to protocol contracts to register and operate the validator's [node](/concepts/client/) and [oracle server](/concepts/oracle-server/).
- Receiving [staking rewards](/concepts/staking/#staking-rewards) from the protocol's reward distribution mechanism for distribution to the validator's stake delegators.
- Receiving [slashing rewards](/concepts/afd/#slashing-rewards) distributed by the [accountability and fault detection protocol](/concepts/afd/) for reporting provable faults committed by an offending validator failing to follow consensus rules.

See the `treasury` parameter of the `config.autonity.validators` object in the [Protocol](/reference/protocol#configautonityvalidators-object) parameter reference.

### Autonity treasury account

The Autonity Protocol's `treasury` account for receiving treasury fees. See `treasury` parameter of the 
`autonity.treasury` object in the [Protocol](/reference/protocol#configautonity-object) parameter reference.	
### Autonity Protocol Contract account

The Autonity Protocol's contract account for holding staking rewards (serving as a 'rewards pool') until reward distribution occurs at epoch end. 

The Autonity Contract account is generated automatically on deployment of the Autonity Protocol Contract at network genesis. See [Protocol Contract Addresses](/concepts/architecture/#protocol-contract-account-addresses) for the address value.

## Temporal constraints

Slashing, unbonding and bonding operations are applied by protocol at specific time points. This is to ensure [voting power](/glossary/#voting-power) changes are applied before committee selection for the next epoch, and to provide guarantees for network security. (I.E. slashing penalties can be applied, stake does not change during a committee ensuring stake cannot decrease while it is _in power_.)

Constraints:

- The committee is selected for an epoch duration.
- Voting power changes are applied at epoch end before the committee for the next epoch is selected. These are adjustments to bonded stake amounts for validators caused by:
	- Slashing stake for accountability and omissions faults.
	- Staking transitions from unbonding and bonding operations.

### epoch

A period of time measured as a number of blocks in which there is no change in consensus committee membership.

### epochPeriod

The period of time for which a consensus committee is elected and defined as a number of blocks. The epoch period can be any integer number > `0`, but _must_ be shorter than the unbonding period. Without this constraint unbonding could take place before slashing penalties and staking transitions are applied.

The duration of the epoch period is set at genesis by the `epochPeriod` parameter, see the [Protocol](/reference/protocol) parameter reference. The setting can be changed by governance calling the [`setEpochPeriod()`](/reference/api/aut/op-prot/#setepochperiod) function.

At each epoch rollover there is an evaluation of the bonded stake. As the last block of an epoch is finalized then:

- Voting power changes affected by staking transitions are applied.
- The committee selection algorithm is run to choose members of the consensus committee for the upcoming epoch.

Bonding and unbonding requests submitted during an epoch are processed and committed to state in the next available block, but the effect of such staking transitions is applied at epoch end.  

::: {.callout-note title="Note" collapse="false"}
Consensus [committee member selection](/concepts/consensus/committee/#committee-member-selection) takes place at epoch end for computation and transactional efficiency.

Further, in an interoperability scenario where state is shared across chains, rather than submit a state proof of a new validator set every block, we only need to send a checkpoint of the validator set every epoch.
:::

### unbondingPeriod

The period of time bonded stake must wait before Newton is redeemed to the staker after processing a stake redeem (`unbond()`) transaction, defined as a number of blocks. The unbonding period can be any integer number > `0`, but _must_ be longer than the epoch period. There is no requirement for the unbonding period to be a multiple of the epoch period, just larger.

Stake remains at risk during the unbonding period. This is a protocol measure that gives the consensus protocol's accountability and omissions  mechanism time to identify and prove faults and apply penalties to bonded stake before stake the unbonding period has expired and the bonded Newton has been redeemed. Byzantine behaviour cannot escape penalties by unbonding before a fault is detected.

The duration of the unbonding period is set at genesis by the `unbondingPeriod` parameter, see the [Protocol](/reference/protocol) parameter reference. The setting can be changed by governance calling the [`setUnbondingPeriod()`](/reference/api/aut/op-prot/#setunbondingperiod) function.

::: {.callout-note title="Note" collapse="false"}

In an unbonding scenario with an epoch period of 30 blocks, an unbonding period of 120 blocks, and an unbonding request issued at block 15 in the epoch. At block 15 the unbonding request is processed and then tracked in memory. At the end of that epoch, block 30, the validator's voting power is reduced and the unbonded amount is added to the unbonding pool. The unbonding period expires at block 135. At the end of the epoch in which the unbonding period falls, block 150, the Newton that is due is returned to the stake delegator.

Stake remains at risk during the unbonding period. The amount of Newton returned to the delegator may be less than the original unbonded amount if the validator has been slashed between submitting the unbond request at block 15 and Newton redemption at block 150.
:::

## Staking transitions

Staking transitions are changes to stake bonded to validators caused by stake bonding and unbonding operations submitted by stake delegators.

Bonding and unbonding requests submitted during an epoch are processed and committed to state in the next available block, but the effect of such staking transitions is only applied at epoch end. Until epoch end, staking transitions are maintained in memory in `BondingRequest` and `UnbondingRequest` data structures. They can be read by listening for and viewing `NewBondingRequest` and `NewUnbondingRequest` events emitted by the [`bond()`](/reference/api/aut/#bond) and [`unbond()`](/reference/api/aut/#unbond) functions of the Autonity Protocol Contract.

In Autonity's [AFD](/concepts/afd/) protocol, slashable faults are likewise processed throughout an epoch. Any changes to delegated stake that are caused by stake slashing are applied to unbonding and bonded stake at the epoch end according to Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model. This takes place before staking transitions are applied. 

As noted in [Protocol assets](/concepts/protocol-assets/), Newton and Liquid Newton token can be in different states. Bonded and unbonding stake is liable to [slashing](/concepts/staking/#slashing) penalties:

- Newton in [states](/concepts/protocol-assets/newton/) `bonded` and `unbonding`
- Liquid Newton in [states](/concepts/protocol-assets/liquid-newton/) `locked` and `unlocked`

Whilst stake is unbonding, the protocol tracks the relative ownership of stake in the delegated and self-bonded unbonding pools via a "share" mechanism. This is so that the PAS slashing priority may be correctly applied to the unbonding stake, and the correct amount of delegated or self-bonded stake may be released at the end of the unbonding period.

::: {.callout-note title="Note" collapse="false"}
Metadata providing the total amount of shares and unbonding stake is returned as part of the response when querying for a validator. See the [`getValidator()`](/reference/api/aut/#getvalidator) response object which contains fields for:

- delegated stake unbonding pool: `unbondingStake` and `unbondingShares`
- self-bonded unbonding pool: `selfUnbondingStake` and `selfUnbondingShares`

The shares and unbonding stake amounts for each unbonding request are stored in the `UnbondingRequest` object. See the `NewUnbondingRequest` event emitted by the [`unbond()`](/reference/api/aut/#unbond) for the object fields.
:::

### Bonding

Stake token is bonded to an active validator through a bonding operation. If bonded stake token belongs to the validator operator, then it is [self-bonded](/glossary/#self-bonded); otherwise the token is [delegated](/glossary/#delegated). The [voting power](/glossary/#voting-power) of a validator is determined by the amount of stake bonded to it. 

On bonding Newton, the stake token is burned on execution of the `bond()` function, the bonding request is tracked in memory, and the resulting voting power change is tracked and the staking transition is applied at epoch end. From this point the stake is actively bonded and able to earn staking rewards. Note that a bond allocation cannot be changed after submission and before the bonding is applied at epoch end.

Autonity implements a [liquid staking](/concepts/staking/#liquid-staking) model and Liquid Newton is minted for [delegated](/glossary/#delegated) stake. Minting Liquid Newton is an autonomous protocol-only function.

::: {.callout-note title="Note" collapse="false"}
Alice submits a [`bond()`](/reference/api/aut/#bond) tx that is processed and included in a block at time $T$, where a `BondingRequest` object for the necessary voting power change is also created. Newton is locked at $T$.

The bonding request is tracked in memory for application at the end of the epoch in which $T$ was processed. At this point, the validator's bonded stake is increased, and Liquid Newton is issued to Alice in the validator’s Liquid Newton ERC20 contract. Actual bonding is then executed at $T$ + remainder of the epoch. Liquid Newton issuance is delayed and not tradable while bonding is pending.
:::

Staking rewards are earned when a nominated validator is a consensus committee member. Bonding across more than one validator is allowed. The committee size is limited and staking rewards are limited to the number of validators in the current committee for the epoch.

::: {.callout-note title="Note" collapse="false"}
Stake can only be bonded to a registered validator in an `active` state. A bonding request to an inactive validator (i.e. one in a `paused`, `jailed`, or `jailbound` state will revert). See [Validator pausing](/concepts/validator/#validator-pausing), [Validator jailing](/concepts/validator/#validator-jailing), and [Validator lifecycle](/concepts/validator/#validator-lifecycle).
:::

### Delegation

See [Bonding](/concepts/staking/#bonding) above.

### Unbonding

Stake is unbonded from a validator through an unbonding operation. Unbonding is subject to an [unbonding period](/concepts/staking/#unbondingperiod) during which it is in an `unbonding` state.  During unbonding the Newton is represented as shares in the validator's unbonding pool, those shares tracking the $\%$ of unbonding stake owned by the stake holder. Once unbonding has completed, the due amount of Newton is minted to the stake holder. The unbonding period applies irrespective of whether the nominated validator is a member of the consensus committee or not. 

Unbonding is triggered by a staker submitting an `unbond()` transaction. Unbonding can begin as soon as the unbond transaction request has been finalized. On processing the transaction, the bonded stake token moves from `bonded` to the intermediate state of `unbonding`. The unbonding request is captured and tracked in memory. The staking transition is applied in two steps:

- _at the end of the epoch in which the unbonding request was issued_: the validator's total bonded stake (and consequently [voting power](/glossary/#voting-power) decreases by the unbonded amount when the unbonding is applied at the end of the epoch

- _at the end of the epoch in which the unbonding period expires_: NTN for the unbonding stake amount are minted to the delegator

::: {.callout-note title="Example" collapse="false"}
Alice has [delegated](/glossary/#delegated) stake to a validator. Alice submits an [`unbond()`](/reference/api/aut/#unbond) tx that is processed and included in a block at time $T$:

- At $T$ Alice's `unbond()` tx is processed and included in a block. Alice's 100 LNTN are locked so they cannot be traded. An `UnbondingRequest` object for the necessary voting power change is also created.
- At $T+1$, the [unbonding period](/glossary/#unbonding-period) begins.

The unbonding request is tracked in memory for application at the end of the epoch in which $T$ was processed, when the validator's bonded stake amount and voting power is reduced as follows:

  - the designated amount of Liquid Newton is unlocked and burnt (this step only applies to [delegated](/glossary/#delegated) stake and not [self-bonded](/glossary/#self-bonded) stake)
  - the amount of stake to reduce the unbonding pool by and Alice's share of the unbonding pool is calculated
  - the amount of Newton bonded to the validator is reduced by the unbonding amount, consequently reducing the validator's voting power

Then, at the end of the epoch in which the unbonding period $(T+1 + unbonding~period)$ expires, Newton redemption (i.e. 'release') occurs and the Newton that is due is minted to Alice's Newton account.

Note that the amount of Newton released to Alice may be less than the original unbonded amount if the validator has been slashed between $T$ and the end of the [epoch](/glossary/#epoch) in which the [unbonding period](/glossary/#unbonding-period) expires.
:::

## Slashing

Bonded stake is subject to economic [slashing penalties](/glossary/#slashing-penalty) if misbehavior by the staked validator node when a member of the [consensus committee](/glossary/#consensus-committee) is detected by an Autonity accountability protocol:

- [Accountability fault detection protocol (AFD)](/concepts/afd/) for failing to follow consensus rules 
- [Omission fault detection protocol (OFD)](/concepts/ofd/) for failing to participate in consensus 
- [Oracle accountability fault detection protocol (OAFD)](/concepts/oafd/) for failing to submit accurate price reports to the oracle protocol on-chain. 

### Economic penalties

Economic penalties vary in severity and are applied according to the type of fault detected and the risk created for network security. 

Penalties are applied at epoch end and take the form of slashing of [bonded](/glossary/#bond) stake token per Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model, loss of [staking rewards](/glossasry/#staking-rewards) and [inflation rewards](/glossary/#inflation-rewards), and loss of future earning opportunity by temporary or permanent barring from the consensus committee ('[jailing](/glossary/#jailing)').

The extent of the penalty varies according to the severity of the fault committed. For the economic disincentives of accountability penalties see:

| Accountability protocol | Disincentive penalty |
|:-- |:--|
| [Accountability fault detection protocol (AFD)](/concepts/afd/) | [slashing penalties](/concepts/afd/#slashing-penalties) |
| [Omission fault detection protocol (OFD)](/concepts/ofd/) | [inactivity penalties](/concepts/ofd/#inactivity-penalties-1)|
| [Oracle accountability fault detection protocol (OAFD)](/concepts/oafd/) | [outlier penalties](/concepts/oafd/#outlier-penalties)|

[Slashing penalties](/glossary/#slashing-penalty) are applied by autonomous protocol action at [epoch](/concepts/staking/#epoch) end as [voting power](/glossary/#voting-power) cannot change mid-epoch.


### Consequences for stake redemption

Bonding stake to a validator enters the staker in to a risk mutualization model shared with the validator, i.e. if the validator is penalized then the stake delegator may lose stake as consequence. This risk is realized when unbonding. Note, though, that Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model mitigates the risk to [delegated](/glossary/#delegated) stake.

As described in [Liquid Newton](/concepts/staking/#liquid-newton), a conversion rate between Liquid Newton and Newton is maintained by the protocol's tokenomics to ensure that a validator's Liquid Newton tokens remain $1:1$ fungible. As consequence, a staker can redeem staked Newton in full _unless_ there has been a slashing event. In this circumstance, the stake redemption will be affected. 

To illustrate:

- 100 Newton is bonded at time $T$:
  - 100 Liquid Newton are issued, backed by 100 Newton
  - If a slashing penalty of 20 is applied to the validator at $T + 1$, then bonded stake is reduced to 80 and the 100 Liquid Newton issued are now backed by 80 Newton
  - The 100 Liquid Newton have a redemption value of 80 Newton 
- An additional 100 Newton are bonded post slashing at time $T + 2$:
  - 125 LNTN are issued, i.e. $current~LNTN~supply * new~bonding~amount / current~bonded~stake$.

The LNTN issuance ratio has increased in light of the reduced bonded stake amount. This compensates for the lower redemption value of LNTN given the reduction in bonded stake, and maintains the fungibility of the validator's LNTN token.

To exemplify redemption in this scenario for a validator $V$:

|Time|Event|Amount|Liquid Newton Issued|Liquid Newton Supply|Newton Redeemed|Bonded Stake Amount|
|----|-----|------|-----------------------------|--------------------|---------------|-------------------|
|$T$|Bond Event |100 NTN|100|100||100|
|$T+1$|Slashing Event|20 NTN||100||80|
|$T+2$|Bond Event|100 NTN|125|225||180|
|$T+3$|Unbond Event|100 LNTN||125|80|100|
|$T+4$|Unbond Event|125 LNTN||0|100|0|

::: {.callout-note title="Note" collapse="false"}
In a trading context, if 100 Liquid Newton is purchased after this slashing event, then on redemption 80 Newton would be received. If the market price for Liquid Newton has dropped you would be purchasing it at a discount.
:::
