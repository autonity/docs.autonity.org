---
title: Setup the Autonity Utility Tool (aut)
description: How to install and configure the `aut` command-line tool on your local machine.
---

The recommended way of interacting with the Autonity network is via the [Autonity Utility Tool](https://github.com/autonity/aut) `aut`, which provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.  In general it only needs to be installed on _local_ machines, to connect to the RPC endpoint of an Autonity Go Client (either your own node, or a node providing public RPC access).

For full details and to report any issues, see the [`aut` repository](https://github.com/autonity/aut).

## Installation {#install}

::: {.callout-note title="Prerequisites" collapse="false"}
A working Python install with the `pip` tool is required.
:::

The tool can be installed using [pipx](https://github.com/pypa/pipx). To get the latest release run:

```bash
pipx install --force git+https://github.com/autonity/aut
```

::: {.callout-note title="Note" collapse="false"}
If you are experiencing errors such as:

```
ImportError: cannot import name 'NodeAddress' from 'autonity.validator'
```

You are using an earlier version of `aut`. Please upgrade your `aut` tool to use the latest release using the installation command above.

It is highly recommended to also follow the [instructions in the repository](https://github.com/autonity/aut) to set up command-line completion.
:::

## Configuration using the `.autrc` file {#configure}

As detailed in the [`aut` repository](https://github.com/autonity/aut#configuration-using-autrc-files), some configuration parameters can be set in an `.autrc` file in the working directory or any parent directory.  As a minimal configuration, it is recommended to create an `.autrc` containing the end-point to use for RPC operations:

```
[aut]
rpc_endpoint=https://rpc1.<NETWORK_NAME>.autonity.org
```

See the [list of available networks](/networks/) to determine the correct endpoint to use.

## Usage {#usage}

The tool is intended to be self documenting via `aut --help`, `aut <command> --help` etc.  Some example commands can be found in the [`aut` repository](https://github.com/autonity/aut).

We suggest trying the following command (which retrieves some basic information about the connected node and network) to confirm that the install and configuration have been successful:

```bash
aut node info
```
```console
{
  "eth_accounts": [],
  "eth_blockNumber": 12803619,
  "eth_gasPrice": 1000000000,
  "eth_syncing": false,
  "eth_chainId": 65100000,
  "net_listening": true,
  "net_peerCount": 19,
  "net_networkId": "65100000",
  "web3_clientVersion": "Autonity/v0.10.0-1183a113-20230118/linux-amd64/go1.19",
  "admin_enode": "enode://d9a7297b2bec3c2f92233dc42f53c0cf98af30528a56765b102d9e28be2a760b7fd3045790246d1a5836af9a8ea5d2dbcc9b56864f6391045ba76391d9db931e@77.86.9.81:30303",
  "admin_id": "8794927d6dda6f8cb45bc7eefd9084dbb3b81ce508ff43e1ccb7fe904ccd2cfc"
}
```

::: {.callout-note title="Note" collapse="false"}
The output above may vary depending on the version of the Autonity Go Client you are connected to.
:::

::: {.callout-note title="Info" collapse="false"}
Now that you have a working `aut` installation, you can  [create](/account-holders/create-acct/) and [fund](/account-holders/fund-acct/) and account on the network, and then [create and submit a transaction](/account-holders/submit-trans-aut/).
:::

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
