---
title: "Migrate Validator"
description: >
  How to migrate an Autonity validator node to a new instance or to a new IP/Port address
---

::: {.callout-note title="Prerequisites" collapse="false"}
- Ensure that the host machine meets the [minimum requirements](/node-operators/install-aut/#requirements)
:::

## Migrating validator node to a new IP/Port address

This guide describes how to migrate a validator node to an environment with a new IP/Port network address by updating the validator's registered enode URL.

::: {.callout-warning title="Important" collapse="false"}
Only the network connection information - IP and/or port - of a registered validator enode can be updated. You **cannot** change the validator's address (i.e. the `PUBKEY` part of the [validator enode URL](/concepts/validator/#validator-enode-url)).
:::

When performing the update the validator **must not** not be an active member of the consensus committee. It is **recommended** that you [`pause`](/concepts/validator/#validator-pausing) your validator before migration. This is to prevent your node being elected as a committee member while you are in the process of migration.

### Step 1: Pause the validator

Pause the validator as described in the guide [Pause as a validator](/validators/pause-vali/#pause-as-a-validator).

If your validator is an active member of the consensus committed, wait for the epoch to end before proceeding further.

::: {.callout-important title="Verify your validator node is not in the active consensus committee" collapse="false"}
Call `aut protocol get-committee` to verify that your validator address does not appear in the list of committee validators returned.
:::

### Step 2: Update enode URL with new IP/Port address

Call [`updateEnode()`](/reference/api/aut/#updateenode) passing in parameters for:

  - `<NODE_ADDRESS>`: the [validator identifier](/concepts/validator/#validator-identifier) address of the validator node
  - `<ENODE>`: the new enode URL value

  ```bash
aut validator update-enode --validator <NODE_ADDRESS> <ENODE> | aut tx sign - | aut tx send -
```
  
On commit, the transaction will update the validator's registered enode URL in system state. you can view the updated enode using `aut validator info --validator`.

### Step 3: Migrate to new environment

Migrate the node to the environment with the new IP/Port address configuration as described in the guide [Migrating validator node to a new environment](/validators/migrate-vali/#migrating-validator-node-to-a-new-environment) on this page.

### Step 4: Start validator node

Start the validator as described in the guide [Run Autonity](/node-operators/run-aut/).

### Step 5: Re-activate the validator

Reactivate the validator as described in the guide [Reactivate as a validator](/validators/pause-vali/#re-activate-a-validator).

The validator has resumed an active state and can join the consensus committee if selected.

## Migrating validator node to a new environment

To migrate a node to a new instance follow the steps described in the node operator's guide [Migrate Autonity](/node-operators/migrate-aut/).

::: {.callout-warning title="Important" collapse="false"}
If your node is in an active state, you must [pause the validator node](/validators/pause-vali/) **before migration**. [Reactivate the validator](/validators/pause-vali/) **after migration**.

Be sure to fully decommission the original node installation!
:::

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
