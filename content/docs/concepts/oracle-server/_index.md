
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
- _Autonity Oracle Contract_, the oracle protocol contract logic deployed to the ledger by AGC. The Oracle Contract manages the computation of median price data for currency pair price reports submitted by oracle servers. The contract provides operations for: computing median price ("_on-chain aggregation_") from submitted price report transactions in oracle voting rounds, providing median price data via interface, and managing the currency-pair symbols for which price data is provided by the Autonity oracle network. See [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract) and concept [Client](/concepts/client/).
- _Networking_, the system uses WebSocket and HTTP network protocols. RPC calls are made to configured data source providers over HTTP, HTTPS, or WebSocket. The system establishes a connection to the AGC validator using WebSocket to (a) submit price report transactions and (b) listen for on-chain Oracle Contract events.

The RPC calls to configured data source might have different network protocols, it may have HTTP, HTTPS, or even Web Socket, the plugin should implement this adaptation protocols, it depends on the provider's scheme.

### State storage

Oracle server is stateless and does not maintain an off-chain database. L1 price aggregation is computed by the server in memory. Price report transactions submitted to the Oracle Contract on-chain are committed to the Autonity network's ledger and persisted in world state. See also [System model](/concepts/system-model/) and the [Ledger object](/concepts/system-model/#the-ledger-object). 

### Data adaptors - plugin architecture

Oracle server provides a standard interface for data adaptors pulling data from external data providers. Any party can build a new plugin implementing this interface and so provide an adaptor for any data source on demand.

The oracle server scans and load plugins from the `/plugins` directory (see how to [install](/oracle/install-oracle/) oracle server) during runtime. Detection of new or updated plugins is dynamic; no shutdown of the oracle client is required to detect and apply the change.

#### Runtime plugin management

- Adding new plugins. To add an adaptor for a new data source, place the new plugin into the oracle server's `/plugins` directory. The oracle server auto-discovers and manages it. There are no other operations required from the operator.
- Replace or upgrade running plugins. To replace a (running) data adaptor plugin with a new version, just replace the binary in the `/plugins` directory. The oracle server auto-discovers the new version by checking the modification time of the binary and manages the plugin replacement itself. There are no other operations required from the operator.

#### Oracle data providers

Valid price data sources are exchanges providing up to date market prices for trades in the currency pairs provided by the oracle server's configuration.

Primary data providers for oracle data are:

- FX and ATN/NTN currency pairs utilised in the Autonity Stability Mechanism.

A basic set of data adaptor plugins for sourcing this data is provided out the box with oracle server for testnet pre-Mainnet:

- Forex plugins: for connecting to public FX data sources. See the `forex_` prefixed adaptors in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins). Four forex plugins are currently provided.
- Simulator plugin: for simulated ATN/NTN data. See the `simulator_plugin` adaptor in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins). 

{{% alert title="Info" color="info"%}}
ATN and NTN symbols are preview listed but untraded:

- https://www.coingecko.com/en/coins/auton
- https://www.coingecko.com/en/coins/newton

Plugins for retrieving ATN/NTN price data are to be developed for Mainnet launch.
{{% /alert %}}

#### Developing data plugins

Additional data adaptors for any external data source can be developed using the oracle server's plugin template. See:

- Adaptor code template `template_plugin` in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins).
- Guide for how _To write a new plugin_ using the template in [`/plugins/README`<i class='fas fa-external-link-alt'></i>](https://github.com/clearmatics/autonity-oracle/tree/master/plugins#readme).

### Oracle server lifecycle

Oracle server lifecycle management is an adjunct of validator operations and comprises software installation and the configuration and (optionally) development of adaptors for data to data sources for currency pair price data.

The sequence of lifecycle events for an oracle server is:

1. Join the oracle network. The validator’s oracle server is installed and configured: oracle server account created, data plugins configured to pull currency pair data from external data sources; oracle server configured to connect to the validator's main client software.
2. Register as a validator. The validator’s node is registered as a validator by the submission of registration parameters, which include the oracle address.
3. Oracle server initialised. The server is initialised and begins retrieving price report data from its connected data sources transactions to its connected validator node.
3. Selection to consensus committee. Assuming stake bonded to validator and if selected to the consensus committee, the validator (a) participates in block validation, (b) participates in oracle voting rounds by oracle server submitting oracle vote transactions to the oracle contract with cryptographic commits and reveals of price report submissions.
4. Runtime plugin management. The validator operator manages and updates data source plugins in accordance with currency pair changes and own operational requirements.

### Interfaces

The oracle server provides interfaces for:

- Oracle Contract Interfaces and JSON-RPC APIs - see [Autonity Interfaces](/reference/api/oracle/) Reference
- Plugin interface - a standard interface implemented by data adaptors developed to pull data from external data sources on demand.

<!--
TODO
- RPC calls from the Autonity Utility Tool `aut`. `aut` provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.
-->

- Command line options for oracle server configuration and interaction - see [Command-line options](/reference/cli/oracle/#command-line-options) Reference.
