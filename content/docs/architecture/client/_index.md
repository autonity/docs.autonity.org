
---
title: "Autonity Go Client (AGC)"
linkTitle: "Client"
weight: 3
description: >
  Main client software features
---

AGC is the reference implementation of the Autonity Protocol and the main client software run by participants in an Autonity network. It is a fork of Geth. The current geth rebase version is 1.10.9.

## Features

### Core logic

- _Autonity Protocol Contract_, the protocol contract logic deployed to the ledger providing operations for: protocol governance, staking, validator registration, consensus committee selection, and staking rewards distribution. See [Autonity Protocol Contract](/autonity/architecture/#autonity-protocol-contract).
- _EVM_, the deterministic virtual machine providing the state transition function for computing global state,
- _Consensus_, the Tendermint BFT consensus protocol managing state replication and block production with dynamic committee selection. See [Blockchain Consensus](/autonity/architecture/#blockchain-consensus).
- _P2P Networking_, transport and wire protocols providing reliable broadcast for blockchain and consensus state synchronisation between participants. See [Communication Layer](/autonity/architecture/#communication-layer)
- _Core_, the core Autonity Go Client codebase managing interactions with the blockchain ledger and EVM.


### State storage
Each participant maintains a local state database synchronised to world state, using a LevelDB k-v store. See also [System model](/autonity/system-model/) and the [Ledger object](/autonity/system-model/#the-ledger-object). 

### APIs
The client provides APIs for:

- JSON-RPC - see [JSON-RPC API](/reference/api/) Reference
- RPC calls from a JavaScript runtime environment - see [Autonity NodeJS Console](/reference/cli/#autonity-nodejs-console) Reference
- Command line options for client configuration and interaction - see [Command-line options](/reference/cli/#command-line-options) Reference
- Metrics and logging, see [Command-line options](/reference/cli/#command-line-options). For `go-metrics`, see the Autonity GitHub [/metrics/README](https://github.com/autonity/autonity/blob/master/metrics/README.md).
