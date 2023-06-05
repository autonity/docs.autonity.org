---
title: "Autonity Oracle Command-line"
linkTitle: "Autonity Oracle Command-line"
weight: 20
description: >
  Command-line options and facilities of the Autonity Oracle Server
---

<!--
## Command-line facilities

Command-line tools for interacting with an Autonity Oracle Server are provided by:

- Autonity Utility Tool `aut`. A Python command-line RPC client for Autonity. The tool provides access to Autonity Oracle Contract interface functions.

For `aut` installation, usage, and command-line options see RReference [Setup the Autonity Utility Tool (aut)](/account-holders/setup-aut/).

For calling Oracle Contract functions using `aut` see Reference [Autonity Interfaces, Oracle Contract interface](/reference/api/oracle/).
-->
## Command-line options

Autonity Oracle Server supports command-line options for configuration.

## Usage

Run `autoracle --help` to view the options:

| Options | Description |
|:--|:--|
| `-oracle_autonity_ws_url` | The websocket URL of autonity client |
| `-oracle_crypto_symbols` | The symbols string separated by comma |
| `-oracle_key_file` | The file that save the private key of the oracle client |
| `-oracle_key_password` | The password to decode your oracle account's key file |
| `-oracle_plugin_dir` | The DIR where the adapter plugins are stored. Default: ./build/bin/plugins |

