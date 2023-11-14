
---
title: "Glossary "
linkTitle: "Glossary"
weight: 100
description: >
  Definitions of terminology and concepts used in the documentation

---

## Application Binary Interface (ABI)
The binary-level interface between a smart contract and the [Ethereum Virtual Machine (EVM)](/glossary/#ethereum-virtual-machine-evm). The ABI defines the contract interface and is used to call contract functions and for contract-to-contract interactions. The ABI is represented as JSON and compiled to [bytecode](/glossary/#bytecode) for execution in the EVM. See the [Contract ABI Specification <i class='fas fa-external-link-alt'></i>](https://solidity.readthedocs.io/en/develop/abi-spec.html) in Solidity programming language docs for design and specification.

## account
An account is an object in the blockchain [system state](/glossary/#system-state) identified by a unique [address](/glossary/#account-address). It has an intrinsic balance denominated in the native coin [auton](/glossary/#auton), transaction state, and if a contract account has EVM code and contract state storage.

There are 2 types of account:

- Externally owned accounts (EOA’s). These are owned and controlled by a [private key](/glossary/#private-key) held by an external user, have no associated EVM code, and submit transactions and calls to the blockchain
- Contract accounts. These are controlled by their associated EVM code, execute that associated EVM code contract logic when a transaction is sent to the account, and may send message calls to other contract accounts as part of their EVM code execution.

## account state
A part of [system state](/glossary/#system-state) that is specific to an [account](/glossary/#account) [address](/glossary/#address). Account state comprises: the account’s native coin balance (_auton_), the count of transactions sent from the account (nonce), and, if a contract account, a hash (storageRoot) of the associated account storage and hash (codeHash) of the associated EVM code.

## address{#address}
A 64 character hex string providing the unique identifier of an [account](/glossary/#account).

## Auton
A [native coin](/glossary/#native-coin) of an Autonity Network. Auton is the native coin in which an [account](/glossary/#account) balance is denominated and is the coin used for paying gas fees within the Autonity Protocol. See also  [Protocol assets, Auton](/concepts/protocol-assets/auton/).

## Auton Currency Unit (ACU) {#acu}
A base-invariant, volatility-minimised index based on a currency basket of 7 free-floating fiat currencies.

The ACU is the _Stabilization Target_ for [Auton](/glossary/#auton) price stability used by the [Auton Stabilization Mechanism (ASM)](/glossary/#asm). 


## Auton Stabilization Mechanism (ASM) {#asm}
The protocol mechanism used to maintain Auton price stability. The _Stabilization Mechanism_ is [CDP](/glossary/#cdp), [Auton](/glossary/#auton) borrowed against [Newton](/glossary/#newton) or [Liquid Newton](/glossary/#liquid-newton) collateral.


## Collateralised Debt Position (CDP) {#cdp}
A [smart contract](/glossary/#smart-contract) based lending mechanism where collateral is deposited and locked in a smart contract to borrow another token-based asset. CDPs operate subject to collateral requirements and may be liquidated if the lender fails to maintain, i.e. breaches, the collateral conditions of the CDP.

CDPs are used by the [Auton Stabilization Mechanism (ASM)](/glossary/#asm) to borrow [Auton](/glossary/#auton) against [Newton](/glossary/#newton) or [Liquid Newton](/glossary/#liquid-newton) collateral.

## Autonity Go Client (AGC)
Autonity Go Client is main client software for accessing and participating in an Autonity network. AGC implements the Autonity Protocol. All [nodes](/glossary/#node) of an Autonity network run AGC software. When connected to an Autonity network an AGC is a [participant](/glossary/#participant) in that network.

For AGC features see Concept [Client](/concepts/client/).

## Autonity network
An instance of an Autonity blockchain [peer-to-peer network](/glossary/#peer-to-peer-network-p2p), all [peer](/glossary/#peer) [nodes](/glossary/#node) running Autonity Go Client main client software. Public Autonity networks are instantiated for specific purposes - e.g. testnet, mainnet.

Autonity network peers are connected in a full [mesh network](/glossary/#mesh-network). Peers discover and connect to one another via Autonity's communication layer protocols which are based on the Ethereum devp2p networking protocol.

## Autonity Oracle Server (AOS)
Autonity Oracle Server (AOS) is software for participating in the [Autonity oracle network](/glossary/#autonity-oracle-network). AOS retrieves exchange rate data for [currency pairs](/glossary/#currency-pair) from data providers, consolidates these data points into a standardised report, and submits to the Autonity Protocol's oracle contract on-chain via the AOS operator's [validator](/glossary/#validator) [node](/glossary/#node). Submitted data reports are then aggregated by the oracle contract which uses a voting mechanism to provide exchange rate reference data agreed by consensus.

Providing [oracle](/glossary/#data-oracle) reference data is a validator responsibility. [Validator](/glossary/#validator) node operators must operate an AOS connected to their validator [node](/glossary/#autonity-go-client-agc).

For AOS features see Concept [Oracle Server](/concepts/oracle-server/).

## Autonity Protocol
A generalization of the Ethereum Protocol modified to incorporate proof-of-stake based Tendermint consensus, native tokenomics, deterministic [finality](/glossary/#finality), an [oracle protocol](/glossary/#oracle-protocol), and [liquid staking](/glossary/#liquid-staking).

The Autonity Protocol uses Ethereum’s EVM-based state transition function. State transition is by transaction, the transaction associated with an economic cost for computation, and transactions affecting [system state](/glossary/#system-state)).

## block
A set of transaction’s validated by consensus and appended to the [blockchain](/glossary/#blockchain).

## blockchain
A decentralised system in which system state is maintained as a sequence of [block](/glossary/#block)s in an append-only data structure maintained as a distributed ledger by consensus between peer nodes.

## block height
The distance of a block from the root block of the system's blockchain, the [genesis block](/glossary/#genesis-block). Block height is measured as the count of blocks from genesis block to current block.

## block period
The minimum period of time between blocks, measured in seconds. The block period delay ensures consistent block production over time.

## bond
The operation of bonding stake to a validator.

Stake can be _delegated_ or _self-bonded_, the distinction being [self-bonded](/glossary/#self-bonded) stake is owned by the identity operating the validator and [delegated](/glossary/#delegated) stake is not.

## bytecode
Executable code passed to the EVM for execution. Bytecode - also known as EVM code - is compiled from the high-level programming language (Solidity) used to write smart contracts for execution in the [Ethereum Virtual Machine (EVM)](/glossary/#ethereum-virtual-machine-evm).

## Byzantine failure
A failure of consensus due to participant behaviour that does not accord with the protocol.

## Byzantine fault tolerance (BFT)
The ability of a distributed system to operate and agree consensus according to protocol under [Byzantine failure](/glossary/#byzantine-failure) conditions.

Autonity implements Tendermint BFT consensus, an asynchronous consensus protocol that can require up to 1/3 of committee members being at fault. Tendermint requires `3f+1` of participant validators behave correctly and is tolerant of `f` faults.

## calldata
Data committed to state by arguments to a smart contract deployed on the blockchain. 'calldata' is accessed by the Solidity `.call()` function. Calldata is non-executable - it is [state](/glossary/#system-state) not [smart contract](/glossary/#smart-contract) [bytecode](/glossary/#bytecode).

## consensus
The computational process by which [system state](/glossary/#system-state) is agreed and replicated by [validator](/glossary/#validator) nodes in a distributed system. Autonity implements a [Proof of Stake (PoS)](/glossary/#proof-of-stake-pos) based [consensus algorithm](/glossary/#consensus-algorithm).

## consensus algorithm
An algorithm used by distributed systems to ensure that peer nodes have consistent state with resilience to computer network or Byzantine behaviour. See [Byzantine-fault tolerance](/glossary/#byzantine-fault-tolerance-bft).

## consensus committee
The set of [validator](/glossary/#validator) nodes participating in the consensus protocol for a [block](/glossary/#block) [epoch period](/glossary/#epoch-period). The committee is responsible for proposing new blocks, voting on block proposals to affirm the validity of proposed blocks and decide if committed to state, and notifying new blocks to peer nodes to replicate the new state.

A new consensus committee is selected at every block epoch in an autonomous process executed by Autonity's [Proof of Stake (PoS)](/glossary/#proof-of-stake-pos) consensus protocol. The selection algorithm ranks registered validators according to the amount of their bonded stake, selecting those with the highest stake to fill the available committee member slots. Ranking by stake serves to maximise the amount of stake securing the network in an epoch.

## cryptocurrency
A digital currency that provides a medium of exchange in a decentralised computer network. The record of transactions in the crypto(graphic) currency is verified and recorded in the network’s distributed ledger using cryptography.

## currency pair
Two currencies valued against one another with a quotation and pricing structure based on quoting one currency against the other. A currency pair consists of a base currency (listed first) and a quote currency (listed second). The currency pair expresses the amount of quote currency required to buy one unit of the base currency.

For example, in the currency pair `JPY/USD 0.0074`, `1` Japanese Yen will trade for `0.0074` US dollars.

## data oracle
An off-chain data feed service that provides data to a [blockchain](/glossary/#blockchain). An oracle data service is considered a secure and reliable source of information on the blockchain and may be used in on-chain logic execution. For example, a price data feed. See also [Autonity Oracle Server (AOS)](/glossary/#autonity-oracle-server-oas)

## decentralised application (dApp)
A software application deployed on to a blockchain p2p network. A dApp interacts with one or more smart contracts and is typically a combination of those contract(s) and a frontend for using that contract. The frontend graphical user interface (GUI) is typically built out using JavaScript, HTML, CSS technologies. User interactions with a dApp are by transactions and calls submitted to a network [peer](/glossary/#peer)'s JSON RPC API using the web3.js library. Interactions may be mediated by a user via a GUI or application-level interactions.

## delegation
The process of bonding stake token to a [validator](/glossary/#validator) by a [stakeholder](/glossary/#stakeholder).

See related concepts: [staking](/glossary/#staking), [delegated](/glossary/#delegated) stake, [self-bonded](/glossary/#self-bonded) stake, and [delegation rate](/glossary/#delegation-rate).

## delegated
Stake token bonded to a [validator](/glossary/#validator) by a [stakeholder](/glossary/#stakeholder). Delegated stake earns [staking rewards](/glossary/#staking-rewards) and the staker is minted [Liquid Newton](/glossary/#liquid-newton) for the [Newton](/glossary/#newton) stake token  bonded. The [account](/glossary/#account) submitting the stake delegation transaction (_cf._ [bond](/glossary/#bond)) can be any network account *except* the validator `treasury` account.

Stake delegation transactions submitted from the validator `treasury` account result in [self-bonded](/glossary/#self-bonded) stake.

## delegation rate
The percentage commission of earned [staking rewards](/glossary/#staking-rewards) that a [validator](/glossary/#validator) charges as a commission on [delegated](/glossary/#delegation) stake.

## enode
The unique identifier of a node in the form of a URI. It provides the network address of a node on an Autonity network, giving the  network location of the node client for p2p networking.

The enode URL is formed according the Ethereum enode url format which is described in the [Ethereum Developers Docs, Networking layer <i class='fas fa-external-link-alt'></i>](https://ethereum.org/en/developers/docs/networking-layer/network-addresses/#enode).

## epoch
A fixed number (i.e. [epochPeriod](/glossary/#epoch-period)) of consecutive blocks where the validator committee - as recorded in the state of the autonity contract - cannot change.

## epoch period
The period of time for which a consensus committee is elected, defined as a number of blocks.  The epoch period can be any integer number > 0, but _must_ be shorter than the unbonding period. Without this constraint unbonding could take place before slashing penalties and staking transitions are applied.

## Ethereum Virtual Machine (EVM)
The distributed state machine responsible for computing system state. The EVM provides the runtime environment for smart contract execution, computing valid state transitions as transactions are computed and smart contract [bytecode](/glossary/#bytecode) executed.

Contract logic is executed by the EVM instruction set (opcodes) which define the allowed computation operations. The set of opcodes allows the EVM to be Turing complete. Strictly it is _quasi Turing complete_ because the gas model constrains execution - transactions will revert before full execution if they run out of gas. The EVM provides an abstraction layer between the execution of application (smart contract) [bytecode](/glossary/#bytecode) and the OS of the machine hosting the Autonity [client](/glossary/#autonity-go-client-agc) software.

## finality
Finality is the quality of being in an end state that cannot be altered. In blockchain, finality refers to the point at which state transitions are immutable. Autonity's Tendermint consensus is deterministic: finality for a block and the transactions within it is achieved at the point a block is appended (i.e. committed) to the blockchain. Each block creates a checkpoint in the chain and provides a guarantee that blocks before that checkpoint cannot be altered.

## genesis block
The first block of a blockchain containing the genesis state of the system and the root of the blockchain.

The genesis state is provided in the [genesis state file](/glossary/#genesis-state-file). As root block, the genesis block has the block number index `0`.

## genesis state file
The JSON-formatted genesis configuration file that contains the data necessary to generate the genesis block of an Autonity network. Typically called `genesis.json` but can be given any custom name.

## gigaton
The denomination of Autonity's [auton](/glossary/#auton) cryptocurrency used to denominate Autonity gas prices. 1 `gigaton` = 1,000,000,000 [ton](/glossary/#ton). The Autonity equivalent of wei is [ton](/glossary/#ton) and of gwei gigaton.

## incentivization scheme
A cryptoeconomic mechanism where economic penalties are applied for incorrect actions or state transitions by network participants, enforced by cryptographic proofs of state or action.

## jailing
A protocol action that excludes a validator from selection to the [consensus committee](/glossary/#consensus-committee) for a designated period of time as a [slashing penalty](/glossary/#slashing-penalty). See [jail period](/glossary#jail-period).

## jail period
The period of time for which a validator is debarred from selection to the consensus committee, defined as a number of [blocks](/glossary/#block).  The jail period is set as a protocol parameter.

## key pair
A pair of public and private cryptography keys used for signing and encryption. The private key is used to produce signatures that are publicly verifiable using the public key. The public key may also be used to encrypt messages intended for the private key holder who can decrypt them using the private key.

## Liquid Newton
The liquid token representing [Newton](/glossary/#newton) stake token  [bonded](/glossary/#bond) to a validator in an Autonity Network (see stake [delegation](/glossary/#delegation)). Unlike bonded [Newton](/glossary/#newton), Liquid Newton is transferrable and the holder receives due staking rewards. See also [Protocol assets, Liquid Newton](/concepts/protocol-assets/liquid-newton/).

## liquid staking
A staking model in which funds staked to a Proof of Stake network have a liquid representation of staked assets in the form of a token. For Autonity's liquid staking model see [Staking, Liquid staking](/concepts/staking/#liquid-staking).

## mesh network
A network topology where each node is connected to one or more other network nodes. All nodes in the  mesh relay data and co-operate in the distribution of data across the network. A mesh topology can be _full_ or _partial_.

In a _full mesh topology_ each node is directly connected to every other node. In a _partial mesh topology_ a node is directly connected to a subset of the other network nodes only.

## native coin
A cryptocurrency that is inherent to a decentralised computer network.

Autonity tokenomics have the native coin [Auton](/glossary/#auton) and ERC20 tokens [Newton](/glossary/#newton) and [Liquid Newton](/glossary/#liquid-newton).

## Newton
The stake token used to stake an [Autonity network](/glossary/#autonity-network). Once Newton is staked it is locked and only redeemable by [unbonding](/glossary/#unbond) after an [unbonding period](/glossary/#unbonding-period). Newton can be in three states (bonded, unbonded, unbonding) as described in [Protocol assets, Newton](/concepts/protocol-assets/newton/). See [Proof of Stake (PoS)](/glossary/#proof-of-stake-pos). 

## node
A participant running the Autonity Go Client software and able to connect to an Autonity network. See [peer](/glossary/#peer) [mesh network](/glossary/#mesh-network), [peer-to-peer network](/glossary/#peer-to-peer-network-p2p).

## oracle network
The network of validator-operated oracles that submits price data from off-chain external data providers on-chain and votes on agreeing an aggregated median price data according to an [oracle protocol](/glossary/#oracle-protocol).

## oracle protocol
The logic and rules governing the calculation of median price data by the [oracle network](/glossary/#oracle-network). The protocol has off- and on-chain operations. Price data is collected from external data providers by [oracle servers](/glossary/#autonity-oracle-server-aos) run by validator operators and submitted on-chain to an oracle [contract](/glossary/#smart-contract). The oracle contract computes aggregate median price data for those currency pairs; consensus committee members vote to agree the median prices by consensus in [voting rounds](/glossary/#voting-round).

## oracle protocol
The logic and rules governing the calculation of median price data by the [oracle network](/glossary/#oracle-network). The protocol has off- and on-chain operations. Price data is collected from external data providers by [oracle servers](/glossary/#autonity-oracle-server-aos) run by validator operators and submitted on-chain to an oracle [contract](/glossary/#smart-contract). The oracle contract computes aggregate median price data for those currency pairs; consensus committee members vote to agree the median prices by consensus in [voting rounds](/glossary/#voting-round).

## participant
A [peer](/glossary/#peer) [node](/glossary/#node) that is currently connected to other nodes in an Autonity network.

A participant is able to sync state, and broadcast and receive transactions, and potentially be a [validator](/glossary/#validator) node.

## peer
A [node](/glossary/#node) which is currently connected to other nodes in a [peer-to-peer network](/glossary/#peer-to-peer-network-p2p) and is a [participant](/glossary/#participant) in that network.

## peer-to-peer network (p2p)
A distributed systems architecture in which the systems' resources are pooled and shared across nodes that are peers of the network.

## Penalty-Absorbing Stake (PAS)
A stake [slashing](/glossary/#slashing) model whereby [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake when applying [slashing penalties](/glossary/#slashing-penalty) for accountability events.

In the PAS model self-bonded stake absorbs any slashing penalties before they are applied pro-rata to the remaining delegated stake.

## permissionless network
A peer-to-peer network where access is open and public. Any node can connect to the network and become a [peer](/glossary/#peer).

## Proof of Stake (PoS)
A [consensus algorithm](/glossary/#consensus-algorithm) where the blockchain is secured by economic value through [bonding](/glossary/#bond) [stake token](/glossary/#stake-token) to [validators](/glossary/#validator). [Consensus committee](/glossary/#consensus-committee) members are chosen by a [selection mechanism](/concepts/consensus/committee/#committee-member-selection) that maximises the amount of stake backing the committee and so the economic value securing the network.

If the protocol determines that a validator has failed to follow consensus rules, [slashing penalties](/glossary/#slashing-penalty) are applied according to Autonity's [accountability and fault detection protocol](/concepts/accountability/). 

## self-bonded
Stake token bonded to a [validator](/glossary/#validator) where the validator is the [stakeholder](/glossary/#stakeholder). The [account](/glossary/#account) submitting the stake delegation transaction (_cf._ [bond](/glossary/#bond)) is the validator `treasury` account.

Self-bonded stake earns [staking rewards](/glossary/#staking-rewards), but unlike [delegated](/glossary/#delegated) stake does not have [Liquid Newton](/glossary/#liquid-newton) minted for the [Newton](/glossary/#newton) stake token bonded. 

## slashing
A protocol action that reduces the amount of a validator's bonded stake as a [slashing penalty](/glossary/#slashing-penalty).

## slashing penalty
An economic penalty applied to a validator for misbehaviour. Examples of slashing penalty are: stake [slashing](/glossary/#slashing), stake freezing, [jailing](/glossary/#jailing).

## smart contract
The program code for encoding and executing decentralised application logic in the [EVM](/glossary/#ethereum-virtual-machine-evm). Smart contracts are written in a higher level programming language such as 'Solidity' and compiled to [bytecode](/glossary/#bytecode) for execution in the EVM. A smart contract stores the application's state.

## stake token
The token used as economic value to secure a blockchain in [Proof of Stake (PoS)](/glossary/#proof-of-stake-pos) consensus.

Autonity's stake token is [Newton](/glossary/#newton).
    
## stakeholder
A network participant that holds an amount of the [Newton](/glossary/#newton) stake token.

## staking
The process by which stake is delegated to a validator node in a Proof of Stake (PoS) blockchain. Validators with bonded stake participate in transaction validation if a member of the consensus committee. Stake can be [self-bonded](/glossary/#self-bonded) or [delegated](/glossary/#delegated).

## staking rewards
Revenue earned for stake [delegation](/glossary/#delegation) by bonded stake actively securing the network during consensus. Only stake delegated to members of the current consensus committee earns staking rewards.

## staking wallet account
The [account](/glossary/#account) used by a [stakeholder](/glossary/#stakeholder) for stake delegation. This is the account address used to submit transactions for operations to:

- [bond](/glossary/#bond) and [unbond](/glossary/#unbond) [Newton](/glossary/#newton) stake token to a [validator](/glossary/#validator) in Autonity's [liquid staking](/glossary/#liquid-staking) model
- transfer [Liquid Newton](/glossary/#liquid-newton) to another account
- claim rewards for stake delegation.

## state database
The local data store of a node used to persist the node’s local copy of [system state](/glossary/#system-state).

## system state
The computational state of an Autonity system. State is  computed according to the [Autonity Protocol](/glossary/#autonity-protocol). System state is stored as key-value pairs, mapping between account [addresses](/glossary/#address) and [account states](/glossary#account-state) in Ethereum's modified Merkle Patricia trie data structure (See [Merkle Patricia Tree, Ethereum Developer docs <i class='fas fa-external-link-alt'></i>](https://ethereum.org/en/developers/docs/data-structures-and-encoding/patricia-merkle-trie/)).

## ton
The smallest denomination of Autonity's [auton](/glossary/#auton) native [cryptocurrency](/glossary/#cryptocurrency). 1 `auton` = 1,000,000,000,000,000,000 ton (10^18). The ton is Autonity's equivalent denomination to Ethereum's [wei](/glossary/#wei). See also [gigaton](/glossary/#gigaton).

## transaction fee mechanism (TFM)
The protocol mechanism for pricing the cost of processing a transaction on a blockchain.

## unbond
The operation of unbonding stake from a validator.

In Autonity's [liquid staking](/glossary/#liquid-staking) model stake can be unbonded at any time, but staked Newton is not redeemable until an [unbonding period](/glossary/#unbonding-period) has elapsed.

## unbonding period
The period of time for which bonded stake remains locked after processing an unbonding transaction. Unbonding period is defined as a number of blocks.

Proof of Stake consensus places constraints on the minimum length of the unbonding period. It must be long enough to allow the detection and reporting of consensus faults by validators, and not short enough to  allow unbonding before a [slashing penalty](/glossary/#slashing-penalty) can be applied. As such it is a security property of the network.

## Unix time
The Unix OS system for representing a point in time as a timestamp. Time is measured as the number of seconds since the Unix Epoch began - 1st January 1970 at 00:00:00 UTC. Unix time is used for Autonity timestamps. For detail and format see [Unix time <i class='fas fa-external-link-alt'></i>](https://en.wikipedia.org/wiki/Unix_time).

## validator
A [participant](/glossary/#participant) [node](/glossary/#node) that has registered as a validator on an [Autonity network](/glossary/#autonity-network). Validator nodes may be selected to the [consensus committee](/glossary/#consensus-committee) and participate in [consensus](/glossary/#consensus) if they have enough [bonded](/glossary/#bond) [stake](/glossary/#staking).

## voting period

The period of time measured in [blocks](/glossary/#block) over which [Autonity oracles](/glossary/#autonity-oracle-server-oas) submit price data reports and an aggregated median price is computed for the [currency pair](/glossary/#currency-pair) provided an Autonity network provides a median price. See [voting round](/glossary/#voting-round).

## voting power
The amount of stake bonded by [delegation](/glossary/#delegation) to a [validator](/glossary/#validator). A validator's voting power may also be referred to as its _weight_. The sum of stake bonded to validators that are members of a [consensus committee](/glossary/#consensus-committee) may be referred to as the _total voting power_ of the committee.

## voting round

An Autonity network's configured [voting period](/glossary/#voting-period) for computing median price data for currency pairs provided by the [oracle network](/glossary/#oracle-network).

## wallet
A software application that provides functionality for a system user to access and manage their [accounts](/glossary/#account).

## wei
The smallest denomination of Ethereum's `ether` native cryptocurrency. 1 `ether` = 1,000,000,000,000,000,000 wei (10^18). In Ethereum gas prices are denominated in gwei - giga wei (10^9), 1 gwei = 1,000,000,000 wei. The Autonity equivalent of wei is [ton](/glossary/#ton) and of gwei [gigaton](/glossary/#gigaton).
