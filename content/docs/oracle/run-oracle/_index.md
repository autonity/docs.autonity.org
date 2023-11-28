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
- Auton (ATN) to seed-fund your oracle server account.
{{< /alert >}}

To run Autonity Oracle Server you will need to generate a keyfile for your oracle server account and seed-fund it, configure plugin(s) for external data sources, set the oracle server configuration, and connect to your Autonity Go Client node. Autonity Oracle Server will initialise, connect to the data sources and node, and then begin to submit price reports to your connected node.

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

2. Create and edit your oracle server config file `plugins-conf.yml` to specify the `name` and `key` for each plugins you are using.

   ```bash
   touch plugins-conf.yml
   ```

   {{< alert title="Info" >}}
   A [sample `plugins-conf.yml` config file <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/blob/master/config/plugins-conf.yml) can be downloaded from the Autonity Oracle Server GitHub.
   {{< /alert >}}


   Edit `plugins-conf.yml` to [configure plugins](/oracle/run-oracle/#configure-plugins) for data sources. See [Set up plugins config file](/oracle/run-oracle/#set-up-plugins-config-file) for how to do this.

3. (Optional) Add your own data source plugin(s). If you have developed your own FX plugins, (a) add sub-directory(ies) containing the plugin source code to the `plugins` sub-directory of your installation; (b) add config entry(ies) to the `plugins-conf.yml` file. 
 
4. Configure the oracle server. Specify the oracle server configuration; see [command line reference](/reference/cli/oracle/). Options can be set as system environment variables or directly in the terminal.

5. Start oracle server:


    ``` bash
    autoracle \
        -key.file="<ORACLE_KEYFILE>" \
        -key.password="<PWD>" \
        -ws="<WS_ADDRESS>"
        -plugin.conf="<PLUGINS_CONFIG_FILE>/plugins-conf.yml" ;
    ```

   where:

   - `<ORACLE_KEYFILE>` specifies the path to your oracle server key file, e.g. `../aut/keystore/oracle.key`
   - `<PWD>` is the password to your oracle server key file
   - `<WS_ADDRESS>` is the WebSocket IP Address of your connected Autonity Go Client node (see [install Autonity, networks](/node-operators/install-aut/#network)
   - `<PLUGINS_CONF_FILE>` is the path to the plugins YAML configuration file `plugins-conf.yml` (defaults to `./plugins-conf.yml`).

Oracle server will connect to external data sources using the providers in the `./plugins` subdirectory and begin submitting price reports to the connected node.

{{< alert title="Info" >}}
See the [Autonity Oracle Server command-line reference](/reference/cli/oracle/#usage) for all available command-line option flags. Configuration can be set using system environment variables or directly in the terminal as console flags. See the oracle server's GitHub repo [README, Configuration <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle#configuration) section for more detail.

By default oracle server will use data source providers packaged in the server release `./plugins` subdirectory.

New plugins are configured by simply adding the binary code to the `/plugins` directory. See [Installing data source plugins](/oracle/install-oracle/#install-plugin).

If plugins for external data sources or the symbols for which oracle server provides price data are changed while oracle server is running, changes are auto-detected and applied. Oracle server does **not** need to be re-started.
{{< /alert >}}

## Run Autonity Oracle Server as Docker image {#run-docker}

- Ensure that the Autonity Oracle Server [Docker image](/oracle/install-oracle/#install-docker) has been installed.

1. Enter your working directory for autonity oracle server.

2. Create and edit your oracle server config file `plugins-conf.yml` to specify the `name` and `key` for each plugins you are using.

   ```bash
   touch plugins-conf.yml
   ```

   {{< alert title="Info" >}}
   A [sample `plugins-conf.yml` config file <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/blob/master/config/plugins-conf.yml) can be downloaded from the Autonity Oracle Server GitHub.
   {{< /alert >}}

   Edit `plugins-conf.yml` to [configure plugins](/oracle/run-oracle/#configure-plugins) for data sources. See [Set up plugins config file](/oracle/run-oracle/#set-up-plugins-config-file) for how to do this.
   
3. Set the Docker configuration and the arguments for running Autonity Oracle Server and connecting to the Autonity Go Client it is serving.

   ```bash
   docker run \
        -t -i \
        --volume $<ORACLE_KEYFILE>:/autoracle/oracle.key \
        --volume $<PATH_TO_PLUGINS_FILE>:/autoracle/plugins-conf.yml \
        --name oracle-server \
        --rm \
        ghcr.io/autonity/autonity-oracle:latest \
        -key.file="/autoracle/oracle.key" \
        -key.password="<PWD>" \
        -ws="<WS_ADDRESS>" \
        -plugin.dir="/usr/local/bin/plugins/" \
        -plugin.conf="/autoracle/plugins-conf.yml"
   ```

   where:
   - `<ORACLE_KEYFILE>` specifies the path to your oracle server key file. E.g. `../aut/keystore/oracle.key`
   - `<PLUGINS_CONF_FILE>` is the path to the oracle server configuration file `plugins-conf.yml`. E.g. `./plugins-conf.yml`.
   - `<PWD>` is the password to your oracle server key file
   - `<WS_ADDRESS>` is the WebSocket IP Address of your connected Autonity Go Client node (see [install Autonity, networks](/node-operators/install-aut/#network). 

   See the [Autonity Oracle Server command-line reference](/reference/cli/oracle/) for the full set of available flags.

{{< alert title="Info" >}}
AOS requires an accessible `ws/wss` AGC endpoint. If you are also running AGC in docker and facing issues in connecting AOS to it, then see docker docs [Networking <i class='fas fa-external-link-alt'></i>](https://docs.docker.com/network/).  
{{< /alert >}}
 
On running the Docker you should see something like:

   ```
 	2023/09/26 10:04:53 


        Running autonity oracle server v0.1.2
        with symbols: AUD-USD,CAD-USD,EUR-USD,GBP-USD,JPY-USD,SEK-USD,ATN-USD,NTN-USD,NTN-ATN
        and plugin directory: ./build/bin/plugins/
        by connecting to L1 node: ws://127.0.0.1:8546
        on oracle contract address: 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D 
   ```

{{< alert title="Important Notes" >}}
- Note that all flags after the image name are passed to the Autonity Oracle Server in the container, and thus follow the same pattern as for [running a binary or source install](#run-binary)

- The command above creates a temporary container, which is deleted (via the `--rm` flag) when the node is shut down.

- The `--volume` flags are needed to mount the key and config files. The plugins are pre-built and included in the Docker container at the path `/usr/local/bin/plugins/`.
{{< /alert >}}

Naturally, the above command line can be tailored to suit a specific deployment. See the docker documentation for the complete list of Docker options.


## Configure plugins

The oracle server will need to provide FX, ATN and NTN currency pairs utilised in the Auton Stabilization Mechanism.

A basic set of data adaptor plugins for sourcing this data is provided out the box with oracle server for testnet pre-Mainnet in the `autonity-oracle` GitHub repo [`/plugins` <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins) directory:

- Forex plugins: for connecting to public FX data sources. See the `forex_` prefixed adaptors. Four forex plugins are currently provided.
- Simulator plugin: for simulated ATN/NTN data. See the `simulator_plugin` adaptor.

### Set up plugins config file
To configure FX data source plugins edit the `plugins_conf.yml` file to add a config entry for each plugin.  The oracle server release contains out-the-box plugins for four publicly accessible FX endpoints with free and paid subscriptions tiers. You will need to create an account and get an API Key to connect. One or more plugin source must be configured.

Navigate to the public GitHub repo [autonity-oracle <i class='fas fa-external-link-alt'></i>] (https://github.com/autonity/autonity-oracle) `README.md` [Configuration <i class='fas fa-external-link-alt'></i>](https://github.com/clearmatics/autonity-oracle#configuration) section to view the supported FX endpoint providers.

For each FX endpoint configured:

1. Get FX plugin API Key(s). Navigate to one of the listed FX endpoint websites and create an account. Make a note of the API Key.
2. Add configuration entry to `plugins-conf.yml`. Edit the file to add an entry for each plugin you are configuring.

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

### ATN and NTN data simulator plugin

No additional configuration is required for the testnet ATN and NTN Simulator built when [installing oracle server data source plugins](/oracle/install-oracle/#install-plugin).

{{< alert title="Info" color="info">}}
The `Simulator_plugin` default configuration will connect to a simulated price feed for `NTN-USD`, `ATN-USD` and `NTN-ATN` at https://simfeed.bakerloo.autonity.org/api/v3/ticker/price.
{{< /alert >}}


### Develop plugins
Additional data adaptors for any external data source can be developed using the oracle server's plugin template. See:

- Adaptor code template `template_plugin` in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins).
- Guide for how _To write a new plugin_ using the template in [`/plugins/README`<i class='fas fa-external-link-alt'></i>](https://github.com/clearmatics/autonity-oracle/tree/master/plugins#readme).


## Stopping the Autonity Oracle Server

To shutdown the oracle server, press `CTRL-C` and wait for it to exit.

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
