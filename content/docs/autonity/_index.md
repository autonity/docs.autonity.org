
---
title: "Autonity "
linkTitle: "Autonity"
weight: 1
description: >
  An overview of the Autonity blockchain protocol and key concepts of the underlying technology
---

## What is Autonity?

Autonity is an EVM-based Layer 1 blockchain protocol for decentralised trading use cases.

Autonity networks are public and permissionless. Access is open and anyone can operate a peer node in the blockchain peer-to-peer network.

Autonity networks are Byzantine fault-tolerant and secured by delegated Proof of Stake using the Tendermint consensus algorithm. Autonity has native protocol coins for settlement and staking, and implements liquid staking.

Key technical features of the Autonity Protocol are:

- Immediate transaction finality in a public environment where participant nodes can join the network dynamically without permission.
- Delegated Proof of Stake consensus for committee selection and blockchain management, using the Tendermint BFT consensus algorithm.
- Native protocol coins: _Auton_  settlement coin used in the transaction fee mechanism; _Newton_ for staking on the network.
- Liquid staking for capital efficiency. Staked _Newton_ yield transferrable _Liquid Newton_ tokens, which can be used to redeem the underlying _Newton_ by unbonding the stake.

## Technology

Core technology is the Autonity Go Client (AGC), a fork of the Go Ethereum '[Geth](https://geth.ethereum.org/)' client. For the Geth base version of AGC see Reference, [Codebase](/reference/codebase/).

AGC is the reference implementation of the Autonity Protocol and provides the main client software run by [participant](/glossary/#participant) peer nodes in an Autonity network system.

The Autonity client extends the underlying Ethereum protocol at application, blockchain, and communication layers to implement:

- A dual coin tokenomic model providing native settlement coin for gas payment and stake token.
- Liquid staking model.
- A delegated proof of stake consensus protocol (based on the Tendermint Byzantine fault tolerant consensus algorithm) with dynamic committee selection, providing finality guarantees for transactions.
- Protocol governance logic.

For explanations of core concepts refer to:

- [Architecture](/autonity/architecture/) for an Autonity system's technical architecture and protocol primitives.
- [System model](/autonity/system-model/) for the functions of participant nodes and blockchain primitives comprising the structure of an Autonity system's peer-to-peer network and distributed ledger.
- [Client](/autonity/client/) for an overview of AGC features.
- [Consensus](/autonity/consensus/) for the protocol's implementation of the Tendermint BFT consensus algorithm, committee selection, and validators.
- [Validator](/autonity/validator) for the role of validators and the functions they perform.
- [Staking](/autonity/staking/) for protocol mechanisms and model for liquid staking.
- [Tokenomics](/autonity/client/) for the protocol's native coin and tokens - _Auton_ settlement coin, _Newton_ stake token, and _Liquid Newton_ stake token.
- The [Glossary](/glossary/#participant) for definitions of terms and concepts used in the documentation.

## System participants

System participants of an Autonity network are:
 - nodes: network peers running the AGC client software.
 - validators: nodes with bonded stake and candidates for selection to the consensus committee. The consensus committee is responsible for proposing and deciding on new blocks.
- stake holder: a holder of _Newton_ stake token that delegates stake to one or more validators in order to secure the network.  Validators may also "self-bond", or delegate stake to their own validator node.  Stake holders receive _Liquid Newton_ for bonded stake.
- account holder: externally owned accounts of human users of the system.
