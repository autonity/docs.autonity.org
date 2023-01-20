---
title: "Unlock an account"
linkTitle: "Unlock an account"
weight: 50
description: >
 How to unlock and re-lock an account for signing and sending transactions
draft: true
---

<!-- TODO: reinstate this content in the appropriate pages, in the
context of "how to sign a transaction using ..." -->

To unlock an account for signing transactions, Autonity currently allows users to:

- Sign without explicit account unlocking. Transactions can be signed without explicitly unlocking the account using tools that prompt the user for the keystore password and handle internally the account unlocking and re-locking (after the transaction is signed and sent). In this way, the complexity of the account unlocking is abstracted away from the user:

  - Sign by using `autcli`:
    - Uses `autcli` to sign and send, using an encrypted private key file configured in the CLI or passed in as a command-line option.
  - Sign by using `clef` with Autonity NodeJS Console.
    - Uses `clef` to sign. User creates transaction in Node JS Console, approves transaction signing in `clef`, and transaction is then sent from NodeJS Console.

- Sign by explicit account unlocking:
  - Sign by unlocking an account on an Autonity Go Client:
    - Uses the node to sign before sending.

  - Sign by importing the private key of an account using the JavaScript CLI Autonity NodeJS Console as a local wallet:
    - Uses the Node JS Console to sign before sending.

  {{% alert title="Note" %}}Both of these unlock approaches have pros and cons, which are outlined in following sections.{{% /alert %}}


## Sign using `autcli`

For how to sign and submit transactions with the Python CLI `autcli` see:

- [Create an account](/howto/create-acct/) for how to create a new account or import an existing account's private key into `autcli`.
- [Submit a transaction from Autonity autcli](/howto/submit-trans-autcli/) for how to configure the keystore and accounts in `.autrc` to sign transactions.

## Sign using `clef` signer with Autonity NodeJS Console

For how to use Clef to sign and submit transactions with the JavaScript CLI NodeJS Console see:

- [Managing keys and accounts](/howto/key-mgt/) and [Connect Clef secure wallet](/howto/key-mgt/clef).

## Sign by unlocking an account on a node

An Autonity node also contains a wallet, which is locked by default. Account(s) in the wallet can be unlocked by:
1. Calling the `personal.unlockAccount` function from the Autonity NodeJS Console.
2. Altering the default behaviour by specifying the address(es) need to be unlocked in the `--unlock` parameter of the autonity binary.

In this way, the user is able to interact with the wallet on the remote node using the `web3.personal` and `web3.eth` APIs. Unlocking the account in the remote node grants the advantage of not needing to specify gas when sending transactions, since the node is able to estimate how much it needs on its own.

Navigate to your Autonity NodeJS Console install directory and initialise a console session, specifying the IP address and port of the node you will connect to.
```bash
./console ws://<IP-ADDRESS>:8546
```

{{< alert title="Note" >}}If the transport is over WebSockets or WebSockets Secure will depend on your node setup. For connecting to a public node WebSockets Secure (`wss`) is advised.{{< /alert >}}

Once connected, you can check whether the wallet is unlocked with the command:
```javascript
web3.personal.listWallets()
```

If the wallet is locked, you can unlock it by calling:
```javascript
web3.personal.unlockAccount("0x2B0...","passphrase",5)
```
The first parameter is the address of the account you want to unlock, while the second parameter is the passphrase you choose at account creation. The last parameter is optional and represents the number of seconds your wallet will stay unlocked. Once the timer expires, your wallet will automatically lock. See https://geth.ethereum.org/docs/rpc/ns-personal#personal_unlockaccount for additional informations.

{{< alert title="Warning" color="warning" >}}The `unlockAccount` function will send your password in clear to the node. Make sure that your connection is properly secured (e.g. Using `wss` instead of `ws`). {{< /alert >}}

You can then send transactions without specifying gas:
```javascript
web3.eth.sendTransaction({from:address1,to:address2,value:5})
```

{{% alert title="Warning" color="warning" %}} Leaving an account unlocked on a node can pose a security threat, as it implies that whoever can access the node will be able to send transactions on your behalf.{{% /alert %}}

## Sign by unlocking an account in the Autonity NodeJS Console

An account can be unlocked in the JavaScript CLI NodeJS console by importing the private key locally into the console session.

To do this you will need to provide the following constants:

- The private key of the account you are using (to unlock the account in the JavaScript environment).
- The account address (your Ethereum formatted account address prefixed by `0x`).
- The amount of gas you will make available to spend on the transaction (i.e. the maximum number of gas units you are willing to provide for the transaction).

Connect to the node in the same way as the previous example:
```bash
./console ws://<IP-ADDRESS>:8546
```

Enter the following in the NodeJS Console, specifying, where:
- `<PRIVATE_KEY_PATH>` - path of the file containing the private key of the account submitting the transaction
- `<GAS>` - the maximum amount of gas units available for transaction computation (i.e. the gas limit being set for processing the transaction).

```javascript
const privatekey = fs.readFileSync('<PRIVATE_KEY_PATH>','utf-8');
const account = web3.eth.accounts.wallet.add(privatekey);
const myAddress = web3.utils.toChecksumAddress(account.address);
const gas = <GAS>;
```

{{% alert title="Warning" color="warning" %}}Always ensure that your private key is stored securely!{{% /alert %}}

You can now send a transaction using:
```javascript
web3.eth.sendTransaction({from:myAddress,to:myAddress,value:5,gas:gas})
```

{{% pageinfo %}}
The current block base fee can be obtained by querying the latest block header:
```javascript
web3.eth.getBlock(await web3.eth.getBlockNumber())
{
  baseFeePerGas: 5000,
...
}
```

If you need to decrypt the private key from an Ethereum keystore file, see the how to [Create an account, Decrypting the private key](/howto/create-acct/#decrypting-the-private-key).
{{% /pageinfo %}}
