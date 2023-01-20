
---
title: "Tendermint BFT consensus"
linkTitle: "Tendermint BFT"
weight: 1
description: >
  Tendermint BFT in Autonity
---

Autonity manages blockchain state machine replication by the deterministic Tendermint [Byzantine-fault tolerant](/glossary/#byzantine-fault-tolerance-bft) consensus algorithm.

Tendermint is Proof-of-Stake (PoS) based and provides state machine replication by a repeated consensus model where each new block is proposed and agreed by a sequential consensus instance proposed and agreed by consensus committee members.

Tendermint provides Byzantine fault tolerance for up to 1/3 of voting power. That is, if the voting power of faulty participants is bounded by _f_, and the total voting power of the system equals _N_, then _N=3f+1_ is required for correct system operation, allowing up to _1/3_ of nodes with fault. A fault is a failure to correctly participate in consensus. Faults can be Byzantine (i.e. malicious) behaviour failing to follow protocol or technical failure to participate in consensus.

### Dynamic committee selection
The consensus committee is dynamic, selected from the validators registered on the Autonity system. For each block [epoch period](/glossary/#epoch-period) a new committee is selected by protocol logic. Selection is weighted by the relative size of the validator's bonded stake amount, maximising consensus stake. The sum of bonded stake in a committee is the amount of stake securing the system's replication against Byzantine faults. A committee member's individual voting power is a function of the amount of stake bonded to it, i.e. to its share of the consensus stake.

To learn more about the committee and the selection algorithm see [Consensus Committee](/autonity/consensus/committee/).

### Consensus round and internal state
In each consensus instance a consensus round of three voting steps is executed as a sequential exchange of cryptographically signed (i.e. 'sealed') messages broadcast between committee members:

- Proposal. A block proposer is selected from the committee. The proposer validates and orders a set of transactions to create a suggested new block and broadcasts this proposal to the committee.
- Prevote. Each committee member validates suggested block correctness and broadcasts a Prevote to approve or reject the proposal.
- Precommit. Each committee member waits to receive a BFT quorum (_2f+1_ aggregate voting power) of Prevote messages to recognise the proposal as a possible decided block, and broadcasts a Precommit to approve or reject the proposal.

If the committee member receives _2f+1_ Precommits, then by protocol the block proposal is decided and:

- the block is broadcast to the network. The block proposer broadcasts the new block, its [block header](/autonity/system-model/#block-header) containing the block proposal and precommit message seals and an array of the committee members that voted for the block. Other committee members broadcast a (new) block announcement.
- the block is committed to the ledger. Participants that receive the new block check validity by verifying the seals. Participants that receive an announcement sync to retrieve the block, verifying  by computing block state as it appends the block to the chain.

If quorum is not reached at Prevote or Precommit stages or there is timeout, then the round terminates and a new consensus instance begins.
