---
title: "Run Autonity Oracle Server"
linkTitle: "Run Autonity Oracle Server"
weight: 20
description: >
  How to run Autonity Oracle Server in your own environment on Linux Ubuntu OS
---

{{< alert title="Prerequisites" >}}
- Ensure that the host machine meets the [minimum requirements](/oracle/install-oracle/#requirements)
- A [running instance of an Autonity Go Client](/validators/) running on your host machine, with [networking](/node-operators/install-aut/#network) configured to allow incoming traffic on its WebSocket port. This will be registered as a validator node and oracle server will be configured to connect to it.
- A configured instance of [`aut`](/account-holders/setup-aut/).
{{< /alert >}}

To run Autonity Oracle Server you will need to generate a keyfile for your oracle server, configure plugin(s) for external data sources, set the oracle server configuration, and connect to your Autonity Go Client node. Autonity Oracle Server will initialise, connect to the data sources and node, and then begin to submit price reports to your connected node.

## Create oracle server account

Begin by creating an [account](/account-holders//create-acct/) that  will be used as the cryptographic identity of the oracle server. Note that the account's:

- private key is used as the [oracle server key](/concepts/oracle-network/#oracle-server-key) to sign price report transactions submitted to the Oracle Contract on-chain
- address is used as the [`oracle identifier`](/concepts/oracle-network/#oracle-identifier), the unique identifier of the oracle server.

Transaction costs for submitting price report data on-chain _are_ refunded but the account needs to be pre-funded to prevent an _out of gas_ error on the first transaction submitted by the server.

1. Generate a key file for the oracle server. Use `aut` to [create an account](/account-holders/create-acct/) for the oracle. Make a note of your oracle account address as this will be required when registering your validator.

2. Pre-fund the oracle server account. See [Fund account](/account-holders/fund-acct/).


## Run Autonity Oracle Server (binary or source code install) {#run-binary}

- Ensure that the Autonity Oracle Server has been installed from a [pre-compiled binary](/oracle/install-oracle/#install-binary) or from [source code](/oracle/install-oracle/#install-source)

1. Enter your working directory for the oracle server.

2. Configure data source plugins. Navigate to the `config` sub-directory of your installation (default: `./build/bin/config`) and edit the `plugins-conf.yml` file to add plugin configuration.

    For how to do this see [Configure plugins](/oracle/run-oracle/#configure-plugins) on this page.

3. (Optional) Add your own data source plugin(s). If you have developed your own FX plugins, (a) add sub-directory(ies) containing the plugin source code to the `plugins` sub-directory of your installation; (b) add config entry(ies) to the `plugin-conf.yml` file. 
 
4. Configure the oracle server. Specify the oracle server configuration; see [command line reference](/reference/cli/oracle/). Options can be set as system environment variables or directly in the terminal.

5. Start oracle server:

    ``` bash
    autoracle \
        -oracle_key_file="<KEYFILE>" \
        -oracle_key_password="<PWD>" \
        -oracle_autonity_ws_url="<WS_ADDRESS>" 
        -oracle_plugin_conf="<PLUGINS_CONFIG_FILE>/plugins-conf.yml" ;
        
    ```

   where:

   - `<KEYFILE>` specifies the path to your oracle key file, e.g. `../aut/keystore/oracle.key`
   - `<PWD>` is the password to your oracle key file
   - `<WS_ADDRESS>` is the WebSocket IP Address of your connected Autonity Go Client node (see [install Autonity, networks](/node-operators/install-aut/#network)
   - `<PLUGINS_CONFIG_FILE>` is the path to the plugins YAML configuration file `plugins-conf.yml`.

See the [Autonity Oracle Server command-line reference](/reference/cli/oracle/#usage) for all available flags.

Oracle server will connect to external data sources using the providers in the `/plugins` subdirectory and begin submitting price reports to the connected node.

{{< alert title="External data source plugins" >}}
By default oracle server will use data source providers packaged in the server release `/plugins` subdirectory.

New plugins are configured by simply adding the binary code to the `/plugins` directory. See [Install Autonity Oracle Server](/oracle/install-oracle/) for how to do this.

If plugins for external data sources or the symbols for which oracle server provides price data are changed while oracle server is running, the server does **not** need to be re-started: changes will be auto-detected and applied. 
{{< /alert >}}

## Configure plugins

The oracle server will need to provide FX and ATN/NTN currency pairs utilised in the Autonity Stability Mechanism.

A basic set of data adaptor plugins for sourcing this data is provided out the box with oracle server for testnet pre-Mainnet:

- Forex plugins: for connecting to public FX data sources. See the `forex_` prefixed adaptors in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins). Four forex plugins are currently provided.
- Simulator plugin: for simulated ATN/NTN data. See the `simulator_plugin` adaptor in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins).

### Configure FX data source plugins

To configure plugins edit the `plugins_conf.yml` file to add a config entry for each plugin.  The oracle server release contains out-the-box multiple plugins for four publicly accessible FX endpoints with free and paid subscriptions tiers. You will need to create an account and get an API Key to connect. One or more plugin source must be configured.

Navigate to the public GitHub repo [autonity-oracle <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle) `README.md` [Configuration <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle#configuration) section to view the supported FX endpoint providers.

For each FX endpoint configured:

1. Get FX plugin API Key(s). Navigate to one of the listed FX endpoint websites and create an account. Make a note of the API Key.
2. Add configuration entry to `plugins-conf.yml`. Navigate to the `config` sub-directory of your installation (default: `./build/bin/config`) and edit the file to add an entry for each plugin you are configuring.

Configuration fields:

| Name | Datatype | Description |
| :-- | :--: | :-- |
| `name` | string | the name of the plugin binary; use the name of the sub-directory in the `plugins` directory |
| `key` | string | the API key granted by your data provider to access their data API |
| `scheme` | string | the data service http scheme, http or https |
| `endpoint` | string | the data service endpoint url of the data provider |
| `timeout` | int | the duration of the timeout period for an API request |
| `refresh` | int | data update interval. Used for a rate limited provider's plugin to limit the request rate. |

An example minimal entry could be:

```yaml
- name: forex_currencyfreaks
  key: 5490e15565e741129788f6100e022ec5
```

### Configure ATN/NTN data source plugin

No configuration is required for the testnet ATN/NTN Simulator built when [installing oracle server data source plugins](/oracle/install-oracle/#install-plugin).

### Develop plugins
Additional data adaptors for any external data source can be developed using the oracle server's plugin template. See:

- Adaptor code template `template_plugin` in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins).
- Guide for how _To write a new plugin_ using the template in [`/plugins/README`<i class='fas fa-external-link-alt'></i>](https://github.com/clearmatics/autonity-oracle/tree/master/plugins#readme).
  
<!--
## Run Autonity Oracle Server as Linux daemon service {#run-daemon}

TODO
-->
<!--
## Run Autonity Oracle Server as Docker image {#run-docker}

TODO
=======
=======
>>>>>>> d8f6842 (Edits to Concept Oracle network, Running an oracle server, Reference CLI and Genesis)
  
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
>>>>>>> 6913a4e (Add Running an Oracle Server section, moving in cinstall and run ontent from Running a Validator)
-->

## Stopping the Autonity Oracle Server

To shutdown the oracle server, press `CTRL-C` and wait for it to exit.

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
