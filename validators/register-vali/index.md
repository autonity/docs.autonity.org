---
title: "Register as a Validator"
description: >
  How to register your node as a Validator on an Autonity network
---

## Prerequisites

To register a validator you need:

- A [running instance of the Autonity Go Client](/node-operators/) running on your host machine, with [networking](/node-operators/install-aut/#network) configured to allow incoming traffic on its WebSocket port.  This will be the node to be registered as a validator.
- A [running instance of the Autonity Oracle Server](/oracle/) running on your host machine, with a funded oracle server account. This will be configured to provide data price reports to your  validator node's WebSocket port.
- A configured instance of [`aut`](/account-holders/setup-aut/).
- An [account](/account-holders//create-acct/) that has been [funded](/account-holders/fund-acct/) with auton (to pay for transaction gas costs). Note that this account will become the validator's [`treasury account`](/concepts/validator/#treasury-account) - the account used to manage the validator, that will also receive the validator's share of staking rewards.

::: {.callout-note title="Note" collapse="false"}
See the [Validator](/concepts/validator/) section for an explanation of the validator, a description of the [validator lifecycle](/concepts/validator/#validator-lifecycle), and a description of the [post-genesis registration](/concepts/validator/#post-genesis-registration) process.

See the [Oracle](/concepts/oracle-server/) section for an explanation of the oracle server.
:::

## Register as a validator

### Step 1. Generate a cryptographic proof of node ownership

This must be performed on the host machine running the Autonity Go Client, using the `autonity genOwnershipProof` command:

```bash
autonity genOwnershipProof --autonitykeys <AUTONITYKEYS_PATH> --oraclekey <ORACLE_KEY_PATH> <TREASURY_ACCOUNT_ADDRESS>
```

where:

  - `<AUTONITYKEYS_PATH>`: is the path to the private key file of the node's `autonitykeys` P2P node keys, specified when running the node. (For generating your `autonitykeys` file see the guide [Run Autonity](/node-operators/run-aut/).)
  - `<ORACLE_KEY_PATH>`: is the path to the private key file of the oracle server key. (For creating this key see the guide [Run Autonity Oracle Server](/oracle/run-oracle/).)
  - `<TREASURY_ACCOUNT_ADDRESS>`: is the account address you will use to operate the validator and receive commission revenue rewards to (i.e. the address you are using to submit the registration transaction from the local machine).

You should see something like this:

```bash
autonity genOwnershipProof --autonitykeys ./keystore/autonityKeys --oraclekey ./keystore/oraclekey 0xf47fdd88c8f6f80239e177386cc5ae3d6bcdeeea

0xad5652191c7b36608b52bdb6479c2de4b8786fb72b7be30cade15c847323ed091542e917d304d9e011892fe26006f359808f01557651607ba70542218a7d329a01a5189e8d50880faf97ad42501375b216b89304c3fd4acf548a1d7fd7136e74771791422819134e2e3fbf720c35652d8c163e3d4f22c798a3c648958f7abcda2c0089d5969f39bc6dff61ae6d90ac4074879e53daaf8857f3bc5b5cc3743725544dfa2954d0fc077a0fddc7c9b01994c96a079f5340bfec22c59e67c9687b4348913b37ed0617dd66a324b8532146c6d33a280d1c5a6425799856648c58d45c9c06
```

This signature hex will be required for the registration.

If you are running the Autonity Go Client in a docker container, setup as described in the guide [Run Autonity as a Docker Image](/node-operators/run-aut#run-docker), the proof can be generated as follows. In this example the keys are mounted in a volume simply named `keystore`:

```bash
docker run -t -i --volume $PWD/keystore:/keystore --name autonity --rm ghcr.io/autonity/autonity:latest genOwnershipProof --autonitykeys /<AUTONITYKEYS_PATH> --oraclekey /<ORACLE_KEY_PATH> <TREASURY_ACCOUNT_ADDRESS>
```

::: {.callout-note title="Note" collapse="false"}
The `genOwnershipProof` command options `--autonitykeys` and `--oraclekey` options require the raw (unencrypted) private key file is passed in as argument. The `autonitykeys` file is unencrypted. If `aut` has been used to generate the oracle key, then the key has been created in encrypted file format using the [Web3 Secret Storage Definition](https://ethereum.org/en/developers/docs/data-structures-and-encoding/web3-secret-storage/).

Autonity's `ethkey` cmd utility can be used to inspect the keystore file and view the account address, public key, and private key after entering your account password:

```
./build/bin/ethkey inspect --private <ORACLE_KEY_PATH>/oracle.key                   

Password: 
```
To install the `cmd` utilities use `make all` when [building Autonity from source code](/node-operators/install-aut/#install-source).

:::

### Step 2. Determine the validator enode and address

<!-- Seems like it should be possible to do this from the host machine with an `autonity ...` cmd. -->

Ensure that `aut` connects to the node that will become a validator.  Query the enode using the `aut node info` command:

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

The [validator address](/concepts/validator/#validator-identifier) or [validator identifier](/concepts/validator/#validator-identifier) is derived from the validator [P2P node key](/concepts/validator/#p2p-node-key)'s public key.  It can be computed from the enode string before registration:

```bash
aut validator compute-address enode://c746ded15b4fa7e398a8925d8a2e4c76d9fc8007eb8a6b8ad408a18bf66266b9d03dd9aa26c902a4ac02eb465d205c0c58b6f5063963fc752806f2681287a915@51.89.151.55:30303
```
```bash
0x49454f01a8F1Fbab21785a57114Ed955212006be
```

Make a note of this identifier.

### Step 3. Submit the registration transaction

::: {.callout-note title="Note" collapse="false"}
The commands given in this step assume that your `.autrc` configuration file contains a `keyfile = <path>` entry pointing to the keyfile for the treasury account used to generate the proof of node ownership above.  If this is not the case, use the `--keyfile` option in the `aut validator register` and `aut tx sign` command below, to ensure that the registration transaction is compatible with the proof.
:::

```bash
aut validator register <ENODE_URL> <ORACLE_ADDRESS> <PROOF> | aut tx sign - | aut tx send -
```

where:

- `<ENODE_URL>`: the enode url returned in Step 2.
- `<ORACLE_ADDRESS>`: the oracle server account address.
- `<PROOF>`: the proof of node ownership generated in Step 1.

Once the transaction is finalized (use `aut tx wait <txid>` to wait for it to be included in a block and return the status), the node is registered as a validator in the active state. It will become eligible for [selection to the consensus committee](/concepts/validator/#eligibility-for-selection-to-consensus-committee) once stake has been bonded to it.

#### Troubleshooting

Errors of the form
```bash
Error: execution reverted: Invalid proof provided for registration
```
indicate a mismatch between treasury address and either:
<!--
- the `from` address of the transaction generated in the `aut validator register` command, AND/OR

-->
- the `from` address of the transaction generated in the `aut contract tx` command, AND/OR
- the key used in the `aut tx sign` command

Check your configuration as described in the "Important Note" at the start of this section.

### Step 4. Confirm registration

Confirm that the validator has been registered by checking that its identifier (noted in Step 2) appears in the validator list:
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

{{pageinfo}}
To self-bond stake to your validator node, submit a bond transaction from the account used to submit the registration transaction - i.e. the validator's treasury account address. For how to  do this see the how to [Bond stake](/delegators/bond-stake/).
{{/pageinfo}}
