---
title: "Submit a transaction from Autonity NodeJS Console"
linkTitle: "Submit a transaction from Autonity NodeJS Console"
weight: 60
description: >
  How to submit transactions to an Autonity network using the NodeJS interface to the RPC API's
draft: true
---

## Prerequisites

To submit transactions to a client node from the Autonity NodeJS Console you need:

- An [installed NodeJS Console](/reference/utility-tools/#installation-1).
- An [unlocked account](/account-holders/unlock-acct) on an Autonity network funded with auton to pay for transaction gas costs.
- Configuration details for the Autonity network you are deploying to, i.e. a public or your own node on a public [Autonity network](/networks/).

Navigate to your Autonity NodeJS Console install directory  and initialise a console session, specifying the IP address of the node you will connect to. The connection is made over WebSockets to port 8546:
```bash
./console ws://<IP-ADDRESS>:8546
```

{{% alert title="Note" %}}If the transport is over WebSockets or WebSockets Secure will depend on your node setup. For connecting to a public node WebSockets Secure (`wss`) is advised.{{% /alert %}}

## Examples

Here are some examples of using `web3` and `autonity` namespaces to transfer value between accounts and call Autonity Protocol Contract ERC20 functionality from the console. In the following examples we will specify the gas parameter, but it can be superfluous depending on how you [unlocked your account](/account-holders/unlock-acct).

{{% pageinfo %}}
The current block base fee can be obtained by querying the latest block header:
```javascript
web3.eth.getBlock(await web3.eth.getBlockNumber())
{
  baseFeePerGas: 5000,
...
}
```
{{% /pageinfo %}}

For parameter definitions and usage see the Reference [Autonity Interfaces](/reference/api/).

To see your addresses you can use the command:
```javascript
web3.eth.getAccounts()
```

### Transfer Auton:

Transferring Autonity's native account coin using the `web3.eth` namespace. Note `.send()` is not necessary:

```javascript
web3.eth.sendTransaction({to:myAddress, from:myAddress, value:100, gas: gas})
```

### Transfer Newton:

Transferring Autonity's native stake token using the `autonity` namespace. Note use of `.send()`:

```javascript
autonity.transfer('<_recipient>', <_amount>).send({from: myAddress, gas: gas})
```

### Approve another account to transfer your Newton stake tokens:

```javascript
autonity.approve('<spender>', <amount>).send({from: myAddress, gas: gas})
```

### Check approved account's allowance for transferring Newton stake tokens:

```javascript
autonity.allowance('<owner>','<spender>').call()
```

### Transfer Newton stake tokens as an approved account:

```javascript
autonity.transferFrom('<sender>', '<recipient>', <amount>).send({from: myAddress, gas: gas})
```
