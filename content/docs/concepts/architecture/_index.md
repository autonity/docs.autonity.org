
---
title: "Architecture "
linkTitle: "Architecture"
weight: 1
description: >
  Architecture of Autonity - protocol primitives and system model
---

Autonity is an EVM-based blockchain which extends the Ethereum protocol to add Autonity-specific functionality to optimise the creation and maintenance of decentralised markets. This section documents the details of these Autonity extensions. An understanding of the core Ethereum principles is assumed.

Autonity inherits from Ethereum:

- The blockchain structure comprising the distributed ledger of the system.
- Peer-to-peer networking protocols forming the communication layer of the system for message broadcast between network peer nodes.
- The EVM and smart contract technology comprising the application level of the system.

Autonity extends Ethereum at three logical layers:

- Application layer: protocol smart contracts:
	- **Autonity Protocol Contract** implementing protocol primitives for governance, tokenomics, liquid staking, and staking rewards distribution.
	- **Liquid Newton** contracts for validator-specific liquid stake tokens.
	- **Autonity Oracle Contract** implementing protocol primitives for computing median price data and managing the set of currency pairs for which Autonity's oracle network provides price data.
	
	Autonity Protocol and Oracle smart contracts are part of the client binary. _Liquid newton_ smart contracts are deployed on validator registration.

- Consensus layer: blockchain consensus provided by the **Proof of Stake Tendermint BFT** protocol. Blocks are proposed by validators and selected by the committee for inclusion in the blockchain, with finality. The consensus mechanism enables dynamic committee selection using a stake-weighting algorithm, maximising the amount of stake securing the system.
- Communication layer: peer-to-peer networking in the **communication layer** is extended with new block and consensus messaging propagation primitives, to enable the gossiping of information among validators and participant nodes.

## Autonity Protocol Contract
The contract implementing much of the Autonity protocol extensions, including primitives for governance, staking, validators, consensus committee selection, and staking reward distribution.

The Autonity Protocol Contract is deployed at network genesis using the null or 'zero' account address `0x0000000000000000000000000000000000000000` as the [deployer](/reference/api/aut/#deployer) address. The protocol contract's account address is computed at contract creation using the standard Ethereum practice for contract account creation: derived from the account address of the creator and the count of transactions sent from that account. As these are constant (the `0` address and an account nonce always equal to `0`) the Autonity Protocol Contract address for a network is deterministic and will always be `0xBd770416a3345F91E4B34576cb804a576fa48EB1`.

The contract stores [protocol parameters](/reference/protocol/) that specify economic, consensus, and governance settings of an Autonity network. Protocol parameters are initialised at network [genesis](/reference/genesis/) in the genesis state provided by the client's config for connecting to public Autonity networks, or a custom [genesis configuration file](/reference/genesis/#genesis-configuration-file) if running a local development network.

Many of the Autonity Protocol Contract functions can be called by all participants, such as those for bonding and unbonding stake, and for reading protocol parameters.  Some functions are restricted to the `operator` account, such as those related to governance of the network.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Autonity Contract Interface](/reference/api/aut/), governance under [Governance and Protocol Only Reference](/reference/api/aut/op-prot/).

### Governance

Autonity system governance is executed:

- At genesis, when the blockchain is initialised with the genesis state.
- After genesis by the operator governance account, by calling the restricted functions of the protocol contract.

Governance operations are used to modify protocol parameterisation set in the genesis system state and enable an Autonity network to evolve dynamically over time. System protocol parameters modifiable by governance include:

- Governance operator account address.
- Minimum base fee for submitting transactions to the network.
- Consensus committee size and block epoch period.
- Stake delegation unbonding period.
- Protocol treasury account address for community funds and the treasury fee.
- The set of currency pairs for which median price data is provided by the oracle network.

For all parameter definitions and the subset of modifiable parameters see the [Protocol Parameter](/reference/protocol/) reference.

### Staking
The Autonity Protocol Contract manages liquid staking,  maintaining the ledger of _newton_ stake token in the system and triggering the deployment of validator-specific _liquid newton_ contracts. The contract implements logic to:

- Maintain the ledger of _newton_ stake token in the system, implementing the ERC20 token contract interface.
- Facilitate liquid staking by triggering the deployment of validator-specific _liquid newton_ ERC20 contracts as validators are registered on the system.
- Provide stake holders operations to bond and unbond stake from validators, managing _newton_ staking transitions and _liquid newton_ emission and redemption.
- Provide stake holders standard ERC20 token operations for accessing the _newton_ stake token ledger and metadata.
- Manage staking transitions, tracking bond and unbond requests until staking transitions are applied at epoch end.
- Trigger computation of median price data at the end of an oracle voting round by the [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract).

To learn more about the concept see [Staking](/concepts/staking/).

### Validators
The Autonity Protocol Contract implements logic to manage validator registration and lifecycle on the system:

- Provides public contract functions to register new validators and query for existing registered validators.
- Trigger the deployment of validator-specific _liquid newton_ ERC20 contracts as validators are registered on the system.
- Provide lifecycle management functions, allowing validator operators to manage their validator and its lifecycle: pause and reactive validator, change commission rate.

To learn more about the concept see [Validators](/concepts/validator/).

### Committee selection
Computing the committee is a protocol only function. As the last block of an epoch is finalised, this function is executed to determine the committee for the following epoch.

The committee is selected from the registered validators maintained in system state by the Autonity contract. Validators are ranked by bonded stake, those with the highest stake being selected to the available committee membership slots. This stake weighting maximises the amount of stake securing the system in each new committee. Each block header records the consensus committee members that voted to approve the block.

To learn more about the concept see [Consensus](/concepts/consensus/) and  [Committee](/concepts/consensus/committee/).

### Reward distribution

Validators and stake delegators are incentivised by the distribution of staking rewards to stake bonded to the active consensus committee. Rewards are paid in Auton.

Rewards accumulate from transaction fees collected by the transaction fee mechanism as blocks are finalised by the committee:

- Block _priority fees_ are distributed to block proposers at block interval.
- Block _base fees_ are added to the rewards pool and distributed at epoch end.

The rewards pool is held in a protocol account until reward distribution occurs as the final block of an epoch is committed to state. Consensus committee members are rewarded proportionally to their share of the bonded stake (the 'voting power') securing the committee.

When distribution occurs:

- A percentage determined by the protocol `treasuryFee` parameter is deducted and transferred to the protocol treasury account for community funds.
- Rewards are distributed to the treasury account of each committee member (validator) on a _pro rata_ basis, depending on their share of the bonded stake in the consensus committee.
- A percentage determined by the validator `delegationRate` parameter is deducted and transferred to the validator treasury account as a commission fee. The initial delegation rate is set globally for all validators in the network, specified by the `delegationRate` protocol parameter in the genesis configuration file.  It can be modified by individual validators after registration.
- Rewards are distributed to stake delegator accounts _pro rata_ according to their share of the stake bonded to the validator.
- Rewards accumulate until claimed by stake delegators 

To learn more about the concept see [Staking rewards and distribution](/concepts/staking/#staking-rewards-and-distribution) and [Staking accounts](/concepts/staking/#staking-accounts).

## Autonity Oracle Contract
The contract implementing the Oracle protocol extensions, including primitives for computing median price data, and managing the set of currency pairs for which Autonity provides price data.

Per the Autonity Protocol Contract, the contract is deployed at network genesis using the null or 'zero' account address and the Autonity Oracle Contract address for a network is deterministic and will always be `0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D`.

The contract stores [protocol parameters](/reference/protocol/) that specify the currency pairs for which the oracle provides median price data and the interval over which an oracle round for submitting and voting on price data runs, measured in blocks. Per the Autonity Protocol Contract, Oracle protocol parameters are initialised at network [genesis](/reference/genesis/).

Oracle Contract functions for returning price data, currency pairs provided, and the oracle network voters can be called by all participants.  Function calls to govern (i.e. manage) the set of currency pairs provided by the oracle are restricted to the `operator` account.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Oracle Contract Interface](/reference/api/oracle/), governance under [Governance and Protocol Only Reference](/reference/api/aut/op-prot/).

### Median price computation

The Autonity Oracle Contract manages the computation of median price data for currency pair price reports submitted by validator-operated oracle servers. The contract implements logic to:

- Aggregate price report data submitted on-chain by validator-operated oracle servers and compute median prices for the currency pairs provided by the oracle network in voting rounds.
- Manage the set of currency pair symbols for which the oracle network must provide price report data.
- Provide contract operations for data consumers to determine the currency pair data provided and retrieve historical and latest computed median price data.

To learn more about the concept see [Oracle network](/concepts/oracle-network/).

### Voting rounds

The Autonity Oracle Contract implements logic to manage submission of price data reports and calculation of median price over [voting rounds](/glossary/#voting-round) by protocol-only functions:

- Set oracle voters based on validators in the consensus committee and update the voter set as the consensus committee is re-selected at the end of an epoch.
- Manage oracle voting rounds, triggering the initiation of a new voting period at the end of a round.


### Voter selection

Participation in the oracle protocol is a validator responsibility and validators in the consensus committee are automatically selected to vote on median price computation by a protocol only function. As the last block of an epoch is finalised, this function is executed to determine the oracle voters for the following epoch.

Consensus committee membership is computed by the Autonity Protocol Contract; see [committee selection](/concepts/architecture/#committee-selection).

## Blockchain Consensus

The append of new blocks to the ledger with immediate finality is managed by the Proof-of-Stake based Tendermint BFT consensus mechanism. It enables dynamic committee selection and maximises stake securing the system by a stake-weighted algorithm for committee selection.

Individual blocks are proposed and agreed in a Tendermint consensus instance, where the process is dynamically repeated as new blocks are finalized. Consensus instances are computed by the consensus committee, a subset of validators whose bonded stake secures the network against Byzantine or malicious behaviour by committee members.

Committee selection is dynamic and stake-based, with a new committee elected for each [epoch](/glossary/#epoch-period). The physical length of an epoch is set as a number of blocks appended to the ledger, and so the temporal duration of an epoch is dependent upon the minimum block period or '[time interval](/glossary/#block-period)' at which blocks are generated by the protocol and appended to the ledger. This interval provides consistent block production to the chain and adherence to the interval is a block validity constraint. Both epoch length and block period are protocol parameters. The number of consensus instances executed in an epoch may be equal to or greater than the number of blocks in the epoch: a consensus round may timeout and fail to complete.

The consensus protocol makes use of:

- The communication layer for consensus round messaging and consensus state synchronisation.
- The Autonity Protocol Contract for committee selection logic.

To learn more about the concept, see [consensus](/concepts/consensus/) and the [protocol parameters](/reference/protocol/) reference.

## Communication Layer
Autonity uses a [fully connected network topology](/glossary/#mesh-network) with peer-to-peer communication based on Ethereum [devp2p <i class='fas fa-external-link-alt'></i>](https://github.com/ethereum/devp2p) network protocols RLPx and wire protocol.

Each participant maintains a current record of peers in the network, updated as new participants join or leave the system. Participants establish an authenticated connection with one another over TCP by the RLPx transport protocol. At the application-level, Autonity extends the Ethereum wire protocol for message broadcast to:

- Add message types for consensus and state synchronisation exchanged by committee members during Tendermint consensus rounds for block proposal, prevote, and precommit.
- Generate cryptographically signed 'seals' for validator messages sent during consensus rounds. Seals are included in the [block header](/concepts/system-model/#block-header) as a cryptographic proof of the validator quorum that agreed the block. There are two types of seal:
    - A proposer seal, seal of the committee member proposing the block
    - A committed seal, aggregated seal of the committee members that voted and agreed on the block
- Provide reliable broadcast logic and duplicate message send prevention under an [eventually synchronous model](/concepts/system-model/#networking) to guarantee the liveness property of consensus messaging in the wire protocol.

To learn more about the concept, see [Networking](/concepts/system-model/#networking) in the System model.

For how bootnode provision works, see the How to [Run Autonity](/node-operators/run-aut/).
