---
title: "Deploy smart contracts to an Autonity network with Truffle"
description: >
  How to deploy smart contracts to an Autonity network using Truffle, with an ERC20 token contract as an example
draft: true
---

This guide uses the Truffle development environment and JavaScript framework to compile and deploy smart contracts. It deploys as example an ERC20 token contract from the OpenZeppelin open source library of smart contracts.

## Prerequisites

- An up-to-date installation of [Truffle <i class="fas fa-external-link-alt"></i>](https://trufflesuite.com/docs/truffle/) and `npm`. See the Truffle Suite docs for the [Installation](https://trufflesuite.com/docs/truffle/how-to/install/) how to.

- An [account](/account-holders/create-acct/) that has been [funded](/account-holders/fund-acct/) with auton, to pay for transaction gas costs. The guide will use the encrypted ethereum keyfile of the account.

- Configuration details for the Autonity network you are deploying to: a [public Autonity network](/networks/) or a [custom network](/developer/custom-networks/) if you are deploying to a local testnet.


### Setup your working environment

1. Install truffle:

```bash
npm i truffle
```

::: {.callout-note title="Note" collapse="false"}
Specifying the `-g ` flag to install Truffle globally will let you use it for future projects without installing in multiple places.
:::

2. Create a working directory and initialise the project with `npm`:

```bash
mkdir ERC20Token && cd ERC20Token
mkdir contracts && mkdir migrations && mkdir keystore
touch truffle-config.js && touch migrations/2_deploy_contracts.js
npm init -y
```

3. Install OpenZeppelin Contracts and Truffle `hd-wallet-provider` modules:

```bash
npm i --save-dev @openzeppelin/contracts
npm install --save truffle-keystore-provider
```
	
The `truffle-keystore-provider` module is used to unlock the encrypted ethereum keystore file and sign the contract deployment  transaction. You will be prompted to enter the key's password to unlock the account when compiling and deploying the contract.

In this guide the `truffle-keystore-provider` dependency is installed locally into a sub-directory: `node_modules/truffle-keystore-provider`.

4. Add your encrypted ethereum keystore file into the `keystore` directory:

```bash
cp <PATH>/<KEYFILE_NAME> ./keystore/<KEYFILE_NAME>
```

### Write the contract

5. In your working directory (`ERC20token`), create a Solidity file for your ERC20 token contract:

```bash
nano contracts/myToken.sol
```

Solidity allows you to build your contract on top of another contract, through inheritance. This guide uses OpenZeppelin's `ERC20PresetFixedSupply` contract, which is an ERC20 contract with a preset token supply that allows the owner to mint and burn tokens. You can view the code for the preset contract code in the OpenZeppelin GitHub [here <i class="fas fa-external-link-alt"></i>](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/presets/ERC20PresetFixedSupply.sol).

For this contract, the guide imports and inherits from the OpenZeppelin preset. If you want to define new contract methods and build on top of the inherited contract you can do so:

```javascript
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

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

6. Edit the `truffle-config.js` file to specify the deployment network information and your account information. Specify in `networks` a configuration for each of the network(s) you may deploy to, where:
	- `<NETWORK_NAME>` is the name identifier used by Truffle to identify the required network configuration.
	- `<ACCOUNT>` is the name of your encrypted ethereum keystore file. This is the private key of the account you are using to submit the transaction.
	- `<DATA_DIR>` is the path to the data directory location of your keystore file.
	- `<PROVIDER_URL>` is the rpc endpoint URL of the network node you are connecting to.
	- `<NETWORK_ID>` is the network identifier of the network you are connecting to.
	- `<GAS_PRICE>` is the gas price used for contract deploys.


```bash
nano truffle-config.js
```
```javascript
const KeystoreProvider = require("truffle-keystore-provider")

const memoizeKeystoreProviderCreator = () => {
	let providers = {}

	return (account, dataDir, providerUrl) => {
		if (providerUrl in providers) {
            return providers[providerUrl]
        } else {
            const provider = new KeystoreProvider(account, dataDir, providerUrl)
            providers[providerUrl] = provider
            return provider
        }
    }
}

const createKeystoreProvider = memoizeKeystoreProviderCreator()

module.exports = {

                networks: {
                        NETWORK_NAME: {
                                provider: createKeystoreProvider(ACCOUNT,DATA_DIR,PROVIDER_URL),
                                network_id: NETWORK_ID,
                                gasPrice: GAS_PRICE
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

In the example beneath, values for deploying to the Piccadilly Testnet are set, `<GAS_PRICE>` is explicitly set to Truffle's default of  20000000000 (20 Gwei), and `ACCOUNT` is set to `alice.key`. Note that the `DATA_DIR` is set to `../../` only: the `truffle-keystore-provider` will look by default for keystore files in `/node_modules/truffle-keystore-provider/keystore`. Setting `DATA_DIR` to `../../keystore` results in the module looking for the key in `/keystore/keystore`.

```javascript
const KeystoreProvider = require("truffle-keystore-provider")

var ACCOUNT = 'alice.key';
var DATA_DIR = '../../';
var PROVIDER_URL = '<RPC FROM https://chainlist.org/?testnets=true&search=autonity>';
var NETWORK_ID = 65100000 ;
var GAS_PRICE = 20000000000 ;

const memoizeKeystoreProviderCreator = () => {
    let providers = {}

    return (account, dataDir, providerUrl) => {
        if (providerUrl in providers) {
            return providers[providerUrl]
        } else {
            const provider = new KeystoreProvider(account, dataDir, providerUrl)
            providers[providerUrl] = provider
            return provider
        }
    }
}

const createKeystoreProvider = memoizeKeystoreProviderCreator()

module.exports = {

                networks: {
                        piccadilly: {
                                provider: createKeystoreProvider(ACCOUNT,DATA_DIR,PROVIDER_URL),
                                network_id: NETWORK_ID,
                                gasPrice: GAS_PRICE
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

### Write deploy script

7. Add the following script `2_deploy_contracts.js` to the `migrations/` directory, where:
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

### Compile the contract

8. Compile the contract with truffle:

```bash
truffle compile
```

You will be prompted for the password to unlock your account. After compilation you should see something like this:

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
> Artifacts written to /home/ubuntu/TEST/contract-deploy/truffle/ERC20Token/build/contracts
> Compiled successfully using:
   - solc: 0.8.0+commit.c7dfd78e.Emscripten.clang
```
### Deploy the contract

9. Deploy the contract to the block chain, specifying the name of the target `<NETWORK>` from a network configured in `truffle-config.js` in Step 5 of [Configure Truffle](/developer/deploy-truffle/#configure-truffle) above:

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
