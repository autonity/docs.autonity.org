---
title: "Deploy smart contracts to an Autonity network with Truffle"
linkTitle: "Deploy smart contracts with Truffle"
weight: 180
description: >
  How to deploy smart contracts to an Autonity network using Truffle, with an ERC20 token contract as an example
draft: false
---

This guide uses the Truffle development environment and JavaScript framework to compile and deploy smart contracts. It deploys as example an ERC20 token contract from the OpenZeppelin open source library of smart contracts.

## Prerequisites

- An up-to-date installation of [Truffle](https://trufflesuite.com/docs/truffle/) and `npm`. See the Truffle Suite docs for the [Installation](https://trufflesuite.com/docs/truffle/how-to/install/) how to.

- An [account](/account-holders//create-acct/) that has been [funded](/account-holders/fund-acct/) with auton, to pay for transaction gas costs. You will need the  private key of the account to unlock the account in the JavaScript environment.

- Configuration details for the Autonity network you are deploying to: a [public Autonity network](/networks/) or a [custom network](/developer/custom-networks/) if you are deploying to a local testnet.


### Setup your working environment

1. Install truffle:

	```bash
	npm i truffle
	```
	
	{{< alert title="Info" >}}Specifying the `-g ` flag to install Truffle globally will let you use it for future projects without installing in multiple places.{{< /alert >}}

2. Create a working directory and initialise the project with `npm`:

	```bash
	mkdir ERC20Token && cd ERC20Token
	mkdir contracts && mkdir migrations
	touch truffle-config.js && touch migrations/2_deploy_contracts.js
	npm init -y
	```

3. Install OpenZeppelin Contracts and Truffle `hd-wallet-provider` modules:

	```bash
	npm i --save-dev @openzeppelin/contracts
	npm i @truffle/hdwallet-provider
	```
	
	The `hdwallet-provider` module is used to add a private key. OpenZeppelin is an open source library of smart contracts.

### Write the contract

4. In your working directory (`ERC20token`), create a Solidity file for your ERC20 token contract:

	```bash
	nano contracts/myToken.sol
	```
	
	Solidity allows you to build your contract on top of another contract, through inheritance. This guide uses OpenZeppelin's `ERC20PresetFixedSupply` contract, which is an ERC20 contract with a preset token supply that allows the owner to mint and burn tokens. You can view the code for the preset contract code in the OpenZeppelin GitHub [here](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/presets/ERC20PresetFixedSupply.sol).
	
	For this contract, the guide imports and inherits from the OpenZeppelin preset. If you want to define new contract methods and build on top of the inherited contract you can do so:

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

### Configure Truffle

5. Edit the `truffle-config.js` file to specify the deployment network information and your account information. Specify in `networks` a configuration for each of the network(s) you may deploy to, where:
	- `<NETWORK_NAME>` is the name identifier used by Truffle to identify the required network configuration.
	- `<NODE_URL>` is the rpc endpoint of the network node you are connecting to.
	- `<NETWORK_ID>` is the network identifier of the network you are connecting to.
	- `<PRIVATE_KEY>` is the private key of the account you are using to submit the transaction.
	- `<GAS_PRICE>` is the gas price used for contract deploys. Truffle's default is 20000000000 (20 Gwei).
	
	```bash
	nano truffle-config.js
	```
	```javascript
	var PrivateKeyProvider = require("@truffle/hdwallet-provider");
	
	module.exports = {
  		networks: {
		
    		<NETWORK_NAME>: {
       		skipDryRun: true,
       		provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "NODE_URL"),
       		network_id: "<NETWORK_ID>",
       		gasPrice: <GAS_PRICE>
       	}
  		},
	
  		compilers: {
          solc: {
            version: "0.8.0",
            	optimizer: {
              	enabled: false, // test coverage won't work otherwise
              	runs: 200
				},
			},
		},
		plugins: ["solidity-coverage"]
	};

	```
	
	{{< alert title="Warning" color="warning" >}}
Including the private key as clear text is done in this example only because this is a testnet setting without real value. Putting a private key in the clear text is **not** recommended.
{{< /alert >}}
	
	In this example, there are 3 networks specified: a development network running on localhost and the public Autonity Testnets Bakerloo and Piccadilly. The `gasPrice` has been explicitly set to Truffle's default of `20000000000` (GWei):
	
	```javascript
	var PrivateKeyProvider = require("@truffle/hdwallet-provider");
	
	module.exports = {
  		networks: {
		
    		development: {
       		skipDryRun: true,
       		provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "http://localhost:8545"),
       		network_id: "*", // Match any network id,
       		gasPrice: 20000000000
       	},
    		bakerloo: {
       		skipDryRun: true,
       		provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "https://rpc1.bakerloo.autonity.org/"),
       		network_id: "65010000",
       		gasPrice: 20000000000
    		},
    		piccadilly: {
       		skipDryRun: true,
       		provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "https://rpc1.piccadilly.autonity.org/"),
       		network_id: "65100000",
       		gasPrice: 20000000000
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

### Write deploy script and compile the contract

6. Add the following script `2_deploy_contracts.js` to the `migrations/` directory, where:
	- `<TOKEN_NAME>` is the text label name for your token.
	- `<TOKEN_SYMBOL>` is the text symbol acronym for your token.
	- `<TOKEN_SUPPLY>` is the amount of token to premint on deployment. For example, `9999999999999999999`
	
	```bash
	nano migrations/2_deploy_contracts.js
	```

	```javascript
	module.exports = function(deployer) {
    		deployer.deploy(artifacts.require("myToken.sol"), '<TOKEN_NAME>', '<TOKEN_SYMBOL>', "<TOKEN_SUPPLY>");
    	// Additional contracts can be deployed here
	};
	```

7. Compile the contract with truffle:

	```bash
	truffle compile
	```

	After compilation you should see something like this:
	
	```bash
	Compiling your contracts...
	===========================
	> Compiling ./contracts/myToken.sol
	> Compiling @openzeppelin/contracts/token/ERC20/ERC20.sol
	> Compiling @openzeppelin/contracts/token/ERC20/IERC20.sol
	> Compiling @openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol
	> Compiling @openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol
	> Compiling @openzeppelin/contracts/token/ERC20/presets/ERC20PresetFixedSupply.sol
	> Compiling @openzeppelin/contracts/utils/Context.sol
	> Compilation warnings encountered:

    	Warning: SPDX license identifier not provided in source file. Before publishing, consider adding a comment containing "SPDX-License-Identifier: <SPDX-License>" to each source file. Use "SPDX-License-Identifier: UNLICENSED" for non-open-source code. Please see https://spdx.org for more information.
	--> project:/contracts/myToken.sol
	
	
	> Artifacts written to /home/ubuntu/TEST/contract-deploy/truffle/ERC20Token/build/contracts
	> Compiled successfully using:
		- solc: 0.8.13+commit.abaa5c0e.Emscripten.clang
   	```

### Deploy the contract

8. Deploy the contract to the block chain, specifying the name of the target `<NETWORK>` from a network configured in `truffle-config.js` in Step 5 of [Configure Truffle](/developer/deploy-truffle/#configure-truffle) above:

	```bash
	truffle deploy --network <NETWORK>
	```
	
	For example, to deploy to Piccadilly Testnet:

	```bash
	truffle deploy --network piccadilly
	```

	After migration you should see something like this:
	
	```bash
	Compiling your contracts...
	===========================
	> Everything is up to date, there is nothing to compile.
	
	
	Starting migrations...
	======================
	> Network name:    'piccadilly'
	> Network id:      65100000
	> Block gas limit: 30000000 (0x1c9c380)
	
	
	2_deploy_contracts.js
	=====================
	
	   Deploying 'myToken'
	   -------------------
	   > transaction hash:    0x529c74d4f5f84726415430638ab9050c53069d8bf6c7cb5f2e3b71403aeebaf7
	   > Blocks: 0            Seconds: 0
	   > contract address:    0xDfe20520f6402bDA7e4b6d718a13bCeBd62383Bc
	   > block number:        262243
	   > block timestamp:     1674757194
	   > account:             0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C
	   > balance:             97.714750017
	   > gas used:            1384235 (0x151f2b)
	   > gas price:           20 gwei
	   > value sent:          0 ETH
	   > total cost:          0.0276847 ETH
	
	   > Saving artifacts
	   -------------------------------------
	   > Total cost:           0.0276847 ETH
	
	Summary
	=======
	> Total deployments:   1
	> Final cost:          0.0276847 ETH
	```
