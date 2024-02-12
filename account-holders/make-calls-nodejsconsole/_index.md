---
title: Make calls from Autonity NodeJS Console
description: How to submit calls to an Autonity network using the NodeJS interface to the RPC API's
draft: true
---


## Prerequisites

To submit calls to a client node from the Autonity NodeJS Console you need:

- An [installed NodeJS Console](/reference/utility-tools/#installation-1).
- Configuration details for the Autonity network you are connecting your console to, i.e. a public or your own node on an Autonity testnet.

## Setup

Navigate to your Autonity NodeJS Console install directory  and initialise a console session, specifying the IP address of the node you will connect to. The connection is made over WebSockets to port 8546:

 ```bash
 ./console ws://<IP-ADDRESS>:8546
 ```

::: {.callout-note title="Note" collapse="false"}If the transport is over WebSockets or WebSockets Secure will depend on your node setup. For connecting to a public node WebSockets Secure (`wss`) is advised.:::

## Examples

Here are some examples of making calls to the network using the Autonity Protocol Contract and Web3 namespaces.

For parameter definitions and usage see the Reference [Autonity Interfaces](/reference/api/).


### Get consensus committee size:

 ```javascript
 autonity.getMaxCommitteeSize().call()
 ```

### Get the genesis config:

To return the protocol parameterisation set at network genesis for:

- operatorAccount
- treasuryAccount
- treasuryFee
- minBaseFee
- delegationRate
- epochPeriod
- unbondingPeriod
- committeeSize
- contractVersion
- blockPeriod

 ```javascript
 autonity.config().call()
 ```

### Get the current consensus committee:

 ```javascript
 autonity.getCommittee().call()
 ```

### Check the auton balance of an account:

 ```javascript
 web3.eth.getBalance('<address>');
 ```

### Check the newton balance of an account:

 ```javascript
 autonity.balanceOf('<_addr>').call()
 ```
