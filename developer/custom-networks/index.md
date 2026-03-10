---
title: "Setting up custom networks"
description: >
  Custom Autonity networks
draft: false
---

To connect your node to a custom Autonity network, you will need the network's:

  - bootnodes, specify statically in a  `static-nodes.json` file or dynamically using the `--bootnodes` command-line option.
  - genesis configuration file,  `genesis.json`.

  See [Local Autonity Network configuration](/reference/genesis/#local-autonity-network-configuration) in the [Genesis](/reference/genesis/) reference for how to create these files.

::: {.callout-tip title="How to identify and configure bootnodes for a custom network" collapse="true"}

A new node must connect to at least one known peer to discover additional peers and begin syncing.

To configure bootnodes for a custom network:

1. **Obtain candidate enode addresses** from one or more of the following sources:
   - public RPC providers, using `admin_nodeInfo` where enabled,
   - validator dashboards,
   - chain state queries,
   - trusted node operators.

2. **Verify TCP reachability**:

   ```bash
   nc -vz <ip> 30303
   ```

   Optionally, verify UDP reachability:

   ```bash
   nc -vzu <ip> 30303
   ```

   Nodes with UDP port `30303` open support more complete peer discovery.

3. **Configure one or more reachable peers** using either of the following methods:
   - add the enode addresses to a `static-nodes.json` file and place it in the chaindata directory, as described in [Setting up custom networks](/developer/custom-networks/),
   - pass a comma-separated list of enode addresses using the `--bootnodes` option when starting the client.

4. **Start the node**. The node connects to the specified peer and expands its peer table. For best results, use a peer with both TCP and UDP port `30303` open.

### Related resources

- Example static nodes file: [Static nodes file](/reference/genesis/#static-nodes-file)
- Custom network configuration: [Setting up custom networks](/developer/custom-networks/)
- Commands for retrieving node addresses and enodes using [Autonity CLI](/account-holders/setup-aut/):
  - `aut validator list`
  - `aut protocol committee-enodes`
  - `aut node info`
- Community validator explorer dashboards: [awesome-autonity](https://github.com/autonity/awesome-autonity?tab=readme-ov-file#explorers)
- Autonity [Discord Server](https://discord.gg/autonity): *Validators* and *Technical Help* channels.

### Example

```bash
nc -vzu 125.181.215.22 30303
Connection to 125.181.215.22 port 30303 [udp/*] succeeded!

nc -vz 125.181.215.22 30303
Connection to 125.181.215.22 port 30303 [tcp/*] succeeded!
```
:::

::: {.callout-caution title="Caution" collapse="false"}
Note that the client provides a [command-line option](/reference/cli/agc/#command-line-options) for connecting to the Autonity Bakerloo Testnet `--bakerloo`. The node will not run if you specify both genesis and bootnodes for a custom network **and** a testnet flag. The client will create a genesis block for the custom network's genesis configuration and the node's local store will then have an incompatible genesis with the testnet.
:::

1. Install Autonity in a working directory and create an `autonity-chaindata` sub-directory as described in [Running a node, Install Autonity](/node-operators/install-aut/).

2. Create and copy the bootnode file into the `autonity-chaindata` sub directory:

```bash
cp ./<PATH>/static-nodes.json ./autonity-chaindata/
```

3. Create and copy the genesis file into the working directory:

```bash
cp ./<PATH>/genesis.json ./
```

4. Run the node as described in [Running a node, Run Autonity](/node-operators/run-aut/), specifying your custom network by the options:
	- `--genesis`: to provide the genesis file.
	- `--networkid`: to provide the network identifier. This is typically the same value as the `chainId` file in the genesis configuration file, but may be different.

	An example run command for a local development network on localhost could be:

```bash
autonity \
		--datadir ./autonity-chaindata \
		--genesis ./genesis.json \
		--networkid 65110000 \
		--http \
		--http.addr 0.0.0.0 \
		--http.api aut,eth,net,txpool,web3,admin \
		--http.vhosts * \
		--ws \
		--ws.addr 0.0.0.0 \
		--ws.api aut,eth,net,txpool,web3,admin \
		--nat extip:<IP_ADDRESS>
		;
```


