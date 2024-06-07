---
title: "Migrate Autonity"
description: >
  How to migrate an Autonity node to a new instance in your own environment
---

::: {.callout-note title="Prerequisites" collapse="false"}
- Ensure that the host machine meets the [minimum requirements](/node-operators/install-aut/#requirements)
:::


## Maintaining node identity

To migrate a node to a new instance the node identity must be preserved. This is done by simply using the existing [P2P node keys: autonityKeys](/concepts/validator/#p2p-node-keys-autonitykeys) and the node's host [ip address](/node-operators/install-aut/#network) for the new node instance.  by doing this the new node instance will have the same node [identifier](/concepts/validator/#validator-identifier) address and [enode url](/glossary/#enode) as the old instance.

Copy the [P2P node keys: autonityKeys](/concepts/validator/#p2p-node-keys-autonitykeys) file to a safe location and be sure to maintain your hosting IP address.

<!--
::: {.callout-note title="Static IP Address is required" collapse="false"}
Running an Autonity node requires maintaining a static ip address as described in the guide [Install Autonity, Networking](/node-operators/install-aut/#network) section.

If you are using a cloud provider for node hosting, then a static IP address for your cloud space should be a stated hosting requirement if you intend to migrate the node. Cloud vendors typically don't supply a static IP address unless it is purchased explicitly.
:::
-->

## Migrating an Autonity Go Client

To migrate, reinstall the node and migrate your node's `autonitykeys`.

### Step 1: Preserve node identity

Copy the [P2P node keys: autonityKeys](/concepts/validator/#p2p-node-keys-autonitykeys) file to a safe location. Ensure the new hosting environment maintains your existing IP address.

### Step 2: Install node software to new environment

Install the node as described in the [install autonity](/node-operators/install-aut/) guide

### Step 3: Migrate node `autonityKeys` keyfile

Migrate the `autonitykeys` saved in [Step 1](/node-operators/migrate-aut/#step-1-preserve-node-identity) above **before** running the node:

- Copy your original `autonitykeys` to the directory location you will use to hold the key when [running the node](/node-operators/run-aut/).

  ::: {.callout-note title="Default location for AGC's node and consensus private keys file  `autonitykeys`" collapse="false"}
On starting, by default AGC will automatically generate an `autonitykeys` file containing your node key and consensus key within the `autonity` subfolder of the `--datadir` specified when running the node. If you choose not to store your key in the default location, then specify the path to where you are keeping your `autonitykeys` file using the `--autonitykeys` option in the run command.
:::

### Step 4: Start the node preserving IP/Port configuration

Start the node as described in the guide [Run Autonity](/node-operators/run-aut/), maintaining the original IP address values for:

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
