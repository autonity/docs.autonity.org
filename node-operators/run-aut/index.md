---
title: "Run Autonity"
description: >
  How to run Autonity in your own environment on Linux Ubuntu OS
---

::: {.callout-note title="Prerequisites" collapse="false"}
- Ensure that the host machine meets the [minimum requirements](/node-operators/install-aut/#requirements)
:::

## Run Autonity (binary or source code install) {#run-binary}

- Ensure that the Autonity Go Client has been installed from a [pre-compiled binary](/node-operators/install-aut#install-binary) or from [source code](/node-operators/install-aut#install-source)

To connect to a network and sync, get the genesis and bootnode files if needed, and run Autonity. Autonity will initialise, connect to the network, and then sync ledger state.

1. Create and enter a working directory for autonity.

2. Create the autonity-chaindata directory to hold the autonity working data:

	```bash
    mkdir autonity-chaindata
    ```

3. Start autonity:

    ``` bash
    autonity \
        --datadir ./autonity-chaindata \
        --piccadilly  \
        --http  \
        --http.addr 0.0.0.0 \
        --http.api aut,eth,net,txpool,web3,admin \
        --http.vhosts "*" \
        --ws  \
        --ws.addr 0.0.0.0 \
        --ws.api aut,eth,net,txpool,web3,admin  \
        --nat extip:<IP_ADDRESS> \
        --consensus.nat <CONSENSUS_NAT> \
        --consensus.port <CONSENSUS_PORT_NUMBER> \
        ;
    ```

   where:

   - `<IP_ADDRESS>` is the node's host IP Address, which can be determined with `curl ifconfig.me`.
   - (Optional) `<CONSENSUS_NAT>` specify the NAT port mapping for the consensus channel (one of "any", "none", "upnp", "pmp", "extip:<IP>") if the default value "any" is not to be used.
   - (Optional) `<CONSENSUS_PORT_NUMBER>` specify the network listening port for the consensus channel if the default port "20203" is not to be used.
   - `--piccadilly` specifies that the node will connect to the Piccadilly testnet.

::: {.callout-note title="Default location for AGC's node and consensus private keys file  `autonitykeys`" collapse="false"}
On starting, by default AGC will automatically generate an `autonitykeys` file containing your node key and consensus key within the `autonity` subfolder of the `--datadir` specified when running the node.

The `autonitykeys` file contains the private keys of (a) the node key used for transaction gossiping with other network peer nodes, and (b) the consensus key used for consensus gossiping with other validators if your node is run as a validator and is participating in consensus.

If you choose not to store your key in the default location, then specify the path to where you are keeping your `autonitykeys` file using the `--autonitykeys` option in the run command.
:::

See the [Autonity command-line reference](/reference/cli) for the full set of available flags.

Autonity will download the blockchain in "snap" syncmode by default.  Once fully synced, it will continue to import new chain segments as they are finalized.

## Run Autonity as Docker image {#run-docker}

- Ensure that the Autonity Go Client [Docker image](/node-operators/install-aut#install-docker) has been installed.

1. Create and enter a working directory for autonity.

2. Create the autonity-chaindata directory to hold the autonity working data:

	```bash
    mkdir autonity-chaindata
    ```
3. Start the node. Set the Docker configuration and the arguments for connecting Autonity to a network.

   ```bash
   docker run \
       -t -i \
       --volume $(pwd)/autonity-chaindata:/autonity-chaindata \
       --publish 8545:8545 \
       --publish 8546:8546 \
       --publish 30303:30303 \
       --publish 30303:30303/udp \
       --publish 20203:20203 \
       --publish 6060:6060 \
       --name autonity \
       --rm \
       ghcr.io/autonity/autonity:latest \
           --datadir ./autonity-chaindata  \
           --piccadilly \
           --http  \
           --http.addr 0.0.0.0 \
           --http.api aut,eth,net,txpool,web3,admin  \
           --http.vhosts "*" \
           --ws  \
           --ws.addr 0.0.0.0 \
           --ws.api aut,eth,net,txpool,web3,admin  \
           --nat extip:<IP_ADDRESS> \
           --consensus.nat <CONSENSUS_NAT> \
           --consensus.port <CONSENSUS_PORT_NUMBER> \
        ;
   ```

   where:
   
   - `<IP_ADDRESS>` is the node's host IP Address, which can be determined with `curl ifconfig.me`.
   - (Optional) `<CONSENSUS_NAT>` specify the NAT port mapping for the consensus channel (one of "any", "none", "upnp", "pmp", "extip:<IP>") if the default value "any" is not to be used.
   - (Optional) `<CONSENSUS_PORT_NUMBER>` specify the network listening port for the consensus channel if the default port "20203" is not to be used.
   - `--piccadilly` specifies that the node will connect to the Piccadilly testnet.

   See the [Autonity command-line reference](/reference/cli) for the full set of available flags.

::: {.callout-note title="Note" collapse="false"}
- Note that all flags after the image name are passed to the Autonity Go Client in the container, and thus follow the same pattern as for [running a binary or source install](#run-binary)
- The command above creates a temporary container, which is deleted (via the `--rm` flag) when the node is shut down.
- The hosts `autonity-chaindata` directory is mounted in the container (via the `--volume` option).  All working data will be saved in this directory and therefore persisted even when the temporary container is removed.
- The same `autonity-chaindata` directory can thereby be used by both a local binary and the docker image (although not at the same time), allowing administrators to switch between run methods at any time.
- The `--publish` flag causes incoming connections to the localhost to be forwarded to the container.
:::

Naturally, the above command line can be tailored to suit a specific deployment. See the docker documentation for the complete list of Docker options.

## Stopping the Autonity Go Client

To shutdown the node, press `CTRL-C` and wait for it to exit.

::: {.callout-warning title="Warning!" collapse="false"}
You *must* wait for the node to exit successfully.  Terminating the process prematurely may risk corruption of the state store (LevelDB).

Exit may take up to 3 minutes. If you are using `systemd` and/or other software services management software, then make sure this is configured to allow for a safe exit time to avoid early shutdown.
:::


::: {.callout-note title="Info" collapse="false"}
Now you can now [connect to your node using `aut`](/node-operators/connect/) from your _local_ machine.
:::

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
