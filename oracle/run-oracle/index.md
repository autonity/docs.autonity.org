---
title: "Run Autonity Oracle Server"
description: >
  How to run Autonity Oracle Server in your own environment on Linux Ubuntu OS
---

::: {.callout-note title="Prerequisites" collapse="false"}
- Ensure that the host machine meets the [minimum requirements](/oracle/install-oracle/#requirements)
- A [running instance of an Autonity Go Client](/validators/) running on your host machine, with [networking](/node-operators/install-aut/#network) configured to allow incoming traffic on its WebSocket port. This will be registered as a validator node and oracle server will be configured to connect to it.
- A configured instance of [`aut`](/account-holders/setup-aut/).
- Auton (ATN) to seed-fund your oracle server account.
:::

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

2. Configure the data plugins. Edit your oracle server data plugins config file `plugins-conf.yml` to specify the plugins configuration. The file can be found in the `/autonity-oracle/config` sub-directory. Edit `plugins-conf.yml` to specify the `name` and `key` for each plugins you are using. For how to do this see the [Set up plugins config file](/oracle/run-oracle/#set-up-plugins-config-file) section on this page.

   ::: {.callout-note title="Note" collapse="false"}
   A [sample `plugins-conf.yml` config file <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/blob/master/config/plugins-conf.yml) can be downloaded from the Autonity Oracle Server GitHub.
   :::

3. (Optional) Add your own data source plugin(s). If you have developed your own FX plugins, (a) add sub-directory(ies) containing the plugin source code to the `plugins` sub-directory of your installation; (b) add config entry(ies) to the `plugins-conf.yml` file. 
 
4. Configure the oracle server. Edit your oracle server config file `oracle-server.config` to specify the oracle server configuration. The file can be found in the `/autonity-oracle/config` sub-directory. For how to do this see the [Set up oracle server config file](/oracle/run-oracle/#set-up-oracle-server-config-file) section on this page.
   
   ::: {.callout-note title="Note" collapse="false"}
   A [sample `oracle-server.config` file <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/blob/master/config/oracle-server.config) can be downloaded from the Autonity Oracle Server GitHub.
   :::
   
5. Start oracle server:


    ``` bash
    ./autoracle --config="./oracle-server.config"
    ```
    
    Oracle server will connect to external data sources using the providers set in the plugins configuration and begin submitting price reports to the connected node.
    
    On running oracle server you should see something like:
    
    ```
    2024/02/10 17:44:48 
    
       Running autonity oracle server v0.1.6
       with plugin directory: ./build/bin/plugins
       by connecting to L1 node: ws://127.0.0.1:8546
       on oracle contract address: 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D
    ```

::: {.callout-note title="Note" collapse="false"}
The oracle server configuration can also be set as system environment variables or directly in the terminal as console flags.  For how to do this see the page section [Setup using command line flags or system env variables](/oracle/run-oracle/#setup-using-command-line-flags-or-system-env-variables).
:::

::: {.callout-note title="Note" collapse="false"}
New or updated plugins are configured by simply adding the binary code to the configured plugins directory (`plugin.dir`). See [Installing data source plugins](/oracle/install-oracle/#install-plugin) for more detail.

If plugins for external data sources or the symbols for which oracle server provides price data are changed while oracle server is running, changes are auto-detected and applied. Oracle server does **not** need to be re-started.
:::


## Run Autonity Oracle Server as Docker image {#run-docker}

- Ensure that the Autonity Oracle Server [Docker image](/oracle/install-oracle/#install-docker) has been installed.

1. Enter your working directory for autonity oracle server.

2. Configure the data plugins. Create and edit your oracle server data plugins config file `plugins-conf.yml` to specify the `name` and `key` for each plugins you are using.

   ```bash
   touch plugins-conf.yml
   ```

   ::: {.callout-note title="Note" collapse="false"}
   A [sample `plugins-conf.yml` config file <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/blob/master/config/plugins-conf.yml) can be downloaded from the Autonity Oracle Server GitHub.
   :::

   Edit `plugins-conf.yml` to [configure plugins](/oracle/run-oracle/#configure-plugins) for data sources. See [Set up plugins config file](/oracle/run-oracle/#set-up-plugins-config-file) for how to do this.

3. Configure the oracle server. Create and edit your oracle server config file `oracle-server.config` to specify the oracle server configuration.

   ```bash
   touch oracle-server.config
   ```
   
   ::: {.callout-note title="Note" collapse="false"}
   A [sample `oracle-server.config` file <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/blob/master/config/oracle-server.config) can be downloaded from the Autonity Oracle Server GitHub.
   :::
   
   Edit `oracle-server.config` to specify the oracle server configuration. See [Set up oracle server config file](/oracle/run-oracle/#set-up-oracle-server-config-file) for how to do this.

4. Set the Docker configuration and the arguments for running Autonity Oracle Server and connecting to the Autonity Go Client it is serving.

   ```bash
   docker run \
        -t -i \
        --volume $<ORACLE_KEYFILE>:/autoracle/oracle.key \
        --volume $<PLUGINS_CONF_FILE>:/autoracle/plugins-conf.yml \
        --volume $<ORACLE_SERVER_CONF_FILE>:/autoracle/plugins-conf.yml \
        --name <ORACLE_CONTAINER_NAME> \
        --rm \
        <DOCKER_IMAGE>:latest \
        ;
   ```

   where:
   
   - `<ORACLE_KEYFILE>` specifies the path to your oracle server key file. E.g. `../aut/keystore/oracle.key`
   - `<PLUGINS_CONF_FILE>` is the path to the data plugins configuration file `plugins-conf.yml`. E.g. `./plugins-conf.yml`.
   - `<ORACLE_SERVER_CONF_FILE>` is the path to the oracle server configuration file `oracle-server.config`. E.g. `./oracle-server.config`.
   - `<ORACLE_CONTAINER_NAME>` is the name you are specifying for the container, i.e. `oracle-server-bakerloo` or `oracle-server-piccadilly`
   - `<DOCKER_IMAGE>` is the Docker image name, i.e. `ghcr.io/autonity/autonity-oracle-bakerloo` or `ghcr.io/autonity/autonity-oracle-piccadilly`. 

   See the [Autonity Oracle Server command-line reference](/reference/cli/oracle/) for the full set of available flags.

   ::: {.callout-note title="Note" collapse="false"}
   AOS requires an accessible `ws/wss` AGC endpoint. If you are also running AGC in docker and facing issues in connecting AOS to it, please execute the following command to correctly identify the IP address required for the `<WS_ADDRESS>`: `docker inspect -f '{{.NetworkSettings.IPAddress}}' <container_id_or_name>`
   :::


   ::: {.callout-note title="Note" collapse="false"}
   - The command above creates a temporary container, which is deleted (via the `--rm` flag) when the node is shut down.

   - The `--volume` flags are needed to mount the key and config files. The plugins are pre-built and included in the Docker container at the path `/usr/local/bin/plugins/`.
   :::

   Naturally, the above command line can be tailored to suit a specific deployment. See the docker documentation for the complete list of Docker options.

5. Start oracle server. On running the Docker you should see something like:

   ```
 	2023/09/26 10:04:53 

        Running autonity oracle server v0.1.2
        with symbols: AUD-USD,CAD-USD,EUR-USD,GBP-USD,JPY-USD,SEK-USD,ATN-USD,NTN-USD,NTN-ATN
        and plugin directory: ./build/bin/plugins/
        by connecting to L1 node: ws://127.0.0.1:8546
        on oracle contract address: 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D 
   ```
   
   Oracle server will connect to external data sources using the providers set in the `plugin.` configuration properties and begin submitting price reports to the connected node.


## Configure oracle server

The runtime configuration of oracle server can be specified using a configuration file, command line flags, or system environment variables. Using the configuration file `oracle-server.config` is the preferred default path.

### Set up oracle server config file
The oracle server config file `oracle-server.config` can be found in the `/autonity-oracle/config` sub-directory.  Edit the file to set the config values where:

   - `tip`: sets a gas priority fee cap for your oracle server data report transactions.
   - `key.file`: is the path to your oracle server key file, e.g. `../aut/keystore/oracle.key`
   - `key.password`: is the password to your oracle server key file
   - `log.level`: sets the logging level. Values are: `0`: No logging, `1`: Trace, `2`:Debug, `3`: Info, `4`: Warn, `5`: Error.
   - `ws`: is the WebSocket IP Address of your connected Autonity Go Client node (see [install Autonity, networks](/node-operators/install-aut/#network)
   - `plugin.dir` is the path to the directory containing the built data plugins.
   - `plugin.conf` is the path to the plugins YAML configuration file `plugins-conf.yml` (defaults to `./plugins-conf.yml`).

   An example configuration could be:

   ```
   tip 1
   key.file ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5>
   key.password 123%&%^$
   log.level 3
   ws ws://127.0.0.1:8546
   plugin.dir ./build/binplugins
   plugin.conf ./config/plugins-conf.yml
   ```
   
### Setup using command line flags or system env variables  
The oracle server configuration can also be set directly in the terminal as console flags or as system environment variables.

For example, to start oracle server specifying command line flags when running the binary, simply specify the config as flags:

   ```bash
   ./autoracle \
        --tip="1" \
        --key.file="../../test_data/keystore/UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe" \
        --key.password="123" \
        --ws="ws://127.0.0.1:8546" \
        --plugin.dir="./plugins" \
        --plugin.conf="./plugins-conf.yml" \
        ;
   ```

For example, to start oracle server specifying command line flags when running the Docker image, specify the Docker configuration and oracle server config as flags:

   ```bash
   docker run \
        -t -i \
        --volume $<ORACLE_KEYFILE>:/autoracle/oracle.key \
        --volume $<PLUGINS_CONF_FILE>:/autoracle/plugins-conf.yml \
        --name <ORACLE_CONTAINER_NAME> \
        --rm \
        <DOCKER_IMAGE>:latest \
        -tip="<TIP>" \
        -key.file="/autoracle/oracle.key" \
        -key.password="<PWD>" \
        -ws="<WS_ADDRESS>" \
        -plugin.dir="/usr/local/bin/plugins/" \
        -plugin.conf="/autoracle/plugins-conf.yml"
   ```

   where:
   
   - `<ORACLE_KEYFILE>` specifies the path to your oracle server key file. E.g. `../aut/keystore/oracle.key`
   - `<PLUGINS_CONF_FILE>` is the path to the data plugins configuration file `plugins-conf.yml`. E.g. `./plugins-conf.yml`.
   - `<ORACLE_CONTAINER_NAME>` is the name you are specifying for the container, i.e. `oracle-server-bakerloo` or `oracle-server-piccadilly`
   - `<DOCKER_IMAGE>` is the Docker image name, i.e. `ghcr.io/autonity/autonity-oracle-bakerloo` or `ghcr.io/autonity/autonity-oracle-piccadilly`
   - `<TIP>` sets a gas priority fee cap for your oracle server data report transactions, e.g. `1`.
   - `<PWD>` is the password to your oracle server key file
   - `<WS_ADDRESS>` is the WebSocket IP Address of your connected Autonity Go Client node, e.g. "ws://172.17.0.2:8546", see [install Autonity, networks](/node-operators/install-aut/#network)). 
   
   ::: {.callout-note title="Note" collapse="false"}
   - Note that all flags after the image name are passed to the Autonity Oracle Server in the container, and thus follow the same pattern as for [running a binary or source install](#run-binary)
   - The command above creates a temporary container, which is deleted (via the `--rm` flag) when the node is shut down.
   - The `--volume` flags are needed to mount the key and config files. The plugins are pre-built and included in the Docker container at the path `/usr/local/bin/plugins/`.
   :::

   See the [Autonity Oracle Server command-line reference](/reference/cli/oracle/) or the oracle server's GitHub repo [README, Configuration of oracle server <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#configuration-of-oracle-server) section [CLI flags <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#cli-flags) for the full set of available flags.

For how to set the flags as system environment variables see the [README <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#configuration-of-oracle-server) section [System Environment Variables <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#system-environment-variables).


## Configure data source plugins

The oracle server will need to provide FX, ATN and NTN currency pairs utilised in the Auton Stabilization Mechanism.

A basic set of data adaptor plugins for sourcing this data is provided out the box with oracle server for testnet pre-Mainnet in the `autonity-oracle` GitHub repo [`/plugins` <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins) directory:

- Forex plugins: for connecting to public FX data sources. See the `forex_` prefixed adaptors. Four forex plugins are currently provided.
- Simulator plugin: for simulated ATN/NTN data. See the `sim_plugin` adaptor.

### Set up plugins config file
To configure FX data source plugins edit the `plugins_conf.yml` file to add a config entry for each plugin.  The oracle server release contains out-the-box plugins for four publicly accessible FX endpoints with free and paid subscriptions tiers. You will need to create an account and get an API Key to connect. One or more plugin source must be configured.

Navigate to the public GitHub repo [autonity-oracle <i class='fas fa-external-link-alt'></i>] (https://github.com/autonity/autonity-oracle) `README.md` [Configuration <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#configuration-of-oracle-server) section to view the supported FX endpoint providers.

For each FX endpoint configured:

1. Get FX plugin API Key(s). Navigate to one of the listed FX endpoint websites and create an account. Make a note of the API Key.
2. Add configuration entry to `plugins-conf.yml`. Edit the file to add an entry for each plugin you are configuring.

Configuration fields:

| Name | Datatype | Mandatory? | Description |
| :-- | :--: | :--: | :-- |
| `name` | string | required | the name of the plugin binary; use the name of the sub-directory in the `plugins` directory |
| `key` | string | required | the API key granted by your data provider to access their data API |
| `scheme` | string | optional | the data service http scheme, http or https. Default value is https. |
| `endpoint` | string | optional | the data service endpoint url of the data provider |
| `timeout` | int | optional | the duration of the timeout period for an API request in seconds. Default value is 10. |
| `refresh` | int | optional | the data update interval in seconds. Used for a rate limited provider's plugin to limit the request rate. Default value is 30. |

An example minimal entry could be:

```yaml
- name: forex_currencyfreaks
  key: 5490e15565e741129788f6100e022ec5
```
   
::: {.callout-note title="Note" collapse="false"}
The optional fields should be set as needed to fit the service level agreed with your rate provider.
:::


### ATN and NTN data simulator plugin

If you are connecting to Bakerloo testnet an ATN and NTN Simulator is deployed and available to provide simulated data for testnet use.  

To connect to this simulator as a data source, you need to edit your `plugins-conf.yml` config file to point to the Bakerloo ATN and NTN data simulator. Just add an entry for the Bakerloo simulator data source:

```yaml
- name: sim_plugin
  endpoint: simfeed.bakerloo.autonity.org
  scheme: https
```

::: {.callout-note title="Note" collapse="false"}
The `sim_plugin` is built and added to the plugins directory when building from source running the `make autoracle-bakerloo` command.

When running `make` on oracle server the simulator plugin is also built to a test directory. So if you didn't run the Bakerloo-specific make command you can still get the plugin by just copying the file to the plugins directory:

```bash
cp e2e_test/plugins/simulator_plugins/sim_plugin build/bin/plugins/sim_plugin
```

The simulator can also be built independently by running the `make simulator` command.
:::

### Develop plugins
Additional data adaptors for any external data source can be developed using the oracle server's plugin template. See:

- Adaptor code template `template_plugin` in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins).
- Guide for how _To write a new plugin_ using the template in [`/plugins/README`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/blob/master/plugins/README.md).


## Stopping the Autonity Oracle Server

To shutdown the oracle server, press `CTRL-C` and wait for it to exit.

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
