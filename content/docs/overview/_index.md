
---
title: "Overview "
linkTitle: "Overview"
weight: 10
description: >
  An overview of the Autonity blockchain protocol and key concepts of the underlying technology
---

## What is Autonity?

Autonity is an EVM-based Layer 1 blockchain protocol for decentralised markets.

Autonity networks are public and permissionless. Access is open and anyone can operate a peer node in the blockchain peer-to-peer network.

Autonity networks are Byzantine fault-tolerant and secured by delegated Proof of Stake consensus using the Tendermint consensus algorithm. Autonity has native protocol coins for settlement and staking. Autonity implements a liquid staking model.

Key technical features of the Autonity Protocol are:

- Immediate transaction finality in a public environment where participant nodes can join the network dynamically without permission.
- Delegated Proof of Stake consensus for committee selection and blockchain management, using the Tendermint BFT consensus algorithm.
- Native [protocol assets](/concepts/protocol-assets/) and [stabilization mechanism](/concepts/asm/): _Auton_ utility coin used in the transaction fee mechanism; _Newton_ staking coin for securing the network. Auton price stability is by a CDP-based stabilization mechanism, the [Auton Stabilization Mechanism (ASM)](/concepts/asm/); the stabilization target is the [Auton Currency Unit (ACU)](/concepts/asm/#acu), a base-invariant, volatility-minimized index.
- [Liquid staking](/concepts/staking/#liquid-staking) for capital efficiency and a [Penalty-Absorbing Stake](/concepts/staking/#penalty-absorbing-stake-pas) model. [Delegated](/glossary/#delegated) _Newton_ stake yields transferrable _Liquid Newton_ tokens, which can be used to redeem the underlying _Newton_ by unbonding stake. [Self-bonded](/glossary/#self-bonded) stake by validator operators does not yield _Liquid Newton_ and is slashed before delegated stake to assure validator integrity and 'skin in the game'.
- [Accountability and fault detection (AFD)](/concepts/accountability/): a protocol for detecting infractions of consensus rules by validators participating in block proposal and voting as a committee member. Failure to adhere to these rules is a rule infraction and AFD will detect and apply slashing penalties for proven rule infractions.
- [Oracle network](/concepts/oracle-network/): a protocol for consensus-computed median price data for selected FX currency pairs as an L1 platform feature. The submission of price data for aggregation and voting is a validator responsibility; validator nodes form an oracle network. 


## Technology

Core technology is the [Autonity Go Client (AGC)](/concepts/client/), a fork of the Go Ethereum '[Geth <i class='fas fa-external-link-alt'></i>](https://geth.ethereum.org/)' client, and the [Autonity Oracle Server (AOS)](/concepts/oracle-server/). For the Geth base version of AGC see Reference, [Codebase](/reference/codebase/).

AGC is the reference implementation of the Autonity Protocol and provides the main client software run by [participant](/glossary/#participant) peer nodes in an Autonity network system - see [Running a Node](/node-operators/). AOS is operated by validator nodes only - see [Running a validator](/validators/).

The Autonity client extends the underlying Ethereum protocol at application, blockchain, and communication layers to implement the key technical features and protocol governance logic.

For explanations of core concepts refer to:

- [Architecture](/concepts/) for an Autonity system's technical architecture and protocol primitives.
- [System model](/concepts/system-model/) for the functions of participant nodes and blockchain primitives comprising the structure of an Autonity system's peer-to-peer network and distributed ledger.
- [Consensus](/concepts/consensus/) for the protocol's implementation of the Tendermint BFT consensus algorithm and consensus committee selection.
- [Autonity Go Client (AGC)](/concepts/client/) for an overview of AGC features.
- [Oracle network](/concepts/oracle-network/) for an overview of the oracle protocol for computing median price data for FX currency pairs.
- [Autonity Oracle Server (AOS)](/concepts/oracle-server/) for an overview of AOS features.
- [Validator](/concepts/validator) for the role of validators and the functions they perform in securing an Autonity network.
- [Staking](/concepts/staking/) for protocol staking mechanisms and Autonity's model for liquid staking.
- [Accountability and fault detection (AFD)](/concepts/accountability/) protocol for proving and applying economic slashing penalties to consensus committee members found guilty of Byzantine behavior.
- [Auton Stabilization Mechanism (ASM)](/concepts/asm/) for protocol mechanisms to stabilize Auton price in a CDP-based stabilization mechanism where Auton is borrowed in return for depositing collateral token.
- [Protocol assets](/concepts/protocol-assets/) for the protocol's native coins and tokens:  _Auton_ utility coin, _Newton_ stake token, and _Liquid Newton_ liquid stake token.
- The [Glossary](/glossary/#participant) for definitions of terms and concepts used in the documentation.

## System actors

The actors of an Autonity network are:

- [Account Holders](/account-holders/): externally owned accounts of human users of the system. Account holders are the users interacting with an Autonity network: operating node and validation infrastructure, deploying and using decentralised applications, building and contributing to the community and ecosystem.

- [Node operators](/node-operators/): network peer nodes running the AGC client software, forming the backbone of the networks p2p infrastructure and shared system ledger. Nodes store an up-to-date copy of the system state and may be run as public rpc endpoints providing open access to an Autonity network.

- [Validator nodes](/validators/): network nodes running the AGC client and AOS oracle server software forming the validation infrastructure proposing and maintaining system state, and the oracle network for computing median price data. Active validator nodes are candidates for selection to the network's consensus committee. The consensus committee is responsible for proposing and deciding on new blocks and computing oracle price data in voting rounds.

- [Stake delegators](/delegators/): account holders that have a _Newton_ stake token balance and delegate stake to one or more validators in order to secure the network. Stake holders receive _Liquid Newton_ for bonded stake.


## Key concepts

In addition to Ethereum concepts such as `address`, `gas`, and `node`, the distinction between _participant_ and _validator_ nodes is key in the Autonity context:

| **Concept** | **Meaning** |
| --------- | --------- |
| [Auton (_ATN_)](/concepts/protocol-assets/auton/) | Autonity's native account coin (intrinsic balance of an account, like "Ether" in Ethereum) used to pay transaction fees. |
| [Newton (_NTN_)](/concepts/protocol-assets/newton/) | Native staking instrument used to secure the Proof-of-Stake consensus mechanism. |
| [Liquid Newton (_LNTN_)](/concepts/protocol-assets/liquid-newton/) | Native liquid token representing [delegated](/glossary/#delegated) Newton stake token bonded to a validator in an Autonity Network. |
| [Participant ](/concepts/system-model/#participants) node | A node running Autonity Go Client software and connected to other nodes in an Autonity network. A participant node maintains a copy of system state and may become a _validator_. |
| [Validator](/concepts/validator/) node | A participant node that has registered as a validator on an Autonity network. A validator node may be selected to the _consensus committee_ if it has sufficient stake _bonded_ to it by a stake delegator. As a consensus committee member, validators are responsible for participating in proposing and agreeing new blocks and participating in the _oracle network_ |
| [Liquid Staking](/concepts/staking/) | Participants in the network can stake Newton to a specific validator to earn a fraction of the rewards granted for securing the network.  In return for [delegated](/glossary/#delegated) staking, a validator issues _Liquid Newton_ tokens to the staker, where these tokens represent a claim on the staked Newton.  Liquid Newton tokens can be freely transferred between participants. |
| [Penalty-Absorbing Stake](/concepts/staking/#penalty-absorbing-stake-pas) |  A stake slashing model whereby [self-bonded](/glossary/#self-bonded) stake is slashed before [delegated](/glossary/#delegated) stake when applying slashing penalties for accountability events. PAS incentivises honest validator behavior. |
| [Consensus Committee](/concepts/consensus/committee/) | The subset of _validator_ nodes that participate in the consensus protocol. The Consensus Committee is updated periodically (every epoch), according to an algorithm prescribed by protocol. |
| [Oracle network](/concepts/oracle-network) | The network of validator-operated oracles that submits price data from off-chain external data providers on-chain and votes on agreeing an aggregated median price data according to an oracle protocol. |
| [Accountability and fault detection (AFD)](/concepts/accountability/) | A protocol for detecting infractions of consensus rules by validators participating in consensus as _consensus committee_ members. |
| [Auton Stabilization Mechanism (ASM)](/concepts/asm/) | The protocol mechanism used to maintain [Auton](/concepts/protocol-assets/auton/) price stability. The Stabilization Mechanism is CDP, [Auton](/concepts/protocol-assets/auton/) borrowed against [Newton](/concepts/protocol-assets/newton/) or [Liquid Newton](/concepts/protocol-assets/liquid-newton/) collateral. |

For all Autonity terminology and concepts see the [Glossary](/glossary/).
