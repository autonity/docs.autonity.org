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

Begin by creating an [account](/account-holders/create-acct/) that  will be used as the cryptographic identity of the oracle server. Note that the account's:

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
   A [sample `plugins-conf.yml` config file](https://github.com/autonity/autonity-oracle/blob/master/config/plugins-conf.yml) can be downloaded from the Autonity Oracle Server GitHub.
   :::

3. (Optional) Add your own data source plugin(s). If you have developed your own FX plugins, (a) add sub-directory(ies) containing the plugin source code to the `plugins` sub-directory of your installation; (b) add config entry(ies) to the `plugins-conf.yml` file. 
 
4. Configure the oracle server. Edit your oracle server config file `oracle-server.config` to specify the oracle server configuration. The file can be found in the `/autonity-oracle/config` sub-directory. For how to do this see the [Set up oracle server config file](/oracle/run-oracle/#set-up-oracle-server-config-file) section on this page.
   
   ::: {.callout-note title="Note" collapse="false"}
   A [sample `oracle-server.config` file](https://github.com/autonity/autonity-oracle/blob/master/config/oracle-server.config) can be downloaded from the Autonity Oracle Server GitHub.
   :::
   
5. Start oracle server:

    ``` bash
    ./autoracle --config="./oracle-server.config"
    ```
    
    Oracle server will connect to external data sources using the providers set in the plugins configuration and begin submitting price reports to the connected node.
    
    On running oracle server you should see something like:
    
    ```
    2025/03/24 14:39:22 
    
       Running autonity oracle server v0.2.3
       with plugin directory: ./plugins
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
   A [sample `plugins-conf.yml` config file](https://github.com/autonity/autonity-oracle/blob/master/config/plugins-conf.yml) can be downloaded from the Autonity Oracle Server GitHub.
   :::

   Edit `plugins-conf.yml` to [configure plugins](/oracle/run-oracle/#configure-plugins) for data sources. See [Set up plugins config file](/oracle/run-oracle/#set-up-plugins-config-file) for how to do this.

3. Configure the oracle server. Create and edit your oracle server config file `oracle-server.config` to specify the oracle server configuration.

   ```bash
   touch oracle-server.config
   ```
   
   ::: {.callout-note title="Note" collapse="false"}
   A [sample `oracle-server.config` file](https://github.com/autonity/autonity-oracle/blob/master/config/oracle-server.config) can be downloaded from the Autonity Oracle Server GitHub.
   :::
   
   Edit `oracle-server.config` to specify the oracle server configuration. See [Set up oracle server config file](/oracle/run-oracle/#set-up-oracle-server-config-file) for how to do this.

4. Set the Docker configuration and the arguments for running Autonity Oracle Server and connecting to the Autonity Go Client it is serving.

   ```bash
   docker run \
        -t -i \
        --volume ./<ORACLE_KEYFILE>:/autoracle/oracle.key \
        --volume ./<PLUGINS_CONF_FILE>:/autoracle/plugins-conf.yml \
        --volume ./<ORACLE_SERVER_CONF_FILE>:/autoracle/oracle-server.config \
        --name <ORACLE_CONTAINER_NAME> \
        --rm <DOCKER_IMAGE>:latest \
        --config="/autoracle/oracle-server.config" \
        ;
   ```

   where:
   
   - `<ORACLE_KEYFILE>` specifies the path to your oracle server key file. E.g. `../aut/keystore/oracle.key`
   - `<PLUGINS_CONF_FILE>` is the path to the data plugins configuration file `plugins-conf.yml`. E.g. `./plugins-conf.yml`.
   - `<ORACLE_SERVER_CONF_FILE>` is the path to the oracle server configuration file `oracle-server.config`. E.g. `./oracle-server.config`.
   - `<ORACLE_CONTAINER_NAME>` is the name you are specifying for the container, i.e. `oracle-server-bakerloo` or `oracle-server-piccadilly`
   - `<DOCKER_IMAGE>` is the Docker image name, i.e. `ghcr.io/autonity/autonity-oracle`. 

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
 	2025/03/25 11:44:45

 	Running autonity oracle server v0.2.3
	with plugin directory: /usr/local/bin/plugins/
 	by connecting to L1 node: ws://127.0.0.1:8546
 	on oracle contract address: 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D
 	```
   
   Oracle server will discover plugins in the `plugins` configuration, set them up, connect to external data sources using the providers set in the `plugins-conf.yml` configuration properties, and begin submitting price reports to the connected node.


## Configure oracle server

The runtime configuration of oracle server can be specified using a configuration file, command line flags, or system environment variables. Using the configuration file `oracle-server.config` is the preferred default path.

### Set up oracle server config file

The oracle server config file `oracle-server.config` can be found in the `/autonity-oracle/config` sub-directory.  Edit the file to set the config values where:

| Option | Description |
|:-------|:------------|
| `tip` | Sets a gas priority fee cap for your oracle server data report transactions. The gas priority fee cap is reimbursed by the Autonity network. Specify in [`ton`](/glossary/#ton). |
| `key.file` | Path to the oracle server key file. e.g. `../aut/keystore/oracle.key`|
| `key.password` | The password to the oracle server key file. |
| `log.level` | Sets logging verbosity. Available logging levels: `0`: No logging, `1`: Trace, `2`: Debug, `3`: Info, `4`: Warn, `5`: Error |
| `ws` | The WS-RPC server listening interface and port of the connected Autonity Go Client node (see [install Autonity, networks](/node-operators/install-aut/#network). E.g.: `"ws://127.0.0.1:8546"` |
| `plugin.dir` | The path to the directory containing the built data plugins. For example `"./plugins"` |
| `plugin.conf` | The path to the plugins configuration file. For example `"./plugins-conf.yml"` |
| `confidence.strategy` | The confidence rule. Available strategies are: `0`: linear, `1`: fixed. |
| `profile.dir` | The profiling report directory, where the profiling report (i.e. runtime state) will be saved to. For example `"."` |

::: {.callout-tip title="Confidence strategy - linear vs. fixed" collapse="false"}

Oracle prices are submitted with a _confidence score_ in the range $(0, 100]$ expressing the oracle's level of trust in the provided price (For detail on confidence score, see the concept description [Oracle accountability fault detection (OAFD)](/concepts/oafd/#confidence-score).

`confidenceStrategy` provides two out-the-box options to compute the confidence score for a symbol:

- `0`: linear, dynamic. The oracle server will use the number of price samples it retrieved during the [voting round](/glossary/#voting-round) for a symbol to compute the confidence score. The higher the number of samples, the higher the confidence score. The confidence score computed is capped at the maximum trust level of $100$.
- `1`: fixed, set to $100$ the maximum trust level.

:::

::: {.callout-caution title="Always review and set `oracle-server.config` to your configuration before running oracle server" collapse="false"}

The `oracle-server.config` file is preset to a testing configuration using test key credentials. 

If you run the server without setting your own configuration, then the test configuration will _de facto_ be picked up and used as a default configuration. Without editing the key options (`key.file`, `key.password`) at minimum, the server will error with an unable to load key message:

```
$ ./autoracle oracle-server.config 
2025/03/20 11:52:09 cannot read key from oracle key file: ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe, open ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe: no such file or directory
could not load key from key store: ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe with password, err: open ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe: no such file or directory
```
:::

   An example configuration for an oracle server binary could be:

   ```
   tip 1
   key.file ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5>
   key.password 123%&%^$
   log.level 3
   ws ws://127.0.0.1:8546
   plugin.dir ./build/bin/plugins
   plugin.conf ./config/plugins-conf.yml
   confidence.strategy 0
   profile.dir .
   ```
  
   An example configuration for an oracle server Docker image could be per beneath. Note the mounted path is used for `key.file` and `plugin.conf` files. A mounted path is not used for the `plugin.dir` config which takes the Docker image plugins directory path `/usr/local/bin/plugins/`:

   ```
   tip 1
   key.file /autoracle/UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5>
   key.password 123%&%^$
   log.level 3
   ws ws://127.0.0.1:8546
   plugin.dir /usr/local/bin/plugins/
   plugin.conf /autoracle/plugins-conf.yml
   confidence.strategy 0
   profile.dir .
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
        --confidence.strategy="0" \
        --profile.dir="."
        ;
   ```

   For example, to start oracle server specifying command line flags when running the Docker image, specify the Docker configuration and oracle server config as flags:

   ```bash
   docker run \
        -t -i \
        --volume ./<ORACLE_KEYFILE>:/autoracle/oracle.key \
        --volume ./<PLUGINS_CONF_FILE>:/autoracle/plugins-conf.yml \
        --name <ORACLE_CONTAINER_NAME> \
        --rm \
        <DOCKER_IMAGE>:latest \
        -tip="<TIP>" \
        -key.file="/autoracle/oracle.key" \
        -key.password="<PWD>" \
        -ws="<WS_ADDRESS>" \
        -plugin.dir="/usr/local/bin/plugins/" \
        -plugin.conf="/autoracle/plugins-conf.yml" \
        -confidence.strategy="<CONFIDENCE_STRATEGY>" \
        -profile.dir="<PROFILE_DIR>"
   ```

   where:
   
   - `<ORACLE_KEYFILE>` specifies the path to your oracle server key file. E.g. `../aut/keystore/oracle.key`
   - `<PLUGINS_CONF_FILE>` is the path to the data plugins configuration file `plugins-conf.yml`. E.g. `./plugins-conf.yml`.
   - `<ORACLE_CONTAINER_NAME>` is the name you are specifying for the container, e.g. `oracle-server-v0.2.3`
   - `<DOCKER_IMAGE>` is the Docker image name, i.e. `ghcr.io/autonity/autonity-oracle`
   - `<TIP>` sets a gas priority fee cap for your oracle server data report transactions, e.g. `1`.
   - `<PWD>` is the password to your oracle server key file
   - `<WS_ADDRESS>` is the WebSocket IP Address of your connected Autonity Go Client node, e.g. "ws://172.17.0.2:8546", see [install Autonity, networks](/node-operators/install-aut/#network)).
   - `<CONFIDENCE_STRATEGY>` sets a confidence score strategy for your oracle server data report transactions, e.g. `0`.
   - `<PROFILE_DIR>` is the path to the directory where your profile report data is saved to, e.g. `.`.

   
::: {.callout-note title="Note" collapse="false"}

- Note that all flags after the image name are passed to the Autonity Oracle Server in the container, and thus follow the same pattern as for [running a binary or source install](#run-binary)
- The command above creates a temporary container, which is deleted (via the `--rm` flag) when the node is shut down.
- The `--volume` flags are needed to mount the key and config files. The plugins are pre-built and included in the Docker container at the path `/usr/local/bin/plugins/`.
:::

   See the [Autonity Oracle Server command-line reference](/reference/cli/oracle/) or the oracle server's GitHub repo [README, Configuration of oracle server](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#configuration-of-oracle-server) section [CLI flags](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#cli-flags) for the full set of available flags.

For how to set the flags as system environment variables see the [README](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#configuration-of-oracle-server) section [System Environment Variables](https://github.com/autonity/autonity-oracle?tab=readme-ov-file#system-environment-variables).

## Configure data source plugins

The oracle server will need to provide FX, ATN and NTN currency pairs utilised in the Auton Stabilization Mechanism.

A basic set of data adaptor plugins for sourcing this data is provided out the box with oracle server for testnet pre-Mainnet in the `autonity-oracle` GitHub repo [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins) directory:

- Forex plugins: for connecting to public FX data sources for ASM [ACU](/concepts/asm/#acu) basket currency prices. See the `forex_` prefixed adaptors in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins). Five forex plugins are currently provided.
- Crypto plugins: for connecting to public CEX and DEX data sources for USD stablecoin and ATN, NTN prices. ATN NTN price data is used for the ASM [Stabilisation CDP](/concepts/asm/#stabilization) mechanism. See the `crypto_` prefixed adaptors in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins). Four crypto plugins are currently provided.
- Simulator plugin: for simulated protocol asset (ATN, NTN, NTN-ATN) data. Used for testnet or local development purposes to provide ATN, NTN price data. See the `simulator_plugin` adaptor in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins).

Plugins are configured by default or by explicit configuration. The `crypto_` plugins have a default configuration set in the plugin source golang code as a `defaultConfig`. The `forex_` and `simulator_` plugin configuration is specified explicitly in the `plugins-conf.yml` file by addding a config entry for each plugin configured.

The full set of plugin configuration fields are:

| Name | Datatype | Mandatory? | Description |
| :-- | :--: | :--: | :-- |
| `name` | string | required | the name of the plugin binary; use the name of the sub-directory in the `plugins` directory |
| `key` | string | required | the API key granted by your data provider to access their data API |
| `scheme` | string | optional | the data service http scheme: http, https, ws or wss. Default value is https. |
| `endpoint` | string | optional | the data service endpoint url of the data provider |
| `timeout` | int | optional | the duration of the timeout period for an API request in seconds. Default value is 10. |
| `refresh` | int | optional | the data update interval in seconds. Used for a rate limited provider's plugin to limit the request rate. Default value is 30. |
| `ntnTokenAddress` | string | optional ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) | The NTN ERC20 token address on the target blockchain. This is the [Autonity Protocol Contract Address](/concepts/architecture/#protocol-contract-addresses). |
| `atnTokenAddress` | string | optional ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) |The Wrapped ATN erc20 token address on the target blockchain. |
| `usdcTokenAddress` | string | optional ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) | USDC ERC20 token address on the target blockchian. For Piccadilly Testnet this is the USDCx ERC20 token address. |
| `swapAddress` | string | optional ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) | UniSwap factory contract address or AirSwap SwapERC20 contract address on the target blockchain. For Piccadilly Testnet this is the Uniswap V2 AMM clone factory contract address. |
| `disabled` | boolean |  optional | The flag to disable a plugin. False by default. |

The configuration fields used depends on the type of plugin. Set optional fields as needed to fit the service level agreed with your rate provider and your own operational practice.

### Setup forex plugin config

To configure FX data source plugins edit the `plugins-conf.yml` file to add a config entry for each plugin. The oracle server release contains out-the-box plugins for five publicly accessible FX endpoints with free and paid subscriptions tiers. You will need to create an account and get an API Key to connect. One or more FX plugin source must be configured.

Navigate to the public GitHub repo [autonity-oracle](https://github.com/autonity/autonity-oracle) `README.md` [Configuration](https://github.com/autonity/autonity-oracle?tab=readme#configuration-of-oracle-server) section to view the supported FX endpoint providers.

For each FX endpoint configured:

1. Get FX plugin API Key(s) for the listed FX endpoint. Navigate to one of the listed FX endpoint websites and create an account. Make a note of the API Key.
2. Add configuration entry to `plugins-conf.yml`. Edit the file to add an entry for each plugin you are configuring.

Plugin Configuration fields:

| Name | Datatype | Mandatory? | Description |
| :-- | :--: | :--: | :-- |
| `name` | string | required | the name of the plugin binary; use the name of the sub-directory in the `plugins` directory |
| `key` | string | required | the API key granted by your data provider to access their data API |
| `scheme` | string | optional | the data service http scheme: http, https, ws or wss. Default value is https. |
| `endpoint` | string | optional | the data service endpoint url of the data provider |
| `timeout` | int | optional | the duration of the timeout period for an API request in seconds. Default value is 10. |
| `refresh` | int | optional | the data update interval in seconds. Used for a rate limited provider's plugin to limit the request rate. Default value is 30. |
| `disabled` | boolean |  optional | The flag to disable a plugin. False by default. |

An example minimal entry could be:

```yaml
- name: forex_currencyfreaks
  key: 5490e15565e741129788f6100e022ec5
```

   
::: {.callout-note title="Note" collapse="false"}
The optional fields should be set as needed to fit the service level agreed with your rate provider and your own operational practice.
:::


::: {.callout-tip title="Tip" collapse="false"}
Remember that the oracle server auto-detects changes to the plugin configuration. If you want to temporarily switch off a plugin you can edit the config to set `disabled` to `true` and toggle it back to `false` to switch it back on again without re-starting the oracle server.
:::

### Setup crypto plugin config

The `crypto_` plugins are configured by default and _are not_ explicitly specified in `plugins-conf.yml`. Default configuration is set in the source code and the plugins are run by default when oracle server is initialised. There are four plugins:

- 1 DEX: `crypto_uniswap`. Connector to retrieve ATN, NTN USDC price data from an on-chain Uniswap V2 AMM on Piccadilly Testnet.
- 3 CEX: `crypto_kraken`, `crypto_coingecko`, `crypto_coinbase`. Connectors to retrieve USDC-USD price data.
 
::: {.callout-note title="Why a USDC-USD price?" collapse="true"}
The oracle server uses the USDC-USD pricing to convert the ATN, NTN USDC market prices from the Testnet Uniswap V2 AMM to ATN,NTN USD prices. The price report for ATN, NTN is then submitted on-chain with USD as the quote pair by the oracle server's connected validator node.

On-chain, the oracle protocol is pricing in USD and not USDC.
:::


Default configuration is specified in the crypto plugins' source golang files in a `defaultConfig` structure. To change the default configuration that structure needs to be edited before building the plugin.

::: {.callout-important title="Only the DEX `crypto_uniswap` plugin requires customisation of the default configuration" collapse="true"}
The validator operator must re-configure the `crypto_uniswap` connector to provide data to their own validator node.

This is because the `crypto_uniswap`plugin [`defaultConfig`](https://github.com/autonity/autonity-oracle/blob/v0.2.3/plugins/crypto_uniswap/crypto_uniswap.go#L26) is set to a testing configuration using an `rpc1-internal` endpoint on the Piccadilly Testnet. If the configured endpoint is not changed, then the plugin will be configured to take data from the rpc1-internal testnet node and not your own validator node state.

It is better practice to retrieve ATN, NTN price data from on-chain using your own hosted validator node rather than testnet infrastructure.
:::

Customise the `crypto_uniswap`plugin:

1. Edit the [`defaultConfig`](https://github.com/autonity/autonity-oracle/blob/v0.2.3/plugins/crypto_uniswap/crypto_uniswap.go#L26) in the source golang file must be edited to change:

    - [`defaultConfig.Endpoint`](https://github.com/autonity/autonity-oracle/blob/v0.2.3/plugins/crypto_uniswap/crypto_uniswap.go#L28): change the `endpoint` to replace the `rpc1-internal` endpoint with the endpoint address of their own connected validator node.
    - [`defaultConfig.Scheme`](https://github.com/autonity/autonity-oracle/blob/v0.2.3/plugins/crypto_uniswap/crypto_uniswap.go#L29): update to the scheme used for the endpoint (http/s or ws/s).

2. Build the plugin. If building oracle server from source, then customise the plugin before running `make autoracle`. Alternatively, build the plugin individually as described in [/plugins/README, Build it](https://github.com/autonity/autonity-oracle/blob/v0.2.3/plugins/README.md#build-it). In the `autonity-oracle` directory run:
   
     ```yaml
     go build -o ./build/bin/plugins/crypto_uniswap ./plugins/crypto_uniswap/crypto_uniswap.go
     ```

The other crypto CEX plugins require no customisation. No additional action is required. These can be run run out the box as-is:

- `crypto_kraken`
- `crypto_coingecko`
- `crypto_coinbase`


### ATN and NTN data simulator plugin

If you are setting up or connecting to a local Autonity testnet an ATN and NTN Simulator plugin is available.

If a simulator has been deployed and is available to provide simulated data for testnet use, this can be connected to by adding a config entryfor the simulated source to your `plugins-conf.yml` file.

1. Edit your `plugins-conf.yml` config file to point to the deployed ATN and NTN data simulator. Just add a `simulator_plugin` entry for the simulator data source, specifying `endpoint` and `scheme` at minimum.

  An example config could be:

  ```yaml
  - name: simulator_plugin
    endpoint: simfeed.bakerloo.autonity.org
    scheme: https
  ```

::: {.callout-note title="Note" collapse="false"}
When running `make` on oracle server the simulator plugin is built to a test directory. So you can get the plugin by just copying the file to your plugins directory:

```bash
cp e2e_test/plugins/simulator_plugins/simulator_plugin build/bin/plugins/simulator_plugin
```

The data source simulator can also be built independently by running the `make simulator` command as described in the [README](https://github.com/autonity/autonity-oracle/tree/v0.2.3?tab=readme-ov-file#other-build-helpers).
:::


### Develop plugins
Additional data adaptors for any external data source can be developed using the oracle server's plugin template. See:

- Adaptor code template `template_plugin` in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins).
- Guide for how _To write a new plugin_ using the template in [`/plugins/README`](https://github.com/autonity/autonity-oracle/blob/master/plugins/README.md).


## Stopping the Autonity Oracle Server

To shutdown the oracle server, press `CTRL-C` and wait for it to exit.

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
