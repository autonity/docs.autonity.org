---
title: "Migrate Validator"
description: >
  How to migrate an Autonity validator node to a new instance or to a new IP/Port address
---

::: {.callout-note title="Prerequisites" collapse="false"}
- Ensure that the host machine meets the [minimum requirements](/node-operators/install-aut/#requirements)
:::


## Migrating validator node to a new environment

To migrate a node to a new instance follow the steps described in the node operator's guide [Migrate Autonity](/node-operators/migrate-aut/).

::: {.callout-warning title="Important" collapse="false"}
If your node is in an active state, you must [pause the validator node](/validators/pause-vali/) **before migration**. [Reactivate the validator](/validators/pause-vali/) **after migration**.

Be sure to fully decommission the original node installation!
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

### Step 2: Update enode URL with new IP/Port address

::: {.callout-note title="Protocol contract calls" collapse="false"}
The guide uses the `aut contract call` and `aut contract tx` commands for the contract interaction.

`aut contract` usage requires that you specify the [ABI](/glossary/#application-binary-interface-abi) file and the protocol contract address of the contract being called. To complete the guide you will need to call 2 protocol contracts:

- the Autonity Protocol Contract (`Autonity.abi`)  with the protocol contract address `0xBd770416a3345F91E4B34576cb804a576fa48EB1`.

The [Autonity Protocol Contract Interfaces](/reference/api/aut/) is called to update the validator enode URL.

The `abi` files are generated when building the client from source and `Autonity.abi` can be found in your `autonity` installation directory at `./params/generated/Autonity.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built the utility when building from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).

The guide explicitly sets the path to the ABI file and contract address for clarity. Note that the ABI file and contract address can be set as defaults in `aut`'s configuration file `.autrc` using the `contract_address` and `contract_abi` flags:

```
#contract_abi = Autonity.abi
#contract_address = 0xBd770416a3345F91E4B34576cb804a576fa48EB1
```

The guide assumes the ABI file is in the directory from which the `aut` command is run, and `aut` is configured to use the validator [treasury account](/concepts/validator/#treasury-account) keyfile.
:::

1. Call [`updateEnode()`](/reference/api/aut/#updateenode) passing in parameters for:

  - `<NODE_ADDRESS>`: the [validator identifier](/concepts/validator/#validator-identifier) address of the validator node
  - `<ENODE>`: the new enode URL value

  ```bash
aut contract tx --abi Autonity.abi --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 updateEnode <NODE_ADDRESS> <ENODE>
```
  
  On commit, the transaction will update the validator's registered enode URL in system state.

### Step 3: Migrate to new environment

Migrate the node to the environment with the new IP/Port address configuration as described in the guide [Migrating validator node to a new environment](/validators/migrate-vali/#migrating-validator-node-to-a-new-environment) on this page.

### Step 4: Start validator node

Start the validator as described in the guide [Run Autonity](/node-operators/run-aut/).

### Step 5: Re-activate the validator

Reactivate the validator as described in the guide [Reactivate as a validator](/validators/pause-vali/#re-activate-a-validator).

The validator has resumed an active state and can join the consensus committee if selected.

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
