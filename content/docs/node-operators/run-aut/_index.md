---
title: "Run Autonity"
linkTitle: "Run Autonity"
weight: 20
description: >
  How to run Autonity in your own environment on Linux Ubuntu OS
---

{{< alert title="Prerequisites" >}}
- Ensure that the host machine meets the [minimum requirements](/howto/install-aut/#requirements)
{{< /alert >}}

## Run Autonity (binary or source code install) {#run-binary}

- Ensure that the Autonity Go Client has been installed from a [pre-compiled binary](/howto/install-aut#install-binary) or from [source code](/howto/install-aut#install-source)

To connect to a network and sync, get the genesis and bootnode files if needed, and run Autonity. Autonity will initialise, connect to the network, and then sync ledger state.

1. Create and enter a working directory for autonity.

1. Create the autonity-chaindata directory to hold the autonity working data:

	```bash
    mkdir autonity-chaindata
    ```

1. Start autonity:

    ``` bash
    autonity \
        --datadir ./autonity-chaindata  \
        --piccadilly  \
        --http  \
        --http.api aut,eth,net,txpool,web3,admin  \
        --ws  \
        --ws.addr 0.0.0.0 \
        --ws.api aut,eth,net,personal,txpool,web3,admin  \
        --nat extip:<IP_ADDRESS>
    ```

   where:

   - `<IP_ADDRESS>` is the node's host IP Address, which can be determined with `curl ifconfig.me`.
   - `--piccadilly` specifies that the node will use the Piccadilly tesnet.  For other tesnets, use the appropriate flag (for example, `--bakerloo`).

See the [Autonity command-line reference](/reference/cli) for the full set of available flags.

Autonity will download the blockchain in "snap" syncmode by default.  Once fully synced, it will continue to import new chain segments as they are finalized.

## Run Autonity as Docker image {#run-docker}

- Ensure that the Autonity Go Client [Docker image](/howto/install-aut#install-docker) has been installed.

1. Create and enter a working directory for autonity.

1. Create the autonity-chaindata directory to hold the autonity working data:

	```bash
    mkdir autonity-chaindata
    ```
1. Start the node. Set the Docker configuration and the arguments for connecting Autonity to a network.

   ```bash
   docker run \
       -t -i \
       --volume $(pwd)/autonity-chaindata:/autonity-chaindata \
       --publish 8545:8545 \
       --publish 8546:8546 \
       --publish 30303:30303 \
       --publish 30303:30303/udp \
       --publish 6060:6060 \
       --name autonity \
       --rm \
       ghcr.io/autonity/autonity/autonity:latest \
           --datadir ./autonity-chaindata  \
           --piccadilly \
           --http  \
           --http.api aut,eth,net,txpool,web3,admin  \
           --ws  \
           --ws.addr 0.0.0.0 \
           --ws.api aut,eth,net,personal,txpool,web3,admin  \
           --nat extip:<IP_ADDRESS>
    ```

   where:
   - `<IP_ADDRESS>` is the node's host IP Address, which can be determined with `curl ifconfig.me`.
   - `--piccadilly` specifies that the node will use the Piccadilly tesnet.  For other tesnets, use the appropriate flag (for example, `--bakerloo`).

   See the [Autonity command-line reference](/reference/cli) for the full set of available flags.

{{< alert title="Important Notes" >}}
- Note that all flags after the image name are passed to the Autonity Go Client in the container, and thus follow the same pattern as for [running a binary or source install](#run-binary)
- The command above creates a temporary container, which is deleted (via the `--rm` flag) when the node is shut down.
- The hosts `autonity-chaindata` directory is mounted in the container (via the `--volume` option).  All working data will be saved in this directory and therefore persisted even when the temporary container is removed.
- The same `autonity-chaindata` directory can thereby be used by both a local binary and the docker image (although not at the same time), allowing administrators to switch between run methods at any time.
- The `--publish` flag causes incoming connections to the localhost to be forwarded to the container.
{{< /alert >}}

Naturally, the above command line can be tailored to suit a specific deployment. See the docker documentation for the complete list of Docker options.

## Stopping the Autonity Go Client

To shutdown the node, press `CTRL-C` and wait for it to exit.

<!-- TODO: Add a link once section exists -->

{{% pageinfo %}}
Now you can now [connect to your node using the `aut` cli tool](/node-operators/connect/) from your _local_ machine.
{{% /pageinfo %}}

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
