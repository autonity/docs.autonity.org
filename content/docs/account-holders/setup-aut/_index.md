---
title: "Setup the Autonity Utility Tool (aut)"
linkTitle: "Setup the Autonity Utility Tool (aut)"
weight: 30
description: >
  How to install and configure the `aut` command-line tool on your local machine.
---

The recommended way of interacting with the Autonity network is via the [Autonity Utility Tool <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/aut) `aut`, which provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.  In general it only needs to be installed on _local_ machines, to connect to the RPC endpoint of an Autonity Go Client (either your own node, or a node providing public RPC access).

For full details and to report any issues, see the [`aut` repository <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/aut).

## Installation {#install}

{{< alert title="Prerequisites" >}}
A working Python install with the `pip` tool is required.
{{< /alert >}}

In general, the tool can be installed using [pipx <i class='fas fa-external-link-alt'></i>](https://github.com/pypa/pipx).

```bash
pipx install git+https://github.com/autonity/aut
```

{{< alert title="Note" >}}
It is highly recommended to also follow the [instructions in the repository <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/aut) to set up command-line completion.
{{< /alert >}}

## Configuration using the `.autrc` file {#configure}

As detailed in the [`aut` repository <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/aut), some configuration parameters can be set in a `.autrc` file in the working directory or any parent directory.  As a minimal configuration, it is recommended to create an `.autrc` containing the end-point to use for RPC operations:

```
[aut]
rpc_endpoint=https://rpc1.<NETWORK_NAME>.autonity.org
```

See the [list of available networks](/networks/) to determine the correct endpoint to use.

## Usage {#usage}

The tool is intended to be self documenting via `aut --help`, `aut <command> --help` etc.  Some example commands can be found in the [`aut` repository <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/aut).

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

{{< alert title="Note" >}}
The output above may vary depending on the version of the Autonity Go Client you are connected to.
{{< /alert >}}

{{% pageinfo %}}
Now that you have a working `aut` installation, you can  [create](/account-holders/create-acct/) and [fund](/account-holders/fund-acct/) and account on the network, and then [create and submit a transaction](/account-holders/submit-trans-aut/).
{{% /pageinfo %}}

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
