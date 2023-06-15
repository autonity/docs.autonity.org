---
title: "Autonity Oracle Server (AOS)"
linkTitle: "Oracle"
weight: 4
description: >
  Oracle server software features
---

AOS is the reference implementation of the Autonity Oracle Protocol and the oracle server software run by validator nodes in an Autonity network. It is composed of off- and on-chain components.

## Features

### Core logic

- _Core_, the core off-chain Autonity Oracle Server codebase managing interactions with the external price data source providers and the on-chain Oracle Contract via the connected Autonity Go Client node. Core executes aggregation of data from external sources ("_L1 aggregation_"), calculates a median price, and submits price report transactions on-chain to the Oracle Contract.
- _Autonity Oracle Contract_, the oracle protocol contract logic deployed to the Autonity network ledger providing operations for: computing median price ("_L2 aggregation_") from submitted price report transactions in oracle voting rounds, providing median price data, and managing the currency-pair symbols for which price data is provided by the Autonity oracle network. See [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract).
>>>>>>> f2a060f (Edits to Reference pages, Concepts: client, add Oracle, Architecture)
- _Networking_, WebSocket and HTTP connections. HTTP RPC calls to configured data source providers; WebSocket connection to the Autonity Go Client validator node served to (a) submit price report transactions; (b) listen for on-chain Oracle Contract events.

### State storage

Oracle server is stateless and does not maintain an off-chain database. L1 price aggregation is computed by the server in memory. Price report transactions submitted to the Oracle Contract on-chain are committed to the Autonity network's ledger and persisted in world state. See also [System model](/concepts/system-model/) and the [Ledger object](/concepts/system-model/#the-ledger-object). 

### Interfaces

The oracle server provides interfaces for:

- Oracle Contract Interfaces and JSON-RPC APIs - see [Autonity Interfaces](/reference/api/oracle/) Reference

<!--
- RPC calls from the Autonity Utility Tool `aut`. `aut` provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.
-->

- Command line options for oracle server configuration and interaction - see [Command-line options](/reference/cli/oracle/#command-line-options) Reference.
