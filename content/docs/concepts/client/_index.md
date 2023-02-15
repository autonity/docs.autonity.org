
---
title: "Autonity Go Client (AGC)"
linkTitle: "Client"
weight: 3
description: >
  Main client software features
---

AGC is the reference implementation of the Autonity Protocol and the main client software run by participants in an Autonity network. It is a fork of Geth. For the current geth rebase version see [Codebase](/reference/codebase/).

## Features

### Core logic

- _Autonity Protocol Contract_, the protocol contract logic deployed to the ledger providing operations for: protocol governance, staking, validator registration, consensus committee selection, and staking rewards distribution. See [Autonity Protocol Contract](/concepts/#autonity-protocol-contract).
- _EVM_, the deterministic virtual machine providing the state transition function for computing global state,
- _Consensus_, Autonity implementation of the  Tendermint BFT consensus protocol managing state replication and block production with dynamic committee selection. See [Blockchain Consensus](/concepts/#blockchain-consensus).
- _P2P Networking_, transport and wire protocols providing reliable broadcast for blockchain and consensus state synchronisation between participants. See [Communication Layer](/concepts/#communication-layer)
- _Core_, the core Autonity Go Client codebase managing interactions with the blockchain ledger and EVM.


### State storage
Each participant maintains a local state database synchronised to world state, using a LevelDB k-v store. See also [System model](/concepts/system-model/) and the [Ledger object](/concepts/system-model/#the-ledger-object). 

### Interfaces
The client provides interfaces for:

- Autonity Contract Interfaces and JSON-RPC APIs - see [Autonity Interfaces](/reference/api/) Reference
<!-- - RPC calls from a JavaScript runtime environment - see [Autonity NodeJS Console](/reference/cli/#autonity-nodejs-console) Reference -->
- RPC calls from the `autcli` tool. This provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.
- Command line options for client configuration and interaction - see [Command-line options](/reference/cli/#command-line-options) Reference
- Metrics and logging, see [Command-line options](/reference/cli/#command-line-options). For `go-metrics`, see the Autonity GitHub [/metrics/README](https://github.com/autonity/autonity/blob/master/metrics/README.md).
