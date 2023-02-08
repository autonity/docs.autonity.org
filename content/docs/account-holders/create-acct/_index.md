---
title: "Create an account"
linkTitle: "Create an account"
weight: 35
description: >
  How to create and import accounts using autcli
---

## Overview

This how to covers the import and generation of new accounts using the `autcli` tool. Accounts are created as Ethereum keystore files using the [Web3 Secret Storage Definition](https://ethereum.org/en/developers/docs/data-structures-and-encoding/web3-secret-storage/), an encrypted file format that provides secure storage for an account's private key.

{{< alert title="Warning" color="warning" >}}
The use of hardware wallets or other key-management tools may be more secure than encrypted files.  Operators may choose to make use of such tools with Autonity, and explicit support for these will be added in the future.  For the purposes of the testnets this guide will assume the use of password-protected  keyfiles.

Ensure that your `keystore` file is stored securely according to your security policy at all times and remember the password phrase you used to create it! If you do not remember the password, you will not be able to decrypt this private key file and may lose any funds associated with this account.
{{< /alert >}}

## Create account using `autcli`

The following command will generate a keyfile with a default generated name, in the keystore (which can be specified with the `--keyfile` flag, or by adding a `keyfile = <path>` entry to the [`.autrc` file](/account-holders/setup-autcli/#configure)).

```bash
aut account new
```
```bash
Password for new account:
Confirm account password:
0x905824A6924F1564348Dac9709b3113AFb7c8C77  ~/.autonity/keystore/UTC--2023-01-20T09-45-05.360588000Z--905824a6924f1564348dac9709b3113afb7c8c77
```

A custom keyfile can be specified using the `--keyfile` flag:
```bash
mkdir keystore
aut account new --key-file ./keystore/alice.key
```
```bash
Password for new account:
Confirm account password:
0x0592486A2491F653484Dac709b91331AF7Cb7c87  keystore/alice.key
```

{{< alert title="Note" >}}To see all options available for account creation, run `aut account new --help`.  See also `aut account list` for working with key-stores.{{< /alert >}}

<!--
## Create account using client binary

To generate a new account using client command line tools, navigate to your Autonity installation `build/bin/`and run the binary with this command. To specify a custom keystore directory include the `--keystore` flag and the `<PATH>` to the directory where you will store the keystore file:

```bash
./autonity account new  --keystore <PATH>
```

This will prompt you to create a new private key file, encrypted using a password. Once complete, the account address will be output in the terminal and the keystore file will be created in the keystore folder with a filename containing a UTC timestamp and your account address minus the `0x` prefix. For example: `UTC--2021-08-14T12-44-47.270599667Z--ab0df1907bb5372c165067fe9230b7da6c1929be`.

The new account keystore file will by default be saved to the `keystore` folder `~/.autonity/keystore`, the client's default data directory location for databases and keystore. A custom directory can be specified using the `--keystore` flag.

{{< alert title="Tip" >}}The keystore password could be passed into the run command as a parameter using the `--password` flag. For example, as raw text or by providing the path to a file containing it. If the `--keystore` path flag is not set, then by default Autonity saves the key to the host machine's home directory (`$HOME`) in `/home/<YOUR_USERNAME>/.autonity/keystore/`.{{< /alert >}}

Run the `list` command to view the account address and keystore location. You will see something like this:

```bash
./autonity  account list

...

Account #0: {ab0df1907bb5372c165067fe9230b7da6c1929be} keystore:///home/alice/.autonity/keystore/UTC--2022-03-24T14-52-07.640133599Z--ab0df1907bb5372c165067fe9230b7da6c1929be
```
The file contents should contain something similar to:

```javascript
 {
	"address":"ab0df1907bb5372c165067fe9230b7da6c1929be",
	"crypto":{
		"cipher":"aes-128-ctr",
		"ciphertext":"084e0f4052a14df5845e5be9904e1197a165a9281eefb0fbebfbbd8f3ef8ff95",
		"cipherparams":{
			"iv":"30ea9f7599bfb8dac19165431d46b35d"
		},
		"kdf":"scrypt",
		"kdfparams":{
			"dklen":32,
			"n":262144,
			"p":1,
			"r":8,
			"salt":"efd3513b8a4bac40324acb9140c817e749555db44a278972460638643fd129f9"
		},
		"mac":"ec3e1a57524d8178a0475c9a0c9a0bb022d5ed8e0dd8c203e2d3f47fcf1270bc"
	},
	"id":"6aa93734-aafd-4ce2-8b7c-4b63c4320cf5",
	"version":3
 }
```

{{< alert title="Note" >}}The address displayed and in the keystore file is not prepended with the string `0x` - the `0x` is formatting but should always be prefixed so the address is a 42 hex string character length 160-bit (20 characters) code per the Yellow Paper (For more information on the 160-bit address identifier of an account, see the Ethereum Yellow Paper, [Appendix F. Signing Transactions](https://ethereum.github.io/yellowpaper/paper.pdf).{{< /alert >}}

## Create account using Clef

{{< alert title="Note" >}}
- An installed instance of the Autonity and the Clef account management tool binaries. See the how to [Install Autonity in your environment, Build from source code](/node-operators/install-aut/#build-from-source-code).
{{< /alert >}}

To generate a new account using the Clef account management utility, navigate to your Autonity installation `build/bin/` directory and run the Clef binary with this command. To specify a custom keystore directory include the `--keystore` flag and a `<PATH>` to the directory where you will store the keystore file:

```bash
./clef newaccount --keystore <PATH>
```

This will display the following message and then prompt to input 'ok':

```bash
  WARNING!

  Clef is an account management tool. It may, like any software, contain bugs.

  Please take care to
   - backup your keystore files,
   - verify that the keystore(s) can be opened with your password.

  Clef is distributed in the hope that it will be useful, but WITHOUT  ANY WARRANTY;
  without even the implied warranty of MERCHANTABILITY or FITNESS FOR  A PARTICULAR
  PURPOSE. See the GNU General Public License for more details.

 Enter 'ok' to proceed:
 >
```

Enter 'ok' and when prompted a password. Note that unlike the client which will allow skipping the password, Clef requires a password of at least 10 characters. Clef confirms account creation and prints the account address and keystore location to the console. You will see something like this:

```bash
 INFO [03-24|15:15:31.071] Starting clef                             keystore=/home/alice/.autonity/keystore light-kdf=false
 DEBUG[03-24|15:15:31.071] FS scan times                             list="189.4µs" set="40.048µs" diff="17.622µs"
 ## New account password

 Please enter a password for the new account to be created (attempt  0 of 3)
 >
 -----------------------
 DEBUG[03-24|15:15:36.750] FS scan times                             list="136.544µs" set="21.668µs" diff="4.191µs"
 INFO [03-24|15:15:36.806] Your new key was generated                address=0x2B913CB7B4AF0B5495345C9095eB0B412Ba97436
 WARN [03-24|15:15:36.806] Please backup your key file!              path=/home/alice/.autonity/keystore/UTC--2022-03-24T15-15-35.670132132Z--2b913cb7b4af0b5495345c9095eb0b412ba97436
 WARN [03-24|15:15:36.806] Please remember your password!
 Generated account 0x2B913CB7B4AF0B5495345C9095eB0B412Ba97436
```
-->

## Import account using `autcli`

An account can be created from an existing private key using the `autcli` command line tool:

1. Create a plain text file that contains the private key in hexadecimal format.  For example, copy your private key into a file named `alice.priv`


2. Import the key using the `import-private-key` command:

   ```bash
   aut account import-private-key ./alice.priv
   ```
   ```bash
   Password for new account:
   Confirm account password:
   0xd4EdDdE5D1D0d7129a7f9C35Ec55254f43b8E6d4  ~/.autonity/keystore/UTC--2023-01-20T09-45-05.360588000Z--d4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4
   ```

The `--keyfile` and `--keystore` flags can be used as with `aut account new` to control the location of the resulting keyfile.

<!--

## Import account using client binary

An account can be created from an existing private key using client command line tools. Navigate to your Autonity installation `build/bin/`and:

1. Create a plain text file that contains the private key you are using for the Autonity account. For example, copy your private key into a file named `alice.key`


2. Run the client binary to import the key and generate an account. Autonity will prompt for a password to be entered. To specify a custom keystore directory include the `--keystore` flag and the `<PATH>` to the directory where you will store the keystore file:

 ```bash
 autonity account import ./alice.key --keystore <PATH>
 ```

 As described in [Create account using client binary](/account-holders/create-acct/#create-account-using-client-binary) above, you will be prompted for a password and the keystore file containing your encrypted private key will be generated in the keystore directory.


## Decrypting the private key

There are many methods for decrypting the private key from an Ethereum keystore file. A simple way to decrypt if you need to is by using the web3 python package - see [Extract private key from geth keyfile](https://web3py.readthedocs.io/en/stable/web3.eth.account.html#extract-private-key-from-geth-keyfile) and a helper library function to convert the extracted key from bytes to a hex string. For example, `Web3.toHex` [Encoding and Decoding Helper](https://web3py.readthedocs.io/en/stable/web3.main.html?highlight=tohex#encoding-and-decoding-helpers), slicing the string result to remove the hex prefix `0x`.

-->

------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
