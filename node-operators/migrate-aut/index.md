---
title: "Migrate Autonity"
description: >
  How to migrate an Autonity node to a new instance in your own environment
---

::: {.callout-note title="Prerequisites" collapse="false"}
- Ensure that the host machine meets the [minimum requirements](/node-operators/install-aut/#requirements)
:::


## Maintaining node identity

To migrate a node to a new instance the node identity must be preserved. This is done by simply using the existing [P2P node keys: autonityKeys](/concepts/validator/#p2p-node-keys-autonitykeys) and the node's host [ip address](/node-operators/install-aut/#network) for the new node instance. By doing this the new node instance will have the same node [identifier](/concepts/validator/#validator-identifier) address and [enode url](/glossary/#enode) as the old instance.

::: {.callout-note title="Additional checks if you are migrating a registered validator node" collapse="false"}
1. Make sure that your validator is not an active member of the consensus committee during the migration. It is recommended that your validator is in a [`paused`](/concepts/validator/#validator-pausing) state before beginning the migration.
2. Verify the node's new IP/Port address is the same as that in your registered enode URL. You can check this by calling `aut validator info --validator` to view the registered enode URL.

If you are operating a validator node it is possible to change your IP/Port address as described in the guide [Migrating validator node to a new IP/Port address](/validators/migrate-vali/#migrating-validator-node-to-a-new-ipport-address).
:::

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

Be sure to fully decommission the original validator node installation environment!

::: {.callout-note title="Additional Step if you are migrating a registered validator node" collapse="false"}
You will need to transition your validator back to an active state so it is once again considered by protocol for consensus committee selection.

To do this [re-activate the validator](/validators/pause-vali/#re-activate-a-validator) instance after migration completes.
:::

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
