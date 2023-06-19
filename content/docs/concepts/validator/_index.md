---
title: "Validator "
linkTitle: "Validator"
weight: 7
description: >
  The role of validators, the functions they perform, and their lifecycle
---

## Overview

This section describes the role of validators, prerequisites for becoming a validator, and the validator lifecycle (registration, pausing, reactivation).

A validator is an Autonity full node with bonded stake that is eligible for selection to an Autonity Network's consensus committee. As a member of the consensus committee its primary function is to ensure the integrity of system state.

To fulfil this purpose the validator participates in consensus computation with other members of the consensus committee:

- Proposing, voting, and validating new [blocks](/glossary/#block) in accordance with the rules of Autonity's implementation of the Tendermint consensus mechanism.
- Reporting infractions of consensus rules by committee members in the accountability and fault detection protocol.
- Submitting price reports and voting on aggregated median price data for selected currency pairs in oracle protocol voting rounds.

It has responsibilities to:

- Propose blocks of ordered transactions as the leader of a consensus round.
- Validate that proposed blocks contain only valid state transitions.
- Vote in consensus rounds, exchanging consensus messages with committee members as the consensus protocol executes.
- Maintain system state by committing new blocks to state as a consensus round completes.
- Propagate new blocks to the network at the end of a consensus round, sending the full block if round leader otherwise sending a new block announcement.
- Provide bonded stake to the Proof of Stake consensus mechanism, providing locked stake for network security economics.
- Participate in the accountability and fault detection protocol, detecting and submitting accountability events committed by other committee members. See concept [accountability and fault detection protocol](/concepts/accountability/).
- Participate in the oracle protocol, inputting raw price data and voting for aggregated median price data for currency pairs provided by the Autonity network during oracle [voting rounds](/glossary/#voting-round). See concept [oracle network](/concepts/oracle-network/).

As an entity contributing bonded stake to secure the network a validator active in the consensus committee is economically incentivised toward correct behaviour and disincentivised from Byzantine behaviour by stake [slashing](/concepts/staking/#slashing) and penalty mechanisms implemented by an [accountability and fault detection protocol](/concepts/accountability/). Consensus committee members are incentivised by [staking rewards](/concepts/staking/#staking-rewards), receiving a share of the transaction fee revenue earned for each block of transactions committed to system state, _pro rata_ to their share of bonded stake securing the system in that block. Consensus committee members are incentivised to report Byzantine behaviour by other committee members by [slashing rewards](/concepts/accountability/#slashing-rewards) for reporting accountability faults resulting in a penalty.

### Validator prerequisites 

To operate as a validator node the operator must operate Autonity [oracle server](/concepts/oracle-server/) software as an adjunct to its Autonity [full node](/concepts/client/) software.

Prerequisites for becoming a validator node operator are:

- A [validator enode URL](/concepts/validator/#validator-enode-url). A node joined to the network.
- An [oracle server](/concepts/oracle-network/) configured to collect external price data from off-chain data providers, and connected to the operator's validator node for on-chain submission of price reports.
- A [treasury account](/concepts/validator/#treasury-account). An EOA account that is the validator node operator's online identity and which:
  - Is the `msg.sender()` account used by the operator to submit state affecting transactions that govern the [validator lifecycle](/concepts/validator/#validator-lifecycle).
  - Will receive the validator's share of [staking rewards](/concepts/staking/#staking-rewards).

## Validator identity, accounts and keypairs
The validator makes use of different accounts and private/public [key pairs](/glossary/#key-pair) for validator lifecycle management (registration, pausing, reactivation), validator identity, staking rewards, consensus participation and cryptographic security. 

### P2P node key
The private/public key pair of the validator node.

The private key is used:

- By a node for negotiating an authenticated and encrypted connection between other network nodes at the devp2p layer in the [RLPx Transport Protocol <i class='fas fa-external-link-alt'></i>](https://github.com/ethereum/devp2p/blob/master/rlpx.md).
- To generate the `proof` of enode ownership required for validator registration. The `proof` is generated using the [`genEnodeProof`](/reference/cli/#command-line-options) command-line option of the Autonity Go Client. 

The public key is used:

- As the identifier or 'node ID' of the node (in RLPx and node discovery protocols).
- As the PUBKEY component of the enode URL as a hex string.
- To verify the signature of consensus level network messages.
- To derive an ethereum format account that is then used to identify the validator node. See [validator identifier](#validator-identifier).

{{< alert title="Note" >}}The private key can be used by Autonity’s `bootnode` utility to derive the hex string used in the `enode` URL. (See Networking Options  `nodekey` and `nodekeyhex` in [Autonity command-line options](/reference/cli/#usage) and, for reference,  the ethereum stack exchange article [how to produce enode from node key <i class='fas fa-external-link-alt'></i>](https://ethereum.stackexchange.com/questions/28970/how-to-produce-enode-from-node-key).){{< /alert >}}


### Validator enode URL
The `enode` URL is the network address of the peer node operated by the validator. It provides the network location of the node client for p2p networking.

The enode URL format is described in the [ethereum Developers docs <i class='fas fa-external-link-alt'></i>](https://ethereum.org/en/developers/docs/networking-layer/network-addresses/#enode).

It takes the form:

```
enode://PUBKEY@IP:PORT
```

The PUBKEY component is the public key from the P2P node key. The PUBKEY is static. The IP and PORT COMPONENTS may change over time.

The PUBKEY component is used to derive an ethereum format account address that is used as the validator identity in validator registration, staking, and accountability and omissions operations - see validator identifier.

### Validator identifier

A unique identifier for the validator used as the validator identity in validator lifecycle management (registration, pausing, reactivation), staking, and accountability and omissions operations. It provides an unambiguous relationship between validator identity and node. For example, it is used to identify the validator in a bond stake function call.

The identity is created as an ethereum format account address, derived on registration by protocol logic from the PUBKEY component of the validator node's enode URL. It is stored in the `nodeAddress` field in the Validator data struct maintained in state.

Note that the identifier is the validator _node's_ on-chain identity and is distinct from the treasury account which is the validator _operator's_ account. 

{{< alert title="Note" >}}An account address rather than the PUBKEY of the [enode](/glossary/#enode) url is used to make use of the address datatype in function calls.{{< /alert >}}

### Treasury account

The `treasury` account is the Autonity Network account used by a validator to submit transactions for validator lifecycle management transactions and to receive its share of staking rewards. It uses a different private/public key pair with respect to the p2p node key. This is because those keys may have different security requirements, as well as because multiple validators could use the same treasury account.

### Oracle identifier

A unique identifier for the Autonity Oracle Server providing price data reports to the validator node.

The identity is created as an ethereum format account address and provided as a validator registration parameter. For more information see concept [oracle network](/concepts/oracle-network/) and [oracle identifier](/concepts/oracle-network/#oracle-identifier). 

## Validator lifecycle

Validator lifecycle management comprises registration, participation in the consensus committee, jailing for accountability faults, pausing, and reactivation.

The sequence of lifecycle events for a validator is:

1. Join the network. The validator's main client software is admitted to the P2P network as a peer node, syncing state on connection.
2. Configure oracle server and data sources. Pre-validator registration, the validator installs the oracle server software and configures data sources for price data provision. 
3. Register as a validator. The validator's node is registered as a validator by the submission of registration parameters.
4. Stake bonding. Stake is bonded to the validator, either by the validator itself or by delegation from a stake token holder. Once the validator has an amount of stake bonded to it, then it is eligible for inclusion in the committee selection process.
5. Selection to consensus committee. In the last block of an epoch, the committee selection process is run and a validator may be selected to the consensus committee for the next epoch. Whilst a member of the consensus committee it is responsible for participating in (a) block validation, proposing and voting on new blocks, and (b) oracle price data submission and voting.
6. Jailed for accountability fault. If a validator is found guilty by the [accountability and fault detection protocol](/concepts/accountability/) of failing to adhere to consensus rules as a member of the consensus committee, then it may enter a `jailed` state. In this state the validator is [jailed and excluded from consensus committee selection](/concepts/validator/#jailing-and-exclusion-from-consensus-committee) for a computed [jail period](/glossary/#jail-period). After expiry of the jail period the validator may be reactivated to resume an `active` state.
7. Pause as a validator. The validator's node enters a `paused` state in which it is no longer included in the committee selection process. The validator is paused from active committee participation until reactivated. Stake is _not_ automatically unbonded.
8. Reactivate as a validator. The validator's node transitions from a `paused` or `jailed` state to resume an `active` state in which it is eligible for inclusion in the committee selection process.

Validator registration can take place at genesis initialisation or after genesis. In the genesis scenario, event steps 1-4 happen automatically as the network is initialised and the validator is included in the genesis run of the committee selection process. After genesis, all lifecycle steps are discrete and initiated by the validator node operator entity. 


### Eligibility for selection to consensus committee

A validator becomes eligible for selection to the consensus committee when:

- It is registered and has an `active` state. Registration is complete: the validator's registration parameters and state are recorded in the `validators` data structure maintained by the Autonity Protocol Contract.
- It has non-zero bonded stake. The amount of stake bonded to the validator, recorded in the `validators` data structure, is greater than `0`.

Eligible validators are included in the committee selection algorithm. The algorithm is run at block epoch end to choose the committee for the upcoming epoch.

### Jailing and exclusion from consensus committee

A validator may be found guilty by the [accountability and fault detection protocol](/concepts/accountability/) of failing to adhere to consensus rules when a member of the consensus committee. In this case, depending on the type of fault committed, [jailing](/glossary/#jailing) for a computed number of blocks (a '[jail period](/glossary/#jail-period)') may be applied as part of a slashing penalty. On jailing the validator:

- is transitioned by protocol from an `active` to a `jailed` state
- is barred from consensus committee selection until the [jail period](/glossary/#jail-period) has expired and the validator has been reactivated to an `active` state
- suffers stake slashing according to autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model and/or loss of  [staking rewards](/concepts/staking/#staking-rewards) earned as a member of the current consensus committee

To get out of jail at the end of the [jail period](/glossary/#jail-period), the validator operator must [reactivate their validator node](/concepts/validator/#validator-re-activation) to (a) transition to an `active` state, and (b) resume eligibility for selection to the consensus committee.

## Stake bonding and delegation

Validators are staked with Autonity's [Newton](/concepts/protocol-assets/newton/) stake token. A genesis validator must bond stake at genesis. After genesis, a validator can bond their own Newton and have Newton staked to them by [delegation](/glossary/#delegation) from other Newton token holders at any time.

Autonity implements a [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model and a [liquid staking](/concepts/staking/#liquid-staking) model.

In this model:

- [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas): [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake, ensuring the validator has "skin in the game" and incentivising reliable and honest validator operations and behaviour.
- [Liquid staking](/concepts/staking/#liquid-staking): [delegated](/glossary/#delegated) stake has [Liquid Newton](/concepts/protocol-assets/liquid-newton/) minted to the staker in proportion to the amount of Newton staked to a validator.

{{% alert title="Note" %}}
Note that:
  - [Liquid Newton](/concepts/protocol-assets/liquid-newton/) is **not** minted for [self-bonded](/glossary/#self-bonded) stake. For rationale see [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas).
  - Staking rewards accrue to all bonded stake active in the current consensus committee; [delegated](/glossary/#delegated) and [self-bonded](/glossary/#self-bonded) stakers earn staking rewards _pro rata_ to their share of the validator's total bonded stake.
{{% /alert %}}

Account addresses owning liquid newton and receiving staking reward revenue are:

- EOA accounts that have bonded [delegated](/glossary/#delegated) stake to a validator node, or have been recipients of a liquid newton transfer.
- Contract accounts that have been recipients of a liquid newton transfer from an EOA or a contract account.

For clarity, these are the `msgSender()` addresses of the account submitting `registerValidator()` and `bond()` transactions to the Autonity Network.

Autonity implements an 'active epoch' staking model, applying staking transitions for bonding and unbonding at the end of each block epoch.

Stake is bonded and redeemed by Newton holders submitting transaction requests to the Autonity Protocol Contract. These requests are recorded in state on submission as `Staking` data structures in the Autonity Protocol Contract state, but there is a temporal delay in effect. Voting power cannot change mid-epoch and so staking transitions are applied at epoch end before the next committee selection is run.

Stake is bonded by submitting a bonding request transaction to the `bond()` function and redeemed by the converse, to the `unbond()` function. In the bonding scenario, liquid newton is minted for [delegated](/glossary/#delegated) stake and the Validator's total bonded stake amount updated in the final block of the epoch. Stake redemption by contrast is an incremental process: liquid newton for [delegated](/glossary/#delegated) stake is burned immediately on processing of the `unbond()` function call, the validator's total bonded stake amount is updated at epoch end, the newton is issued (i.e. minted) to the staker at the end of the unbonding period. If the unbonding request is included in block `T`, then actual unbonding is then executed at `T` + `unbondingPeriod` + remainder of the epoch in which the unbonding period falls. At this point, the staker's due newton is minted to them.


## Validator economics

Validator economic returns are determined by the amount of stake bonded to them, their participation in the consensus committee, commission rate, and any slashing penalties applied for accountability and omissions.

Staking reward revenue is proportionate to the validator's share of the stake active in a consensus round in which it participates. Staking rewards are distributed to consensus committee members _pro rata_ to the amount of stake they have at stake. Validators can earn from:

- Staking rewards earned from their own [self-bonded](/glossary/#self-bonded) stake.
- Commission charged on [delegated](/glossary/#delegated) stake per the delegation rate they charge as commission.
- The priority fee 'tip' that may be specified in a transaction and which is given to the block proposer as an incentive for including the transaction in a block.
- [Slashing rewards](/concepts/accountability/#slashing-rewards) earned for reporting slashed faults in the [accountability and fault detection](/concepts/accountability/) protocol.

Staking reward revenue potential is determined by the frequency with which a validator is an active member of the consensus committee. This is driven by:

-  The amount of stake the validator has bonded to it.
-  The committee size and number of registered validators.
-  The frequency with which the validator proposes blocks.
-  The amount of transaction revenue earned from transactions included in blocks committed when the validator is a member of the committee.
-  The validator's commission rate. The percentage amount deducted by a validator from staking rewards before rewards are distributed to the validator's stake delegators. The rate can be any value in the range `0 - 100%`. At registration all validators have commission set to a default rate specified by the Autonity network's genesis configuration. (See Reference [Genesis, `delegationRate`](/reference/genesis/#configautonity-object).) After registration the validator can modify its commission rate - see [Validator commission rate change](/concepts/validator/#validator-commission-rate-change) on this page.

Bonded stake may be slashed and/or staking rewards may be reduced or forfeited by slashing penalties applied to the validator for accountable faults. The extent of the fine varies according to the severity of the fault committed. See Concept [accountability and fault detection protocol](/concepts/accountability/) and [slashing economics](/concepts/accountability/#slashing-economics).

## Validator registration
A validator is registered at or after genesis by submitting registration parameters to the Autonity Network. Prerequisites for registration are:

-  The validator has a node address (an enode URL).
-  The validator has a connected [oracle server](/concepts/oracle-server/).
-  The validator has a funded account on the network.

A validator's registration is recorded and maintained as a state variable in a `Validator` data structure. (See [`registerValidator()`](/reference/api/aut/#registervalidator)).

### Genesis registration
At genesis the process is:

- Registration parameters for the genesis validator set are listed in the network's genesis configuration file (See`validators` struct):
   - `treasury` - the account address that will receive staking rewards the validator earns.
   - `enode` - the enode URL of the validator node.
   - `oracleAddress` - the identifier address of the validator node's connected oracle server.
   - `bondedStake` - the amount of stake the validator is bonding at genesis.
   - `delegationRate` - the amount of commission that the validator will charge on staking rewards earned from delegated stake. This is a global value set for all validators, specified by the `delegationRate` parameter in the genesis configuration file.

   Example:

   ```
   {
    "treasury": "0xd0A5fB6A3CBD7cB0328ae298598527E62bE90A0F",
    "enode": "enode://bdbae1dede11147d0f1de2b6339a25fae9d46edfbeb48b3441d8dfff5d396bcb0b99f2ade05bf37239451f9a  dc60015f7a7b744321ea9a845b7c3a1f1ebd73e3@127.0.0.1:5003",
    "oracleAddress":"0x636d3D9711F0f3907313dC5E2Aa08e73c0608A03",
   "bondedStake": 10000
   },
   ```

- Genesis of the Autonity Network is initialised and for each validator:
   - The `registerValidator()` function is called. The registration metadata is recorded in a `Validator` state variable data structure. A Liquid Newton ERC20 contract is deployed for the Validator and recorded in the Liquid Newton Contract Registry maintained by the Autonity Protocol Contract.
   - A `RegisteredValidator` event is emitted by the Autonity Protocol Contract.
   - The `bond()` function is called. The `bondedStake` amount is bonded to the validator's address and a corresponding amount of Liquid Newton minted to the validator's `treasury` account address. This is recorded in a `Staking` state variable data structure ready to be applied to the genesis state.

The validator is registered and eligible for selection to the genesis consensus committee.

Note that genesis registration requires the validator [self-bond](/glossary/#self-bonded) stake. The chain will not deploy if `bondedStake` for a genesis validator is null. This constraint guarantees genesis validators have stake and are eligible for selection to the consensus committee. This mitigates the risk of having no consensus committee for the genesis block and so a chain halt at initialisation!

### Post-genesis registration

After genesis the process is:

- Prospective validator submits a registration request transaction to the Autonity Protocol Public APIs, calling the `registerValidator()` function to submit the Validator registration parameters `enode` URL, `oracleAddress` [oracle identifier](/concepts/validator/#oracle-identifier), and a `proof` of node ownership generated from the private key of the validator node’s [P2P node key](/concepts/validator/#p2p-node-key) and the validator’s [oracle server key](/concepts/oracle-network/#oracle-server-key). The transaction `msgSender()` address is used for the validator's `treasury` parameter value. The registration metadata is recorded in a `Validator` state variable data structure. A Liquid Newton ERC20 contract is deployed for the Validator and recorded in the Liquid Newton Contract Registry maintained by the Autonity Protocol Contract.
- A `RegisteredValidator` event is emitted by the Autonity Protocol Contract.
- To bond stake to the validator, the staker submits a bonding request transaction to the Autonity Protocol Public APIs, calling the `bond()` function with its validator address (`enode`) and the bonded stake amount. This is recorded in a `Staking` state variable data structure ready to be applied at epoch end

The validator is registered and eligible for selection to the consensus committee.

{{% alert title="Note" %}}Note that registration after genesis allows a validator to register with zero bonded stake. The validator bonds stake after registration to become eligible for committee selection.{{% /alert %}}

## Validator jailing

A validator can be jailed by protocol as a penalty for failing to adhere to consensus rules when serving as a member of the consensus committee. If a slashing penalty imposes [jailing](/glossary/#jailing), this will be applied at epoch end when the penalty is processed. 

In this state:

- It is ignored by the committee selection algorithm run at the epoch end.
- New stake delegations are not accepted.
- The information that the validator is being jailed and barred from active validator duty is visible to delegators.

Note that:

- Pending stake delegation requests (bonding, unbonding) submitted _before_ the jailing are still applied.
- The Validator's Liquid Newton remains transferrable and redeemable for Newton while the validator is jailed.

At end of epoch the [accountability and fault detection protocol](/concepts/accountability/) processes slashable faults and for each offending validator:

- Computes the [slashing amount](/concepts/accountability/#autonity-slashing-amount-calculation) and [jail period](/glossary/#jail-period), the count of blocks for which the validator is 'in jail' and excluded from selection to the consensus committee.
- Applies the slashing amount fine.
- Changes the validator's state from `active` to `jailed`.
- A `SlashingEvent` event is emitted detailing: validator identifier address, slashing amount, jail release block: the block number at which the jail period expires.

The validator is jailed and ignored by the committee selection algorithm. Stake delegation transactions bonding stake are reverted until the validator resumes an `active` state.

To get out of jail and resume an active state, the validator must [reactivate their validator](/concepts/validator/#validator-re-activation). This can be done at any point after expiry of the [jail period](/glossary/#jail-period). Returned to an `active` state, the validator is again eligible for selection to the consensus committee.


## Validator pausing

A validator can pause from active committee participation by submitting a pause request to the Autonity Network. Once the pause request has been processed the validator's state changes from `active` to `paused`. In this state:

- It is ignored by the committee selection algorithm run at the epoch end.
- New stake delegations are not accepted.
- That the validator is pausing from active validator duty is visible to potential delegators (from event data).

Note that:

- Pending stake delegation requests (bonding, unbonding) submitted _before_ the pause request was processed are still applied.
- The Validator's Liquid Newton remains transferrable and redeemable for Newton while a pause request is 'pending' application at effective block and after pausing has been 'applied'.
- Unbonding of stake from the validator is _not_ automated and has to be initiated by the staker.

The process is:

- The validator operator entity submits a pause request transaction to the Autonity Protocol Public APIs, calling the [`pauseValidator()`](/reference/api/aut/#pausevalidator) function, submitting the transaction from the account used to register the validator (validator `treasury` account) and passing in the validator identifier address.
- Transaction processed and committed to state:
   - The validator's state is changed from `active` to `paused`.
   - A `PausedValidator` event is emitted detailing: validator operator entity treasury address, validator identifier address, effective block height at which pausing takes effect: projected block number for epoch end.
- Pause request tracked for execution until effective block height: epoch end.
- Validator pausing is applied at epoch end before the next committee selection is run.

The validator is paused and ignored by the committee selection algorithm. Stake delegation transactions bonding stake are reverted until the validator resumes an `active` state.

{{< alert title="Note" >}}Pausing has no impact on unbonding constraints. For example, if a validator pauses at time `T` and a staker immediately detects the `PausedValidator` event and submits an unbond transaction at time `T+1`, the unbonding period begins to count at `T+1`. Unbonding is then executed at `T+1 + unbondingPeriod + remainder of the epoch` in which `unbondingPeriod` falls.{{< /alert >}}

## Validator re-activation

A validator can re-activate and resume active committee participation by submitting an activate request to the Autonity network. Once the activate request has been submitted the validator's state changes from its inactive state (`paused` or `jailed`) to `active`. In this state:

- It is again included by the committee selection algorithm run at the epoch end.
- New stake delegations are accepted.
- That the validator is resuming active validator duty is visible to potential delegators.

Note that:

- New stake delegation requests bonding stake to the validator submitted _after_ the activate request was processed no longer revert and are accepted.

The process is:

- The validator operator entity submits an activate request transaction to the Autonity Protocol Public APIs, calling the [`activateValidator()`](/reference/api/aut/#activatevalidator) function, submitting the transaction from the account used to register the validator (validator `treasury` account) and passing in the validator identifier address.
- Transaction processed and committed to state:
   - The validator's state is changed from `paused` to `active`.
   - An `ActivatedValidator` event is emitted detailing: validator operator entity treasury address, validator identifier address, effective block height at which re-activation takes effect: projected block number for epoch end.

The validator is active, able to accept new stake delegations, and once again eligible for selection to the consensus committee.

## Validator commission rate change

A validator operator can modify its validator commission rate from the global default rate set for the validator on initial registration  (see Reference [Genesis, `delegationRate`](/reference/genesis/#configautonity-object)) by submitting a commission rate change request to the Autonity Network.

Commission rate changes are subject to the same temporal [unbonding period](/concepts/staking/#unbondingperiod) constraint as staking transitions. This gives the stake delegator protection from validator commission rate changes intra-epoch.

The process is:

- The validator operator entity submits a commission rate change request transaction to the Autonity Protocol Public APIs, calling the [`changeCommissionRate()`](/reference/api/aut/#changecommissionrate) function, submitting the transaction from the account used to register the validator (validator `treasury` account) and passing in the validator identifier address and the new commission rate in basis points (bps).
- Transaction processed and committed to state:
   - The commission rate change request is tracked in memory and the [unbonding period](/concepts/staking/#unbondingperiod) lock constraint begins.
   - The rate change is applied at the end of the epoch in which the unbonding period expires as the last block of the epoch is finalised.
   - A `CommissionRateChange` event is emitted detailing: validator identifier address, new rate value.

{{< alert title="Note" >}}
A stake delegator can use the `CommissionRateChange` event to listen for upcoming commission rate changes. The effective block of the commission rate change can then be calculated from data points: the `changeCommissionRate` transaction commit block number, and the network `unbondingPeriod` and `epochPeriod` values.
{{< /alert >}}

