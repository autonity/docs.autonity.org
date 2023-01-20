
---
title: "Consensus Committee"
linkTitle: "Consensus Committee"
weight: 2
description: >
  The role of the consensus committee on the Autonity network - eligibility, selection, and mechanism
---

## Overview

The consensus committee is the set of validator nodes participating in the consensus protocol for a block epoch. It is responsible for proposing new blocks, voting on block proposals to affirm the validity of proposed blocks and decide if committed to state, and notifying new blocks to peer nodes to replicate the new state. 

A new consensus committee is selected at every block epoch in an autonomous process executed by the Autonity Protocol. The selection algorithm ranks registered validators according to the amount of their bonded stake, selecting those with the highest stake to fill the available committee member slots. Ranking by stake serves to maximise the amount of stake securing the network in an epoch. 

For performance optimisation, due to the constraints of BFT consensus algorithms, the maximum committee size is set as a protocol parameter. It is set at genesis, but can be changed during runtime to optimise the trade-off between performance of the consensus round and democratising access to participate in consensus.

## Committee member selection

The Consensus Committee for an upcoming epoch is chosen by an autonomous protocol-only function. The algorithm is run  as the last block of the current epoch is finalised to choose the committee for the upcoming epoch. Committee members are selected by ranking according to the stake bonded to them. 

The selection algorithm:

- determines the set of eligible validators: registered validators with bonded stake `> 0`
- ranks these candidates by the amount of stake bonded
- selects those with the highest amount of stake to fill the available committee member slots 

At genesis of an Autonity Network committee selection is run against the set of validators specified in the `genesis.json` configuration file to determine the genesis consensus committee. (See [Genesis Reference](/reference/genesis)). Post genesis, the set of validators eligible for selection becomes dynamic as new validators are registered and become active, existing validators pause and are removed from future  committee selection until active again, and voting power changes as stake is bonded and unbonded.

The committee set is recorded in every block header in the `committee` field.

## Proposer selection

The proposer for each consensus instance is computed  by the protocol using a stateless weighted round robin (WRR)  selection algorithm. The proposer is chosen from the committee by weighted random sampling, weighting the probability of a committee member's selection by the amount of its voting power. The selection mechanism is deterministic and will always select the same address, given the same block height, round, and committee in Autonity Contract state.
  
The selection algorithm:

- calculates the total voting power of the current consensus committee, summing the voting power of each committee member
- calculates a deterministic seed for selecting the index position of the block proposer from the list of committee members
    - The index position is calculated by the [modulo](https://docs.soliditylang.org/en/latest/types.html#modulo) of an integer value (derived from keccak256 hashing of the proposed block's height and consensus round number) and the total voting power of the committee. I.e. `index = value % total_voting_power`. 
- selects the proposer by selecting the committee member at the index position from the committee list.

## Committee size

The `committeeSize` is set as a default value in the Autonity Contract but can be changed after network genesis by governance. See Reference section [API function `setCommitteeSize()`](/reference/api#governance-api). 

The consensus committee size is theoretically constrained due to the overhead of the signature verification of each committee member required by the BFT consensus protocol's implementation.

In this version of Autonity the optimal size is in the range of 20-30 committee members. Protocol developent will improve this to increase decentralisation, targeting committee membership of 100.

## Voting power changes

Transactions to bond and unbond stake to a validator are submitted at any point in an epoch but do not affect committee membership or stake reward distribution in the current epoch. Staking transitions and the resulting change in voting power are applied at epoch end before the committee selection algorithm is run to select the committee for the upcoming epoch.

## Committee functions

Consensus committee members are responsible for proposing and voting on new blocks in consensus rounds. For every round a new leader is selected by the protocol, responsbile for proposing a new block and initiating a consensus round in which committee members propose a new block. On approval of a new block, the leader is responsible for propagating the new block to the P2P network and broadcasting it on the Autonity Communication Layer. The other consensus committee members coincidentally broadcast notification of the new block, facilitating rapid state machine replication by giving notification of the new block to sync request if not already held in local state.

## Audit trail

Committee membership and pending staking transitions can be audited by RPC call to the Autonity Contract:

- `getCommittee()` to return the current committee members
- `getBondingReq()` and `getUnbondingReq()` to return pending bonding and unbonding requests to be applied at finalisation of the current epoch's last block

Historic data can be retrieved by querying system state:

- block header `committee` field
- block transactions for bond and unbond requests
