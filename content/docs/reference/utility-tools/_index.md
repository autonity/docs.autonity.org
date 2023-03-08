---
title: "Utility tools "
linkTitle: "Utility tools"
weight: 1000
description: >
  Tools for interacting with the Autonity Go Client and an Autonity Network
draft: true
---


Reference and command line options for tooling and utilities provided for submitting transactions and calls to an Autonity Go Client node, and interacting with an Autonity Network.

Details on:

- Installation and connecting to a node on an Autonity network, usage, and RPC calls available.

## Python CLI: `aut`

The Autonity CLI is a command-line RPC client for Autonity written in Python.

### Installation

For how to install, configure, and connect `aut` to a node on an Autonity network see the instructions in the GitHub `autonity/aut` repo [README.md](https://github.com/autonity/aut#readme).

### Usage

Run `aut --help` to view the options.

```
Usage: aut [OPTIONS] COMMAND [ARGS]...

  Command line interface to Autonity functionality.

Options:
  -v, --verbose  Enable additional output (to stderr)
  --version      Show the version and exit.
  --help         Show this message and exit.

Commands:
  account    Commands related to specific accounts.
  block      Commands for querying block information.
  node       Commands related to querying specific Autonity nodes.
  protocol   Commands related to Autonity-specific protocol operations.
  token      Commands for working with ERC20 tokens.
  tx         Commands for transaction creation and processing.
  validator  Commands related to the validators.
```
For how to execute RPC calls using `aut` commands, see the instructions in the GitHub `autonity/aut`repo [README.md](https://github.com/autonity/aut#readme).


### RPC Calls
#### Calling the `account` commands

Run `aut account --help` to view the options.

```
Usage: aut account [OPTIONS] COMMAND [ARGS]...

  Commands related to specific accounts.

Options:
  --help  Show this message and exit.

Commands:
  balance             Print the current balance of the given account.
  import-private-key  Read a plaintext private key file (as hex), and...
  info                Print some information about the given account...
  list                List the accounts for files in the keystore directory.
  lntn-balances       Print the current balance of the given account.
  new                 Create a new key and write it to a keyfile.
  sign-message        Use the private key in the given keyfile to sign...
  signtx              Sign a transaction using the given keyfile.
  verify-signature    Verify that the signature in SIGNATURE_FILE` is...
```
#### Calling the `block` commands

Run `aut block --help` to view the options.

```
Usage: aut block [OPTIONS] COMMAND [ARGS]...

  Commands for querying block information.

Options:
  --help  Show this message and exit.

Commands:
  get  Print information for block, where <identifier> is a block number...
```
#### Calling the `node` commands

Run `aut node --help` to view the options.

```
Usage: aut node [OPTIONS] COMMAND [ARGS]...

  Commands related to querying specific Autonity nodes.

Options:
  --help  Show this message and exit.

Commands:
  info  Print general information about the RPC node configuration and...
```
#### Calling the `protocol` commands

Run `aut protocol --help` to view the options.

```
Usage: aut protocol [OPTIONS] COMMAND [ARGS]...

  Commands related to Autonity-specific protocol operations.  See the Autonity
  contract reference for details.

Options:
  --help  Show this message and exit.

Commands:
  burn                       Burn the specified amount of NTN stake token...
  commission-rate-precision  Precision of validator commission rate values
  config                     Print the Autonity contract config
  deployer                   Contract deployer
  epoch-id                   ID of current epoch
  epoch-reward               Reward for this epoch
  epoch-total-bonded-stake   Total stake bonded this epoch
  get-bonding-req            Get queued bonding information between start...
  get-committee              Get current committee"
  get-committee-enodes       Enodes in current committee
  get-last-epoch-block       Block of last epoch
  get-max-committee-size     Maximum committee size
  get-minimum-base-fee       Minimum base fee
  get-operator               Contract operator
  get-proposer               Proposer at the given height and round
  get-unbonding-req          Get queued unbonding information between...
  get-validators             Get current validators
  get-version                Contract version
  head-bonding-id            Head ID of bonding queue
  head-unbonding-id          Head ID of unbonding queue
  last-epoch-block           Block number of the last epoch
  mint                       Mint new stake token (NTN) and add it to the...
  set-committee-size         Set the maximum size of the consensus...
  set-epoch-period           Set the epoch period.
  set-minimum-base-fee       Set the minimum gas price.
  set-operator-account       Set the Operator account.
  set-treasury-account       Set the global treasury account.
  set-treasury-fee           Set the treasury fee.
  set-unbonding-period       Set the unbonding period.
  tail-bonding-id            Tail ID of bonding queue
  tail-unbonding-id          Tail ID of unbonding queue
  total-redistributed        Total fees redistributed
  ```

#### Calling the `token` commands

Run `aut token --help` to view the options.

```
Usage: aut token [OPTIONS] COMMAND [ARGS]...

  Commands for working with ERC20 tokens.

Options:
  --help  Show this message and exit.

Commands:
  allowance      Returns the quantity in tokens that OWNER has granted...
  approve        Create a transaction granting SPENDER permission to...
  balance-of     Returns the balance in tokens of ACCOUNT.
  decimals       Returns the number of decimals used in the token balances.
  name           Returns the token name (if available).
  symbol         Returns the token symbol (if available).
  total-supply   Total supply (in units of whole Tokens).
  transfer       Create a transaction transferring AMOUNT of tokens to...
  transfer-from  Create a transaction transferring AMOUNT of tokens held...
```

#### Calling the `tx` commands

Run `aut tx --help` to view the options.

```
Usage: aut tx [OPTIONS] COMMAND [ARGS]...

  Commands for transaction creation and processing.

Options:
  --help  Show this message and exit.

Commands:
  make  Create a transaction given the parameters passed in.
  send  Send raw transaction (as generated by signtx) contained in the...
  sign  Sign a transaction using the given keyfile.
  wait  Wait for a transaction with a specific hash, and dump the receipt.
```
#### Calling the `validator` commands

Run `aut validator --help` to view the options.

```
Usage: aut validator [OPTIONS] COMMAND [ARGS]...

  Commands related to the validators.

Options:
  --help  Show this message and exit.

Commands:
  activate           Create transaction to activate a paused validator.
  bond               Create transaction to bond Newton to a validator.
  claim-rewards      Create transaction to claim rewards from a Validator.
  info               Get information about a validator.
  list               Get current validators
  pause              Create transaction to pause the given validator.
  register           Create transaction to register a validator
  unbond             Create transaction to unbond Newton from a validator.
  unclaimed-rewards  Check the given validator for unclaimed-fees.
```

## BlockScout block explorer

You can interact with the Autonity Network using the explorer utility https://piccadilly.autonity.org/. This is a fork of BlockScout and provides GraphQL and RPC APIs to inspect and analyse chain data.

BlockScout provides query API's:

- RPC API. This API is provided for developers transitioning their applications from Etherscan to BlockScout. It supports GET and POST requests. [Documentation](https://piccadilly.autonity.org//api-docs).

- Eth RPC API. This API is provided to support some rpc methods in the exact format specified for ethereum nodes. This is useful to allow sending requests to BlockScout without having to change anything about the request. However, in general, the custom RPC is recommended. [Documentation](https://piccadilly.autonity.org/eth-rpc-api-docs).

- GraphQL API. This API is provided for developers to write custom GraphQL queries using a [graphiql](https://piccadilly.autonity.org/graphiql) interface. For usage see the BlockScout docs API page [GraphQL in BlockScout](https://docs.blockscout.com/for-users/api/graphql).
