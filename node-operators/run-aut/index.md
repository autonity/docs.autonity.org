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

1. Create the autonity-chaindata directory to hold the autonity working data:

	```bash
    mkdir autonity-chaindata
    ```

2. Generate the `autonitykeys` private key file for your node. This must be performed on the host machine running the Autonity Go Client, using the `autonity genAutonityKeys --writeaddress` command:

	```bash
	./autonity genAutonityKeys --writeaddress ./<DIR_PATH>/<OUT_KEY_FILE_NAME>
	```

	where:

	- `<DIR_PATH>`: is the path to the directory where you will store the private key file of the node.
	- `<OUT_KEY_FILE_NAME>`: is the name of the P2P autonity keys private key file you are generating for your node.

	For example, running the command where the directory is `(pwd)/keystore` and the file name `autonitykeys`:

	```bash
	./autonity/build/bin/autonity genAutonityKeys --writeaddress ./keystore/autonitykeys
	```

	You should see something like this output to your terminal:

	```bash
	Node address: 0x0f083e047725bF1dFf3efe110430B98AAac55986
	Node public key: 0xee0f1195d19b422cd6fc69b060853b7c21094a84e66a225b549afafe7ba44996f85015d6a7f19d32e1e978db26db4083c8db8e153ddea6f1aa4c65608374c868
	Consensus public key: 0x8aa83a28e235072ffdae48ff01ccc46e2b8d9dc16df9b6ff87ffa5ff6d8f90a2852649a60563237cd66a256f60a92e69
	```
	
	Make a note of the output. If you intend to register your validator as a node, you will need to provide the `Consensus public key` as a validator registration parameter.

::: {.callout-important title="Important" collapse="false"}
Remember to backup your `autonitykeys` file! Copy it to a safe location!
:::

::: {.callout-tip title="Tip" collapse="false"}
Autonity’s `ethkey` cmd utility can be used to inspect the `autonitykeys` file and view the `Node address`, `Node public key`, and `Consensus public key`:

```
./build/bin/ethkey autinspect <DIR_PATH>/autonitykeys                  
```

To install the cmd utilities use `make all` when [building Autonity from source code](/node-operators/install-aut/#install-source).
:::


4. Start autonity:

    ``` bash
    autonity \
        --datadir ./autonity-chaindata \
        --autonitykeys ./<PATH_TO_AUTONITYKEYS_FILE> \
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

   - `<PATH_TO_AUTONITYKEYS_FILE>` is the path to the `autonitykeys` file generated in Step 2.
   - `<IP_ADDRESS>` is the node's host IP Address, which can be determined with `curl ifconfig.me`.
   - (Optional) `<CONSENSUS_NAT>` specify the NAT port mapping for the consensus channel (one of "any", "none", "upnp", "pmp", "extip:<IP>") if the default value "any" is not to be used.
   - (Optional) `<CONSENSUS_PORT_NUMBER>` specify the network listening port for the consensus channel if the default port "20203" is not to be used.
   - `--piccadilly` specifies that the node will connect to the Piccadilly testnet.  For other testnets, use the appropriate flag (for example, `--bakerloo`).

::: {.callout-note title="Note" collapse="false"}
If the `--autonitykeys` command option is *not* specified, then on starting AGC will automatically generate an `autonitykeys` file  by default within the `autonity` subfolder of the `--datadir` specified when running the node. 

AGC would then use that `autonitykeys` for the public key component of the enode, *not* the `autonitykeys` file you generated.
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
3. Generate the `autonitykeys` private key file for your node and write the key file to your key directory. This must be performed on the host machine running the Autonity Go Client, using the `autonity genAutonityKeys --writeaddress` command:

	```bash
	docker run -t -i --volume $PWD/<DIR_PATH>:/<DIR_PATH> --name autonity --rm ghcr.io/autonity/autonity:latest genAutonityKeys  --writeaddress /<DIR_PATH>/<OUT_KEY_FILE_NAME>
	```

	where:

	- `<DIR_PATH>`: is the path to the directory where you will store the private key file of the node.
	- `<OUT_KEY_FILE_NAME>`: is the name of the P2P autonity keys private key file you are generating for your node.

	To generate, run the Autonity Go Client docker container with the `<DIR_PATH>` directory mapped to a host directory of the same name.

	For example, running the command where the directory is `(pwd)/keystore` and the file name `autonitykeys`:

	```bash
	docker run -t -i --volume $PWD/keystore:/keystore --name autonity --rm ghcr.io/autonity/autonity:latest genAutonityKeys  --writeaddress /keystore/autonitykeys
	```

	You should see something like this:

	```bash
	Node address: 0x550454352B8e1EAD5F27Cce108EF59439B18E249
	Node public key: 0xcef6334d0855b72dadaa923ceae532550ef68e0ac50288a393eda5d811b9e81053e1324e637a202e21d04e301fe1765900bdd9f3873d58a2badf693331cb1b15
	Consensus public key: 0x90e54b54718c6d5e50d10b93743d743ebcec2f2a2fd43be6813dc5399e11a9bae891c0a357c8f3aa8ca411f9a526a03f
	```
	
	Make a note of the output. If you intend to register your validator as a node, you will need to provide the `Consensus public key` as a validator registration parameter.

::: {.callout-important title="Important" collapse="false"}
Remember to backup your `autonitykeys` file! Copy it to a safe location!
:::

::: {.callout-tip title="Tip" collapse="false"}
Autonity’s `ethkey` cmd utility can be used to inspect the `autonitykeys` file and view the `Node address`, `Node public key`, and `Consensus public key`:

```
./build/bin/ethkey autinspect <DIR_PATH>/autonitykeys                  
```

To install the cmd utilities use `make all` when [building Autonity from source code](/node-operators/install-aut/#install-source).
:::

4. Start the node. Set the Docker configuration and the arguments for connecting Autonity to a network.

   ```bash
   docker run \
       -t -i \
       --volume $(pwd)/autonity-chaindata:/autonity-chaindata \
       --volume $(pwd)/<DIR_PATH>:/<DIR_PATH>
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
           --autonitykeys ./<DIR_PATH>/<AUTONITYKEYS_FILE_NAME> \
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
   
   - `<DIR_PATH>` is the path to the directory where you will store the `autonitykeys` private key file of the node.
   - `<AUTONITYKEYS_FILE_NAME>` is the path to the `autonitykeys` file generated in Step 2.
   - `<IP_ADDRESS>` is the node's host IP Address, which can be determined with `curl ifconfig.me`.
   - (Optional) `<CONSENSUS_NAT>` specify the NAT port mapping for the consensus channel (one of "any", "none", "upnp", "pmp", "extip:<IP>") if the default value "any" is not to be used.
   - (Optional) `<CONSENSUS_PORT_NUMBER>` specify the network listening port for the consensus channel if the default port "20203" is not to be used.
   - `--piccadilly` specifies that the node will connect to the Piccadilly testnet.  For other testnets, use the appropriate flag (for example, `--bakerloo`).

::: {.callout-note title="Note" collapse="false"}
If the `--autonitykeys` command option is *not* specified, then on starting AGC will automatically generate an `autonitykeys` file  by default within the `autonity` subfolder of the `--datadir` specified when running the node. 

AGC would then use that `autonitykeys` for the public key component of the enode, *not* the `autonitykeys` file you generated.
:::

   See the [Autonity command-line reference](/reference/cli) for the full set of available flags.

::: {.callout-note title="Note" collapse="false"}
- Note that all flags after the image name are passed to the Autonity Go Client in the container, and thus follow the same pattern as for [running a binary or source install](#run-binary)
- The command above creates a temporary container, which is deleted (via the `--rm` flag) when the node is shut down.
- The hosts `autonity-chaindata` directory is mounted in the container (via the `--volume` option).  All working data will be saved in this directory and therefore persisted even when the temporary container is removed.
- The same `autonity-chaindata` directory can thereby be used by both a local binary and the docker image (although not at the same time), allowing administrators to switch between run methods at any time.
- The hosts `<DIR_PATH>` directory for the `autonitykeys`is mounted in the container (via the `--volume` option).  The private key will be saved in this directory and therefore persisted even when the temporary container is removed.

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

## Migrating an Autonity Go Client

To migrate a node to a new instance the node identity must be preserved. The [P2P node keys: autonityKeys](/concepts/validator/#p2p-node-keys-autonitykeys) and the node's host [ip address](/node-operators/install-aut/#network) must be maintained to keep the same node [identifier](/concepts/validator/#validator-identifier) address and [enode url](/glossary/#enode).

Copy the [P2P node keys: autonityKeys](/concepts/validator/#p2p-node-keys-autonitykeys) file to a safe location and be sure to maintain your hosting IP address.

::: {.callout-note title="Static IP Address is required" collapse="false"}
Running an Autonity node requires maintaining a static ip address as described in the guide [Install Autonity, Networking](/node-operators/install-aut/#network) section.

If you are using a cloud provider for node hosting, then a static IP address for your cloud space should be a stated hosting requirement if you intend to migrate the node. Cloud vendors typically don't supply a static IP address unless it is purchased explicitly.
:::

To migrate, when reinstalling and running the node:

- Install the node as described in the [install autonity](/node-operators/install-aut/) guide
- Migrate the `autonitykeys` before running the node:
  - Copy your original `autonitykeys` to the directory location you will use to hold the key when running the node. See `<DIR_PATH>` in Step 4 of this Guide.
- Start the node per Step 4 in this guide, maintaining the original IP address value for:
  - `--nat extip:<IP_ADDRESS>`.
  - (Optional) `--consensus-nat extip:<IP_ADDRESS>` if you are not using AGC's default settings for the consensus gossiping channel and have set `extip`.

Autonity will detect and use the original `autonitykeys`. The new node installation will have the same identity as the original.

::: {.callout-note title="Note" collapse="false"}
If you are running a validator node you need to:

- [pause the validator node](/validators/pause-vali/) **before migration**, and 
- [reactivate the new validator](/validators/pause-vali/) **after migration**

Be sure to fully decommission the original node installation.
:::

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
