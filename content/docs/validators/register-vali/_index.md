---
title: "Register as a Validator"
linkTitle: "Register Validator"
weight: 120
description: >
  How to register your node as a Validator on an Autonity network
---

## Prerequisites

To register a validator you need:

- A running instance of the Autonity Go Client running on your host machine.  This will be the nod to be registered as a validator.
- A configured instance of [`autcli`](/howto/setup-autcli).
- An [account](/howto/create-acct) that has been [funded](/howto/fund-acct) with auton (to pay for transaction gas costs). Note that this account will become the validator's [`treasury account`](/architecture/validator/#treasury-account) - the account used to manage the validator, that that will also receive the validator's share of staking rewards.

This guide also assumes that the command-line JSON processor `jq` is available - see [additional helpers](/howto/#additional-helpers).

{{< alert title="Note" >}}See the [Validator](/architecture/validator/) section for an explanation of the validator, a description of the [validator lifecycle](/architecture/validator/#validator-lifecycle), and a description of the [post-genesis registration](/architecture/validator/#post-genesis-registration) process.{{< /alert >}}

## Register as a validator

### Step 1. Generate a cryptographic proof of node ownership

This must be performed on the host machine running the Autonity Go Client, using the `autonity genEnodeProof` command:

```bash
autonity genEnodeProof --nodekey <NODE_KEY_PATH> <TREASURY_ACCOUNT_ADDRESS>
```

where
    - `<NODE_KEY_PATH>`: is the path to the private key file of the P2P node key (by default within the `autonity` subfolder of the `--datadir` specified when running the node`. (For setting the data directory see How to [Run Autonity](/howto/run-aut).)
    - `<TREASURY_ACCOUNT_ADDRESS>`: is treasury account address (i.e. the address you are using to submit the registration transaction from the local machine).

You should see something like this:

```bash
autonity genEnodeProof --nodekey ./blockchain/autonity/nodekey 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4
Signature hex: 0x4563c91c4a1c0371ff3633f1e8c23f211e4ac6b50852689dbaa17f6b74711f2869e41d847862d5ad2a08a15d57b4d5a3b4315eb10dd22f69aa27c3ce229539c700
```

This signature hex will be required for the registration.

### Step 2. Determine the validator enode

<!-- Seems like it should be possible to do this frmo the host machine with an `autonity ...` cmd. -->

Ensure that the `aut` CLI tool connects to the node that will become a validator.  Query the enode using the `aut node info` command:

```bash
aut node info
```
```bash
$ aut node info
{
"eth_accounts": [],
"eth_blockNumber": 113463,
"eth_gasPrice": 1000000000,
"eth_hashrate": 0,
"eth_mining": false,
"eth_syncing": false,
"eth_chainId": 65000011,
"net_listening": true,
"net_peerCount": 0,
"net_networkId": "65100000",
"web3_clientVersion": "Autonity/v0.9.0-773923af-20221021/linux-amd64/go1.18.1",
"admin_enode": "enode://c746ded15b4fa7e398a8925d8a2e4c76d9fc8007eb8a6b8ad408a18bf66266b9d03dd9aa26c902a4ac02eb465d205c0c58b6f5063963fc752806f2681287a915@51.89.151.55:30303",
"admin_id": "f8d35fa6019628963668e868a9f070101236476fe077f4a058c0c22e81b8a6c9"
}
```

The url is returned in the `admin_enode` field.

### Step 3. Submit the registration transaction.

```bash
aut validator register <ENODE_URL> <PROOF> | aut tx sign - | aut tx send -
```
where

   - `<ENODE_URL>`: the enode url returned in Step 1.
   - `<PROOF>`: the proof of enode ownership generated in Step 2.

Once the transaction is finalized (use `aut tx wait <txid>` to wait for it to be included in a block and return the status), the node is registered as a validator in the active state. It will become eligible for [selection to the consensus committee](/architecture/validator/#eligibility-for-selection-to-consensus-committee) once stake has been bonded to it.

### Step 4. Identify the validator ID

Requery the list of validators to determine the validator ID.
The [validator identifier](/architecture/validator/#validator-identifier) is created in the form of an account address derived from the validator [P2P node key](/architecture/validator/#p2p-node-key)'s public key. The newly registered validator's identifier should appear at the end of the validator list

```bash
aut validator list
```
```bash
0x32F3493Ef14c28419a98Ff20dE8A033cf9e6aB97
0x31870f96212787D181B3B2771F58AF2BeD0019Aa
0xE03D1DE3A2Fb5FEc85041655F218f18c9d4dac55
0x52b89AFA0D1dEe274bb5e4395eE102AaFbF372EA
0x49454f01a8F1Fbab21785a57114Ed955212006be
```

Confirm the validator details using:

```bash
aut validator info --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be
```

and check that the information is as expected for your validator.

{{% pageinfo %}}
To self-bond stake to your validator node, submit a bond transaction from the account used to submit the registration transaction - i.e. the validator's treasury account address. For how to  do this see the how to [Bond stake](/howto/bond-stake).
{{% /pageinfo %}}