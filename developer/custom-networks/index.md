---
title: "Setting up custom networks"
description: >
  Custom Autonity networks
draft: false
---

To connect your node to a custom Autonity network, you will need the network's:
  - bootnodes, typically given in a  `static-nodes.json` file or specified when running the node with the `--bootnodes` command-line option.
  - genesis configuration file,  `genesis.json`.

  See [Local Autonity Network configuration](/reference/genesis/#local-autonity-network-configuration) in the [Genesis](/reference/genesis/) reference for how to create these files.

::: {.callout-note title="Note" collapse="false"}
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


