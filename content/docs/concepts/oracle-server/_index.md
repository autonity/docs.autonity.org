
---
title: "Autonity Oracle Server (AOS)"
linkTitle: "Oracle Server"
weight: 4
description: >
  Oracle server software features
---

AOS is the reference implementation of the Autonity Oracle Protocol and the oracle server software run by validator nodes in an Autonity network. It is composed of off- and on-chain components.

## Features

### Core logic

- _Core_, the core off-chain Autonity Oracle Server (AOS) codebase. Core manages interactions with external price data source providers via data adaptor 'plugins' and the connected Autonity Go Client (AGC) validator node AOS serves. Core executes aggregation of data from external sources ("_L1 aggregation_"), calculates an aggregated median price, and submits price report transactions on-chain to the Oracle Contract.
- _Autonity Oracle Contract_, the oracle protocol contract logic deployed to the ledger by AGC. The Oracle Contract manages the computation of median price data for currency pair price reports submitted by oracle servers. The contract provides operations for: computing median price ("_L2 aggregation_") from submitted price report transactions in oracle voting rounds, providing median price data via interface, and managing the currency-pair symbols for which price data is provided by the Autonity oracle network. See [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract) and concept [Client](/concepts/client/).
- _Networking_, the system uses WebSocket and HTTP connections. HTTP RPC calls are made to configured data source providers, and a WebSocket connection is established to the AGC validator to (a) submit price report transactions and (b) listen for on-chain Oracle Contract events.

### State storage

Oracle server is stateless and does not maintain an off-chain database. L1 price aggregation is computed by the server in memory. Price report transactions submitted to the Oracle Contract on-chain are committed to the Autonity network's ledger and persisted in world state. See also [System model](/concepts/system-model/) and the [Ledger object](/concepts/system-model/#the-ledger-object). 

### Interfaces

The oracle server provides interfaces for:

- Oracle Contract Interfaces and JSON-RPC APIs - see [Autonity Interfaces](/reference/api/oracle/) Reference
- Plugin interface - a standard interface implemented by data adaptors developed to pull data from external data sources on demand.

The oracle server scans and load plugins from the plugin directory during runtime. Detection of new or changed plugins is dynamic;
no shutdown of the oracle client is required to detect and apply the change.
<!--
- RPC calls from the Autonity Utility Tool `aut`. `aut` provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.
-->

- Command line options for oracle server configuration and interaction - see [Command-line options](/reference/cli/oracle/#command-line-options) Reference.
