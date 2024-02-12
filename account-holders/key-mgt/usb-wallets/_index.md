---
title: Connect hardware wallet
description: How to setup and use go-ethereum supported hardware wallets with an Autonity Go Client node, using the NodeJS Console
---

## Prerequisites

- physical access to a running local instance of an Autonity Go Client [connected to an Autonity network](/node-operators/run-aut/)
- a running instance of the Autonity NodeJS Console attached to your node, configured for your account as described in Submit a transaction from Autonity NodeJS Console
- one of the supported hardware wallets holding your account keys:
  - USB wallets: Ledger, Trezor
- `udev` rules for the chosen hardware wallet have been configured on the host Linux machine if a USB wallet:
  - Ledger. Refer to *Solution 1. Set up udev rules* in the Ledger support article [Fix USB connection issues with Ledger Live](https://support.ledger.com/hc/en-us/articles/115005165269-Fix-connection-issues?support=true) run:
  - Trezor. Refer to the Trezor Wiki article set up [Udev rules](https://wiki.trezor.io/Udev_rules).
- installed app for the chosen hardware wallet:
 - Trezor Suite app. Refer to the Trezor Wiki article [Apps: Trezor Suite](https://wiki.trezor.io/Apps:Trezor_Suite)
 - Ledger Live app. Refer to the Ledger support article [Download and install Ledger Live](https://support.ledger.com/hc/en-us/articles/4404389606417-Download-and-install-Ledger-Live?docs=true)


## Overview
This how to describes the workflow for connecting Trezor and Ledger Nano S hardware wallets to an Autonity Go Client, signing and sending transactions with the NodeJS Console.

Autonity maintains go-ethereum's out-the-box support for external hardware secure wallets. Before connecting a USB external hardware wallet to a Linux machine you will need to configure the Linux Udev subsystem with device-specific rules for the external drive to be recognised. For how to setup `udev` rules see prerequisites above.


## Use Trezor wallet with the Autonity client

1. Start the Autonity client and connect to your chosen Autonity network. Connect NodeJS Console to the node

2. Plug Trezor wallet into the host machine and unlock using Trezor Suite app

3. Get the URL of the Trezor wallet by calling from NodeJS Console:

   ```bash
   web3.personal.listWallets()
   ```
   The result will look something like this:

   ```bash
   [
     {
       url: 'trezor://1209:53c1:03',
       status: 'Closed',
    failure: 'failed to write to device: libusb: i/o error [code -1]'
     }
   ]
   ```

4. Open the Trezor wallet using the PIN code  set with Trezor:

   ```bash
   web3.personal.openWallet('trezor://1209:53c1:03', '<TREZOR_PINCODE>')
   ```

5. Get the address of the Trezor wallet account:

   ```bash
   const wallet = await web3.personal.listWallets()
   const address = web3.utils.toChecksumAddress(wallet[0].accounts[0].address)
   address
   ```

6. Verify the wallet account is functioning. Send a test transaction using Trezor:

   ```bash
   web3.eth.sendTransaction({from: <ADDRESS>, to: <ADDRESS>})
   ```
   You will be prompted on the Trezor hardware wallet to confirm the transaction.

To transfer value, you will need to specify transaction fee values, configuring the NodeJS Console with `gas` constants as described in the How to Submit a transaction from Autonity NodeJS Console. For example, to transfer an amount of _newton_ stake token to another address by calling the Autonity Protocol Contract using Trezor:

```bash
const gas = 10000000;
autonity.transfer('<TO_ADDRESS>', <AMOUNT>).send({from: myAddress, gas: gas})
```

You will be prompted on the Trezor wallet to confirm the transaction.


## Use Ledger wallet with the Autonity client

1. Start the Autonity client and connect to your chosen Autonity network. Connect NodeJS Console to the node

2. Plug Ledger Nano S wallet into the host machine, unlock using Ledger Live app, and open the Ethereum application on the Ledger

3. Get the address of the Ledger wallet account:

   ```bash
   const wallet = web3.personal.listWallets()
   const address = web3.utils.toChecksumAddress(wallet[0].accounts[0].address)
   address
   ```

4. Verify the wallet account is functioning. Send a transaction using the Ledger Nano S:

   ```bash
   web3.eth.sendTransaction({from: <ADDRESS>, to: <ADDRESS>})
   ```
   You will be prompted on the Ledger hardware wallet to confirm the transaction


To transfer value, you will need to:

- enable blind signing in the settings of the Ethereum application on the Ledger
- specify transaction fee values, configuring the NodeJS Console with a `gas` constant as described in the How to Submit a transaction from Autonity NodeJS Console.

For example, to transfer an amount of _newton_ stake token to another address:

   ```bash
   const gas = 10000000;
   autonity.transfer('<TO_ADDRESS>', <AMOUNT>).send({from: address, gas: gas})
   ```
You will be prompted on the Ledger wallet to confirm the transaction.
