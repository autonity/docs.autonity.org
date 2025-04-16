---
title: "Autonity Go Client (AGC)"
description: >
  Main client software features
---

AGC is the reference implementation of the Autonity Protocol and the main client software run by participants in an Autonity network. It is a fork of Geth. For the current geth rebase version see [Codebase](/reference/codebase/).

## Features

### Core logic

- _Autonity Protocol Contract_, the core Autonity Protocol contract providing operations for: protocol governance, staking, validator registration, consensus committee selection, and staking rewards distribution. See [Autonity Protocol Contract](/concepts/architecture/#autonity-protocol-contract).
- _Autonity Accountability Contracts_, the accountable and omission fault detection protocol contracts providing operations for: detecting consensus rule infractions and failure to participate in consensus voting rounds, and computing rewards and penalties to incentivise correct and disincentivise incorrect behavior [by committee members](/concepts/consensus/committee/). See [Autonity Accountability Contract](/concepts/architecture/#autonity-accountability-contract), [Autonity Omission Accountability Contract](/concepts/architecture/#autonity-omission-accountability-contract) and concepts [Accountability fault detection (AFD)](/concepts/afd/) and [Omission fault detection (OFD)](/concepts/ofd/).
- _Autonity Oracle Contract_, the oracle protocol contract providing operations for: computing median price data, managing the currency-pair symbols for which price data is provided by the Autonity oracle network, and oracle accountability fault detection to incentivise correct and timely price reporting by the oracle network. See [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract) and concepts [Oracle Server](/concepts/oracle-server/), [Oracle network](/concepts/oracle-network/), and [Oracle accountability fault detection (OAFD)](/concepts/oafd/).
- _EVM_, the deterministic virtual machine providing the state transition function for computing global state
- _Consensus_, Autonity implementation of the  Tendermint BFT consensus protocol managing state replication and block production with dynamic committee selection. See [Blockchain Consensus](/concepts/architecture/#blockchain-consensus)
- _P2P Networking_, transport and wire protocols providing reliable broadcast for blockchain and consensus state synchronisation between participants. See [Communication Layer](/concepts/architecture/#communication-layer)
- _Core_, the core Autonity Go Client codebase managing interactions with the blockchain ledger and EVM.

### State storage
Each participant maintains a local state database synchronised to world state, using a LevelDB k-v store. See also [System model](/concepts/system-model/) and the [Ledger object](/concepts/system-model/#the-ledger-object). 

### Interfaces
The client provides interfaces for:

- Autonity Contract Interfaces and JSON-RPC APIs - see [Autonity Interfaces](/reference/api/) Reference
- RPC calls from Autonity CLI that provides a [command-line interface](/reference/cli/#command-line-facilities) to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.
- Command line options for client configuration and interaction - see [Command-line options](/reference/cli/agc/#command-line-options) Reference
- Metrics and logging, see [Command-line options](/reference/cli/agc/#command-line-options). For `go-metrics`, see the Autonity GitHub [/metrics/README](https://github.com/autonity/autonity/blob/master/metrics/README.md).
