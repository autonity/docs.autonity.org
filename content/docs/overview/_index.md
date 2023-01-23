
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

Autonity networks are Byzantine fault-tolerant and secured by delegated Proof of Stake consensus using the Tendermint consensus algorithm. Autonity has native protocol coins for settlement and staking, and implements a liquid staking model.

Key technical features of the Autonity Protocol are:

- Immediate transaction finality in a public environment where participant nodes can join the network dynamically without permission.
- Delegated Proof of Stake consensus for committee selection and blockchain management, using the Tendermint BFT consensus algorithm.
- Native protocol coins: _Auton_ utility coin used in the transaction fee mechanism; _Newton_ for staking the network.
- Liquid staking for capital efficiency. Staked _Newton_ yield transferrable _Liquid Newton_ tokens, which can be used to redeem the underlying _Newton_ by unbonding stake.

## Technology

Core technology is the Autonity Go Client (AGC), a fork of the Go Ethereum '[Geth](https://geth.ethereum.org/)' client. For the Geth base version of AGC see Reference, [Codebase](/reference/codebase/).

AGC is the reference implementation of the Autonity Protocol and provides the main client software run by [participant](/glossary/#participant) peer nodes in an Autonity network system.

The Autonity client extends the underlying Ethereum protocol at application, blockchain, and communication layers to implement:

- A dual coin tokenomic model providing native protocol coin for gas payment and staking.
- Delegated proof of stake consensus protocol (based on the Tendermint Byzantine fault tolerant consensus algorithm) with dynamic committee selection.
- A liquid staking model: liquid newton receives rewards from staking and is transferrable, bringing liquidity and capital efficiency benefits to staking.
- Protocol governance logic.

For explanations of core concepts refer to:

- [Architecture](/concepts/architecture/) for an Autonity system's technical architecture and protocol primitives.
- [System model](/concepts/system-model/) for the functions of participant nodes and blockchain primitives comprising the structure of an Autonity system's peer-to-peer network and distributed ledger.
- [Client](/concepts/client/) for an overview of Autonity Go Client features.
- [Consensus](/architecture/consensus/) for the protocol's implementation of the Tendermint BFT consensus algorithm and consensus committee selection.
- [Validator](/architecture/validator) for the role of validators and the functions they perform in securing an Autonity network.
- [Staking](/architecture/staking/) for protocol staking mechanisms and Autonity's model for liquid staking.
- [Protocol assets](/concepts/protocol-assets/) for the protocol's native coins and tokens:  _Auton_ utility coin, _Newton_ stake token, and _Liquid Newton_ liquid stake token.
- The [Glossary](/glossary/#participant) for definitions of terms and concepts used in the documentation.

## System actors

The actors of an Autonity network are:

- [Account Holders](/account-holders/): externally owned accounts of human users of the system. Account holders are the users interacting with an Autonity network: operating node and validation infrastructure, deploying and using decentralised applications, building and contributing to the community and ecosystem.

- [Node operators](/node-operators/): network peer nodes running the AGC client software, forming the backbone of the networks p2p infrastructure and shared system ledger. Nodes store an up-to-date copy of the system state and may be run as public rpc endpoints providing open access to an Autonity network.

- [Validators](/validators/): nodes with bonded stake forming the validation infrastructure proposing and maintaining system state. Active validator nodes are candidates for selection to the network's consensus committee. The consensus committee is responsible for proposing and deciding on new blocks.

- [Stakers](/staking/): stake delegators hold  _Newton_ stake token and delegate stake to one or more validators in order to secure the network. Stake holders receive _Liquid Newton_ for bonded stake.


## Key concepts

In addition to Ethereum concepts such as `address`, `gas`, and `node`, the distinction between _participant_ and _validator_ nodes is key in the Autonity context:

| **Concept** | **Meaning** |
| --------- | --------- |
| [Auton (_XTN_)](/concepts/protocol-assets/auton/) | Autonity's native account coin (intrinsic balance of an account, like "Ether" in Ethereum). |
| [Newton (_NTN_)](/concepts/protocol-assets/newton/) | Native staking instrument used to secure the Proof-of-Stake consensus mechanism. |
| [Participant ](/concepts/system-model/#participants) node | A node running Autonity Go Client software and connected to other nodes in an Autonity network. A participant node maintains a copy of system state and may become a _validator_. |
| [Validator](/concepts/validator/) node | A participant node that has registered as a validator on an Autonity network. A validator node may be selected to the _Consensus Committee_ if it has sufficient stake _bonded_ to it by a stake delegator. |
| [Liquid Staking](/concepts/staking/) | Participants in the network can stake Newton to a specific validator to earn a fraction of the rewards granted for securing the network.  In return for staking, a validator issues _Liquid Newton_ tokens to the staker, where these tokens represent a claim on the staked Newton.  Liquid Newton tokens can be freely transferred between participants. |
| [Consensus Committee](/concepts/consensus/committee/) | The subset of _validator_ nodes that participate in the consensus protocol. The Consensus Committee is updated periodically (every epoch), according to an algorithm prescribed by protocol. |

For all Autonity terminology and concepts see the [Glossary](/glossary/).
