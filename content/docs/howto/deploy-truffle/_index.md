---
title: "Deploy smart contracts to an Autonity network with Truffle"
linkTitle: "Deploy smart contracts with Truffle"
weight: 180
description: >
  How to deploy smart contracts to an Autonity network using Truffle, with an ERC20 token contract as an example
draft: true
---

Truffle is a JS framework that can be used to compile and deploy smart contracts to an EVM network. This guide demonstrates step by step how to use Truffle to deploy an ERC20 contract to an Autonity network.

## Prerequisites

- An account on an Autonity network funded with auton to pay for transaction gas costs
- Configuration details for the Autonity network you are deploying to, i.e. a public or your own node on a public Autonity network
- To provide the following constants:
  - The private key of the account you are using (to unlock the account in the JavaScript environment)
  - Gas (the maximum amount of gas units you are willing to provide for the transaction).


### Setup

Install truffle globally, so you can use it for future projects without installing in multiple places:

```bash
npm i -g truffle
```

Create a new directory and initialise the project with npm and truffle:

```bash
mkdir ERC20token && cd ERC20token
npm init -y
truffle init
```

Next install OpenZeppelin Contracts, and a module we need to add a private key. OpenZeppelin is an open source library of smart contracts.

```bash
npm i --save-dev @openzeppelin/contracts
npm i @truffle/hdwallet-provider
```

### Write the contract

From the 'ERC20token' directory, enter the following commands to start writing the contract:

```bash
nano contracts/mytoken.sol
```

Solidity allows you to build your contract on top of another contract, through inheritance. For this tutorial, we will be using the preset contract `ERC20PresetFixedSupply` which is an ERC20 that is preset so it can be minted and burned. See the code for the contract [here](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/presets/ERC20PresetFixedSupply.sol).

For this contract, import the preset then describe the new contract, inheriting from the preset:

```javascript
pragma solidity ^0.8.13;

import "@openzeppelin/contracts/token/ERC20/presets/ERC20PresetFixedSupply.sol";

contract mytoken is ERC20PresetFixedSupply {

    constructor(
        string memory name,
        string memory symbol,
        uint256 initialSupply
    ) ERC20PresetFixedSupply(name, symbol, initialSupply, msg.sender){}

    // Enter additional code here to build on top of the smart contract

}
```

### Compile and deploy the contract

Compile the contract with truffle:

```bash
truffle compile
```

Edit the `truffle-config.js` file to enter a private key to deploy the contract and rpc node url:

```javascript
var PrivateKeyProvider = require("@truffle/hdwallet-provider");

module.exports = {
  networks: {

    devnet: {
       skipDryRun: true,
       provider: () => new PrivateKeyProvider("<PRIVATE_KEY>", "NODE_URL"),
       network_id: "*", // Match any network id,
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

Finally deploy the contract to the block chain:

```bash
truffle deploy --network devnet
```

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
