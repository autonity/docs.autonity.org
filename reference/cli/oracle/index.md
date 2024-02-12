---
title: "Autonity Oracle Server Command-line"
linkTitle: "Autonity Oracle Server Command-line"
weight: 20
description: >
  Command-line options and facilities of the Autonity Oracle Server
---

## Command-line options

Autonity Oracle Server provides command-line options for displaying version and help information, and setting oracle server configuration.

## Usage

Run `autoracle --help` to view the options:

| COMMANDS: | Description |
|:--|:--|
| `version`, `v` | Print version information and default configuration |
| `--help`, `-h`  | Shows a list of Oracle Server configuration options |


| ORACLE SERVER OPTIONS: | Description | Default | Required? |
|:--|:--|:--|:--|
| `-ws` | The WS-RPC server listening interface and port of the connected Autonity Go Client node. | "ws://127.0.0.1:8546" | Yes |
| `-tip` | The gas priority fee cap set for oracle data report transactions. Must be a non-zero value. | Default `1` | No |                                                             
| `-symbols` | The currency pair symbols the oracle returns data for. A comma-separated list. | "AUD-USD,CAD-USD,SEK-USD,EUR-USD,GBP-USD,JPY-USD,ATN-USD,NTN-USD" | No |
| `-key.file` | The path to the oracle server key file. | (Defaults to testing key in `/test_data/keystore`) | Yes |
| `-key.password` | The password to the oracle server key file. | (Defaults to password for testing key in `/test_data/keystore`) | Yes |
| `-plugin.dir` | The path to the DIR where the data source plugins are stored. | `./plugins` | No |
| `-plugin.conf` | The path to the data source plugins YAML configuration file `plugins-conf.yml`. | `./plugins-conf.yml` | Yes |
| `-log.level` | The logging level. Available levels are:  0: NoLevel, 1: Trace, 2:Debug, 3: Info, 4: Warn, 5: Error. | `2` | No |
