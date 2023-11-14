
---
title: "Autonity Go Client (AGC)"
linkTitle: "Autonity Go Client (AGC)"
weight: 4
description: >
  Main client software features
---

AGC is the reference implementation of the Autonity Protocol and the main client software run by participants in an Autonity network. It is a fork of Geth. For the current geth rebase version see [Codebase](/reference/codebase/).

## Features

### Core logic

- _Autonity Protocol Contract_, the core Autonity Protocol contract providing operations for: protocol governance, staking, validator registration, consensus committee selection, and staking rewards distribution. See [Autonity Protocol Contract](/concepts/architecture/#autonity-protocol-contract).
- _Autonity Accountability Contract_, the accountability and fault detection protocol contract providing operations for: returning accountability history and status, handling submitted accountability events, and computing accountability and slashing penalties. See [Autonity Accountability Contract](/concepts/architecture/#autonity-accountability-contract) and concept [Accountability and fault detection](/concepts/accountability/).
- _Autonity Oracle Contract_, the oracle protocol contract providing operations for: computing median price data, and managing the currency-pair symbols for which price data is provided by the Autonity oracle network. See [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract) and concepts [Oracle Server](/concepts/oracle-server/) and [Oracle network](/concepts/oracle-network/).
- _EVM_, the deterministic virtual machine providing the state transition function for computing global state
- _Consensus_, Autonity implementation of the  Tendermint BFT consensus protocol managing state replication and block production with dynamic committee selection. See [Blockchain Consensus](/concepts/architecture/#blockchain-consensus)
- _P2P Networking_, transport and wire protocols providing reliable broadcast for blockchain and consensus state synchronisation between participants. See [Communication Layer](/concepts/architecture/#communication-layer)
- _Core_, the core Autonity Go Client codebase managing interactions with the blockchain ledger and EVM.

### State storage
Each participant maintains a local state database synchronised to world state, using a LevelDB k-v store. See also [System model](/concepts/system-model/) and the [Ledger object](/concepts/system-model/#the-ledger-object). 

### Interfaces
The client provides interfaces for:

- Autonity Contract Interfaces and JSON-RPC APIs - see [Autonity Interfaces](/reference/api/) Reference
- RPC calls from the Autonity Utility Tool `aut`. `aut` provides a [command-line interface](/reference/cli/#command-line-facilities) to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.
- Command line options for client configuration and interaction - see [Command-line options](/reference/cli/agc/#command-line-options) Reference
- Metrics and logging, see [Command-line options](/reference/cli/agc/#command-line-options). For `go-metrics`, see the Autonity GitHub [/metrics/README <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity/blob/master/metrics/README.md).
