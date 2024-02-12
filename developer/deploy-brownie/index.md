---
title: "Deploy smart contracts to an Autonity network with Brownie"
linkTitle: "Deploy smart contracts with Brownie"
weight: 170
description: >
  Deploying smart contracts to an Autonity network using Brownie, using an ERC20 token contract as an example
draft: false
---

This guide uses Brownie and Python to deploy an ERC20 token contract based on the OpenZeppelin open source library.

## Setup `brownie`

Using [pipx <i class='fas fa-external-link-alt'></i>](https://github.com/pypa/pipx) or any other python package manager, install brownie:
```bash
pipx install eth-brownie
```

Add the testnet you would like to deploy the contract to:
```bash
brownie networks add Ethereum piccadilly host=https://rpc1.piccadilly.autonity.org/ chainid=65100000
```
Here we have used the [Piccadilly testnet](/networks/testnet-piccadilly/) as an example.  See [here](/networks/) for other possible networks.

Install the OpenZeppelin package, which contains a base ERC20 token implementation:
```bash
brownie pm install OpenZeppelin/openzeppelin-contracts@4.8.1
```

## Create the token project

```bash
mkdir token
cd token
brownie init
```

Create a file `brownie-config.yaml` in the `token` directory:
```
dependencies:
  - OpenZeppelin/openzeppelin-contracts@4.8.1
compiler:
  solc:
    version: 'v0.8.19'
    remappings:
      - '@openzeppelin=OpenZeppelin/openzeppelin-contracts@4.8.1'
```

## Create the token contract

Before you begin, decide upon a (unique) name `<TOKEN NAME>`, a 3 or 4
digit symbol `<TOKEN SYMBOL>` and a total supply `<TOKEN SUPPLY>` for
your token (in units of 10^-18 tokens, e.g. a supply of 10 tokens
corresponds to `10^19 = 10_000_000_000_000_000_000` units).

Create a file `contracts/<TOKEN NAME>.sol` (for
example, if your token name is `MyToken`, create the file
`contracts/MyToken.sol`:

```solidity
// SPDX-License-Identifier: None

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract <TOKEN NAME> is ERC20{
    constructor (address owner) ERC20("<TOKEN NAME>","<TOKEN SYMBOL>") {
        _mint(owner, <TOKEN SUPPLY>);
    }
}
```

Check that the contract compiles:
```bash
brownie compile
```

## Deploy the Token contract

[Create](/account-holders/create-acct/) or nominate an account <OWNER>
under your control to act as the owner of the token (the initial
holder of the total supply).

Create a deployment script `scripts/deploy.py`:
```python
from brownie import accounts, <TOKEN NAME>

def main(owner):
    deployer = accounts.load('deployer')
    <TOKEN NAME>.deploy(owner, {'from': deployer})
```

Generate a `deployer` account (and password) in brownie.
```bash
brownie accounts generate deployer
```
(Enter a suitable password when prompted).  Alternatively, an existing account can be imported into brownie - see `brownie accounts --help`.

[Fund the account](/account-holders/fund-acct/) in order to pay gas fees.

Run the deploy script on the testnet:
```bash
brownie run --network piccadilly deploy main <OWNER>
```

Take note of the address of the deployed contract.  This can be used with the `--token` option of the `aut token` commands in order to interact with the deployed token.
