---
title: "Submit governance transaction from Autonity aut CLI"
linkTitle: "Submit governance transaction from Autonity aut CLI"
weight: 110
description: >
  How to call operator only functions as the governance account using the Python3 interface to the RPC API’s

draft: false
---

{{% pageinfo %}}
Governance functions are only callable from the governance operator account of an Autonity network. See the Autonity Interfaces Reference section [Operator only](/reference/api/aut/op-prot/#operator-only) for the listing of governance API methods.
{{% /pageinfo %}}

## Prerequisites

To submit transactions restricted to the governance `operator` account from the Autonity `aut` CLI you need:

- An installation of [`aut`](https://github.com/autonity/autcli) CLI - see the [howto](/account-holders/setup-autcli/) for further help.

- To have setup the governance `operator` account in `aut` CLI. Import the private key of the governance account as described in [Import account using `autcli`](/account-holders/create-acct/#import-account-using-autcli).

- To have funded your governance `operator` account. If you are running the client in dev mode, the account is already funded. If you are creating a local testnet using a genesis file, you will need to fund the operator account in the [genesis configuration file](/reference/genesis/#genesis-configuration-file)'s [`alloc`](/reference/genesis/#alloc-object) data structure.

- The `aut` CLI tool should be configured to connect to the local Autonity testnet you have setup.

## Examples

For parameter definitions and usage of the operator only governance functions and the  see the Autonity Contract Interfaces [Operator only](/reference/api/aut/op-prot/#operator-only) reference.

### Mint Newton stake token:
    
Mint Autonity's native staking token, specifying the `<RECIPIENT_ADDRESS>` and `<AMOUNT>`:

```bash
aut protocol mint 1 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
```

### Burn Newton stake token:
    
Burn Autonity's native staking token, specifying the `<RECIPIENT_ADDRESS>` and `<AMOUNT>`:

```bash
aut protocol burn 1 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
```

### Set minimum base fee:
    
Set a new minimum base fee denominated in `Auton`, specifying a decimal value:


```bash
aut protocol set-minimum-base-fee 50000000 | aut tx sign - | aut tx send -
```
