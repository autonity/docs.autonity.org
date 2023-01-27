---
title: "Deploy smart contracts to an Autonity network with node.js"
linkTitle: "Deploy smart contracts with node.js"
weight: 170
description: >
  How to deploy smart contracts to an Autonity network using `node.js` and JavaScript, with an ERC20 token contract as an example
draft: false
---

This guide uses node.js and JavaScript to deploy precompiled ERC20 token contracts using the OpenZeppelin open source library of smart contracts.

This method will allow you to deploy several contracts at once or sequentially.

## Prerequisites

- An up-to-date installation of [node.js](https://nodejs.org/en/download/) and `npm`. A guide [Downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) is on npm Docs.

- An [account](/account-holders//create-acct/) that has been [funded](/account-holders/fund-acct/) with auton, to pay for transaction gas costs. You will need the  private key of the account to unlock the account in the JavaScript environment.

- Configuration details for the Autonity network you are deploying to: a [public Autonity network](/networks/) or a [custom network](/developer/custom-networks/) if you are deploying to a local testnet.

## Setup your working environment

1. Create a working directory and initialise the project with `npm`:

```bash
mkdir ERC20token && cd ERC20token
npm init -y
```

2. Install OpenZeppelin Contracts and `web3` modules:

```bash
npm i --save-dev @openzeppelin/contracts
npm i web3
```

The `web3` module is used to add a private key. OpenZeppelin is an open source library of smart contracts.

## Write the deploy script

3. Add the following script `deploy.js` to your working directory, where:
	- `<NODE_URL>` is the rpc endpoint of the node you are connecting to.
	- `<PRIVATE_KEY>` is the private key of the account you are using to submit the transaction.
	- `<TOKEN_NAME>` is the text label name for your token.
	- `<TOKEN_SYMBOL>` is the text symbol acronym for your token.
	
	{{< alert title="Warning" color="warning" >}}
Including the private key as clear text is done in this example only because this is a testnet setting without real value. Putting a private key in the clear text is **not** recommended.
{{< /alert >}}

	```javascript
	const Web3 = require("web3");
	const ERC20 = require("./node_modules/	@openzeppelin/contracts/build/contracts/	ERC20PresetFixedSupply.json");
	
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
           	 "<TOKEN_NAME>",
            	"<TOKEN_SYMBOL>",
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
    	const wallet = 	web3.eth.accounts.wallet.add(prvKey);
    	const myAddress = web3.utils.toChecksumAddress(wallet.address);
		
    	await deployTokens(web3, myAddress);
	}
	
	main()
	```
	
	{{< alert title="How it works" >}}
The arguments used to deploy the ERC20 token are set within the `deployTokens` function.

This script uses the prebuilt json file `ERC20PresetFixedSupply.json` of the smart contract from the OpenZeppelin node module.
	
The main function in the script makes a `web3` object using the rpc address, and uses that to create a `web3` `wallet` object, which is then used to send transactions.

It then calls the `deployTokens` function, which constructs a `web3` `contract` object, then calls the `send` method of the `contract` object to deploy the smart contract to the blockchain.
	{{< /alert >}}

## Deploy the contract

4. Deploy the smart contract by running the `deploy.js` script:

	```bash
	node deploy.js
	```
	
	You should get an output resembling the following:

	```bash
	node deploy.js
	receipt {
  	blockHash: '0xa283a1df5cf1429ac4e94881834d92b9a11aff3e8e4ed13df517f52d520deb6d',
  	blockNumber: 243895,
  	contractAddress: '0x1317f9a0A07aa88C4C4bfC8f09df662Df0F46FB3',
  	cumulativeGasUsed: 718601,
  	effectiveGasPrice: 3000000000,
  	from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  	gasUsed: 718601,
  	logsBloom: '0x00000000000000000000000000000400000000010000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000000000002000000000000000000000000000000020000000000000000000800000000000000000200000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000002000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000',
  	status: true,
  	to: null,
  	transactionHash: '0x54e57a645eda1fd223e66b68af78908596cca7c515d26a243f88245dac5eed5a',
  	transactionIndex: 0,
  	type: '0x2',
  	events: {
    	Transfer: {
      		address: '0x1317f9a0A07aa88C4C4bfC8f09df662Df0F46FB3',
      		blockNumber: 243895,
      		transactionHash: '0x54e57a645eda1fd223e66b68af78908596cca7c515d26a243f88245dac5eed5a',
      		transactionIndex: 0,
      		blockHash: '0xa283a1df5cf1429ac4e94881834d92b9a11aff3e8e4ed13df517f52d520deb6d',
      		logIndex: 0,
      		removed: false,
      		id: 'log_30de2bf4',
      		returnValues: [Result],
      		event: 'Transfer',
      		signature: '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
      		raw: [Object]
    		}
  		}
	}
	token address:  0x1317f9a0A07aa88C4C4bfC8f09df662Df0F46FB3
	```
