---
title: "Get setup"
linkTitle: "Get setup"
weight: 1
description: >
  How to setup and configure your environment for running an Autonity Go Client node on an Autonity testnet
---

This section enumerates the steps to install, configure and run an Autonity Go Client (AGC) on an Autonity testnet, and to setup client tools for connecting to the node and performing some basic operations.

We assume that the Autonity Go Client will run on a _host_ machine (a VPS or other host that is always-on and persistently available), and a distinct _local_ machine will be used for creating transactions and queries which are then sent to the Autonity Go Client on the _host_ via the RPC endpoint.

## Install and run the Autonity Go Client (host machine)

- Follow the [Autonity Go Client installation guide](/howto/install-aut/) to install the client on the host machine.
- [Launch the Autonity Go Client](/howto/run-aut/) on the host machine.

You should now have a running node connected to the network which can sync the blockchain and accept RPC calls from you local machine.

## Connect to the Autonity Go Client (local machine)

- [Setup and configure the `aut` CLI tool](/howto/setup-autcli) on your local machine. This will be the client that connects to and interacts with your Autonity node via its RPC endpoint.

- Configure the `aut` CLI tool (local machine)

  To configure the `aut` tool to connect to your node, edit the `rpc_endpoint` entry in your `.autrc` file:

  ```
  rpc_endpoint=http://XX.XX.XX.XX:8545/
  ```

  where `XX.XX.XX.XX` is the IP address used to connect to your host machine running the Autonity Go Client.

  {{< alert title="Note" >}}
  If you chose to expose the Web Socket end-point of your node, the URL will be of the form `ws://XX.XX.XX.XX:8546/`.
  {{< /alert >}}

  Use the `node info` query to check the connection:

  ```bash
  aut node info
  ```
  ```bash
  {
    "eth_accounts": [],
    "eth_blockNumber": 12803619,
    "eth_gasPrice": 1000000000,
    "eth_syncing": false,
    "eth_chainId": 65100000,
    "net_listening": true,
    "net_peerCount": 19,
    "net_networkId": "65100000",
    "web3_clientVersion": "Autonity/v0.9.0/linux-amd64/go1.19",
    "admin_enode": "enode://d9a7297b2bec3c2f92233dc42f53c0cf98af30528a56765b102d9e28be2a760b7fd3045790246d1a5836af9a8ea5d2dbcc9b56864f6391045ba76391d9db931e@77.86.9.81:30303",
    "admin_id": "8794927d6dda6f8cb45bc7eefd9084dbb3b81ce508ff43e1ccb7fe904ccd2cfc"
  }
  ```

  The `admin_enode` entry should display the external IP of your host machine at the end.

<!-- TODO: The section below could arguably be it's own HOWTO "Execute some basic queries with `aut` CLI" -->

## Further simple queries

The following are examples of simple queries to help familiarize yourself with the `aut` CLI tool and the Autonity network.

### Get the block number:

```bash
aut block height
```
```bash
12877058
```
### Get maximum consensus committee size:

```bash
aut protocol get-max-committee-size
```
```bash
100
```

#### Get all nodes in the consensus committee:

```bash
aut protocol get-committee
```
```bash
[
  {
    "address": "0x2F3339fE44c184291a98Ff20dE8A303cfB96ae79",
    "voting_power": 10087
  },
  {
    "address": "0x1378f0691272781D18B3B277F185FAB2De0091Aa",
    "voting_power": 10002
  },

  ...

  {
    "address": "0xeda5be17ccA4aa99fca6326Fb8fFDDDe72d813eF",
    "voting_power": 50
  }
]
```

### List the set of registered validators

```bash
aut validator list
```
```bash
0x32F3493Ef14c28419a98Ff20dE8A033cf9e6aB97
0x31870f96212787D181B3B2771F58AF2BeD0019Aa
0x6EBb5A45728be7Cd9fE9c007aDD1e8b3DaFF6B3B
0xAC245aF88265E72881CD9D21eFb9DDC32E174B69
0x36288C1F8C990fd66A1C5040a61d6f3EcF3A49c1
0xb3A3808c698d82790Ac52a42C05E4BCb3dfCd3db
0x467D99EA9DACC495E6D1174b8f3Dd20DDd531335
0xba35a25badB802Cb3C0702e0e2df392e00511CA2
0x9fd408Bdb83Be1c8504Ff13eBcCe7f490DCCC2cF
0xE03D1DE3A2Fb5FEc85041655F218f18c9d4dac55
0x52b89AFA0D1dEe274bb5e4395eE102AaFbF372EA
0xFae912BAdB5e0Db5EC0116fe6552e8D6Bdb4e82b
0xE4Ece2266Ea7B7468aD3E381d08C962641b567f2
0xCD46183D0075116175c62dCDe568f2e0c4736597
0xeb25090AA0fD5c940F87A172Aaf62413Eb625b63
0x2AF517e6EdF3C01f8256E609122f004457024E67
0x9f793D2c7E1D5a72A020281F383bfc5e3086AcA9
0xde5aeb71cc4Aaa99cf6a23F68bFfDdDD7e8231Fe
```

### Check the auton balance of an account:

```bash
aut account balance <_addr>
```
```bash
9.00341
```

### Check the newton balance of an account:

```bash
aut account balance --ntn <_addr>
```
```bash
3.73401
```

{{% pageinfo %}}
Once your node has been properly set up, you can now [create](/howto/create-acct/) and [fund](/howto/fund-acct) and account on the network, and then [create and submit a transaction](/howto/submit-trans-autcli/).
{{% /pageinfo %}}

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
