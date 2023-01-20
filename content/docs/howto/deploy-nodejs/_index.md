---
title: "Deploy smart contracts to an Autonity network with NodeJS"
linkTitle: "Deploy smart contracts with NodeJS"
weight: 170
description: >
  How to deploy smart contracts to an Autonity network using NodeJS scripts, with an ERC20 token contract as an example
draft: true
---

Instead of using a deployment framework like Truffle, you can use NodeJS to write scripts to deploy precompiled contracts. This method is preferable if you want to deploy several contracts at once, or sequentially.

## Prerequisites

- An account on an Autonity network funded with auton to pay for transaction gas costs
- Configuration details for the Autonity network you are deploying to, i.e. a public or your own node on a public Autonity network
- To provide the following constants:
  - The private key of the account you are using (to unlock the account in the JavaScript environment)
  - Gas (the maximum amount of gas units you are willing to provide for the transaction).

## Setup

Create a new directory and initialise the project with npm:

```bash
mkdir ERC20token && cd ERC20token
npm init -y
```

Next install OpenZeppelin Contracts, and other required modules. OpenZeppelin is an open source library of smart contracts.

```bash
npm i --save-dev @openzeppelin/contracts
npm i web3
```

## Write the deploy script

Add the following script `deploy.js`, filling in the RPC node url, and the private key of the account you are using to make the transaction. The arguments used to deploy the ERC20 token are set within the `deployTokens` function.

```javascript
const Web3 = require("web3");
const ERC20 = require("./node_modules/@openzeppelin/contracts/build/contracts/ERC20PresetFixedSupply.json");

const RPC = "<NODE URL>";
const prvKey = "<PRIVATE KEY>";
const GasLimit = 8000000;

// deploy ERC20 contract
async function deployTokens(web3, sender) {
    try {
      let token = new web3.eth.Contract(ERC20.abi);

      token = await token
        .deploy({
          data: ERC20.bytecode,
          arguments: [
            "mytoken",
            "TKN",
            web3.utils.toWei("9999999999999999999", "ether"),
            sender,
          ],
        })
        .send({ from: sender, gas: GasLimit })
        .on("receipt", function (receipt) {
            console.log("receipt", receipt);
          });

      console.log("token address: ", token.options.address);

      return [token.options.address];
    } catch (error) {
      console.log("ERC20 deployment went wrong! Lets see what happened...");
      console.log(error);
    }
  }

async function main(){
    const web3 = new Web3(RPC);
    const wallet = web3.eth.accounts.wallet.add(prvKey);
    const myAddress = web3.utils.toChecksumAddress(wallet.address);

    await deployTokens(web3, myAddress);
}

main()
```

This script uses the prebuilt json file `ERC20PresetFixedSupply.json` of the smart contract, from the OpenZeppelin node module.

The main function in the script makes a `web3` object using the rpc address, then uses that to create a `web3` `wallet` object, which can be used to send transactions.

It then calls the `deployTokens` function, which constructs a `web3` `contract` object, then calls the `send` method of the `contract` object to deploy the smart contract to the blockchain.

## Deploy the contract

Deploy the smart contract by running the `deploy.js` script:

```bash
node deploy.js
```

You should get an output resembling the following:

```bash
receipt {
  blockHash: '0x8a655a7153585ad0bbeb58a47c6a71f3767c284d4b218fa8d17be7cacc1e5e7c',
  blockNumber: 781449,
  contractAddress: '0x49762b3dbe63B96a1DE6b7f595d19e356D311B49',
  cumulativeGasUsed: 756665,
  effectiveGasPrice: 2500005000,
  from: '0x769b2b36e851e6c94384fdb20345677cd99583cd',
  gasUsed: 756665,
  logsBloom: '0x00000000420000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000002000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000020200000000000000000800000000000000000000000010000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: null,
  transactionHash: '0x49fc749e3bc10c8844b3ea0a8aeaa0ee68c54d57ed1b70b9e5553d3c89812b21',
  transactionIndex: 0,
  type: '0x2',
  events: {
    Transfer: {
      address: '0x49762b3dbe63B96a1DE6b7f595d19e356D311B49',
      blockNumber: 781449,
      transactionHash: '0x49fc749e3bc10c8844b3ea0a8aeaa0ee68c54d57ed1b70b9e5553d3c89812b21',
      transactionIndex: 0,
      blockHash: '0x8a655a7153585ad0bbeb58a47c6a71f3767c284d4b218fa8d17be7cacc1e5e7c',
      logIndex: 0,
      removed: false,
      id: 'log_eea8599f',
      returnValues: [Result],
      event: 'Transfer',
      signature: '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
      raw: [Object]
    }
  }
}
token address:  0x49762b3dbe63B96a1DE6b7f595d19e356D311B49
```
