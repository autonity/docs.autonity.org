---
title: "Run Autonity Oracle Server"
linkTitle: "Run Autonity Oracle Server"
weight: 120
description: >
  How to run Autonity Oracle Server in your own environment on Linux Ubuntu OS
---

{{< alert title="Prerequisites" >}}
- Ensure that the host machine meets the [minimum requirements](/validators/install-oracle/#requirements)
{{< /alert >}}

## Run Autonity Oracle Server (binary or source code install) {#run-binary}

- Ensure that the Autonity Oracle Server has been installed from a [pre-compiled binary](/validators/install-oracle/#install-binary) or from [source code](/validators/install-oracle/#install-source)

To run Autonity Oracle Server you will need to generate a keyfile for your oracle server, configure plugin(s) for external data sources, and set the oracle server configuration, and connect to your Autonity Go Client node. Autonity Oracle Server will initialise, connect to the data sources and node, and then begin to submit price reports to your connected node.

1. Create and enter a working directory for the oracle server.

2. Generate a key file for the oracle server. Use `aut` to [create an account](/account-holders/create-acct/) for the oracle. Make a note of your oracle account address as this will be required when registering your validator.

3. Fund the oracle server account. Oracle transactions fees for submitting price reports on-chain are refunded, but the initial price report transaction requires seed funding. (See [Fund account](/account-holders/fund-acct/).)

4. (Optional) Add data source plugins. Navigate to the `plugins` sub-directory of your installation (default: `./build/bin/plugins`) and add sub-directories for additional plugins you are configuring.

5. Configure the oracle server. Specify the oracle server configuration; see [command line reference](/reference/cli/oracle/). Options can be set as system environment variables or directly in the terminal.


6. Start oracle server:

    ``` bash
    autoracle \
        -oracle_key_file="<KEYFILE>" \
        -oracle_key_password="<PWD>" \
        -oracle_autonity_ws_url="<IP_ADDRESS>" ;
        
    ```

   where:

   - `<KEYFILE>` specifies the path to your oracle key file, e.g. `../aut/keystore/oracle.key`
   - `<PWD>` is the password to your oracle key file
   - `<IP_ADDRESS>` is the WebSocket IP Address of your connected Autonity Go Client node (see [install Autonity, networks](/node-operators/install-aut/#network).

See the [Autonity Oracle Server command-line reference](/reference/cli/oracle/#usage) for all available flags.

Oracle server will connect to external data sources using the providers in the `/plugins` subdirectory and begin submitting price reports to the connected node.

{{< alert title="External data source plugins" >}}
By default oracle server will use data source providers packaged in the server release `/plugins` subdirectory.

New plugins are configured by simply adding the binary code to the `/plugins` directory. See [Install Autonity Oracle Server](/validators/install-oracle/) for how to do this.

If plugins for external data sources or the symbols for which oracle server provides price data are changed while oracle server is running, the server does **not** need to be re-started: changes will be auto-detected and applied. 
{{< /alert >}}

## Run Autonity Oracle Server as Linux daemon service {#run-daemon}

TO DO

## Run Autonity as Docker image {#run-docker}

TO DO

<!--
## Run Autonity as Docker image {#run-docker}

- Ensure that the Autonity Go Client [Docker image](/node-operators/install-aut#install-docker) has been installed.

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
       ghcr.io/autonity/autonity:latest \
           --datadir ./autonity-chaindata  \
           --piccadilly \
           --http  \
           --http.addr 0.0.0.0 \
           --http.api aut,eth,net,txpool,web3,admin  \
           --http.vhosts \* \
           --ws  \
           --ws.addr 0.0.0.0 \
           --ws.api aut,eth,net,txpool,web3,admin  \
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
-->

## Stopping the Autonity Oracle Server

To shutdown the oracle server, press `CTRL-C` and wait for it to exit.

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
