---
title: Connect Clef secure wallet
description: 
  How to setup and use the Clef wallet with an Autonity Go Client node using the NodeJS Console
---

## Prerequisites

- An installation of Autonity built with `make all` as described in the How to [Install Autonity](howto/install-aut/#build-from-source-code).
- A funded account on the network with the keystore file save to the keystore directory that Clef will be specified in Clef's configuration. (See [Use Clef with the Autonity client](/account-holders/key-mgt//clef/#use-clef-with-the-autonity-client) beneath.
- an [installed NodeJS Console](/node-operators/install-aut/) configured as described in the [Submit a transaction using NodeJS Console](/account-holders/submit-trans-nodejsconsole/)


## Overview

Clef is the replacement for Go Ethereum's account management functionality, but it is not a Geth module. Rather, it is a standalone daemon that works with any Ethereum client. It is a framework to unify all existing methods of signing transactions through a pluggable architecture. It works by exposing an API to local clients via IPC or HTTP. Clef currently supports keyfile-format accounts as well as hardware wallets.

This how to describes setting up Clef and using it with Autonity for account management and signing transactions.

::: {.callout-note title="Further Information" collapse="false"}
For tutorials and in-depth information on clef we recommend referring to the Go Ethereum Clef docs at https://geth.ethereum.org/docs/clef/introduction.
:::

## Setup Clef

The following are the steps to successfully demonstrate clef working with Autonity:

1. Navigate to the working directory for your Autonity installation. Initialise the clef utility:

   ```bash
   ./autonity/build/bin/clef init
   ```
   Clef will initialise and print to the console, prompting you to enter OK:

   ```bash
   WARNING!

	Clef is an account management tool. It may, like any software, contain bugs.

	Please take care to
	- backup your keystore files,
	- verify that the keystore(s) can be opened with your password.

	Clef is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
	without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
	PURPOSE. See the GNU General Public License for more details.

	Enter 'ok' to proceed:
	>
   ```

   Enter 'ok' and enter a password when prompted for the `masterseed.json` file:

	```bash
	The master seed of clef will be locked with a password.
	Please specify a password. Do not forget this password!
	Password:
	Repeat password:

	A master seed has been generated into /home/alice/.clef/masterseed.json

	This is required to be able to store credentials, such as:
	* Passwords for keystores (used by rule engine)
	* Storage for JavaScript auto-signing rules
	* Hash of JavaScript rule-file

	You should treat 'masterseed.json' with utmost secrecy and make a backup of it!
	* The password is necessary but not enough, you need to back up the master seed too!
	* The master seed does not contain your accounts, those need to be backed up separately!
   ```

   Clef is now setup and ready to use.

::: {.callout-note title="Note" collapse="false"}
The password that you are setting here is not the password for your keystore. It is the password for the clef masterseed, which is used for a variety of functions, including storing keystores passwords. It is strongly suggested to choose a strong password, different from the keystore one.
:::


## Use Clef with the Autonity client

1. Start the Clef binary, specifying:

	- (optional) the `<PATH>` to the keystore directory holding the accounts you will use. If not specified, the default location will be used as described in the how to [Create an account using Clef](/account-holders/create-acct/#create-account-using-clef)
	- the `<CHAINID>` for the Autonity network to which your Autonity Go Client node is connected:



   ```bash
   ./clef --keystore ~/.autonity/keystore --chainid 65010000
   ```

	You will be prompted to enter 'ok' and then your masterseed password. Clef will initialise and print its status to the console:

   ```bash
	-----------------------
	INFO [03-25|15:14:40.579] Starting signer                          	chainid=444,800 keystore=/home/alice/.autonity/keystore light-kdf=false 	advanced=false
	DEBUG[03-25|15:14:40.579] FS scan times                            	list="83.278µs" set="11.424µs" diff="4.714µs"
	DEBUG[03-25|15:14:40.580] Ledger support enabled
	DEBUG[03-25|15:14:40.580] Trezor support enabled via HID
	DEBUG[03-25|15:14:40.580] Trezor support enabled via WebUSB
	INFO [03-25|15:14:40.580] Smartcard socket file missing, disabling err="stat /run/pcscd/pcscd.comm: no such file or directory"
	INFO [03-25|15:14:40.580] Audit logs configured                    	file=audit.log
	DEBUG[03-25|15:14:40.580] IPCs registered                          	namespaces=account
	INFO [03-25|15:14:40.580] IPC endpoint opened                      url=/	home/alice/.clef/clef.ipc
	------- Signer info -------
	* intapi_version : 7.0.1
	* extapi_version : 6.1.0
	* extapi_http : n/a
	* extapi_ipc : /home/alice/.clef/clef.ipc
	DEBUG[03-25|15:14:47.597] Served account_version                   reqid=1 	duration="147.624µs"
	DEBUG[03-25|15:14:47.599] RPC connection read error                err=EOF
	DEBUG[03-25|15:36:54.364] Served account_version                   reqid=1 	duration="97.296µs"
   ```

   Make a note of the `extapi_ipc` url in the 'Signer info' section. This is the endpoint the Autonity client will connect to. In the example above this is `/home/alice/.clef/clef.ipc`.

2. Run the Autonity client binary with the addition of the `--signer`flag, specifying as the `<PATH>` the `extapi_ipc` value from the preceding step:

   ```bash
   --signer=<PATH>/.clef/clef.ipc
   ```


##  Submit transactions using NodeJS Console
::: {.callout-note title="Note" collapse="false"}
Since you are using clef to sign transactions, whenever you issue a command on the NodeJS console which requires a signature from your private key, the nodejs console will hang. This is because it is waiting for the signature from clef, that you need to manually approve. This process can be automated using the clef rule engine https://geth.ethereum.org/docs/clef/tutorial#automatic-rules
:::

1. Start the Autonity NodeJS Console and then, to view the accounts in Clef, enter as follows:

   ```javascript
   const wallet = await web3.personal.listWallets()
   const address = web3.utils.toChecksumAddress(wallet[0].accounts[0].address)
   address
   ```

	This will retrieve the first address in the configured keystore directory. If there is more than one account in the wallet, edit the list index position from which you will retrieve the account in `accounts[0]`. For example, change to `accounts[2]` to return the third address listed in the wallet.

	Clef will prompt to approve the request. Enter 'y'. The NodeJS Console will return something like this:

   ```bash
   > address
   '0xcC50C345B34a80c6bDc51Be4dd79dC73ee81190e'
   ```

4. Send a transaction with your chosen account in the Autonity NodeJS Console.

	Note that gas costs are automatically calculated by the Autonity client if the gas-related parameters are not included in the method arguments passed to the called RPC method.

	To verify Clef signing is functioning correctly, send an empty transaction using `eth.sendTransaction`, specifying 'from' and 'to' account addresses:

   ```bash
   web3.eth.sendTransaction({from: address, to: address})
   ```

   	For example:

   ```bash
   > web3.eth.sendTransaction({from: '0xcC50C345B34a80c6bDc51Be4dd79dC73ee81190e',to: '0xbC50C347A44a80c6bDc51Be4dd79eC73ee89290f'})
   ```

   Clef will print the transaction request to the console and prompt you to approve the request. For example:

   ```bash
	-----------------------
	WARN [03-25|17:21:42.172] Served account_signTransaction           reqid=6 	duration=4.372186471s    err="request denied"
	--------- Transaction request-------------
	to:    0xbC50C347A44a80c6bDc51Be4dd79eC73ee89290f
	from:               0xcC50C345B34a80c6bDc51Be4dd79dC73ee81190e [chksum ok]
	value:              0 wei
	gas:                0x5208 (21000)
	maxFeePerGas:          2500010000 wei
	maxPriorityFeePerGas:  2500000000 wei
	nonce:    0x1 (1)
	chainid:  0x6c980
	Accesslist

   Request context:
		NA -> ipc -> NA

   Additional HTTP header data, provided by the external caller:
		User-Agent: ""
		Origin: ""
	-------------------------------------------
	Approve? [y/N]:
   ```

   Enter 'y' and when prompted enter the password for the account:

	```bash
   > y
   WARN [03-25|17:22:08.510] Key does not exist                          key= 0xcC50C345B34a80c6bDc51Be4dd79dC73ee81190e
   ## Account password

   Please enter the password for account 0xcC50C345B34a80c6bDc51Be4dd79dC73ee81190e
   >
   ```

	The transaction will then send. Clef prints details of the transaction signed to console:

	```bash
	-----------------------
	Transaction signed:
 	{
 	   "type": "0x2",
    	"nonce": "0x1",
    	"gasPrice": null,
    	"maxPriorityFeePerGas": "0x9502f900",
   	 	"maxFeePerGas": "0x95032010",
   	 	"gas": "0x5208",
   	 	"value": "0x0",
   	 	"input": "0x",
   	 	"v": "0x0",
    	"r": "0x78b3940aa2aaef9b86845bce56aeb6fde141e3b161b3e7b98f884df3d2424cfb",
    	"s": "0x2b410bf9164e6cfcf77784ba65d9eec578e881be971b120e7cf005ca09414b71",
    	"to": "0xbc50c347a44a80c6bdc51be4dd79ec73ee89290d",
    	"chainId": "0x6c980",
    	"accessList": [],
    	"hash": "0x892bbed9991f03d89afa65a4170c8dc9703b76a905407f4b281d1939a747a3c1"
  	}
	DEBUG[03-25|17:22:34.304] Served account_signTransaction           reqid=7 	duration=47.892717474s
   ```

   In the NodeJS Console, on completion of the `sendTransaction`, the method returns and the blockhash is returned:


	```bash
	> web3.eth.sendTransaction({from: '0xcC50C345B34a80c6bDc51Be4dd79dC73ee81190e',to: '0xbC50C347A44a80c6bDc51Be4dd79eC73ee89290f'})
	{ blockHash:
   	'0x6bc8c3eb68834207a8b0516d599c4d0d85cebcbd3e6399ee9bd98e5f996e924e',
  	blockNumber: 6339,
  	contractAddress: null,
  	cumulativeGasUsed: 21000,
  	effectiveGasPrice: 2500005000,
  	from: '0xcC50C345B34a80c6bDc51Be4dd79dC73ee81190e',
  	gasUsed: 21000,
  	logs: [],
  	logsBloom:
   	'0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  	status: true,
  	to: '0xbC50C347A44a80c6bDc51Be4dd79eC73ee89290f',
  	transactionHash:
   	'0x892bbed9991f03d89afa65a4170c8dc9703b76a905407f4b281d1939a747a3c1',
  	transactionIndex: 0,
  	type: '0x2' }
	>
   ```

## Examples

Here are some examples of calling Autonity Protocol Contract ERC20 functionality from the console using Clef to sign.

For parameter definitions and usage see the Reference [Autonity Interfaces](/reference/api/).


### Transfer Auton between accounts using eth `web3.eth.sendTransaction`:

```bash
web3.eth.sendTransaction({from: "<address>",to: "<address>", value: <AMOUNT>})
```


### Transfer Newton stake token to another account using `autonity.transfer`:

```bash
autonity.transfer('<_recipient>', <_amount>).send({from: myAddress, gas: gas})
```
