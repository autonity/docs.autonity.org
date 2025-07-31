---
title: Setup Autonity CLI
description: How to install and configure the `aut` command-line tool on your local machine.
---

The recommended way of interacting with the Autonity network is via [Autonity CLI](https://github.com/autonity/autonity-cli), which provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality. In general it only needs to be installed on _local_ machines, to connect to the RPC endpoint of an Autonity Go Client (either your own node, or a node providing public RPC access).

For full details and to report any issues, see its [repository](https://github.com/autonity/autonity-cli).

## Installation {#install}

::: {.callout-note title="Prerequisites" collapse="false"}
A working Python install with the `pip` tool is required.
:::

The tool can be installed using [pipx](https://github.com/pypa/pipx). To get the latest release run:

```bash
pipx install autonity-cli
```

Once installed, the tool can be invoked with the `aut` command.

::: {.callout-warning title="Always use the latest version of Autonity CLI" collapse="false"}
If you are experiencing errors such as:

```
ImportError: cannot import name 'NodeAddress' from 'autonity.validator'
```

You are using an earlier version. Please upgrade your Autonity CLI to use the latest release with the installation command:

```bash
pipx upgrade autonity-cli
```

It is highly recommended to also follow the [instructions in the repository](https://github.com/autonity/autonity-cli) to set up command-line completion.
:::

## Configuration using the `.autrc` file {#configure}

As detailed in its [repository](https://github.com/autonity/autonity-cli#configuration-using-autrc-files), some configuration parameters can be set in an `.autrc` file in the working directory or any parent directory.  As a minimal configuration, it is recommended to create an `.autrc` containing the end-point to use for RPC operations:

Given an `RPC_URL` from <https://chainlist.org/?search=autonity&testnets=true>.

```
[aut]
rpc_endpoint=$RPC_URL
```

See the [list of available networks](/networks/) to determine the correct endpoint to use.

## Usage {#usage}

The tool is intended to be self documenting via `aut --help`, `aut <command> --help` etc. Some example commands can be found in its [repository](https://github.com/autonity/autonity-cli).

Try the following command (which retrieves some basic information about the connected node and network) to confirm that the install and configuration have been successful:

```bash
aut node info
```

Which will print to terminal:

```console
{
  "eth_accounts": [],
  "eth_blockNumber": 297602,
  "eth_gasPrice": 1000000000,
  "eth_syncing": false,
  "eth_chainId": 65110004,
  "net_listening": true,
  "net_peerCount": 31,
  "net_networkId": "65110004",
  "web3_clientVersion": "Autonity/v1.1.0/linux-amd64/go1.24.0",
  "admin_enode": "enode://71b3066d89718920c785ed1b919073ca27fa32a7982f77ff1603ca5f56c3678c7f4b8d7e6cd6c7c79d9cbd01e83b571b73ccc138178126f5c53dcb2a399db6c0@34.142.33.129:30303",
  "admin_id": "5546108b77f2d5ea1b4d87319564eb7b0d12c50114f2eaf39ca08a2c15bb5bae"
}
```

::: {.callout-note title="Note" collapse="false"}
The output above may vary depending on the version of the Autonity Go Client you are connected to.
:::

::: {.callout-tip title="Next steps &hellip;" collapse="false"}
Now that you have a working `aut` installation, you can  [create](/account-holders/create-acct/) and [fund](/account-holders/fund-acct/) and account on the network, and then [create and submit a transaction](/account-holders/submit-trans-aut/).
:::

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
