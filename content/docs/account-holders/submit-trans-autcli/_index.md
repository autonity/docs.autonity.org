---
title: "Submit a transaction from Autonity autcli"
linkTitle: "Submit a transaction from Autonity autcli"
weight: 60
description: >
  How to submit transactions to an Autonity network using the Python3 interface to the RPC API's
---

## Prerequisites

To submit transactions to a client node from the Autonity `autcli` you need:

- An installation [of `aut`](https://github.com/autonity/autcli) - see the [howto](/account-holders/setup-autcli/) for further help.

- An [account](/account-holders//create-acct/) that has been [funded](/account-holders/fund-acct/) with auton, to pay for transaction gas costs.

- The `aut` CLI tool should be configured to connect to the appropriate node or Autonity network (see the [list of networks including public RPC endpoints](/networks/).

{{< alert title="Note" >}}
This guide assumes that the following have been set in your `.autrc` file, or will be added to the commands below using the appropriate flags:
- `rpc_endpoint`: the endpoint URI of the node you will connect to.
- `keyfile`: the path to the encrypted private key file for your default testnet account.
- (optional) `keytore`: the default directory containing keyfiles
{{< /alert >}}

## Examples

For parameter definitions and usage see the Reference [Autonity Contract Interfaces](/reference/api/).

### Transfer Auton:

Transfer Autonity's native account coin, specifying the `<RECIPIENT_ADDRESS>`:

```bash
aut tx make --to <RECIPIENT_ADDRESS>  --value 1 | aut tx sign - | aut tx send -
0xA473bC8B8449A2f02719F2569Ae8137F0bEcdb1843Ab78C84B9A4f02712F9529
```

#### A note about signing and submitting

The output of each command above is being piped to the next in this example.  Alternatively, the output can be written to files, for example to be signed using a hardware waller or other key management systems).

This use of piping will appear in many example commands, for convenience.  For reference:
- `aut tx make ...` outputs a transaction in JSON format
- `aut tx sign ...` signs the transaction and outputs the signed transaction in JSON format
- `aut tx send ...` send the transaction and outputs the transaction hash

### Waiting for transactions

Wait for (and return the receipt from) a given transaction using its hash:
```bash
aut tx wait 0xA473bC8B8449A2f02719F2569Ae8137F0bEcdb1843Ab78C84B9A4f02712F9529
```

### Transfer Newton:

Transferring Autonity's native stake token Newton, specifying the `<RECIPIENT_ADDRESS>` and the `--ntn` flag:

```console
aut tx make --to <RECIPIENT_ADDRESS> --value 1 --ntn | aut tx sign - | aut tx send -
```

### Get auton balance:

Getting an account's balance in Autonity's native protocol coin Auton:

```console
aut account balance
```

By default, the account associated with the default `keyfile` is used.  Use `aut account balance <ACCOUNT_ADDRESS>` to check the balance of other accounts.

### Get newton balance:

Getting an account's balance in Autonity's native stake token Newton, using the `--ntn` flag:

```console
aut account balance --ntn
```

(Similarly, `aut account balance --ntn <ACCOUNT_ADDRESS>` can be used to check other accounts.)

### ERC20 tokens:

The `--token` flag can be used to interact with any ERC20 token, including the Liquid Newton tokens for registered validators.

```bash
aut account balance --token <TOKEN_ADDRESS>
```
```bash
aut tx make --to <RECIPIENT_ADDRESS> --value 1.2 --token <TOKEN_ADDRESS> | aut tx sign - | aut tx send -
```

The following command can be used to determine the Liquid Newton contract address of the validator `<VALIDATOR>`.

```bash
aut validator info --validator <VALIDATOR>
```

See the `liquid_contract` field of the JSON output for the contract address.

{{< alert title="Note" >}}
See also `aut token --help` for more command to interact with ERC20 tokens.
{{< /alert >}}
