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

2. Setup the oracle server configuration. Edit your oracle server config file `oracle_config.yml` as described in [Configure oracle server](/oracle/run-oracle/#configure-oracle-server). 

3. Start oracle server:

    ``` bash
    ./autoracle ./config/oracle_config.yml
    ```
    
    Oracle server will connect to external data sources using the providers set in the plugins configuration and begin submitting price reports to the connected node.
    
    On running oracle server you should see something like:
    
    ```console
    2025/08/05 13:48:16
    
    
    	Running autonity oracle server v0.2.4
    	with plugin directory: ./plugins
    	by connecting to L1 node: ws://127.0.0.1:8546
    	on oracle contract address: 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D
    ```

::: {.callout-note title="Note" collapse="false"}
New or updated plugins are configured by simply adding the binary code to the configured plugins directory (`plugin.dir`). See [Installing data source plugins](/oracle/install-oracle/#install-plugin) for more detail.

If plugins for external data sources or the symbols for which oracle server provides price data are changed while oracle server is running, changes are auto-detected and applied. Oracle server does **not** need to be re-started.
:::


## Run Autonity Oracle Server as Docker image {#run-docker}

- Ensure that the Autonity Oracle Server [Docker image](/oracle/install-oracle/#install-docker) has been installed.

1. Enter your working directory for autonity oracle server.

2. Setup the oracle server configuration. Edit your oracle server config file `oracle_config.yml` as described in [Configure oracle server](/oracle/run-oracle/#configure-oracle-server).

3. Set the Docker configuration and the arguments for running Autonity Oracle Server and connecting to the Autonity Go Client it is serving.

   ```bash
   docker run \
        -t -i \
        --volume ./<ORACLE_KEYFILE>:/autoracle/oracle.key \
        --volume ./<ORACLE_SERVER_CONF_FILE>:/autoracle/oracle_config.yml \
        --name <ORACLE_CONTAINER_NAME> \
        --rm <DOCKER_IMAGE>:<VERSION> \
        oracle_config.yml \
        ;
   ```

   where:
   
   - `<ORACLE_KEYFILE>` specifies the path to your oracle server key file. E.g. `../aut/keystore/oracle.key`
   - `<ORACLE_SERVER_CONF_FILE>` is the path to the oracle server configuration file `oracle_config.yml`. E.g. `./oracle_config.yml`.
   - `<ORACLE_CONTAINER_NAME>` is the name you are specifying for the container, e.g. `oracle-server-bakerloo` or `oracle-server-mainnet`
   - `<DOCKER_IMAGE>` is the Docker image name, i.e. `ghcr.io/autonity/autonity-oracle`
   - `<VERSION>` is the docker image version, i.e. `v0.2.4`. 

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
   2025/08/05 13:10:35 


 	Running autonity oracle server v0.2.4
	with plugin directory: ./plugins
 	by connecting to L1 node: ws://127.0.0.1:8546
 	on oracle contract address: 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D 
 	```
   
   Oracle server will discover plugins in the `plugins` configuration, set them up, connect to external data sources using the providers set in the `oracle_config.yml` configuration properties, and begin submitting price reports to the connected node.


## Configure oracle server

The runtime configuration of oracle server is specified using a configuration file `oracle_config.yml`.

The oracle server and its associated data source plugin configuration are both set in `oracle_config.yml`. The file can be downloaded from the Autonity Oracle Server GitHub at [`/autonity-oracle/config/oracle_config.yml`](https://github.com/autonity/autonity-oracle/blob/master/config/oracle_config.yml).

Edit the config file to:
   
   - [Setup the oracle server configuration](/oracle/run-oracle/#set-up-oracle-server-configuration)
   - [Setup data plugins configuration](/oracle/run-oracle/#setup-data-plugins-configuration).

::: {.callout-tip title="Adding your own data source plugins?" collapse="false"}

If you have developed your own FX plugins, (a) add sub-directory(ies) containing the plugin source code to the `plugins` sub-directory of your installation; (b) add config entry(ies) to the `oracle_config.yml` file.

:::

### Set up oracle server configuration

To specify the oracle server configuration edit the `oracle_config.yml` file to set the oracle server runtime configuration settings.  

| Option | Description | Default Configuration |
|:-------|:------------|:----------------------|
| `logLevel` | Sets logging verbosity. Available logging levels: `0`: No logging, `1`: Trace, `2`: Debug, `3`: Info, `4`: Warn, `5`: Error | `3` |
| `gasTipCap` | Sets a gas priority fee cap for your oracle server data report transactions. The gas priority fee cap is reimbursed by the Autonity network. Specify in [`ton`](/glossary/#ton). | `1000000000` ([`gigaton`](/glossary/#gigaton)) |
| `voteBuffer` | Sets the buffering time window in blocks to resume voting after the last penalty event. With a time buffer, the node operator can check and repair local infrastructure without being penalized for failing to vote while debugging. Specify in seconds. | `86400`  ( 3600 * 24, i.e. 1 day) |
| `keyFile` | Path to the oracle server key file. e.g. `../aut/keystore/oracle.key`| No default |
| `keyPassword` | The password to the oracle server key file. | No default |
| `autonityWSUrl` | The WS-RPC server listening interface and port of the connected Autonity Go Client node (see [install Autonity, networks](/node-operators/install-aut/#network). | `"ws://127.0.0.1:8546"` |
| `pluginDir` | The path to the directory containing the built data plugins. For example | `"./plugins"` |
| `profileDir` | The profiling report directory, where runtime state will be saved to. | `"."` |
| `confidenceStrategy` | The confidence strategy. Available strategies are: `0`: linear, `1`: fixed. | `0` |

::: {.callout-tip title="Confidence strategy - linear vs. fixed" collapse="false"}

Oracle prices are submitted with a _confidence score_ in the range $(0, 100)$ expressing the oracle's level of trust in the provided price (For detail on confidence score, see the concept description [Oracle accountability fault detection (OAFD)](/concepts/oafd/#confidence-score).

`confidenceStrategy` provides two out-the-box options to compute the confidence score for a symbol:

- `0`: linear, dynamic. The oracle server will use the number of price samples it retrieved during the [voting round](/glossary/#voting-round) for a symbol to compute the confidence score. The higher the number of samples, the higher the confidence score. The confidence score computed is capped at the maximum trust level of $100$.
- `1`: fixed, set to $100$ the maximum trust level.

:::

::: {.callout-caution title="Always review and set `oracle_config.yml` to your configuration before running oracle server" collapse="false"}

The `oracle_config.yml` file is preset to a testing configuration set to use the test credentials. 

If you run the server without setting your own configuration, then the test configuration will _de facto_ be picked up and used as a default configuration. Without editing the key options (`keyFile`, `keyPassword`) at minimum, the server will error with an unable to load key message:

```
$ ./autoracle oracle_config.yml 
2025/03/20 11:52:09 cannot read key from oracle key file: ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe, open ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe: no such file or directory
could not load key from key store: ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe with password, err: open ./UTC--2023-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe: no such file or directory
```
:::

   An example Oracle Server Configuration for an oracle server binary could be:

   ```yaml
   logLevel: 3
   gasTipCap: 1000000000
   voteBuffer: 86400
   keyFile: "./UTC--2025-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe"
   keyPassword: "123%&%^$"
   autonityWSUrl: "ws://127.0.0.1:8546"
   pluginDir: "./plugins"
   profileDir: "."
   confidenceStrategy: 0
   ```
  
   An example configuration for an oracle server Docker image could be per beneath. Note the mounted path is used for the `keyFile`file. A mounted path is not used for the `plugin.dir` config which takes the Docker image plugins directory path `/usr/local/bin/plugins/`:

   ```yaml
   logLevel: 3
   gasTipCap: 1000000000
   voteBuffer: 86400
   keyFile: "/autoracle/UTC--2025-02-27T09-10-19.592765887Z--b749d3d83376276ab4ddef2d9300fb5ce70ebafe"
   keyPassword: "123%&%^$"
   autonityWSUrl: "ws://127.0.0.1:8546"
   pluginDir: "/usr/local/bin/plugins/"
   profileDir: "."
   confidenceStrategy: 0
   ```

### Setup data plugins configuration

The oracle server will need to provide FX, ATN and NTN currency pairs utilised in the Auton Stabilization Mechanism.

A basic set of data adaptor plugins for sourcing this data is provided out the box with oracle server for testnet pre-Mainnet in the `autonity-oracle` GitHub repo [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins) directory:

- Forex plugins: for connecting to public FX data sources for ASM [ACU](/concepts/asm/#acu) basket currency prices. See the `forex_` prefixed adaptors in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins). Five forex plugins are currently provided.
- Crypto plugins: for connecting to public CEX and DEX data sources for USD stablecoin and ATN, NTN prices. ATN NTN price data is used for the ASM [Stabilisation CDP](/concepts/asm/#stabilization) mechanism. See the `crypto_` prefixed adaptors in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins). Four crypto plugins are currently provided.
- Simulator plugin: for simulated protocol asset (ATN, NTN, NTN-ATN) data. Optionally used for testnet or local development purposes to provide a simulated ATN, NTN price data. See the `simulator_plugin` adaptor in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins). If used, the `simulator_` plugin configuration is specified explicitly in `oracle_config.yml` file by adding a [simulator config entry](/oracle/run-oracle/#atn-and-ntn-data-simulator-plugin).

Plugins are configured by default or by explicit configuration. The `crypto_` plugins have a default configuration set in the plugin source golang code as a `defaultConfig`. The `forex_` plugin configuration is specified explicitly in the `oracle_config.yml` file by adding a config entry for each plugin configured.

The full set of plugin configuration fields are:

| Name | Datatype | Mandatory? | Description |
| :-- | :--: | :--: | :-- |
| `name` | string | &#x2714; | the name of the plugin binary; use the name of the sub-directory in the `plugins` directory |
| `key` | string | &#x2714; | the API key granted by your data provider to access their data API |
| `scheme` | string | | the data service http scheme: http, https, ws or wss. Default value is https. |
| `endpoint` | string | | the data service endpoint url of the data provider |
| `timeout` | int | | the duration of the timeout period for an API request in seconds. Default value is 10. |
| `refresh` | int | | the data update interval in seconds. Used for a rate limited provider's plugin to limit the request rate. Default value is 30. |
| `ntnTokenAddress` | string | ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) | The NTN ERC20 token address on the target blockchain. This is the [Autonity Protocol Contract Address](/concepts/architecture/#protocol-contract-addresses). |
| `atnTokenAddress` | string | ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) |The Wrapped ATN erc20 token address on the target blockchain. |
| `usdcTokenAddress` | string | ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) | USDC ERC20 token address on the target blockchian. For Bakerloo Testnet this is the USDCx ERC20 token address. |
| `swapAddress` | string | ([`crypto_uniswap_usdcx`](https://github.com/autonity/autonity-oracle/blob/0b64c2a3bbc9abeb44db9c5ccdad4b344cf1ad76/plugins/crypto_uniswap/uniswap_usdcx/crypto_uniswap_usdcx.go#L12C5-L12C18) plugin only) | UniSwap factory contract address or AirSwap SwapERC20 contract address on the target blockchain. For Bakerloo Testnet this is the Uniswap V2 AMM clone factory contract address. |
| `disabled` | boolean |  | The flag to disable a plugin. False by default. |

The configuration fields used depends on the type of plugin. Set optional fields as needed to fit the service level agreed with your rate provider and your own operational practice.

#### Setup forex plugin config

To configure FX data source plugins edit the `oracle_config.yml` file to add a config entry for each plugin. The oracle server release contains out-the-box plugins for five publicly accessible FX endpoints with free and paid subscriptions tiers. You will need to create an account and get an API Key to connect. One or more FX plugin source must be configured.

Navigate to the public GitHub repo [autonity-oracle](https://github.com/autonity/autonity-oracle) `README.md` [Configuration](https://github.com/autonity/autonity-oracle?tab=readme#configuration-of-oracle-server) section to view the supported FX endpoint providers.

For each FX endpoint configured:

1. Get FX plugin API Key(s) for the listed FX endpoint. Navigate to one of the listed FX endpoint websites and create an account. Make a note of the API Key.
2. Add configuration entry to `oracle_config.yml`. Edit the file to add an entry for each plugin you are configuring.

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

#### Setup crypto plugin config

The `crypto_` plugins have default configuration and run by default when oracle server is initialised. There are four plugins:

- 1 DEX: `crypto_uniswap`. Connector to retrieve ATN, NTN USDC price data from an on-chain Uniswap V2 AMM on Bakerloo Testnet.
- 3 CEX: `crypto_kraken`, `crypto_coingecko`, `crypto_coinbase`. Connectors to retrieve USDC-USD price data.

Configure the `crypto_uniswap` plugin to set the RPC endpoint of a Bakerloo Testnet Full Node (i.e. your own node or a [public rpc endpoint](/networks/testnet-bakerloo/#public-endpoints)). Un-comment and edit the `crypto_uniswap` entry in `oracle_config.yml`. Edit the configuration fields:

| Name | Datatype | Mandatory? | Description |
| :-- | :--: | :--: | :-- |
| `scheme` | string | required | edit to the scheme used for connecting to your full node: `http`, `https`, `ws` or `wss` |
| `endpoint` | string | required | edit to the rpc endpoint address of your connected full node |

No editing of default configuration is required for the 3 CEX connectors used to retrieve USDC-USD price data.

::: {.callout-note title="Why a USDC-USD price?" collapse="true"}
The oracle server uses the USDC-USD pricing to convert the ATN, NTN USDC market prices from the Testnet Uniswap V2 AMM to ATN,NTN USD prices. The price report for ATN, NTN is then submitted on-chain with USD as the quote pair by the oracle server's connected validator node.

On-chain, the oracle protocol is pricing in USD and not USDC.
:::

#### ATN and NTN data simulator plugin

If a simulator has been deployed and is available to provide simulated data for testnet or local development network use, this can be connected to by adding a config entry for the simulated source to your `oracle_config.yml` file.

1. Edit your `oracle_config.yml` config file to point to the deployed ATN and NTN data simulator. Just add a `simulator_plugin` entry for the simulator data source, specifying `endpoint` and `scheme` at minimum.

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


## Develop plugins
Additional data adaptors for any external data source can be developed using the oracle server's plugin template. See:

- Adaptor code template `template_plugin` in [`/plugins`](https://github.com/autonity/autonity-oracle/tree/master/plugins).
- Guide for how _To write a new plugin_ using the template in [`/plugins/README`](https://github.com/autonity/autonity-oracle/blob/master/plugins/README.md).


## Stopping the Autonity Oracle Server

To shutdown the oracle server, press `CTRL-C` and wait for it to exit.

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
