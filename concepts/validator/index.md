---
title: "Validator "
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
- Participate in the accountability and fault detection protocol, detecting and submitting accountability events committed by other committee members. See concept [accountability and fault detection protocol](/concepts/afd/).
- Participate in the oracle protocol, inputting raw price data and voting for aggregated median price data for currency pairs provided by the Autonity network during oracle [voting rounds](/glossary/#voting-round). See concept [oracle network](/concepts/oracle-network/).

As an entity contributing bonded stake to secure the network, a validator active in the [consensus committee](/concepts/consensus/committee/) is economically incentivised toward correct behaviour by [staking rewards](/concepts/staking/#staking-rewards) and [slashing rewards](/concepts/afd/#slashing-rewards). Validators are disincentivised from Byzantine behaviour by stake [slashing](/concepts/staking/#slashing) and penalty mechanisms implemented by an [accountability and fault detection protocol](/concepts/afd/). See [validator economics](/concepts/validator/#validator-economics) on this page for details.

### Validator prerequisites 

To operate as a validator node, the operator must operate Autonity [oracle server](/concepts/oracle-server/) software as an adjunct to its Autonity [full node](/concepts/client/) software.

Prerequisites for becoming a validator node operator are:

- A [validator enode URL](/concepts/validator/#validator-enode-url). A node joined to the network.
- An [oracle server](/concepts/oracle-network/) configured to collect external price data from off-chain data providers, and connected to the operator's validator node for on-chain submission of price reports.
- A [treasury account](/concepts/validator/#treasury-account). An EOA account that is the validator node operator's online identity and which:
  - Is the `msg.sender()` account used by the operator to submit state affecting transactions that govern the [validator lifecycle](/concepts/validator/#validator-lifecycle).
  - Will receive the validator's share of [staking rewards](/concepts/staking/#staking-rewards).

## Validator identity, accounts and keypairs
The validator makes use of different accounts and private/public [key pairs](/glossary/#key-pair) for validator lifecycle management (registration, pausing, reactivation), validator identity, staking rewards, consensus participation and cryptographic security. 

### P2P node keys: autonityKeys
The private/public key pair of the validator node. The `autonitykeys` file contains the private keys for the transaction and consensus message signing in the [communication layer](/concepts/architecture/#communication-layer). The keys are concatenated together to create a 128 character string:

- the first 64 characters are the `node key`: used for transaction signing with other network peer nodes
- the second 64 characters are the `consensus key`: used for consensus signing with other validators whilst participating in consensus

::: {.callout-tip title="Generating the `autonitykeys` file with `genAutonityKeys`" collapse="true"}

By default AGC will automatically generate an `autonitykeys` file containing your node key and consensus key within the `autonity` subfolder of the `--datadir` specified when [running the node](/node-operators/run-aut/).

The `autonitykeys` file can be generated using AGC's command-line option [`genAutonityKeys`](/reference/cli/agc/):

```
./build/bin/autonity genAutonityKeys  --writeaddress <KEYFILE_NAME>                
```

The command will generate an `autonitykeys` keyfile with the given `<KEYFILE_NAME>` and print to terminal the `Node Address`, `Node Public Key` and `Consensus Public Key` for the node.

For example:

```
Node Address:           0x550454352B8e1EAD5F27Cce108EF59439B18E249
Node Public Key:        0xcef6334d0855b72dadaa923ceae532550ef68e0ac50288a393eda5d811b9e81053e1324e637a202e21d04e301fe1765900bdd9f3873d58a2badf693331cb1b15
Consensus Public Key:   0x1aa83a28e235072ffdae41fg01ccc46e2b8d9dc16df3b6ff87ffa5ff6d7f90a2852649a60563237cd66a256f60a92e71
```

If you choose to generate the `autonitykeys` file and _do not store your key in the default location, then you must specify the path to where you are keeping your `autonitykeys` file using the `--autonitykeys` option in the run command.

:::


The private `autonitykeys` are used:

- By a node for:
  - transaction signing (`nodekey`), for negotiating an authenticated and encrypted connection between other network nodes at the devp2p layer in the [RLPx Transport Protocol](https://github.com/ethereum/devp2p/blob/master/rlpx.md).
  - consensus signing (`consensuskey`), for voting in consensus rounds whilst a member of the [consensus committee](/concepts/consensus/committee/)
- To generate the `proof` of enode ownership required for validator registration. The `proof` is generated using the [`genOwnershipProof`](/reference/cli/#command-line-options) command-line option of the Autonity Go Client. 

::: {.callout-tip title="Viewing the node and consensus private keys" collapse="true"}
The `autonitykeys` file is 128 characters and is a concatenation of the p2p node and consensus private keys each of which is 64 characters.

You can view the private keys individually by simply extracting the first or last 64 characters.

For example, to inspect the node key from your `autonitykeys` file, the simple command `head -c 64 <DIR_PATH>/autonitykeys`, where `<DIR_PATH>` is the path to your `autonitykeys` file, will print the private node key from the `autonitykeys` file to terminal.
:::

The corresponding public keys are used:

- As the identifier or 'node ID' of the node (in RLPx and node discovery protocols) (`node public key`).
- As the PUBKEY component of the enode URL as a hex string (`node public key`).
- To derive an ethereum format account that is then used to identify the validator node. See [validator identifier](#validator-identifier) (`node public key`).
- To verify the signature of consensus level network messages  (`consensus public key`).

::: {.callout-tip title="Viewing the node and consensus public keys with `autinspect`" collapse="true"}

The node and consensus public keys can be viewed using Autonity's `ethkey` cmd utility and the `autinspect` command to sinspect the `autonitykeys` file:

```
./build/bin/ethkey autinspect <KEYFILE>                
```

The command will return the `Node Address`, `Node Public Key` and `Consensus Public Key` of the node.

For example:

```
Node Address:           0x550454352B8e1EAD5F27Cce108EF59439B18E249
Node Public Key:        0xcef6334d0855b72dadaa923ceae532550ef68e0ac50288a393eda5d811b9e81053e1324e637a202e21d04e301fe1765900bdd9f3873d58a2badf693331cb1b15
Consensus Public Key:   0x1aa83a28e235072ffdae41fg01ccc46e2b8d9dc16df3b6ff87ffa5ff6d7f90a2852649a60563237cd66a256f60a92e71
```

Note that (a) the `Node public key` value minus the leading `0x` marker of the HEX string is the public key component of your [validator enode url](/concepts/validator/#validator-enode-url), and, (b) the `Node Address` value is the [validator identifier address](/concepts/validator/#validator-identifier).

:::

### Validator enode URL
The `enode` URL is the network address of the peer node operated by the validator. It provides the network location of the node client for p2p networking.

The enode URL format is described in the [ethereum Developers docs](https://ethereum.org/en/developers/docs/networking-layer/network-addresses/#enode).

It takes the basic form:

```
enode://PUBKEY@IP:PORT
```

The PUBKEY component is the public key from the P2P node key. The PUBKEY is static. The IP and PORT COMPONENTS may change over time (see [Migrating validator node to a new IP/Port address](/validators/migrate-vali/#migrating-validator-node-to-a-new-ipport-address)).

::: {.callout-tip title="Specifying enode query parameters for non-default IP and port settings" collapse="true"}

A node operator may choose to deploy their node with non-default IP and port settings. This is done in the enode URL scheme by specifying the required IP and port settings using optional `query` parameters. 

For how to do this, see the concept [System model, Networking](/concepts/system-model/#networking) and [Separate channels for transaction and consensus gossiping](/concepts/system-model/#separate-channels-for-transaction-and-consensus-gossiping).

:::

### Validator identifier

A unique identifier for the validator used as the validator identity in validator lifecycle management (registration, pausing, reactivation), staking, and accountability and omissions operations. It provides an unambiguous relationship between validator identity and node. For example, it is used to identify the validator in a bond stake function call.

The identity is created as an ethereum format account address, derived on registration by protocol logic from the PUBKEY component of the validator node's enode URL. It is stored in the `nodeAddress` field in the Validator data struct maintained in state.

Note that the identifier is the validator _node's_ on-chain identity and is distinct from the treasury account which is the validator _operator's_ account. 

::: {.callout-note title="Note" collapse="false"}
An account address rather than the PUBKEY of the [enode](/glossary/#enode) url is used to make use of the address datatype in function calls.
:::

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
3. Register as a validator. The validator's node is registered as a validator by the submission of registration parameters. The validator enters an `active` state.
4. Stake bonding. Stake is [bonded](/glossary/#bond) to the validator, either by the validator itself or by delegation from a [stake token holder](/glossary/#stakeholder). Once the validator has an amount of stake bonded to it, then it is eligible for inclusion in the [committee selection process](/concepts/consensus/committee/#committee-member-selection).
5. Selection to consensus committee. In the last block of an epoch, the [committee selection process](/concepts/consensus/committee/#committee-member-selection) is run and a validator may be selected to the consensus committee for the next epoch. Whilst a member of the consensus committee it is responsible for participating in (a) block validation, proposing and voting on new blocks, and (b) oracle price data submission and voting.
6. Jailed for accountability fault. If as a committee member the validator is found guilty for failing to adhere to consensus rules by the [Accountability fault detection protocol (AFD)](/concepts/afd/) or for failing to participate in consensus by the [Omission fault detection protocol (OFD)](/concepts/ofd/), then [jailing](/glossary/#jailing) may be applied. In this state the validator is [jailed and excluded from consensus committee selection](/concepts/validator/#jailing-and-exclusion-from-consensus-committee) for a computed duration.

    Depending on the gravity of the fault committed, jailing may be temporary or permanent and the validator will enter a [jailed](/glossary/#jailed) or [jailbound](//glossary/#jailbound) state:
    
    6.a. Temporary jailing: `jailed` or `jailedForInactivity` state. The validator is *impermanently* jailed for a number of blocks. The block height at which the jail period ends is recorded in the validator's state as the [`jailReleaseBlock`](/reference/api/aut/#response-26) property. After expiry of the [jail period](/glossary/#jail-period) the validator may be [re-activated](/concepts/validator/#validator-re-activation) to resume an `active` state.
    
    6.b. Permanent jailing: `jailbound` or `jailboundForInactivity` state. In this state the validator is *permanently* jailed and becomes [jailbound](/glossary/#jailbound). Permanent jailing is only applied for committing a fault with a 100% stake slashing penalty by [AFD](/concepts/afd/) or for committing an inactivity offence while on probation by [OFD](/concepts/ofd/).

7. Pause as a validator. The validator's node enters a `paused` state in which it is no longer included in the committee selection process. The validator is paused from active committee participation until [re-activated](/concepts/validator/#validator-re-activation). Stake is _not_ automatically unbonded.
8. Re-activate as a validator. The validator's node transitions from a `paused` or `jailed` state to resume an `active` state in which it is eligible for inclusion in the committee selection process.

Validator registration can take place at genesis initialisation or after genesis. In the genesis scenario, event steps 1-4 happen automatically as the network is initialised and the validator is included in the genesis run of the [committee selection process](/concepts/consensus/committee/#committee-member-selection). After genesis, all lifecycle steps are discrete and initiated by the validator node operator entity. 


### Eligibility for selection to consensus committee

A validator becomes eligible for selection to the [consensus committee](/concepts/consensus/committee/) when:

- It is registered and has an `active` state. Registration is complete: the validator's registration parameters and state are recorded in the `validators` data structure maintained by the [Autonity Protocol Contract](/concepts/architecture/#autonity-protocol-contract).
- It has non-zero bonded stake. The amount of stake bonded to the validator, recorded in the `validators` data structure, is greater than `0`.

Eligible validators are included in the committee selection algorithm. The algorithm is run at block [epoch](/glossary/#epoch) end to choose the committee for the upcoming epoch.

### Jailing and exclusion from consensus committee

A validator may be found guilty of failing to adhere to consensus rules by the [Accountability fault detection protocol (AFD)](/concepts/afd/) or of failing to participate in consensus by the [Omission fault detection protocol (OFD)](/concepts/ofd/) when a member of the consensus committee. In this case, depending on the type of fault committed, [jailing](/glossary/#jailing) for a computed number of blocks may be applied as part of a slashing penalty.

On entering a jailed state a validator is ignored by the consensus committee selection algorithm and cannot be elected as a consensus committee member. The duration of validator jailing may be *temporary* or *permanent* depending on the gravity of the committed accountability fault.  If *temporary*, the validator enters a [jailed](/glossary/#jailed) state. If *permanent*, the validator enters a [jailbound](/glossary/#jailbound) state.

See [Validator jailing](/concepts/validator/#validator-jailing) on this page.

## Stake bonding and delegation

Validators are staked with Autonity's [Newton](/concepts/protocol-assets/newton/) [stake token](/glossary/#stake-token). A genesis validator must [self-bond](/glossary/#self-bonded) stake at genesis. After genesis, a validator can [self-bond](/glossary/#self-bonded) their own Newton and have Newton staked to them by [delegation](/glossary/#delegation) from other Newton [stakeholders](/glossary/#stakeholder) at any time.

Autonity implements a [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model and a [liquid staking](/glossary/#liquid-staking) model.

In this model:

- [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas): [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake, ensuring the validator has "skin in the game" and incentivising reliable and honest validator operations and behaviour.
- [Liquid staking](/concepts/staking/#liquid-staking): [delegated](/glossary/#delegated) stake has [Liquid Newton](/concepts/protocol-assets/liquid-newton/) minted to the staker in proportion to the amount of Newton staked to a validator.

::: {.callout-note title="Note" collapse="false"}
Note that:
  - [Liquid Newton](/concepts/protocol-assets/liquid-newton/) is **not** minted for [self-bonded](/glossary/#self-bonded) stake. For rationale see [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas).
  - Staking rewards accrue to all bonded stake active in the current consensus committee; [delegated](/glossary/#delegated) and [self-bonded](/glossary/#self-bonded) stakers earn staking rewards _pro rata_ to their share of the validator's total bonded stake.
:::

Account addresses owning liquid newton and receiving staking reward revenue are:

- EOA accounts that have bonded [delegated](/glossary/#delegated) stake to a validator node, or have been recipients of a liquid newton transfer.
- Contract accounts that have been recipients of a liquid newton transfer from an EOA or a contract account.

For clarity, these are the `msgSender()` addresses of the account submitting [`registerValidator()`](/reference/api/aut/#registervalidator) and [`bond()`](/reference/api/aut/#bond) transactions to the Autonity Network.

Autonity implements an 'active epoch' staking model, applying staking transitions for bonding and unbonding at the end of each block epoch.

Stake is bonded and redeemed by Newton holders submitting transaction requests to the Autonity Protocol Contract. These requests are recorded in state on submission as `BondingRequest` and `UnbondingRequest` data structures in the Autonity Protocol Contract state, but there is a temporal delay in effect. Voting power cannot change mid-epoch and so staking transitions are applied at epoch end before the next committee selection is run.

Stake is bonded by submitting a bonding request transaction to the [`bond()`](/reference/api/aut/#bond) function and redeemed by the converse, a transaction to the [`unbond()`](/reference/api/aut/#unbond) function. Bonding and unbonding is an incremental process.

In the case of bonding: newton for the stake [delegation](/glossary/#delegation) amount is burned immediately on processing of the `bond()` function call and the corresponding amount of Newton is deducted from the stake delegator's Newton account balance. If the bonding request is included in block `T`, then actual bonding is executed at epoch end, i.e. `T` + remainder of the epoch. The validator's total bonded stake amount is then updated at epoch end when the staking transition is applied. When bonding liquid newton is minted for [delegated](/glossary/#delegated) stake only. The liquid newton is minted to the stake delegator's account at epoch end per the NTN-LNTN conversion rate for the validator (see [Staking, Liquid Newton](/concepts/staking/#liquid-newton)). Liquid newton is not minted for [self-bonded](/glossary/#self-bonded) stake.

In the case of unbonding: if the unbonding request is included in block `T`, then actual unbonding is then executed at `T` + [`unbondingPeriod`](/concepts/staking/#unbondingperiod) + remainder of the [`epoch`](/concepts/staking/#epoch) in which the unbonding period falls. At this point, the staker's due newton is redeemed and minted to the staker. The redemption flow varies depending on whether the unbonding is for [self-bonded](/glossary/#self-bonded) or [delegated](/glossary/#delegated) stake:

- For [self-bonded](/glossary/#self-bonded) stake, the unbonding request amount is stated in NTN and that amount of newton is redeemed at epoch end after unbonding period expiry.
- For [delegated](/glossary/#delegated) stake, the unbonding request amount is stated in LNTN and the amount of newton redeemed depends upon the NTN-LNTN conversion rate for the validator (see [Staking, Liquid Newton](/concepts/staking/#liquid-newton)). At the end of the [`epoch`](/concepts/staking/#epoch) in which the [`unbond()`](/reference/api/aut/#unbond) transaction was processed the Liquid Newton is burned and the validator's total bonded stake amount is reduced. The due amount of newton is redeemed at epoch end after unbonding period expiry.

## Validator economics
Validators active in the consensus committee are incentivised toward correct consensus behaviour by rewards and disincentivised from Byzantine behaviour by penalties.

Incentives are economic gains from [validator commission](/glossary/#delegation-rate) on [staking rewards](/concepts/staking/#staking-rewards), [slashing rewards from AFD](/concepts/afd/#slashing-rewards), block proposer rewards, and rewards from the accountability protocols ([AFD](/concepts/afd/), [OFD](/concepts/ofd/), [OAFD](/concepts/oafd/)) for correct participation in consensus and oracle price reporting.

Disincentives are economic losses incurred for proven validator faults committed while a member of the consensus committee. Disincentives are applied by the accountability protocols ([AFD](/concepts/afd/), [OFD](/concepts/ofd/), [OAFD](/concepts/oafd/)) and include stake [slashing](/concepts/staking/#slashing), barring from selection to the consensus committee ('[jailing](/glossary/#jailing)'), the loss of [staking rewards](/glossary/#staking-rewards) and [inflation rewards](/glossary/#inflation-rewards) . 

### Incentives
Validator economic returns are earned from:

- Staking rewards earned from their own [self-bonded](/glossary/#self-bonded) stake.
- Commission charged on [staking rewards](/glossary/#staking-rewards) on [delegated](/glossary/#delegated) stake per the [delegation rate](/glossary/#delegation-rate) they charge as commission.
- The priority fee 'tip' that may be specified in a transaction and which is given to the block proposer as an incentive for including the transaction in a block.
- Rewards from accountability protocols:
  - [AFD rewards](/concepts/afd/#slashing-rewards) earned for reporting slashed faults.
  - [OFD rewards](/concepts/ofd/#rewards) earned as a block proposer generating activity proofs that contain signatures for $> \frac{2}{3}$ of block quorum voting power.
  - [OAFD rewards](/concepts/oafd/#rewards) earned for oracle price reporting

Staking reward revenue potential is determined by the amount of stake bonded to them (their [voting power](/glossary/#voting-power)) and the frequency of their participation in the consensus committee. This is driven by:

-  The amount of stake the validator has bonded to it.
-  The committee size and number of registered validators.
-  The frequency with which the validator proposes blocks.
-  The amount of transaction revenue earned from transactions included in blocks committed when the validator is a member of the committee.
-  The validator's commission rate on delegated stake. Commission is a percentage amount deducted by a validator from staking rewards before rewards are distributed to the validator's stake delegators. The rate can be any value in the range `0 - 100%`. At registration all validators have commission set to a default rate specified by the Autonity network's genesis configuration. (See Reference [Genesis, `delegationRate`](/reference/genesis/#configautonity-object).) After registration the validator can modify its commission rate - see [Validator commission rate change](/concepts/validator/#validator-commission-rate-change) on this page.

| Economic gain | Receiving account | Distribution | Description |
|:-- |:--|:--|:--|
| staking rewards | [`treasury`](/concepts/validator/#treasury-account) account | epoch end | This is from their own self-bonded stake |
| commission revenue | [`treasury`](/concepts/validator/#treasury-account) account | epoch end | This is commission on staking rewards for the total bonded stake bonded to the validator taken according to the validator's commission rate |
| priority fee tips | [`validator identifier`](/concepts/validator/#validator-identifier) account | block finalisation | When a block proposer, priority fees for transactions included in the block are transferred directly to the validator node address, the [`validator identifier`](/concepts/validator/#validator-identifier) account |
| AFD slashing rewards |  [`treasury`](/concepts/validator/#treasury-account) account | epoch end | As the _reporting validator_ of an accountable fault a validator may receive slashing rewards. The staking rewards earned by the _offending validator_ for the epoch are forfeited and become the slashing rewards sent to the _reporting validator_. Amount determined by the [Slashing amount calculation](/concepts/afd/#slashing-amount-calculation). |
| OFD block proposer rewards | [`treasury`](/concepts/validator/#treasury-account) account | epoch end | The block proposer rewards earned by the validator for the epoch. Amount determined by the [Proposer reward calculation](/concepts/ofd/#proposer-reward-calculation) formula. |
| OAFD oracle rewards | [`treasury`](/concepts/validator/#treasury-account) account | epoch end | The ATN staking rewards and NTN inflation rewards earned for price reporting by the validator for the epoch. ATN is transferred to the validator's [`treasury`](/concepts/validator/#treasury-account) account and NTN inflation rewards are auto-bonded to the validator's [`treasury`](/concepts/validator/#treasury-account) account becoming [self-bonded](/glossary/#self-bonded) stake. Amount determined by the [Oracle reward calculation](/concepts/oafd/#oracle-reward-calculation) formula. |


### Disincentives
Validator economic losses are determined by any slashing penalties applied for accountable faults.

Disincentives are slashing penalties applied at epoch end and take the form of slashing of [bonded](/glossary/#bond) stake token according to Autonity's [Penalty-Absorbing Stake (PAS)](/glossary/#penalty-absorbing-stake-pas) model, loss of [staking rewards](/glossasry/#staking-rewards) and [inflation rewards](/glossary/#inflation-rewards), and loss of future earning opportunity by temporary or permanent barring from the consensus committee ('[jailing](/glossary/#jailing)').

The extent of the fine varies according to the severity of the fault committed. Slashing penalties may also apply temporary or permanent 'jailing', excluding the validator from future participation in the consensus committee.

For a table of the economic losses from applied slashing penalties see the accountability protocol concept pages:

- [Accountability fault detection protocol (AFD)](/concepts/afd/) [slashing penalties](/concepts/afd/#slashing-penalties).
- [Omission fault detection protocol (OFD)](/concepts/ofd/) [inactivity penalties](/concepts/ofd/#inactivity-penalties-1).
- [Oracle accountability fault detection protocol ()AFD)](/concepts/oafd/) [outlier penalties](/concepts/oafd/#outlier-penalties).

## Validator registration

A validator is registered at or after genesis by submitting registration parameters to the Autonity Network. Prerequisites for registration are:

-  The validator has a node address (an enode URL).
-  The validator has a connected [oracle server](/concepts/oracle-server/).
-  The validator node operator has a funded account on the network (to fund submitting the [validator registration](/validators/register-vali/) transaction).

A validator's registration is recorded and maintained as a state variable in a `Validator` data structure. (See [`registerValidator()`](/reference/api/aut/#registervalidator)).

### Genesis registration

At genesis the process is:

- Registration parameters for the genesis validator set are listed in the network's genesis configuration file (See`validators` struct):
   - `treasury` - the account address that will receive staking rewards the validator earns
   - `enode` - the enode URL of the validator node
   - `consensusKey` - the BLS public key from [`autonitykeys`](/concepts/validator/#p2p-node-keys-autonitykeys) used for P2P consensus
   - `oracleAddress` - the identifier address of the validator node's connected oracle server
   - `bondedStake` - the amount of stake the validator is bonding at genesis
   
   The amount of commission that the validator will charge on staking rewards earned from delegated stake defaults to the value specified by the `delegationRate` parameter in the genesis configuration file. This is a global value set for all validators at genesis.

   Example:

   ```
   {
	"enode": "enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310",
	"treasury": "0xe22617BD2a4e1Fe3938F84060D8a6be7A18a2ef9",
	"consensusKey": "0x776d2602de06e7x2d294c77d0706c772x077d242076e97cx44feex00e27d09707f7c7779j0e49il2etc4kd2ar39ov3a7",
	"oracleAddress": "0xD689E4D1061a55Fd9292515AaE9bF8a3C876047d",
	"bondedStake": 10000000000000000000000
   }
   ```

- Genesis of the Autonity Network is initialised and for each validator:
   - The `registerValidator()` function is called. The registration metadata is recorded in a `Validator` state variable data structure. A Liquid Newton ERC20 contract is deployed for the Validator and recorded in the Liquid Newton Contract Registry maintained by the Autonity Protocol Contract.
   - A `RegisteredValidator` event is emitted by the Autonity Protocol Contract.
   - The `bond()` function is called. The `bondedStake` amount is bonded to the validator's address and a corresponding amount of Liquid Newton minted to the validator's `treasury` account address. This is recorded in a `Staking` state variable data structure ready to be applied to the genesis state.

The validator is registered and eligible for selection to the genesis consensus committee.

Note that genesis registration requires the validator [self-bond](/glossary/#self-bonded) stake. The chain will not deploy if `bondedStake` for a genesis validator is null. This constraint guarantees genesis validators have stake and are eligible for selection to the consensus committee. This mitigates the risk of having no consensus committee for the genesis block and so a chain halt at initialisation!

### Post-genesis registration

After genesis the process is:

- Prospective validator submits a registration request transaction to the Autonity Protocol Public APIs, calling the [`registerValidator()`](/reference/api/aut/#registervalidator) function to submit the Validator registration parameters `enode` URL, `oracleAddress` [oracle identifier](/concepts/validator/#oracle-identifier), and a `proof` of node ownership generated from the private key of the validator node’s [P2P node keys: `autonityKeys`](/concepts/validator/#p2p-node-keys-autonitykeys), private key of the [oracle server key](/concepts/oracle-network/#oracle-server-key), and the validator's [`treasury` account](/concepts/validator/#treasury-account) address. The `treasury` account address used in the ownership proof is used as the `msgSender()` address when submitting the registration transaction. The registration metadata is recorded in a `Validator` state variable data structure. A Liquid Newton ERC20 contract is deployed for the Validator and recorded in the Liquid Newton Contract Registry maintained by the Autonity Protocol Contract.
- A `RegisteredValidator` event is emitted by the Autonity Protocol Contract.
- To bond stake to the validator, the staker submits a bonding request transaction to the Autonity Protocol Public APIs, calling the `bond()` function with its validator address (`enode`) and the bonded stake amount. This is recorded in a `Staking` state variable data structure ready to be applied at epoch end

The validator is registered and eligible for selection to the consensus committee.

::: {.callout-note title="Note" collapse="false"}
Note that registration after genesis allows a validator to register with zero bonded stake. The validator bonds stake after registration to become eligible for committee selection.
:::

## Validator accountability
Validators are held accountable for failing to adhere to consensus rules or submit accurate prices from their oracles when a member of the consensus committee. There are 3 accountability protocols:

- [Accountability fault detection protocol (AFD)](/concepts/afd/) for failing to follow consensus rules 
- [Omission fault detection protocol (OFD)](/concepts/ofd/) for failing to participate in consensus 
- [Oracle accountability fault detection protocol (OAFD)](/concepts/oafd/) for failing to submit accurate price reports to the oracle protocol on-chain. 

Depending on the severity of the accountability fault committed, a validator may suffer: stake slashing according to autonity's [Penalty-Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas) model, the loss of [staking rewards](/concepts/staking/#staking-rewards) and Newton [inflation rewards](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation), and [validator jailing](/concepts/validator/#validator-jailing).

Accountability protocols detect and track faults as they are committed during the epoch. Penalties for faults are then calculated and applied at the end of each epoch according to the accountability protocol. Accountability protocols will for each offending validator:

- Calculate the severity of the detected fault(s).
- Calculate economic disincentives and incentives for correct behaviour according to the accountability protocol.
- Apply accountability penalties - stake slashing, forfeiture of [staking rewards](/glossary/#staking-rewards) and [inflation rewards](/glossary/#inflation-rewards), temporary or permanent [validator jailing](/concepts/validator/#validator-jailing).

## Validator jailing
A validator can be jailed when serving as a member of the consensus committee as a penalty for failing to adhere to consensus rules by the [Accountability fault detection protocol (AFD)](/concepts/afd/) and for failing to participate in consensus by the [Omission fault detection protocol (OFD)](/concepts/ofd/). If an accountability penalty imposes [jailing](/glossary/#jailing), then this will be applied at epoch end by AFD or OFD. 

Jailing is either temporary or permanent:

- On temporary jailing the validator enters a `jailed` or `jailedForInactivity` state and is *impermanently* jailed for a number of blocks, the [jail period](/glossary/#jail-period). To get out of jail and resume an active state, the validator operator must [reactivate their validator](/concepts/validator/#validator-re-activation). This can be done at any point after expiry of the [jail period](/glossary/#jail-period). Returned to an `active` state, the validator is again eligible for selection to the consensus committee.
 
- On permanent jailing the validator enters a `jailbound` or `jailboundForInactivity` state and is *permanently* jailed. It becomes [jailbound](/glossary/#jailbound) and cannot get out of jail. Permanent jailing is only applied for committing a fault with a 100% stake slashing penalty by [AFD](/concepts/afd/) or for committing an inactivity offence while on probation by [OFD](/concepts/ofd/).

Note that:

- On jailing a validator is ignored by the committee selection algorithm run at the epoch end.
- New stake delegation transactions bonding stake are reverted until the validator resumes an `active` state. Pending stake delegation requests (bonding, unbonding) submitted _before_ a jailing event are still applied.
- The Validator's Liquid Newton remains transferrable and redeemable for Newton while the validator is jailed.
- The information that the validator is being jailed and barred from active validator duty is visible to delegators.


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

::: {.callout-note title="Note" collapse="false"}
Pausing has no impact on unbonding constraints. For example, if a validator pauses at time `T` and a staker immediately detects the `PausedValidator` event and submits an unbond transaction at time `T+1`, the unbonding period begins to count at `T+1`. Unbonding is then executed at `T+1 + unbondingPeriod + remainder of the epoch` in which `unbondingPeriod` falls.
:::

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
   - The validator's state is changed from its inactive state (`paused` or `jailed`) to `active`.
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

::: {.callout-note title="Note" collapse="false"}
A stake delegator can use the `CommissionRateChange` event to listen for upcoming commission rate changes. The effective block of the commission rate change can then be calculated from data points: the `changeCommissionRate` transaction commit block number, and the network `unbondingPeriod` and `epochPeriod` values.
:::
