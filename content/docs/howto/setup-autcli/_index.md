---
title: "Setup the aut CLI tool"
linkTitle: "Setup aut CLI"
weight: 30
description: >
  How to install and configure the `aut` cli tool on your local machine.
---

The recommended way of interacting with the Autonity network if via the [`aut` CLI tool](https://github.com/autonity/autcli), which provides a command-line interface to Autonity-specific queries and operations, as well as much of the base Ethereum functionality.  In general it only needs to be installed on _local_ machines, to connect to the RPC endpoint of an Autonity Go Client (either your own node, or a node providing public RPC access).

For full details and for trouble-shooting, see the [`aut` CLI repository](https://github.com/autonity/autcli).

## Installation {#install}

{{< alert title="Prerequisites" >}}
A working Python install with the `pip` tool is required.
{{< /alert >}}

In general, the tool can be installed using [pipx](https://github.com/pypa/pipx).

```bash
pipx install https://github.com/autonity/autcli
```

{{< alert title="Note" >}}
It is highly recommended to also follow the [instructions in the repository](https://github.com/autonity/autcli) to set up command-line completion.
{{< /alert >}}

## Configuration using the `.autrc` file {#configure}

As detailed in the [`aut` CLI repository](https://github.com/autonity/autcli), some configuration parameters can be set in a `.autrc` file in the working directory or any parent directory.  As a minimal configuration, it is recommended to create an `.autrc` containing the end-point to use for RPC operations:

```
[aut]
rpc_endpoint=https://NETWORK_NAME.autonity.org
```

## Usage {#usage}

The tool is intended to be self documenting via `aut --help`, `aut <command> --help` etc.  Some example commands can be found in the [`aut` CLI repository](https://github.com/autonity/autcli).

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
Now that you have a working `aut` CLI installation, you can  [create](/howto/create-acct/) and [fund](/howto/fund-acct) and account on the network, and then [create and submit a transaction](/howto/submit-trans-autcli/).
{{% /pageinfo %}}

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
