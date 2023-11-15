---
title: "Autonity Oracle Server Command-line"
linkTitle: "Autonity Oracle Server Command-line"
weight: 20
description: >
  Command-line options and facilities of the Autonity Oracle Server
---
<!--
## Command-line facilities

Command-line tools for interacting with an Autonity Oracle Server are provided by:

- Autonity Utility Tool `aut`. A Python command-line RPC client for Autonity. The tool provides access to Autonity Oracle Contract interface functions.

For `aut` installation, usage, and command-line options see Reference [Setup the Autonity Utility Tool (aut)](/account-holders/setup-aut/).

For calling Oracle Contract functions using `aut` see Reference [Autonity Interfaces, Oracle Contract interface](/reference/api/oracle/).
-->
## Command-line options

Autonity Oracle Server provides command-line options for displaying version and help information, and setting oracle server configuration.

## Usage

Run `autoracle --help` to view the options:

| COMMANDS: | Description |
|:--|:--|
| `version`, `v` | Print version information and default configuration |
| `-help`, `-h`  | Shows a list of Oracle Server configuration options |


| ORACLE SERVER OPTIONS: | Description | Default | Required? |
|:--|:--|:--|:--|
| `-oracle_autonity_ws_url` | The WS-RPC server listening interface and port of the connected Autonity Go Client node. | "ws://127.0.0.1:8546" | Yes |
| `-oracle_gas_tip_cap` | The gas priority fee cap set for oracle data report transactions. Must be a non-zero value. | Default `1` | No |                                                             
| `-oracle_symbols` | The currency pair symbols the oracle returns data for. A comma-separated list. | "AUD-USD,CAD-USD,SEK-USD,EUR-USD,GBP-USD,JPY-USD,ATN-USD,NTN-USD" | No |
| `-oracle_key_file` | The path to the oracle server key file. | (Defaults to testing key in `/test_data/keystore`) | Yes |
| `-oracle_key_password` | The password to the oracle server key file. | (Defaults to password for testing key in `/test_data/keystore`) | Yes |
| `-oracle_plugin_dir` | The path to the DIR where the data source plugins are stored. | `./build/bin/plugins` | No |
| `-oracle_plugin_conf` | The path to the data source plugins YAML configuration file `plugins-conf.yml`. | `./build/bin/plugins/plugins-conf.yml` | Yes |
