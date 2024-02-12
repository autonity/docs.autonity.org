---
title: Connect Smartcard hardware wallet
description: How to setup and use go-ethereum supported hardware wallets with an Autonity Go Client node, using the NodeJS Console
draft: true
---

## Prerequisites

- physical access to a running local instance of an Autonity Go Client [connected to an Autonity network](/node-operators/run-aut/)
- a running instance of the Autonity NodeJS Console attached to your node, configured for your account as described in Submit a transaction from Autonity NodeJS Console
- a running Linux [pcsc daemon](https://linux.die.net/man/8/pcscd) service (if you need to install `sudo apt install pcscd`)
- a Status Keycard hardware wallet
- an ISO 7816 compliant USB smart card reader

- installed applications for the Smartcard hardware wallet:
	 - [keycard-cli](https://github.com/status-im/keycard-cli) command-line tool. For how to install see the GitHub repository's [Installation](https://github.com/status-im/keycard-cli#installation) section. For how to use shell scripts with it, see keycard.tech posts:
	     - [Upgrading & Updating your Keycard - How and Why?](https://news.keycard.tech/upgrading-updating-your-keycard-how-why/)
	     - [Using the Keycard CLI & Shell Software](https://news.keycard.tech/using-the-keycard-cli-shell/)
	 - (Optional) Status Desktop app. Refer to the Download page [https://status.im/get/](https://status.im/get/) and linked [Desktop Beta Installation](https://status.im/user_guides/desktop_beta_install.html) guide.
	 - (Optional) Status for Mobile app. Refer to the Download page [https://status.im/get/](https://status.im/get/).
	 - .
	 - Status Keycard app. Refer to the status [Get Status](https://status.im/get/) page to download and the discussion [Get your node running](https://discuss.status.im/t/get-your-node-running/1488) linked from the status FAQ [Can I run go-ethereum myself or on a server?](https://status.im/faq/).


## Overview

This how to describes the workflow for connecting Trezor, Ledger Nano S, and Status Keycard hardware wallets to an Autonity Go Client, signing and sending transactions with the NodeJS Console.

Autonity maintains go-ethereum's out-the-box support for external hardware secure wallets. Before connecting a USB external hardware wallet to a Linux machine you will need to configure the Linux Udev subsystem with device-specific rules for the external drive to be recognised. For how to setup `udev` rules see prerequisites above.


## Setup Status keycard

Initialise and setup the Status Keycard ready for use with the Autonity client.

1. Verify the `pcsc` daemon is running:

	```bash
	`/etc/init.d/pcscd status
	```
	If stopped run `/etc/init.d/pcscd start`

2. Plug the USB card reader into the host machine and insert the keycard.

3. Verify the keycard-cli binary is connected to the smart card. Navigate to the working directory where you have installed the keycard CLI and run:

	```bash
	./keycard info -l debug
	```
	The `INFO` messages should report card found and connected to.

	{{% alert title="Tip" %}}If you get a bash permission denied error, then this indicates you do not have execution privileges for the keycard binary. Login as sudo and run `chmod u+x keycard` to grant execution privilege over the binary. If you run `ls -la` in your installation directory `keycard` should show your `/usr/` has `rwx` and not just `rw` permissions.{{% /alert %}}

	Follow the instructions in the [keycard-cli](https://github.com/status-im/keycard-cli/) repository's README [Usage](https://github.com/status-im/keycard-cli#usage) section to:

	- install the keycard application (applet) on the keycard if necessary - the keycard should come with the applet already installed.
	- list wallets - the keycard will show as pending initiaisation:

	```bash
	web3.personal.listWallets()
	[ { url: 'keycard://c2f98801',
    	status: 'Empty, waiting for initialization' } ]
	```

	- initialise the wallet. This will initialise the smartcard wallet ready for use and print to console the credentials you need to open the wallet and pair with the card: PIN, PUK, pairing phrase. On initialisation you should see something like this:


	```bash
	./keycard init
	INFO [03-30|14:36:11.257] waiting for a card                       	package=status-go/cmd/keycard
	INFO [03-30|14:36:11.257] card found                               	package=status-go/cmd/keycard index=0
	INFO [03-30|14:36:11.319] initialization started                   	package=status-go/cmd/keycard
	INFO [03-30|14:36:11.390] select keycard applet                    	package=status-go/cmd/keycard
	INFO [03-30|14:36:11.423] initializing                             	package=status-go/cmd/keycard
	PIN 012345
	PUK 012345678901
	Pairing password: a1z2AbCdefGhijKL
	```
	Remember the PIN, PUK, pairing password for future use. Without them you will not be able to access the wallet or accounts within it.

## Use Status Keycard wallet with the Autonity client

1. Start the `pcscd` service if not already running.

2. Plug USB card reader into the host machine and insert Status Keycard.

3. Start the Autonity client and connect to your chosen Autonity network. Connect NodeJS Console to the node

4. Get the URL of the smartcard wallet by calling from NodeJS Console:

   ```bash
   web3.personal.listWallets()
   ```
   The result will look something like this:

   ```bash
   [ { url: 'keycard://c2f98801',
    status: 'Unpaired, waiting for pairing password' } ]
   ```

5. Open the wallet and pair the keycard with your Autonity client, using your keycard initialisation details:

	- <PAIRING_PWD> - the pairing password returned from keycard initialisation
	- <PIN> is the PIN number returned from keycard initialisation
	- <URL> is the keycard URL

	```
	web3.personal.openWallet("<URL>","<PAIRING_PWD>")	web3.personal.openWallet("<URL>","<PIN>")
	```

	To view status, run listWallets again. The wallet will show as online:

	```bash
	web3.personal.listWallets()
	[ { url: 'keycard://c2f98801',
    	status: 'Empty, waiting for initialization' } ]
	```

6. Add an account to the wallet. This will generate an account and return a seed string of 24 words:

	```
	web3.personal.initializeWallet("<URL>")
	```

	You should see something like:

	```bash
	web3.personal.initializeWallet("keycard://c2f98801")
	'seed ... ... words'
	```

	Note your seed phrase for account recovery and keep it in a safe place. Your wallet is now initialised with an account.

	Run list wallet again - the keycard should show as online:

	```bash
	const listWallets = web3.personal.listWallets()
	undefined
	console.log(JSON.stringify(listWallets,null,3)) ;
	[
		{
			"url": "keycard://c2f98801",
			"status": "Online",
			"accounts": [
			{
			"address": "0x144e0d78d2e83ff083d4182a40bf9435a5a7c6a2",
			"url": "keycard://c1g7/m/44'/60'/0'/0/0"
			}
		]
       }
    ]
    ```


EDIT

8. Verify the wallet account is functioning. Send a test transaction:

   ```bash
   web3.eth.sendTransaction({from: <ADDRESS>, to: <ADDRESS>})
   ```
   You will be prompted by keycard-cli to confirm the transaction.

To transfer value, you will need to specify transaction fee values, configuring the NodeJS Console with a `gas` constant as described in the How to Submit a transaction from Autonity NodeJS Console. For example, to transfer an amount of _newton_ stake token to another address by calling the Autonity Protocol Contract using Trezor:

```bash
const gas = 10000000;
autonity.transfer('<TO_ADDRESS>', <AMOUNT>).send({from: myAddress, gas: gas})
```

You will be prompted on the wallet to confirm the transaction.
