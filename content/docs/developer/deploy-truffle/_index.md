---
title: "Deploy smart contracts to an Autonity network with Truffle"
linkTitle: "Deploy smart contracts with the Truffle development environment"
weight: 180
description: >
  How to deploy smart contracts to an Autonity network using Truffle, with an ERC20 token contract as an example
draft: false
---

This guide uses the Truffle development environment and JavaScript framework to compile and deploy smart contracts. It deploys as example an ERC20 token contract from the OpenZeppelin open source library of smart contracts.

## Prerequisites

- An up-to-date installation of [Truffle](https://trufflesuite.com/docs/truffle/) and `npm`. See the Truffle docs for [Installation](https://trufflesuite.com/docs/truffle/how-to/install/) is on npm Docs.

- An [account](/account-holders//create-acct/) that has been [funded](/account-holders/fund-acct/) with auton, to pay for transaction gas costs. You will need the  private key of the account to unlock the account in the JavaScript environment.

- Configuration details for the Autonity network you are deploying to: a [public Autonity network](/networks/) or a [custom network](/developer/custom-networks/) if you are deploying to a local testnet.


### Setup your working environment

1. Install truffle globally, so you can use it for future projects without installing in multiple places:

	```bash
	npm i -g truffle
	```

2. Create a working directory and initialise the project with `npm`:

	```bash
	mkdir ERC20token && cd ERC20token
	npm init -y
	```

3. Install OpenZeppelin Contracts and Truffle `hd-wallet-provider` modules:

	```bash
	npm i --save-dev @openzeppelin/contracts
		npm i @truffle/hdwallet-provider
	```
	
	The `hdwallet-provider` module is used to add a private key. OpenZeppelin is an open source library of smart contracts.

### Write the contract

4. In your working directory (`ERC20token`), create the ERC20 contract. Create a Solidity file for your token contract:

	```bash
	nano contracts/myToken.sol
	```
	
	Solidity allows you to build your contract on top of another contract, through inheritance. This guide uses OpenZeppelin's `ERC20PresetFixedSupply` contract, which is an ERC20 contract with a preset token supply that allows the owner to mint and burn tokens. You can view the code for the preset contract code in the OpenZeppelin GitHub [here](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/presets/ERC20PresetFixedSupply.sol).
	
	For this contract, import the preset then describe the new contract, inheriting from the preset:

	```javascript
	pragma solidity ^0.8.13;
	
	import "@openzeppelin/contracts/token/ERC20/presets/ERC20PresetFixedSupply.sol";
	
	contract myToken is ERC20PresetFixedSupply {
	
    	constructor(
        	string memory name,
        	string memory symbol,
        	uint256 initialSupply
    	) ERC20PresetFixedSupply(name, symbol, initialSupply, msg.sender){}
	
    	// Enter additional code here to build on top of the smart contract
	
	}
	```

### Compile and deploy the contract

5. Compile the contract with truffle:

	```bash
	truffle compile
	```

6. Edit the `truffle-config.js` file to enter account private key and rpc node endpoint, where:
	- `<NODE_URL>` is the rpc endpoint of the node you are connecting to.
	- `<PRIVATE_KEY>` is the private key of the account you are using to submit the transaction.

	```javascript
	var PrivateKeyProvider = require("@truffle/hdwallet-provider");
	
	module.exports = {
  		networks: {
		
    		localtestnet: {
       		skipDryRun: true,
       		provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "NODE_URL"),
       		network_id: "*", // Match any network id,
       		gasPrice: 10000000000
       	},
    		bakerloo: {
       		skipDryRun: true,
       		provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "NODE_URL"),
       		network_id: "65010000", // Match any network id,
       		gasPrice: 10000000000
    		},
    		piccadilly: {
       		skipDryRun: true,
       		provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "NODE_URL"),
       		network_id: "65100000", // Match any network id,
       		gasPrice: 10000000000
    		}
  		},
	
  		compilers: {
          solc: {
            version: "0.8.13",
            	optimizer: {
              	enabled: false, // test coverage won't work otherwise
              	runs: 200
				},
			},
		},
		plugins: ["solidity-coverage"]
	};

	```

Add the following deployment script in migrations:

```bash
nano migrations/2_deploy_contracts.js
```

```javascript
module.exports = function(deployer) {
    deployer.deploy(artifacts.require("mytoken.sol"), 'mytoken', 'TKN', "9999999999999999999");
    // Additional contracts can be deployed here
};
```

Deploy the contract to the block chain, specifying the name of the target `<NETWORK>` from a network configured in `truffle-config.js` in Step 6:

```bash
truffle deploy --network <NETWORK>
```

For example, to deploy to Piccadilly Testnet, `truffle deploy --network piccadilly`.

You should receive an output resembling the following:

```bash
Compiling your contracts...
===========================
> Everything is up to date, there is nothing to compile.


Starting migrations...
======================
> Network name:    'devnet'
> Network id:      444800
> Block gas limit: 8000000 (0x7a1200)


2_deploy_contracts.js
=====================

   Deploying 'mytoken'
   -------------------
   > transaction hash:    0x45c1d5b319b9030abd333a78677176763f6ade652d298a73c1a79ae59be02fd2
   > Blocks: 0            Seconds: 0
   > contract address:    0x2c949C5911C1AA38CD342d5C46245591c17FAD6D
   > block number:        776573
   > block timestamp:     1649256853
   > account:             0xe4D6b31c12725D7c3ec3B274D8299b884eF0814b
   > balance:             999.97542232
   > gas used:            1449327 (0x161d6f)
   > gas price:           10 gwei
   > value sent:          0 ETH
   > total cost:          0.01449327 ETH

   > Saving migration to chain.
   > Saving artifacts
   -------------------------------------
   > Total cost:          0.01449327 ETH

Summary
=======
> Total deployments:   1
> Final cost:          0.01449327 ETH

```
