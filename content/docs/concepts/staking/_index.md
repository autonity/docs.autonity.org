
---
title: "Staking "
linkTitle: "Staking"
weight: 6
description: >
  Autonity's Liquid Staking and Penalty-Absorbing Stake (PAS) model, staking and staking rewards, temporal constraints governing staking transitions, and economic penalties for Byzantine behaviour.
---


## Overview

Autonity implements the Tendermint Proof of Stake consensus protocol, enhanced by a [liquid staking](/concepts/staking/#liquid-staking) and [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model. PoS consensus secures the network by an economic incentivisation scheme that rewards honest behaviour with revenue from transaction fees and punishes dishonest behaviour by slashing penalties that may confiscate a portion of bonded stake or otherwise impact the staking rewards a [validator](/glossary/#validator) would earn while participating in consensus.

Stake in an Autonity network is represented as the [Newton](/concepts/protocol-assets/newton/) stake token. Any network participant holding Newton becomes a [stakeholder](/glossary/#stakeholder) and is able to participate in securing the network and earn a share of [staking rewards](/glossary/#staking-rewards) proportionate to their stake in return. As default, Newton is in an unbonded and unlocked state and can be transferred to other stakeholders. On bonding, Newton is locked and no longer transferrable; Liquid Newton is minted for [delegated](/glossary/#delegated) stake in equal proportion to the stake locked. In this liquid staking model the Liquid Newton receives the staking reward entitlements due to the bonded stake it represents; Liquid Newton is transferrable. To redeem stake, the converse to bonding occurs. Liquid Newton for [delegated](/glossary/#delegated) stake is burned (so it is no longer tradable) and after the expiry of a [locking (unbonding) period](/concepts/staking/#unbondingperiod) the bonded Newton is redeemed.

Staking is open - any network participant is able to purchase stake token and bond stake by [delegation](/glossary/#delegation) to validators. 

Staking rewards are distributed to [delegated](/glossary/#delegated) stake that is actively backing consensus. That is, to the subset of validator nodes participating in the [consensus committee](/glossary/#consensus-committee). Stake delegators to committee member validators receive a share of those rewards in proportion _pro rata_ to their share of the stake bonded to the committee.

{{% alert title="Note" %}}
Note that in Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model, validator [self-bonded](/glossary/#self-bonded) stake does _not_ result in minting of Liquid Newton. Validator revenue is derived from commission, block proposal, staking rewards on self-bonded stake, and slashing rewards. See [validator economics](/concepts/validator/#validator-economics).
{{% /alert %}}


## Liquid staking

Autonity implements a liquid staking model, bringing benefits of:

- Capital efficiency: rewards from staking combined with the liquidity benefits of bonded stake that is transferable
- Composability: liquid stake tokens can be used in other protocols (e.g., as collateral)

### Liquid Newton

Liquid Newton is minted for [delegated](/glossary/#delegated) Newton stake bonded to a validator. On registration each validator has an ERC20 Liquid Newton contract created and deployed autonomously by the Autonity Protocol Contract (which maintains a registry of all Liquid Newton token contracts deployed).

It is important to note that stake bonded by the validator operator to its own validator - [self-bonded](/glossary/#self-bonded) stake - does _not_ result in minting of Liquid Newton. This is part of Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model.

Liquid Newton is validator-specific because there is a separate ERC20 token for each registered validator. Liquid Newton for a given validator is fungible, but Liquid Newton tokens of different validators are _not_ fungible with each other.

When [delegated](/glossary/#delegated) stake is bonded to a validator, Liquid Newton is minted for the Newton staked and the staked Newton is locked. The amount of Liquid Newton minted is subject to the amount of delegated stake the validator has at the time the bonding is applied. This conversion rate between Liquid Newton and Newton is maintained by a validator's Liquid Newton contract as the reference price for Newton bonding and unbonding operations. The  rate is determined by the ratio of issued liquid tokens over the total amount of stake tokens bonded to the validator.
             
As consequence, the Liquid Newton minted is subject to any accountability and omissions penalties applied to the validator resulting in a stake slashing event:

- If at the time of bonding a validator's [delegated](/glossary/#delegated) stake amount _has not_ been reduced by a stake slashing event, then Liquid Newton is minted `1:1` for the [delegated](/glossary/#delegated) Newton staked.
- However, if the validator's existing [delegated](/glossary/#delegated) stake amount is less than the supply of issued Liquid Newton, then Liquid Newton is minted in proportion to the validator's [delegated](/glossary/#delegated) stake remaining, resulting in a `>1:1` issuance of Liquid Newton for Newton staked.

This tokenomic mechanism ensures that a validator's Liquid Newton tokens remain fungible as they are issued over time: the amount of Liquid Newton issued on bonding has a value matching that of the Newton being bonded.

The Liquid Newton has staking reward entitlement rights, is freely transferable, and represents the Liquid Newton holder's share of the total stake bonded to the validator (i.e. the holder's share of the validator's Liquid Newton pool).

When stake is unbonded it is subject to an unbonding period and the holder's Liquid Newton is redeemed in proportion to its share of the Liquid Newton pool minus any slashing penalties applied. 

For example, if a validator had suffered a slashing penalty equivalent to 1% of its stake pool, then stake redemption value after slashing would be 99% of the original stake amount.


### Fundamental operations

Liquid Newton has fundamental operations for:

- Transfer: the holder can transfer ownership by sending to another network participant.
  - Upon receipt of Liquid Newton the holder becomes a delegator to the associated validator, and has a claim to some staked Newton.
- Redemption by unbonding: the holder can unbond stake from a validator and redeem for Newton stake token at any time subject to the unbonding period set for the chain. On unbonding:
  - Liquid Newton is burned for [delegated](/glossary/#delegated) stake unbonding
  - the bonded stake remains locked for the duration of an [unbonding period](/glossary/#unbonding-period) during which it is not transferrable and remains subject to any [slashing penalties](/glossary/#slashing-penalty) applied to the validator in that period. 
  
Stake redemption takes place at the end of the epoch in which the unbonding period falls. At this point the validator's stake pool is reduced by the unbonded amount and Newton is returned to the staker.

{{% alert title="Note" %}}It's important to note that Liquid Newton is validator-specific and as such is not 1:1 fungible with Liquid Newton bonded to a different validator. A validator may or may not have had [slashing penalties](/glossary/#slashing-penalty) applied and the redemption value of Liquid Newton may vary across validators according to their fault slashing history.{{% /alert %}}

### Transferring Liquid Newton

For details on how to transfer Liquid Newton from a stake delegation to another account, see:

- How to [Transfer Liquid Newton](/delegators/transfer-lntn/).

## Penalty-Absorbing Stake (PAS)

Autonity implements a [_penalty absorbing stake (PAS)_](/glossary/#penalty-absorbing-stake-pas) model where a validator's [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake when applying [slashing penalties](/glossary/#slashing-penalty) for accountability events.

Slashing priority is simply:

- [Self-bonded](/glossary/#self-bonded) stake is slashed as a first priority until exhausted. If the validator has unbonding stake, then the unbonding stake is slashed before bonded stake.
- [Delegated](/glossary/#delegated) stake is slashed as a second priority when the slashing amount exceeds the amount of self-bonded stake available. If the delegator has unbonding stake, then the unbonding stake and bonded stake are slashed _pro rata_ with equal priority.

In the PAS model self-bonded stake has a different risk profile to delegated stake _because it provides loss absorbing capital in the case of a slashing event_. For this reason, Liquid Newton is only minted for delegated stake to ensure validator liquid newton has a uniform risk profile.

{{% alert title="Note" %}}
Self-bonding stake by a validator puts "skin in the game" and is a public commitment to the operational integrity of a validator node by a validator operator. Potential stake delegators can use the amount of self-bonded stake of a validator as a decision factor when conducting due diligence before staking.
{{% /alert %}}

## Staking rewards

Staking rewards are a distribution of fee revenue entitlement to all holders of bonded stake actively backing consensus. Reward distribution takes place _pro-rata_ to the share of total stake bonded to validators in the consensus committee. The fee revenue comes from the _base fees_ charged for computing transactions included in blocks committed to the system ledger. The optional _priority fee_ of a transaction is not included in the rewards pool but awarded to the block proposer according to the EIP 1559 transaction fee mechanism.

{{% alert title="Note" %}}
For more detail on EIP 1559 and the distinction between _base fee_ and _priority fee_, see [Transaction fees](/concepts/system-model/#transaction-fees) in the System model.
{{% /alert %}}

Staking rewards are collected by protocol and accumulate in a protocol account as blocks are processed throughout a block epoch. The fees are out of circulation until epoch end, at which point the protocol distributes them to validator committee members. Rewards are then distributed to validator self-bonded and delegated stake holders _pro rata_ to their share of the validator's total bonded stake. After this distribution, the rewards become _claimable_ by stake delegators. Delegators then [claim rewards](/concepts/staking/#claiming-rewards) in a "pull" model, at the frequency they choose. 

As rewards are distributed, due fees are deducted from fee revenue by the protocol:

- Protocol treasury fee. A percentage of staking rewards is deducted for community funding. The fee goes to the Autonity Treasury account (See below), sent at epoch end when the epoch rewards are distributed to committee validators. The percentage value is set at genesis.  See `treasuryFee` parameter of the `config.autonity` object in the [Protocol](/reference/protocol#configautonity-object) section.

- Validator commission fees. The percentage commission rate charged by a validator to stakers delegating to the validator; essentially, the validator's service fee for providing a staking service to delegators. The fee is deducted from the validator's portion of the fee revenue before staking rewards are apportioned to the stake delegators _pro rata_ to their share of bonded stake. The percentage value is set at validator registration. See `delegationRate` parameter of the `config.autonity` object in the [Protocol](/reference/protocol#configautonity-object) section.

The remaining fee revenue is then distributed to stake delegators. 

### Reward distribution

The _priority fee_ reward is distributed to the validator proposing the block each block.

Stake delegation rewards are distributed to validator committee members at each block epoch end, at which point they become claimable by stake delegators.

### Claiming rewards

Fees accumulate until claimed by delegators in a pull-based model. Staking rewards are manually retrieved by calling the validator specific Liquid Newton contract. This incurs transaction costs, so stake delegators should allow fees to accumulate until they exceed the gas cost of claiming them. 

For details on how to claim and the functionality for claiming staking rewards, see:

- How to [Claim Staking Rewards](/delegators/claim-rewards/).

## Staking accounts

The protocol makes use of different accounts for fee revenue collection and distribution.

### Staker account

The `account` address submitting a bond or unbonding request. A staker can bond stake across as many validators as it chooses. The `msg.sender` address of the request is the account that receives the staker's due share of staking reward entitlements, and determines if the stake is [delegated](/glossary/#delegated) or [self-bonded](/glossary/#self-bonded):

- [delegated](/glossary/#delegated): `msg.sender` = any network [account](/glossary/#account) _except_ the validator `treasury` account
- [self-bonded](/glossary/#self-bonded): `msg.sender` = [validator `treasury` account](/concepts/staking/#validator-treasury-account)

### Validator treasury account

The validator operator's account address. The `treasury` is used as the account:

- Identifying the validator operator entity itself.
- For submitting transactions to protocol contracts to register and operate the validator's [node](/concepts/client/) and [oracle server](/concepts/oracle-server/).
- Receiving [staking rewards](/concepts/staking/#staking-rewards) from the protocol's reward distribution mechanism for distribution to the validator's stake delegators.
- Receiving [slashing rewards](/concepts/accountability/#slashing-rewards) distributed by the [accountability and fault detection protocol](/concepts/accountability/) for reporting provable faults committed by an offending validator failing to follow consensus rules.

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

At each epoch rollover there is an evaluation of the bonded stake. As the last block of an epoch is finalised then:

- Voting power changes affected by staking transitions are applied.
- The committee selection algorithm is run to choose members of the consensus committee for the upcoming epoch.

Bonding and unbonding requests submitted during an epoch are processed and committed to state in the next available block, but the effect of such staking transitions is applied at epoch end.  

{{< alert title="Note" >}}Consensus [committee member selection](/concepts/consensus/committee/#committee-member-selection) takes place at epoch end for computation and transactional efficiency.

Further, in an interoperability scenario where state is shared across chains, rather than submit a state proof of a new validator set every block, we only need to send a checkpoint of the validator set every epoch.{{< /alert >}}

### unbondingPeriod

The period of time bonded stake must wait before Newton is redeemed to the staker after processing a stake redeem (`unbond()`) transaction, defined as a number of blocks. The unbonding period can be any integer number > `0`, but _must_ be longer than the epoch period. There is no requirement for the unbonding period to be a multiple of the epoch period, just larger.

Stake remains at risk during the unbonding period; it is locked and in a non-transferrable state. This locking period is a protocol measure that gives the consensus protocol's accountability and omissions  mechanism time to identify and prove faults and apply penalties to bonded stake before stake is unlocked and redeemed. Byzantine behaviour cannot escape penalties by unbonding before a fault is detected.

The duration of the unbonding period is set at genesis by the `unbondingPeriod` parameter, see the [Protocol](/reference/protocol) parameter reference. The setting can be changed by governance calling the [`setUnbondingPeriod()`](/reference/api/aut/op-prot/#setunbondingperiod) function.

For example, an unbonding scenario with an epoch period of 30 blocks, an unbonding period of 120 blocks, and an unbonding request issued at block 15 in the epoch. The unbonding request is processed immediately and tracked in memory. The unbonding period expires at block 135. The unbonding is executed at the end of the epoch in which the unbonding period falls, block 150: the validator's voting power is reduced and due Newton is returned to the staker.

## Staking transitions

Staking transitions are the application of changes to stake bonded to validators. Newton stake token can be in [three states](/concepts/protocol-assets/newton/):
 - The default state of `unbonded`.
 - The locked state of `bonded`.
 - An intermediate state of `unbonding` when it is locked pending redemption.

Staking transitions are created by stake bonding and unbonding operations. Stake token is liable to protocol application of slashing penalties for accountability and omissions faults applied to validators whilst locked in the `bonded` and `unbonding` states.

Bonding and unbonding requests submitted during an epoch are processed and committed to state in the next available block, but the effect of such staking transitions is only applied at epoch end. Until epoch end they are maintained in memory in the `Staking` data structure and can be viewed using the `getBondingReq()`, `getUnbondingReq()` functions of the Autonity Protocol Contract. (See the [Autonity Contract Interface](/reference/api/aut/).)


### Bonding

Stake token is bonded to an active validator through a bonding operation. Once in a bonded state the token is locked and cannot be transferred to other stakeholders. If the stake token belongs to the validator then it is [self-bonded](/glossary/#self-bonded), otherwise the token is [delegated](/glossary/#delegated). The  [voting power](/glossary/#voting-power) of a validator is determined by the amount of stake bonded to it. 

On bonding Newton, the stake token is locked on execution of the `bond()` function and Liquid Newton is minted for [delegated](/glossary/#delegated) stake. Minting Liquid Newton is an autonomous protocol-only function. The resulting voting power change is tracked and the staking transition is applied at epoch end. From this point the stake is actively bonded and able to earn staking rewards. Note that a bond allocation cannot be changed after submission and before the bonding is applied at epoch end.

{{< alert title="Example" >}}
Alice sends `bond()` tx at time `T`, a block in an epoch. Newton is locked at `T`. The bonding request is tracked in memory for application at the end of the epoch. At this point, the validator's bonded stake is increased, and Liquid Newton is issued to Alice in the validator’s Liquid Newton ERC20 contract. Actual bonding is then executed at `T` + remainder of the epoch. Liquid Newton issuance is delayed and not tradable while bonding is pending.
{{< /alert >}}

Staking rewards are earned when a nominated validator is a consensus committee member. Bonding across more than one validator is allowed. The committee size is limited and staking rewards are limited to the number of validators in the current committee for the epoch.

{{< alert title="Note" >}}Stake can only be bonded to a registered validator in an `active` state. A bonding request to a validator in a `paused` state will revert. See [Validator pausing](/concepts/validator/#validator-pausing) and [Validator lifecycle](/concepts/validator/#validator-lifecycle).{{< /alert >}}

### Delegation

See [Bonding](/concepts/staking/#bonding) above.

### Unbonding

Stake is unbonded from a validator through an unbonding operation. Unbonding is subject to an [unbonding period](/concepts/staking/#unbondingperiod) during which it remains locked. The unbonding period applies irrespective of whether the nominated validator is a member of the consensus committee or not. 

Unbonding is triggered by a staker submitting an `unbond()` transaction. Unbonding can begin as soon as the unbond transaction request has been finalised. On processing the transaction the bonded stake token moves from `bonded` to the intermediate state of `unbonding`. The stake is still locked during the unbonding period. The unbonding request is captured and tracked in memory and the staking transition is applied at the end of the epoch in which the unbonding period expires: unbonding is applied, reducing the validator’s bonded stake amount and so applying the voting power change to the validator.

{{< alert title="Example" >}}
Alice sends an `unbond()` tx at time `T`, a block in an epoch. Liquid Newton is burned at `T` and unbonding begins in the next block, `T+1`. The unbonding request is tracked in memory for application at the end of the epoch in which the unbonding period falls. At this point, the validator's bonded stake is reduced and Newton is unlocked and redeemed to Alice. Actual unbonding is then executed at `T+1` + `unbondingPeriod` + remainder of the epoch in which the `unbondingPeriod` expires.
{{< /alert >}}

## Slashing

Bonded stake is subject to economic [slashing penalties](/concepts/accountability/#slashing-penalties) if misbehaviour by the staked validator node is detected by the [accountability and fault detection (AFD) protocol](/concepts/accountability/). The AFD protocol detects infractions of consensus rules by validators participating in [consensus](/glossary/#consensus) as [consensus committee](/glossary/#consensus-committee) members.

### Economic penalties

[Slashing penalties](/concepts/accountability/#slashing-penalties) are applied by autonomous protocol action at epoch end as voting power cannot change mid epoch.

Economic penalties vary in severity and are applied according to the type of fault detected and the risk created for network security.

See concept [Accountability and fault detection](/concepts/accountability/) and [slashing penalties](/concepts/accountability/#slashing-penalties) for protocol logic and penalty computation.

### Consequences for stake redemption

Bonding stake to a validator enters the staker in to a risk mutualisation model shared with the validator, i.e. if the validator is penalised then the staker may lose stake as consequence. This risk is realised when unbonding. Note, though, that Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model mitigates the risk to [delegated](/glossary/#delegated) stake.

As described in [Liquid Newton](/concepts/staking/#liquid-newton), a conversion rate between Liquid Newton and Newton is maintained by the protocol's tokenomics to ensure that a validator's Liquid Newton tokens remain 1:1 fungible. As consequence, a staker can redeem staked Newton in full _unless_ there has been a slashing event. In this circumstance, the stake redemption will be affected. 

To illustrate:

- 100 Newton is bonded at time `T`:
  - 100 Liquid Newton are issued, backed by 100 Newton
  - If a slashing penalty of 20 is applied to the validator at `T + 1`, then bonded stake is reduced to 80 and the 100 Liquid Newton issued are now backed by 80 Newton
  - The 100 Liquid Newton have a redemption value of 80 Newton 
- An additional 100 Newton are bonded post slashing at time `T + 2`:
  - 125 LNTN are issued, i.e. `current LNTN supply * new bonding amount / current bonded stake`

The LNTN issuance ratio has increased in light of the reduced bonded stake amount. This compensates for the lower redemption value of LNTN given the reduction in bonded stake, and maintains the fungibility of the validator's LNTN token.

To exemplify redemption in this scenario for a validator `V`:

|Time|Event|Amount|Liquid Newton Issued|Liquid Newton Supply|Newton Redeemed|Bonded Stake Amount|
|----|-----|------|-----------------------------|--------------------|---------------|-------------------|
|`T` |Bond Event |100 NTN|100|100||100|
|`T+1`|Slashing Event|20 NTN||100||80|
|`T+2`|Bond Event|100 NTN|125|225||180|
|`T+3`|Unbond Event|100 LNTN||125|80|100|
|`T+4`|Unbond Event|125 LNTN||0|100|0|


{{% alert title="Note" %}}In a trading context, if 100 Liquid Newton is purchased after this slashing event, then on redemption 80 Newton would be received. If the market price for Liquid Newton has dropped you would be purchasing it at a discount.{{% /alert %}}
