---
title: "Autonity Contract Interface"
linkTitle: "Autonity Contract Interface"

description: >
  Autonity Protocol Contract functions
---

Interface for interacting with Autonity Contract functions using:

<!-- - Wrapper functions implemented by the NodeJS Console to submit calls to inspect state and state-affecting transactions. -->
- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.
- JSON-RPC methods to submit calls to inspect state.

{{% pageinfo %}}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).
{{% /pageinfo %}}

## activateValidator

Changes the state of a paused validator on an Autonity Network from `paused` to `active`. (See [`pauseValidator`](/reference/api/aut/#pausevalidator) method.)

The `activateValidator` method provides as argument the validator identifier address.

On method execution the `Validator.state` object data property is updated in memory and set to `active`.

Constraint checks are applied:

- the `address` of the validator is registered
- the `msg.sender` address of the transaction is equal to the validator's `treasury` address
- the validator state must be `paused`

Validator re-activation is executed on transaction commit. New stake delegations to the validator are accepted and the validator is included in the consensus committee selection algorithm at epoch end.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_address` | `address` | the validator identifier account address |

### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.


### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator activate --validator _address
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.activateValidator(_address).send()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator activate --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 

0x0849c0307bc446bb3fbb61b5c1518847574356aedb0b986248158d36f1eb2a5b
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.activateValidator("0x80CC1b0aC7A53e74DAD3E5B39727EA971A3e6f8B").send({from: myAddress, gas: gas})
{
  blockHash: '0xc747f08393336e71c705200dd8082c25541fde58edb35b8f386f930bf0994c60',
  blockNumber: 1690,
  contractAddress: null,
  cumulativeGasUsed: 27177,
  effectiveGasPrice: 12500000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 27177,
  logsBloom: '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0x55e4424f206e0ac192fe6c639d6c922df301fe1e21a006adf92310795557afdf',
  transactionIndex: 0,
  type: '0x2',
  events: {}
}
{{< /tab >}}
-->
## allowance

Returns the amount of stake token that remains available for a spender to withdraw from a Newton stake token owner's account.

Using `aut` you can return the allowance for an ERC20 token contract account, e.g. a Liquid Newton account.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `owner` | `address` | address of a Newton stake token owner account from which a spender account has approval to transfer token|
| `spender` | `address` | address of an account with approval to transfer Newton stake token from a token owner's account |

### Response

| Field | Datatype | Description |
| --| --| --|
| `amount` |  `uint256`  | the amount of Newton stake token the spender is able to withdraw |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token allowance [OPTIONS] OWNER
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_allowance", "params":["owner", "spender"]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.allowance('owner', 'spender').call()
{{< /tab >}}
-->

### Example

To return a spender's allowance for a Newton stake token account specify the `--ntn` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token allowance --ntn 0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C
100.000000000000000000
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_allowance", "params":["0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C","0xD9B99BAe9E9550A6Ac2F74bA7DdE483a4462C548"], "id":1}'
{"jsonrpc":"2.0","id":1,"result":100}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.allowance("0xD9B99BAe9E9550A6Ac2F74bA7DdE483a4462C548","0xeF1cB4F00924F7a3B65B1941b7Af9B31Bc80C75E").call()
'100'
{{< /tab >}}
-->

To return a spender's allowance for an ERC20 contract token (e.g. Liquid Newton) account specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token allowance --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37  0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C
1000.000000000000000000
{{< /tab >}}
{{< /tabpane >}}

## approve

Approves a `spender` account to withdraw Newton stake token from the token owner's account up to the  designated `amount`. The amount is set as the spender's allowance over the caller's tokens. The owner calls the function again to set a new `amount` allowance.

Constraint checks:

- The `owner` cannot be the zero address
- The `spender` cannot be the zero address

Using `aut` you can approve a `spender` account allowance for an ERC20 token contract account, e.g. a Liquid Newton account.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `spender` | `address` | address of spender |
| `amount` | `uint256` | amount available |

### Response

The method returns a boolean flag specifying whether the `spender` was approved or not.

### Event

On a successful call the function emits an `Approval` event, logging: `owner`, `spender`, `amount`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token approve [OPTIONS] SPENDER AMOUNT
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.approve('spender', amount).send()
{{< /tab >}}
-->
### Example

To approve a spender for a Newton stake token account specify the `--ntn` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token approve --ntn 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 100 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x715749a9aed398da7f25e66767c2ed9d3cd00c02f7306453949b9203b9a034a6
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.approve('0xeF1cB4F00924F7a3B65B1941b7Af9B31Bc80C75E', 100).send({from: myAddress, gas: gas})
{
  blockHash: '0xb23911a2da5c52f7b86302ed46b2aeba0c399d2f7efc1d46ee8d4649adb40388',
  blockNumber: 591153,
  contractAddress: null,
  cumulativeGasUsed: 44754,
  from: '0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4',
  gasUsed: 44754,
  logsBloom: '0x00004000000000000000000000020000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000020000000000000000000000000000000000000000000000000000000000004800000000000000000000000000000000000000000000000000000002000000000010000000000000000000000000000080000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0xe3a73b9dcabf5513502d3df64bf7cdb0f005b7a06a210b9fff51ffb93d6c4aa4',
  transactionIndex: 0,
  events: {
    Approval: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 591153,
      transactionHash: '0xe3a73b9dcabf5513502d3df64bf7cdb0f005b7a06a210b9fff51ffb93d6c4aa4',
      transactionIndex: 0,
      blockHash: '0xb23911a2da5c52f7b86302ed46b2aeba0c399d2f7efc1d46ee8d4649adb40388',
      logIndex: 0,
      removed: false,
      id: 'log_9d98625a',
      returnValues: [Result],
      event: 'Approval',
      signature: '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->

To approve a spender for an ERC20 contract token (e.g. Liquid Newton) account specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token approve --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 1000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xa20ae3a75009fb967ed53897b980e6e88dd580fada133c08071183b5b452ca2c
{{< /tab >}}
{{< /tabpane >}}

##  balanceOf

Returns the amount of unbonded Newton stake token held by an account.

Using `aut` you can return the account balance for an ERC20 token contract account, e.g. a Liquid Newton account.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_addr` | `address` | address of token account |

### Response

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | the amount of unbonded Newton token held by the account |


### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token balance-of [OPTIONS] ACCOUNT
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_balanceOf", "params":["_addr"]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.balanceOf('_addr').call()
{{< /tab >}}
-->

### Example

To return the Newton stake token balance for an account specify the `--ntn` option:
{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token balance-of --ntn 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4
1000.000000000000000000
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_balanceOf", "params":["0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4"], "id":1}'
{"jsonrpc":"2.0","id":1,"result":1000}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.balanceOf("0xD9B99BAe9E9550A6Ac2F74bA7DdE483a4462C548").call()
'1000'
{{< /tab >}}
-->

To return an ERC20 contract token (e.g. Liquid Newton) balance for an account specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token balance-of --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 0x11a87b260dd85ff7189d848fd44b28cc8505fa9c
999.000000000000000000
{{< /tab >}}
{{< /tabpane >}}

{{< alert title="Info" >}}All Liquid Newton balances for an account can be returned in one call using the `aut` command `aut account lntn-balances [OPTIONS] ACCOUNT`.{{< /alert >}}


## bond

Delegates an amount of Newton stake token to a designated validator. The bonded Newton amount is locked on successful processing of the method call and a bonding object for the necessary voting power change is created and tracked in memory until applied at epoch end.

Constraint checks:

- the `validator` address is registered as a validator
- the `validator` state is `active`. A bonding operation submitted to a validator in `paused` state will revert
- the `amount` is a positive integer value > 0
- the Newton balance of the account submitting  the `bond()` method call has a Newton balance >= to the `amount` being bonded

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `validator`  | `address` | the [validator identifier](/concepts/validator/#validator-identifier) address |
| `amount` | `uint256` | the amount of Newton bonded to the validator |

### Response

No response object is returned on successful execution of the method call.

The pending voting power change is tracked in memory until applied and can be returned by calling:

- the [`headBondingID`](/reference/api/aut/#headbondingid) method to return the ID of the pending bonding request, and
- the [`getBondingReq`](/reference/api/aut/#getbondingreq) method to return metadata including the start block when the bonding will be applied.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator bond [OPTIONS] AMOUNT
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.bond('validator', amount).send()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut validator bond --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xaa3705ef2d38cf2d98925660e6ca55de8948e8a075e7ee9edf6be7fa540ffe51
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.bond('0xC2B1be82bdC33b5bA3825Cf0A2036305E78a5afa', 100).send({from: myAddress, gas: gas})
{
  blockHash: '0x4b4697b3024aedcee1efc692a2cd3d92a10c915f415d53ed0f420829bfd086ba',
  blockNumber: 587610,
  contractAddress: null,
  cumulativeGasUsed: 120119,
  from: '0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4',
  gasUsed: 120119,
  logsBloom: '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0x398de6af66d011d59a047b337b13ea6963014e60c6c968f099c09320489084cd',
  transactionIndex: 0,
  events: {}
}
{{< /tab >}}
-->

## changeCommissionRate

Changes the percentage fee of staking rewards deducted by a validator as commission from delegated stake. At registration all validators have commission set to a default rate specified by the Autonity network's genesis configuration. (See Reference [Genesis, `delegationRate`](/reference/genesis/#configautonity-object).)

Validators may change commission rate at any time after registration.

The `changeCommissionRate` method provides as arguments the validator identifier address and the new commission rate expressed as basis points (bps).

On method execution the `Validator.commissionRate` object data property is updated in memory and set to the new rate.

Constraint checks are applied:

- the `address` of the validator is registered
- the `msg.sender` address of the transaction is equal to the validator's `treasury` address
- the commission rate precision is correctly expressed in basis points as an integer value in the range `0`-`10000` (`10000` = 100%).

The rate change is applied at the next unbonding period modulo epoch.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the validator identifier account address |
| `_rate` | `uint256 ` | the new commission rate in basis points (bps), value range between 0-10000 (10000 = 100%) |


### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits a `CommissionRateChange` event, logging: `_validator`, `_rate`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator change-commission-rate [OPTIONS] RATE
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.changeCommissionRate('_validator', _rate).send()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut validator change-commission-rate --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9 900 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x7a4c6bb2e19eb8a4a160723b07eeb538e835db512541621aef0062cd9e1e15f2
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.changeCommissionRate("0xA9F070101236476fe077F4A058C0C22E81b8A6C9",9999).send({from: myAddress, gas: gas})
{
  blockHash: '0xb9752263983f450cad8716bddf6ed8153b3100c2d9475ce5eaf3d02ea5a56f08',
  blockNumber: 2120,
  contractAddress: null,
  cumulativeGasUsed: 117463,
  effectiveGasPrice: 12500000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 117463,
  logsBloom: '0x00004000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000100000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0x71d371904e1843c80650bd7013c8f051794508a0d349b46d17ece199c8350b09',
  transactionIndex: 0,
  type: '0x2',
  events: {
    CommissionRateChange: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 2120,
      transactionHash: '0x71d371904e1843c80650bd7013c8f051794508a0d349b46d17ece199c8350b09',
      transactionIndex: 0,
      blockHash: '0xb9752263983f450cad8716bddf6ed8153b3100c2d9475ce5eaf3d02ea5a56f08',
      logIndex: 0,
      removed: false,
      id: 'log_9da76020',
      returnValues: [Result],
      event: 'CommissionRateChange',
      signature: '0x4fba51c92fa3d6ad8374d394f6cd5766857552e153d7384a8f23aa4ce9a8a7cf',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->
## config

Returns the Autonity Network configuration at the block height the call was submitted.

### Parameters

None.

### Response

Returns a `Config` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `operatorAccount` | `address` | the address of the Autonity governance account |
| `treasuryAccount` | `address payable` | the address of the Autonity Treasury account for community funds |
| `treasuryFee` | `uint256` | the percentage of staking rewards deducted from staking rewards and sent to the Autonity Treasury account for community funding before staking rewards are distributed |
| `minBaseFee` | `uint256` | the minimum gas price for a unit of gas used to compute a transaction on the network, denominated in [attoton](/glossary/#attoton) |
| `delegationRate` | `uint256` | the percentage of staking rewards deducted by validators as a commission from delegated stake |
| `epochPeriod` | `uint256` | the period of time for which a consensus committee is elected, defined as a number of blocks |
| `unbondingPeriod` | `uint256` | the period of time for which bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction, defined as a number of blocks |
| `committeeSize` | `uint256` | the maximum number of validators that may be members of a consensus committee on the network |
| `contractVersion` | `uint256 ` | the version number of the Autonity Protocol Contract. An integer value set by default to `1` and incremented by `1` on contract upgrade |
| `blockPeriod` | `uint256` | the minimum time interval between two consecutive blocks, measured in seconds |



### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol config [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_config", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.config().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol config -r https://rpc1.piccadilly.autonity.org
{
  "operator_account": "0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397",
  "treasury_account": "0xF74c34Fed10cD9518293634C6f7C12638a808Ad5",
  "treasury_fee": 10000000000000000,
  "min_basefee": 500000000,
  "delegation_rate": 1000,
  "epoch_period": 1800,
  "unbonding_period": 21600,
  "committee_size": 100,
  "contract_version": 1,
  "block_period": 1
}
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_config", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":["0xd32c0812fa1296f082671d5be4cbb6beeedc2397","0xf74c34fed10cd9518293634c6f7c12638a808ad5",10000000000000000,500000000,1000,1800,21600,100,1,1]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.config().call()
Result {
  '0': '0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397',
  '1': '0xF74c34Fed10cD9518293634C6f7C12638a808Ad5',
  '2': '10000000000000000',
  '3': '500000000',
  '4': '1000',
  '5': '1800',
  '6': '21600',
  '7': '100',
  '8': '1',
  '9': '1',
  operatorAccount: '0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397',
  treasuryAccount: '0xF74c34Fed10cD9518293634C6f7C12638a808Ad5',
  treasuryFee: '10000000000000000',
  minBaseFee: '500000000',
  delegationRate: '1000',
  epochPeriod: '1800',
  unbondingPeriod: '21600',
  committeeSize: '100',
  contractVersion: '1',
  blockPeriod: '1'
}
{{< /tab >}}
-->

## deployer

Returns the address of the account deploying the contract. The address is used to restrict access to functions that can only be invoked by the protocol (the `msg.sender` of a transaction is checked against the `deployer` address by the `onlyProtocol` access modifier), bypassing transaction processing and signature verification. It is set to the zero address.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the address of the account deploying the Autonity contract |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol deployer [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_deployer", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.deployer().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol deployer --rpc-endpoint https://rpc1.piccadilly.autonity.org
0x0000000000000000000000000000000000000000
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_deployer", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":"0x0000000000000000000000000000000000000000"}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.deployer().call()
'0x0000000000000000000000000000000000000000'
{{< /tab >}}

-->
## epochID

Returns the unique identifier of a block epoch as an integer value.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the identifier of a block epoch. Initial value is `0`. |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol epoch-id [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_epochID", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.epochID().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol epoch-id --rpc-endpoint https://rpc1.bakerloo.autonity.org
7371
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_epochID", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":7371}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.epochID().call()
'0'
{{< /tab >}}
-->

## epochReward

Returns the amount of Auton transaction fees available for distribution as staking rewards for stake bonded to validators in the consensus committee at the block height of the call. Actual reward distribution takes place as the last block of an epoch is finalised.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the amount of Auton transaction fees available for distribution to consensus committee members at the block height of the call |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol epoch-reward [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_epochReward", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.epochReward().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol epoch-reward --rpc-endpoint https://rpc1.piccadilly.autonity.org
121166000000000
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_epochReward", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":121166000000000}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.epochReward().call()
'30'
{{< /tab >}}
-->

## epochTotalBondedStake

Returns the amount of Newton stake token bonded to consensus committee members and securing the network during the epoch of the call.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the amount of Newton stake token bonded to consensus committee validators in the epoch  of the call |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol epoch-total-bonded-stake [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_epochTotalBondedStake", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.epochTotalBondedStake().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol epoch-total-bonded-stake --rpc-endpoint https://rpc1.piccadilly.autonity.org
61338
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_epochTotalBondedStake", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":61338}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.epochTotalBondedStake().call()
'133652'
{{< /tab >}}
-->

##  getBondingReq

Returns an array of pending bonding request within a requested block range. Staking transitions are maintained in memory until voting power changes are applied at epoch end before selection of the next consensus committee.

The array range is specified by a start and end index using the bonding request identifier. Bonding identifiers can be returned by calling:

- [tailBondingID](/reference/api/aut/#tailbondingid) to return the ID of the last processed bonding request,
- [headBondingID](/reference/api/aut/#headbondingid) to return the ID of the last received pending bonding request.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `startId` | `uint256` | the bonding identifier specifying the start index of the array |
| `lastId` | `uint256` | the bonding identifier specifying the end index of the array |

### Response

Returns a `_results` array of `Staking` objects, each object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `delegator` | `address payable` | account address of the account bonding stake |
| `delegatee` | `address` | validator identifier account address of the validator to which stake is being bonded |
| `amount` | `uint256` | the amount of Newton stake token being bonded to the `delegatee` account |
| `startBlock` | `uint256` | the block number at which a bonding transaction was committed. Only applicable to bonding staking transitions |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-unbonding-req [OPTIONS] START END
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getBondingReq", "params":[startId, lastId]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getBondingReq(startId, lastId).call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-unbonding-req -r https://rpc1.piccadilly.autonity.org 0 2
[
  {
    "delegator": "0x75474aC55768fAb6fE092191eea8016b955072F5",
    "delegatee": "0x32F3493Ef14c28419a98Ff20dE8A033cf9e6aB97",
    "amount": 10000,
    "start_block": 0
  },
  {
    "delegator": "0x821BC352E77D885906B47001863f75e15C114f70",
    "delegatee": "0x31870f96212787D181B3B2771F58AF2BeD0019Aa",
    "amount": 10000,
    "start_block": 0
  }
]
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getBondingReq", "params":[0,1], "id":1}'
{"jsonrpc":"2.0","id":1,"result":[{"delegator":"0x3e08fec6abaf669bd8da54abee30b2b8b5024013","delegatee":"0x4b7275d5f5292c3027a16e0eb891d75a0ef39cc7","amount":10000,"startBlock":0}]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getBondingReq(0,1).call()
[
  [
    '0x61EE7d3244642E5f6D654416a098DEabFBF5306e',
    '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
    '10000',
    '0',
    delegator: '0x61EE7d3244642E5f6D654416a098DEabFBF5306e',
    delegatee: '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
    amount: '10000',
    startBlock: '0'
  ]
]
{{< /tab >}}
-->

##  getCommittee

Returns a list of the validators selected as members of the consensus committee at the block height of the method call.

The method returns the current consensus committee if called before the Autonity Protocol has invoked the `finalize()` method, the consensus committee for the next epoch if called after.

See also the `onlyProtocol` function [`finalize`](/reference/api/aut/op-prot/#finalize).

### Parameters

None.

### Response

Returns a `committee` array of `CommitteeMember` objects, each object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `addr` | `address` | account address of the committee member |
| `votingPower` | `uint256` | the amount of Newton stake token bonded to the committee member |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-committee [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getCommittee", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getCommittee().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-committee -r https://rpc1.bakerloo.autonity.org
[
  {
    "address": "0x4b7275d5F5292C3027a16E0eb891D75a0Ef39cc7",
    "voting_power": 10000
  },
  {
    "address": "0x5e08564Ee99E96e690E9b25591191aE0c78351a3",
    "voting_power": 10000
  },
  {
    "address": "0x33BF54630991f0a1A23B9f102873b3B54C4b94B3",
    "voting_power": 10000
  },
  {
    "address": "0x1ae9B1B3207195430a36D82Fc0bDA1f857D0AA72",
    "voting_power": 10000
  },
  {
    "address": "0x0c7dC2aB00c7b5934EDA097a8585f56367A94dA4",
    "voting_power": 10000
  },
  {
    "address": "0xf5A48b1Df2a3a616AdB92E57d6ce36E17c3C2a0b",
    "voting_power": 10000
  },
  {
    "address": "0x5FE87eE4f61Da6E640Aec02CE818CdcD30B8cB13",
    "voting_power": 10000
  },
  {
    "address": "0xEbF9dD85cc99a15f1AFB78A6A7cb28a9103e9a12",
    "voting_power": 10000
  },
  {
    "address": "0x9f26942A9710099A7F2b4b64e53522bB16d2Af7d",
    "voting_power": 10005
  }
]
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getCommittee", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":[{"addr":"0x4b7275d5f5292c3027a16e0eb891d75a0ef39cc7","votingPower":10000},{"addr":"0x5e08564ee99e96e690e9b25591191ae0c78351a3","votingPower":10000},{"addr":"0x33bf54630991f0a1a23b9f102873b3b54c4b94b3","votingPower":10000},{"addr":"0x1ae9b1b3207195430a36d82fc0bda1f857d0aa72","votingPower":10000},{"addr":"0x0c7dc2ab00c7b5934eda097a8585f56367a94da4","votingPower":10000},{"addr":"0xf5a48b1df2a3a616adb92e57d6ce36e17c3c2a0b","votingPower":10000},{"addr":"0x5fe87ee4f61da6e640aec02ce818cdcd30b8cb13","votingPower":10000},{"addr":"0xebf9dd85cc99a15f1afb78a6a7cb28a9103e9a12","votingPower":10000},{"addr":"0x9f26942a9710099a7f2b4b64e53522bb16d2af7d","votingPower":10005}]}{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getCommittee().call()
[
  [
    '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
    '10000',
    addr: '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
    votingPower: '10000'
  ],
  [
    '0x8CC985DEd2546e9675546Db6bcF34f87f4A16c56',
    '50563',
    addr: '0x8CC985DEd2546e9675546Db6bcF34f87f4A16c56',
    votingPower: '50563'
  ],
  [
    '0x0be4Ee22d794c640366352Ef6CE666E52229886d',
    '10000',
    addr: '0x0be4Ee22d794c640366352Ef6CE666E52229886d',
    votingPower: '10000'
  ],
  [
    '0x055A7c97b73Db9649fF03ac50DB0552C959cCa91',
    '10000',
    addr: '0x055A7c97b73Db9649fF03ac50DB0552C959cCa91',
    votingPower: '10000'
  ],
  [
    '0x35379A60fc0f108583d6692cc6D2fa0317cc9724',
    '10000',
    addr: '0x35379A60fc0f108583d6692cc6D2fa0317cc9724',
    votingPower: '10000'
  ],
  [
    '0x94C1EEe283fac8102dDB08ac0661a268d4977B2d',
    '10000',
    addr: '0x94C1EEe283fac8102dDB08ac0661a268d4977B2d',
    votingPower: '10000'
  ],
  [
    '0x255eCbeaad1482471fAEE185608Dedb96CD249F6',
    '10000',
    addr: '0x255eCbeaad1482471fAEE185608Dedb96CD249F6',
    votingPower: '10000'
  ]
]
{{< /tab >}}
-->
##  getCommitteeEnodes

Returns the enode URLs of validators selected as members of the consensus committee at the block height of the method call.

The protocol uses this function to inform committee nodes which other committee nodes to connect to.

### Parameters

None.

### Response

Returns a `committeeNodes` list of committee member enode URL addresses consisting of:

| Field | Datatype | Description |
| --| --| --|
| value | `string` | enode url for the committee member |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-committee-enodes [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getCommitteeEnodes", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getCommitteeEnodes().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-committee-enodes -r https://rpc1.bakerloo.autonity.org
['enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303', 'enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303', 'enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303', 'enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308', 'enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309', 'enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310', 'enode://c6ae16b58cf2e073649ec34ed59550c57389fcb949f51b806d6f7de26e7961cfc33794fde67b484ce9966a30e5ab5331c610b1b659249a6d66cc9e6d8a3d23d1@143.198.240.242:30303', 'enode://06facaec377a55fe8fd9e30cc922bedc7ee97e292294435635fa3b053c30215b87954daa27c79a73e3a5013124318b084907c81f518bcf36f88dad4d01e952ec@138.68.118.4:30303', 'enode://0c71d8076f0543505aae22901471d5437f1fd92b3d154d154edcec5baf0d7b121e6e8dc85ae725daf77cbc50ff5616727d59d36c2606751401000580e155e2bc@5.181.104.29:30303']
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getCommitteeEnodes", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":["enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303","enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303","enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303","enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308","enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309","enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310","enode://c6ae16b58cf2e073649ec34ed59550c57389fcb949f51b806d6f7de26e7961cfc33794fde67b484ce9966a30e5ab5331c610b1b659249a6d66cc9e6d8a3d23d1@143.198.240.242:30303","enode://06facaec377a55fe8fd9e30cc922bedc7ee97e292294435635fa3b053c30215b87954daa27c79a73e3a5013124318b084907c81f518bcf36f88dad4d01e952ec@138.68.118.4:30303","enode://0c71d8076f0543505aae22901471d5437f1fd92b3d154d154edcec5baf0d7b121e6e8dc85ae725daf77cbc50ff5616727d59d36c2606751401000580e155e2bc@5.181.104.29:30303"]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getCommitteeEnodes().call()
[
  'enode://b2748268c31ebab8603058335bb4bed062e05b9ceaa3562f69868a01d1038a84136fc587fb913e1cb8ce821f1eb0bf9879e3249f18adcd39f1211a104ceb57a9@35.197.223.249:30303',
  'enode://da83d6ca0a52091cd1684f560b1fef78574e3b599cd5a8de6682bd4920bd2b54e9fd4ed66211cf439012484b9f9937fde836a06a15ea1e9d53f44b4582acaf74@34.89.41.50:30303',
  'enode://7dcec0303190230b29691e8024133a46e7b9dd526f0238d4874aa20f8155df735098d869508c029e98eefea3fb2a50f0b9b17ab1e0ef027311e4946473a92ac8@35.197.202.245:30303',
  'enode://301040cf64c79a3eb19201a5df8100f989830b44eb367e820d882d7787e00d8403a073b32e80ea5e83dc3343bdcbe3da8dc3a18c0e5fd5c751474067d4ec8655@35.177.59.62:30308',
  'enode://3c151817c1647ccdfcaa402bbb5d4776c839fa6678dfd757c6ee5ad08550f9a733f03096b312b8e61bc126a174da8ad4ca4ea5b03bd83999549d9c6bdfad4b98@18.130.21.221:30309',
  'enode://9ead042f4d5a95cc9a95730471366d979545435d3249669b37d819f016d3306d5f1edd5ebc8ada15bfcad61bb315245e832272d6945505395fdab40f13a0c4a6@3.11.174.186:30310',
  'enode://1d90ec3dc5568caa86b3fc4ea01f237e068320abb9c42d4c4c5ad8b5f8992da5ddda387d84e970da76b6014bcc28401b879246260a67e95414562bbbb4a339ad@35.199.70.162:30303'
]
{{< /tab >}}
-->

##  getMaxCommitteeSize

Returns the protocol setting for the maximum number of validators that can be selected to the consensus committee.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `committeeSize` | `uint256` | the maximum number of validators allowed in the consensus committee |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-max-committee-size [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getMaxCommitteeSize", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getMaxCommitteeSize().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-max-committee-size --rpc-endpoint https://rpc1.bakerloo.autonity.org/
50
{{< /tab >}}
{{< tab header="RPC" >}}
curl --location --request GET 'https://rpc1.bakerloo.autonity.org/' \
--header 'Content-Type: application/json' \
--data-raw '{
        "jsonrpc":"2.0",
        "method":"aut_getMaxCommitteeSize",
        "params":[],
        "id":1
}'
{"jsonrpc":"2.0","id":1,"result":50}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getMaxCommitteeSize().call()

50
{{< /tab >}}
-->

##  getMinimumBaseFee

Returns the protocol setting for the minimum price per unit of gas for computing a transaction on an Autonity network.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `minBaseFee` | `uint256` | the minimum price per unit of gas, denominated in [attoton](/glossary/#attoton) |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-minimum-base-fee [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getMinimumBaseFee", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getMinimumBaseFee().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-minimum-base-fee --rpc-endpoint https://rpc1.bakerloo.autonity.org/
500000000
{{< /tab >}}
{{< tab header="RPC" >}}
curl --location --request GET 'https://rpc1.bakerloo.autonity.org/' \
--header 'Content-Type: application/json' \
--data-raw '{
        "jsonrpc":"2.0",
        "method":"aut_getMinimumBaseFee",
        "params":[],
        "id":1
}'

{"jsonrpc":"2.0","id":1,"result":500000000}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getMinimumBaseFee().call()
500000000
{{< /tab >}}
-->
##  getNewContract

The getNewContract method is used as part of the Autonity Protocol Contract upgrade process. It provides a getter function to retrieve the compiled EVM bytecode and Contract ABI of a new Autonity Protocol Contract when an upgrade is initiated.

The method retrieves the compiled Solidity code and JSON formatted Contract ABI representation, and performs an upgrade.

See also the `onlyOperator` function [`upgradeContract`](/reference/api/aut/op-prot/#upgradecontract).

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `newContractBytecode` | `bytes` | the EVM bytecode compiled from the new Autonity Protocol Contract's source Solidity |
| `newContractABI` | `string` | the Application Binary Interface (ABI) of the new Autonity Protocol Contract as a JSON representation |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="RPC" >}}
{"method": "aut_getNewContract", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getNewContract().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="RPC" >}}
curl --location --request GET 'https://rpc1.bakerloo.autonity.org/' \
--header 'Content-Type: application/json' \
--data-raw '{
        "jsonrpc":"2.0",
        "method":"aut_getNewContract",
        "params":[],
        "id":1
}'
{"jsonrpc":"2.0","id":1,"result":["",""]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getNewContract().call()
Result { '0': '', '1': '' }
{{< /tab >}}
-->

## getOperator

Returns the address of the Autonity governance account.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the operator governance account address |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-operator [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_getOperator", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getOperator().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-operator -r https://rpc1.bakerloo.autonity.org/
0x293039dDC627B1dF9562380c0E5377848F94325A
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getOperator", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":"0x293039dDC627B1dF9562380c0E5377848F94325A"}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getOperator().call()
'0x2f3BcE2d6C2602de594d9a6662f0b93416cfB4d7'
{{< /tab >}}
-->

##  getProposer

Returns the address of the consensus committee member proposing a new block for a specified block height and consensus round.

The proposer is selected from the committee via weighted random sampling, with selection probability determined by the voting power of each committee member. The selection mechanism is deterministic and will always select the same address, given the same height, round and contract state.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `height` | `uint256` | the block number for which the proposer is requested  |
| `round` | `uint256` | the consensus round number for which the proposer is requested |

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the address of the proposer at the designated block height and consensus round |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-proposer [OPTIONS] HEIGHT ROUND
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getProposer", "params":[height, round]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getProposer(height, round).call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-proposer -r https://rpc1.bakerloo.autonity.org/ 4576868 0
0x0c7dC2aB00c7b5934EDA097a8585f56367A94dA4
{{< /tab >}}
{{< tab header="RPC" >}}
curl --location --request GET 'https://rpc1.bakerloo.autonity.org/' \
--header 'Content-Type: application/json' \
--data-raw '{
        "jsonrpc":"2.0",
        "method":"aut_getProposer",
        "params":[4576868,0],
        "id":1
}'
{"jsonrpc":"2.0","id":1,"result":"0x0c7dc2ab00c7b5934eda097a8585f56367a94da4"}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getProposer(4576868,0).call()
'0x5fe87ee4f61da6e640aec02ce818cdcd30b8cb13'
{{< /tab >}}
-->
##  getUnbondingReq

Returns an array of pending unbonding requests within a requested block range. Staking transitions are maintained in memory until voting power changes are applied at epoch end before selection of the next consensus committee.

The array range is specified by a start and end index using the unbonding request identifier. Unbonding identifiers can be returned by calling:

- [tailUnbondingID](/reference/api/aut/#tailunbondingid) to return the ID of the last processed unbonding request,
- [headUnbondingID](/reference/api/aut/#headunbondingid) to return the ID of the last received pending unbonding request.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `startId` | `uint256` | the unbonding identifier specifying the start index of the array |
| `lastId` | `uint256` | the unbonding identifier specifying the last index of the array |


### Response

Returns a `_results` array of `Staking` objects, each object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `delegator` | `address payable` | account address of the account bonding stake |
| `delegatee` | `address` | validator identifier account address of the validator to which stake is being bonded |
| `amount` | `uint256` | the amount of Newton stake token being bonded to the `delegatee` account |
| `startBlock` | `uint256` | the block number at which an unbonding transaction was committed and from which the unbonding period begins. Only applicable to unbonding staking transitions |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-unbonding-req [OPTIONS] START END
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getUnbondingReq", "params":[startId, lastId]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getUnbondingReq(startId, lastId).call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-unbonding-req --rpc-endpoint https://rpc1.piccadilly.autonity.org 0 1
[
  {
    "delegator": "0xB17b5DD3fD63c736e538172A640ab0510E608a80",
    "delegatee": "0x32F3493Ef14c28419a98Ff20dE8A033cf9e6aB97",
    "amount": 11,
    "start_block": 486499
  }
]
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getUnbondingReq", "params":[0,1], "id":1}'
{"jsonrpc":"2.0","id":1,"result":[{"delegator":"0xb17b5dd3fd63c736e538172a640ab0510e608a80","delegatee":"0x32f3493ef14c28419a98ff20de8a033cf9e6ab97","amount":11,"startBlock":486499}]}
{{< /tab >}}
{{< /tabpane >}}


<!--
{{< tab header="NodeJS Console" >}}
> autonity.getUnbondingReq(0,1).call()
[
  [
    '0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C',
    '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
    '100',
    '1379927',
    delegator: '0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C',
    delegatee: '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
    amount: '100',
    startBlock: '1379927'
  ]
]
{{< /tab >}}

-->

## getValidator

Returns the data for a designated validator identifier address from system state. The method response may be empty if there is no associated validator object for the address argument provided.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_addr` | `address` | the validator identifier account address |

### Response

Returns a `Validator` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `treasury` | `address payable` | the address that will receive staking rewards the validator earns |
| `nodeAddress` | `address` | the validator identifier account address |
| `oracleAddress` | `address` | the identifier account address of the validator's oracle server |
| `enode` | `string` | the enode url of the validator node |
| `commissionRate` | `uint256` | the percentage commission that the validator will charge on staking rewards from delegated stake |
| `bondedStake` | `uint256` | the total amount of delegated and self-bonded stake that has been bonded to the validator |
| `totalSlashed` | `uint256` | a counter of the number of times that a validator has been penalised for accountability and omission faults since registration |
| `liquidContract` | `Liquid` | the address of the validator's Liquid Newton contract |
| `liquidSupply` | `uint256` | the total amount of Liquid Newton in circulation |
| `registrationBlock` | `uint256` | the block number in which the registration of the validator was committed to state|
| `state` | `ValidatorState` | the state of the validator. `ValidatorState` is an enumerated type with enumerations: `active`, `paused` |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator info [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getValidator", "params":[_addr]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getValidator(_addr).call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut validator info --rpc-endpoint https://rpc1.piccadilly.autonity.org --validator 0xaB471b6F6E59dfD81ba9988f0D0B6950C5c3FEC1
{
  "treasury": "0xaB471b6F6E59dfD81ba9988f0D0B6950C5c3FEC1",
  "node_address": "0xaB471b6F6E59dfD81ba9988f0D0B6950C5c3FEC1",
  "oracle_address": "0xaB471b6F6E59dfD81ba9988f0D0B6950C5c3FEC1",
  "enode": "enode://87e1a4e04544ce628c3b26fbffbefa355f6cbd2c285dd07a8906f32711f06e9a6b759e257182ad06b1714c2c6dfb2f95850bdfee2e8dd90938dd3c5fa92b00a6@35.205.16.40:30303",
  "commission_rate": 1000,
  "bonded_stake": 52,
  "total_slashed": 0,
  "liquid_contract": "0xF8060D5D9FBbAF99fF63E37C2118343001558a60",
  "liquid_supply": 52,
  "registration_block": 6734993,
  "state": 0
}
{{< /tab >}}
{{< tab header="RPC" >}}
$ curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getValidator", "params":["0xaB471b6F6E59dfD81ba9988f0D0B6950C5c3FEC1"], "id":1}'
{"jsonrpc":"2.0","id":1,"result":{"treasury":"0xab471b6f6e59dfd81ba9988f0d0b6950c5c3fec1","nodeAddress":"0xab471b6f6e59dfd81ba9988f0d0b6950c5c3fec1","oracleAddress":"0x300d7ce23a6cd8d660aeaf595e9ee15e635f4taa","enode":"enode://87e1a4e04544ce628c3b26fbffbefa355f6cbd2c285dd07a8906f32711f06e9a6b759e257182ad06b1714c2c6dfb2f95850bdfee2e8dd90938dd3c5fa92b00a6@35.205.16.40:30303","commissionRate":1000,"bondedStake":52,"totalSlashed":0,"liquidContract":"0xf8060d5d9fbbaf99ff63e37c2118343001558a60","liquidSupply":52,"registrationBlock":6734993,"state":0}}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getValidator('0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C').call()
[ '0x61EE7d3244642E5f6D654416a098DEabFBF5306e',
  '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
  'enode://b2748268c31ebab8603058335bb4bed062e05b9ceaa3562f69868a01d1038a84136fc587fb913e1cb8ce821f1eb0bf9879e3249f18adcd39f1211a104ceb57a9@35.197.223.249:30303',
  '100000000',
  '10000',
  '0',
  '0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37',
  '10000',
  'validator-0.devnet.clearmatics.network',
  '0',
  '0',
  treasury: '0x61EE7d3244642E5f6D654416a098DEabFBF5306e',
  addr: '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
  enode: 'enode://b2748268c31ebab8603058335bb4bed062e05b9ceaa3562f69868a01d1038a84136fc587fb913e1cb8ce821f1eb0bf9879e3249f18adcd39f1211a104ceb57a9@35.197.223.249:30303',
  delegationRate: '100000000',
  bondedStake: '10000',
  totalSlashed: '0',
  liquidContract: '0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37',
  liquidSupply: '10000',
  registrationBlock: '0',
  state: '0' ]
{{< /tab >}}
-->

##  getValidators

Returns the current list of validators from system state.

The response is returned as a list of validator identifier addresses, sorted by registration index in ascending order. I.E. the last value in the array is always the last processed registration request.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `validatorList` | `address` array | an array of registered validators, sorted by registration index in ascending order  |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator list [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getValidators", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getValidators().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut validator list --rpc-endpoint https://rpc1.piccadilly.autonity.org
0x32F3493Ef14c28419a98Ff20dE8A033cf9e6aB97
0x31870f96212787D181B3B2771F58AF2BeD0019Aa
0x6EBb5A45728be7Cd9fE9c007aDD1e8b3DaFF6B3B
0xAC245aF88265E72881CD9D21eFb9DDC32E174B69
0x36288C1F8C990fd66A1C5040a61d6f3EcF3A49c1
0xb3A3808c698d82790Ac52a42C05E4BCb3dfCd3db
0x467D99EA9DACC495E6D1174b8f3Dd20DDd531335
0xa940eB48368324E2032b97723BE487505981edce
0xba35a25badB802Cb3C0702e0e2df392e00511CA2
0x1114fE559b302403BB3a89806bC08F7fA5299E99
0x9fd408Bdb83Be1c8504Ff13eBcCe7f490DCCC2cF
0xE03D1DE3A2Fb5FEc85041655F218f18c9d4dac55
0x52b89AFA0D1dEe274bb5e4395eE102AaFbF372EA
0x914d06dBaaA3c51085692F59230769EAa32f3A94
0xFae912BAdB5e0Db5EC0116fe6552e8D6Bdb4e82b
0x7fc0ae4918C0D8eAa1A259fa455B32A2cEB58eA4
0x82b6eacA5014DCa39b3A37d68C246f1466B15aA9
0xE4Ece2266Ea7B7468aD3E381d08C962641b567f2
0xCD46183D0075116175c62dCDe568f2e0c4736597
0xcd50C31356fDdBD9e704cf58751a0ED2B178d8b0
0xaB471b6F6E59dfD81ba9988f0D0B6950C5c3FEC1
0xeb25090AA0fD5c940F87A172Aaf62413Eb625b63
0x2AF517e6EdF3C01f8256E609122f004457024E67
0x9d458E21b15C0C1A95db65c5fAe639d1477cE4DC
0x724E26894a5fcf0233fdc5849Aaf0fbB2dd5b0E8
0xE9Ce74FBA6F04345516c9a3028292a1d62A409B3
0x9f793D2c7E1D5a72A020281F383bfc5e3086AcA9
0xde5aeb71cc4Aaa99cf6a23F68bFfDdDD7e8231Fe
{{< /tab >}}
{{< tab header="RPC" >}}
$ curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getValidators", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":["0x32f3493ef14c28419a98ff20de8a033cf9e6ab97","0x31870f96212787d181b3b2771f58af2bed0019aa","0x6ebb5a45728be7cd9fe9c007add1e8b3daff6b3b","0xac245af88265e72881cd9d21efb9ddc32e174b69","0x36288c1f8c990fd66a1c5040a61d6f3ecf3a49c1","0xb3a3808c698d82790ac52a42c05e4bcb3dfcd3db","0x467d99ea9dacc495e6d1174b8f3dd20ddd531335","0xa940eb48368324e2032b97723be487505981edce","0xba35a25badb802cb3c0702e0e2df392e00511ca2","0x1114fe559b302403bb3a89806bc08f7fa5299e99","0x9fd408bdb83be1c8504ff13ebcce7f490dccc2cf","0xe03d1de3a2fb5fec85041655f218f18c9d4dac55","0x52b89afa0d1dee274bb5e4395ee102aafbf372ea","0x914d06dbaaa3c51085692f59230769eaa32f3a94","0xfae912badb5e0db5ec0116fe6552e8d6bdb4e82b","0x7fc0ae4918c0d8eaa1a259fa455b32a2ceb58ea4","0x82b6eaca5014dca39b3a37d68c246f1466b15aa9","0xe4ece2266ea7b7468ad3e381d08c962641b567f2","0xcd46183d0075116175c62dcde568f2e0c4736597","0xcd50c31356fddbd9e704cf58751a0ed2b178d8b0","0xab471b6f6e59dfd81ba9988f0d0b6950c5c3fec1","0xeb25090aa0fd5c940f87a172aaf62413eb625b63","0x2af517e6edf3c01f8256e609122f004457024e67","0x9d458e21b15c0c1a95db65c5fae639d1477ce4dc","0x724e26894a5fcf0233fdc5849aaf0fbb2dd5b0e8","0xe9ce74fba6f04345516c9a3028292a1d62a409b3","0x9f793d2c7e1d5a72a020281f383bfc5e3086aca9","0xde5aeb71cc4aaa99cf6a23f68bffdddd7e8231fe"]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getValidators().call()
[
  '0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C',
  '0x8CC985DEd2546e9675546Db6bcF34f87f4A16c56',
  '0x0be4Ee22d794c640366352Ef6CE666E52229886d',
  '0x055A7c97b73Db9649fF03ac50DB0552C959cCa91',
  '0x35379A60fc0f108583d6692cc6D2fa0317cc9724',
  '0x94C1EEe283fac8102dDB08ac0661a268d4977B2d',
  '0x255eCbeaad1482471fAEE185608Dedb96CD249F6'
]
{{< /tab >}}
-->

##  getVersion

Returns the version of the Autonity Protocol Contract.

Versioning is recorded by a single-digit incrementing version number.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `contractVersion` | `uint256 ` | the version number of the Autonity Protocol Contract. An integer value set by default to `1` and incremented by `1` on contract upgrade |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-version [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getVersion", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.getVersion().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-version -r https://rpc1.piccadilly.autonity.org/8545/
1
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getVersion", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":1}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.getVersion().call()`
'1'
{{< /tab >}}
-->

## headBondingID

Returns the index identifier of the last received bonding request tracked in Autonity Protocol contract memory.

The 'tail' and 'head' bonding IDs are indexes used to specify the set of bonding requests to apply when computed. `tailBondingID` is the last processed bonding request and `headBondingID` is the last received request. The Autonity Protocol contract processes bonding requests at the end of each epoch from `tailBondingID` to `headBondingID - 1`.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256 ` | the index identifier of the last received bonding request |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol head-bonding-id [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_headBondingID", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.headBondingID().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol head-bonding-id -r https://rpc1.piccadilly.autonity.org/
139
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_headBondingID", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":139}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.headBondingID().call()
'43665'
{{< /tab >}}
-->
## headUnbondingID

Returns the index identifier of the last received unbonding request tracked in Autonity Protocol contract memory.

The 'tail' and 'head' unbonding IDs are indexes used to specify the set of unbonding requests to apply when computed. `tailUnbondingID` is the last processed unbonding request and `headUnbondingID` is the last received request. The Autonity Protocol contract processes unbonding request at the end of the epoch in which the unbonding period expires from `tailUnbondingID` to `headUnbondingID - 1`.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the index identifier of the last received unbonding request |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol head-unbonding-id [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_headUnbondingID", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.headUnbondingID().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol head-unbonding-id -r https://rpc1.piccadilly.autonity.org/
48
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_headUnbondingID", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":48}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.headUnbondingID().call()
'2'
{{< /tab >}}
-->

## lastEpochBlock

Returns the number of the last block in the preceding epoch at the block height of the call.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the number of the last block in the preceding epoch |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-last-epoch-block [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_lastEpochBlock", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.lastEpochBlock().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-last-epoch-block -r https://rpc1.piccadilly.autonity.org
12981684
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_lastEpochBlock", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":12981684}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.lastEpochBlock().call()
'2526990'
{{< /tab >}}
-->

## name

Returns the name of the Newton stake token as a human-readable string. Set as contract metadata to the value of `Newton`.

Using `aut` you can return the name for an ERC20 token contract account, e.g. a Liquid Newton contract.

### Parameters

None.

### Response

| Returns | Datatype | Description |
| --| --| --|
| value | `string` | the name of the Newton stake token |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token name [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_name", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.name().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token name --ntn -r https://rpc1.piccadilly.autonity.org
Newton
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_name", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":"Newton"}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.name().call()
'Newton'
{{< /tab >}}
-->

To return the `name` for an ERC20 (e.g. a Liquid Newton token) token contract specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token name -r https://rpc1.piccadilly.autonity.org --token 0xC500751c4F96d49B954D20EAE42Fa29278B96beB
LNTN-4
{{< /tab >}}
{{< /tabpane >}}

## pauseValidator

Changes the state of a registered validator on an Autonity Network from `active` to `paused`. (A paused validator can be re-activated by calling the  [`activateValidator`](/reference/api/aut/#activatevalidator) method.)

The `pauseValidator` method provides as argument the validator identifier address.

On method execution the `Validator.state` object data property is updated in memory and set to `paused`.

Constraint checks are applied:

- the `address` of the validator is registered
- the `msg.sender` address of the transaction is equal to the validator's `treasury` address
- the validator state must be `active`

Validator pausing is executed on transaction commit. New stake delegations are reverted from submission of the pausing transaction. Exclusion of the validator from the consensus commmittee selection algorithm takes effect at epoch end (i.e. the 'effective block').

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_address` | `address` | the validator identifier account address |

### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits a `PausedValidator ` event, logging: `val.treasury`, `_address`, `effectiveBlock`.


### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator pause [OPTIONS]
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.pauseValidator(_address).send()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator pause --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x942328bea54a0096ca9b2fb88acd337c883f7923c2ef6b8290a340c5baec2d20
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.pauseValidator("0x80CC1b0aC7A53e74DAD3E5B39727EA971A3e6f8B").send({from: myAddress, gas: gas})
{
  blockHash: '0xfb83c3b36db54fd486cde018a04c99f7a158c044b284737545fc4255082c4cf4',
  blockNumber: 1152,
  contractAddress: null,
  cumulativeGasUsed: 55802,
  effectiveGasPrice: 12500000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 55802,
  logsBloom: '0x00004000000000000000010000020004000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0x8b6d2985ff988ce1e72e46e2533f960d6f18759af481ca93f83e3c5a48d6d195',
  transactionIndex: 0,
  type: '0x2',
  events: {
    PausedValidator: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 1152,
      transactionHash: '0x8b6d2985ff988ce1e72e46e2533f960d6f18759af481ca93f83e3c5a48d6d195',
      transactionIndex: 0,
      blockHash: '0xfb83c3b36db54fd486cde018a04c99f7a158c044b284737545fc4255082c4cf4',
      logIndex: 0,
      removed: false,
      id: 'log_35a5ab36',
      returnValues: [Result],
      event: 'PausedValidator',
      signature: '0x75bdcdbe540758778e669d108fbcb7ede734f27f46e4e5525eeb8ecf91849a9c',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->

## registerValidator

Registers a validator on an Autonity Network.

The `registerValidator` method provides as argument the [enode](/glossary/#enode) URL of the validator node, the validator's oracle server address, and a proof of node ownership generated using the private key of the validator node's [P2P node key](/concepts/validator/#p2p-node-key) and the validator's [oracle server key](/concepts/oracle-network/#oracle-server-key).

On method execution a `Validator` object data structure is constructed in memory, populated with method arguments and default values ready for validator registration processing:

| Field | Datatype | Description |
| --| --| --|
| `treasury` | `address payable` | Set to the `msg.sender` address submitting the `registerValidator` method call transaction |
| `nodeAddress` | `address` | Set to temporary value of `0` before assignment |
| `oracleAddress`| `string` | Assigned the value of the `_oracleAddress` argument to the method call |
| `enode`| `string` | Assigned the value of the `_enode` argument to the method call |
| `commissionRate` | | Assigned the value of the `delegationRate` parameter in the genesis configuration file |
| `bondedStake` | `uint256` | Set to the value of `0`. There is no stake bonded to the newly registered validator at this point. |
| `totalSlashed` | `uint256` | Set to the value of `0`. The counter recording the number of times the validator has been penalised for accountability and omission faults is set to `0`. |
| `liquidContract` | `address`| address of the newly registered validator's Liquid Newton Contract |
| `liquidSupply` | `uint256` | Set to the value of `0`. There is no liquid token supply until stake is bonded to the newly registered validator. |
| `registrationBlock` | `uint256` | Set to the number of the block that the register validator transaction will be committed |
| `state` | `ValidatorState` | Set to `active` |

Constraint checks are applied:

- the `enode` URL is not empty and is correctly formed
- the `address` of the validator is not already registered
- the `proof` of node ownership is valid: a cryptographic proof containing the string of the validator's `treasury` account address signed by (a) the validator's private P2P node key and (2) the validator's oracle server private key. The two signatures are concatenated together to create the ownership proof. The validator's `treasury` account address is recovered from the proof using the public key of (1) the validator's P2P node key and (2) the oracle server key.

Validator registration is then executed, the temporary address assignments updated, and the new validator object appended to the indexed validator list recorded in system state. I.E. the most recently registered validator will always have the highest index identifier value and will always be the last item in the validator list returned by a call to get a network's registered validators (see [`getValidators`](/reference/api/aut/#getvalidators)).

A validator-specific Liquid Newton contract is deployed; the contract's `name` and `symbol` properties are both set to `LNTN-<ID>` where `<ID>` is the validator's registration index identifier.


### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_enode` | `string` | the enode url for the validator node  |
| `_oracleAddress` | `address` | the oracle server identifier account address |
| `_multisig` | `bytes` | the proof of node ownership. A combination of two signatures of the validator `treasury` account address string, appended sequentially, generated using (a) the validator P2P node key private key, (2) the Oracle server private key. |

### Response

No response object is returned on successful execution of the method call.

The validator registration entry can be retrieved from state by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits a `RegisteredValidator` event, logging: `msg.sender`, `_val.nodeAddress`, `_oracleAddress`, `_enode`, `address(_val.liquidContract)`.


### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator register [OPTIONS] ENODE PROOF
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.registerValidator('`_enode`','`proof`').send()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator register --rpc-endpoint https://rpc1.piccadilly.autonity.org enode://c746ded15b4fa7e398a8925d8a2e4c76d9fc8007eb8a6b8ad408a18bf66266b9d03dd9aa26c902a4ac02eb465d205c0c58b6f5063963fc752806f2681287a915@51.89.151.55:30303 0xc68fcac6ba8e9f565ab3c1be1a08571f1f0740d6fe1093741276a8327e8c096e4abda696773050e14b94385cb9c0f175a422efed9c24bc1d88803bcd508c50ce0170591627ab24883e9be5465bc1fa8c3514e095389edbc44846bf6bfab6b8d6be07a534c2fbaa07f5d96ced57eb0296b592dc73fad3b8df5d8072b5d213a4a0e401 | aut tx sign - | aut tx send -
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.registerValidator('enode://9c863def6b9e53b66b19c3ac8746b2118c37650fdcf53be599ef35715c088c40669e59de68ca3ba56d82f766fefbfbde75c65056a4e212e0d606a2eceb833a51@51.89.151.55:30303?discport=0', 1000).send({from: myAddress, gas: gas})
{
  blockHash: '0x94ff71aa5939c6c05ca6062864e3abd80fd9740ba21f39a433845e58b4ec375d',
  blockNumber: 588576,
  contractAddress: null,
  cumulativeGasUsed: 1668883,
  from: '0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4',
  gasUsed: 1668883,
  logsBloom: '0x00004000000000000000000000020000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0x29f20ce829c84a3b3366b6cc5bd454ed14f2fe6bb68f68dd5b5d0e8b2ceb60ef',
  transactionIndex: 0,
  events: {
    RegisteredValidator: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 588576,
      transactionHash: '0x29f20ce829c84a3b3366b6cc5bd454ed14f2fe6bb68f68dd5b5d0e8b2ceb60ef',
      transactionIndex: 0,
      blockHash: '0x94ff71aa5939c6c05ca6062864e3abd80fd9740ba21f39a433845e58b4ec375d',
      logIndex: 0,
      removed: false,
      id: 'log_bab633bc',
      returnValues: [Result],
      event: 'RegisteredValidator',
      signature: '0x6921859367aca5023ddf910758cd0cda74261b2e5c8425c253e9d03b62b950b8',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->

## symbol

Returns the three-letter symbol of the Newton stake token as a string. Set as contract metadata to the value of `NTN`.

Using `aut` you can return the symbol for an ERC20 token contract account, e.g. a Liquid Newton contract.

### Parameters

None.

### Response

| Returns | Datatype | Description |
| --| --| --|
| value | `string` | the symbol for the Newton stake token - `NTN` |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token symbol [OPTIONS]
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.symbol().call()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_symbol", "params":[]}
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token symbol --ntn -r https://rpc1.piccadilly.autonity.org
NTN
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_symbol", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":"NTN"}
{{< /tab >}}
{{< /tabpane >}}

<!--

{{< tab header="NodeJS Console" >}}
> autonity.symbol().call()
'NTN'
{{< /tab >}}
-->

To return the `symbol` for an ERC20 (e.g. a Liquid Newton token) token contract specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token symbol --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37
LNTN-0
{{< /tab >}}
{{< /tabpane >}}

## tailBondingID

Returns the index identifier of the last processed bonding request.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the unique tail identifier of the pending bonding request |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol tail-bonding-id [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_tailBondingID", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.tailBondingID().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol tail-bonding-id --rpc-endpoint https://rpc1.piccadilly.autonity.org
139
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_tailBondingID", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":139}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.tailBondingID().call()
'43665'
{{< /tab >}}
-->
## tailUnbondingID

Returns the index identifier of the last processed unbonding request.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the unique tail identifier of the pending unbonding request |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol tail-unbonding-id [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_tailUnbondingID", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.tailUnbondingID().call()
{{< /tab >}}
-->
### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol tail-unbonding-id --rpc-endpoint https://rpc1.piccadilly.autonity.org
48
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_tailUnbondingID", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":48}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.tailUnbondingID().call()
'2'
{{< /tab >}}
-->
## totalRedistributed

Returns the total amount of staking rewards distributed since genesis minus treasury fee.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the amount of Auton utility token distributed as staking rewards |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol total-redistributed [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_totalRedistributed", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.totalRedistributed().call()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol total-redistributed -r https://rpc1.piccadilly.autonity.org
47981813599875371606
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_totalRedistributed", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":47981813599875371606}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.totalRedistributed().call()
'7052488137400919237'
{{< /tab >}}
-->

## totalSupply

Returns the total supply of Newton stake token in circulation.

Using `aut` you can return the allowance for an ERC20 token contract account, e.g. a Liquid Newton account.

### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| `stakeSupply` | `uint256` | the total supply of Newton in circulation |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token total-supply [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_totalSupply", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.totalSupply().call()
{{< /tab >}}
-->

### Example

To return total supply for the Newton stake token specify the `--ntn` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token total-supply --ntn -r https://rpc1.piccadilly.autonity.org
63402
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_totalSupply", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":63402}
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.totalSupply().call()
'100000134027'
{{< /tab >}}
-->

To return the total supply for an ERC20 contract token (e.g. Liquid Newton) specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token total-supply --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37   -r https://rpc1.piccadilly.autonity.org
10087
{{< /tab >}}
{{< /tabpane >}}


## transfer

Transfers a designated amount of Newton stake token from the caller account to a recipient account.

Constraint checks:

- the `amount` value is `>= 0`
- the caller's account balance is `>= amount`

Using `aut` you can transfer from an ERC20 token contract account, e.g. a Liquid Newton account.


### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_recipient` | `address` | the recipient address |
| `_amount` | `uint256` | the value amount of Newton stake tokens being transferred |

### Response

The method returns a boolean flag specifying whether the `transfer` was executed or not.

### Event

On a successful call the function emits a `Transfer` event, logging: `msg.sender`, `_recipient`, `amount`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token transfer [OPTIONS] RECIPIENT AMOUNT
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.transfer(_recipient, _amount).send()
{{< /tab >}}
-->

### Example

To transfer an amount of Newton stake token to a recipient specify the `--ntn` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token transfer --ntn 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 1| aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x17092d181653c4f13642698233966010a83a39f34846f65cef7dc860ad13644d
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.transfer('0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4', 100).send({from: myAddress, gas: gas})
{
  blockHash: '0xeea1c7ec34991521ebdf1052aa2cbaf1e32ad7cec4b16b7ca7ff14ab2c714b47',
  blockNumber: 584585,
  contractAddress: null,
  cumulativeGasUsed: 37614,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 37614,
  logsBloom: '0x00004000000000000000000000020400000000010000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000004000000002000000000000000000000000000000000000000000000002000000000000000000000000000000000000000080000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0x3e127847baac07a78c44a2d158e2e19d92917d9df790523cafc105adfac323db',
  transactionIndex: 0,
  events: {
    Transfer: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 584585,
      transactionHash: '0x3e127847baac07a78c44a2d158e2e19d92917d9df790523cafc105adfac323db',
      transactionIndex: 0,
      blockHash: '0xeea1c7ec34991521ebdf1052aa2cbaf1e32ad7cec4b16b7ca7ff14ab2c714b47',
      logIndex: 0,
      removed: false,
      id: 'log_ea603180',
      returnValues: [Result],
      event: 'Transfer',
      signature: '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->

To transfer an amount from an ERC20 contract token (e.g. Liquid Newton) to a recipient specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token transfer --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 10 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x2d78e64d82d1e54aeb487c4c10834dc3a1e17fabbd1f5775a2d72c6390db7b26
{{< /tab >}}
{{< /tabpane >}}


##  transferFrom

Transfers a designated amount of Newton stake token from a specified sender account to a recipient account.

The `transferFrom` method is used for withdraw workflows where the sender account has authorised the method caller (the `spender`, the `msg.sender`) to transfer tokens on the sender's behalf.

Constraint checks:

- `sender` and `recipient` accounts must be allowed to hold Newton stake token
- `sender` must have an account balance `>= amount`
- the `msg.sender` has been approved by the `sender` to withdraw tokens from their account
- the `msg.sender`'s remaining allowance to withdraw `sender`'s tokens is `>= amount`

Using `aut` you can call `transferFrom` on an ERC20 token contract (e.g. Liquid Newton) account.

### Parameters

| Field | Datatype | Description |
| --| --|  --|
| `sender` | `address` | the account from which Newton stake token are being transferred |
| `recipient` | `address` | the account to which Newton stake token are being transferred |
| `amount` | `uint256` | the value amount of Newton stake tokens being transferred |

### Response

The method returns a boolean flag specifying whether the `transfer` was executed or not.

### Event

On a successful call the function emits:

- a `Transfer` event, logging: `msg.sender`, `_recipient`, `amount`.
- an `Approval` event, logging: `owner`, `spender`, `amount`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut token transfer-from [OPTIONS] SPENDER RECIPIENT AMOUNT
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.transferFrom('sender', 'recipient', amount).send()
{{< /tab >}}
-->

### Example

To transfer an amount of Newton stake token to a recipient specify the `--ntn` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token transfer-from --ntn --from 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 0x11a87b260dd85ff7189d848fd44b28cc8505fa9c 0xbf2f718f948de541123f3e0a06a9100ee1df128c 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x2d277f8eee73d900f3cb3994796cfbb4ddef22ca78870344bf910bbd1b64f22c
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.transferFrom('0x11a87b260dd85ff7189d848fd44b28cc8505fa9c', '0xbf2f718f948de541123f3e0a06a9100ee1df128c', 51).send({from: myAddress, gas: gas})
{
  blockHash: '0x4826ccf629c565546c050e58cf8c464a3ba0105dd46c9f69e63f38cf30b48db5',
  blockNumber: 585558,
  contractAddress: null,
  cumulativeGasUsed: 61622,
  from: '0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4',
  gasUsed: 61622,
  logsBloom: '0x00004000000000000000000000020400000000010000000000001000000000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000002000000004000000002000000000000000000200000000000000000000000000002000000000010000000000000000000000000000080000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0xbcb5bbce024293e0abb152c1b1d88b2adfc17958ba6b0e79b52aca212c45fec4',
  transactionIndex: 0,
  events: {
    Transfer: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 585558,
      transactionHash: '0xbcb5bbce024293e0abb152c1b1d88b2adfc17958ba6b0e79b52aca212c45fec4',
      transactionIndex: 0,
      blockHash: '0x4826ccf629c565546c050e58cf8c464a3ba0105dd46c9f69e63f38cf30b48db5',
      logIndex: 0,
      removed: false,
      id: 'log_768f1475',
      returnValues: [Result],
      event: 'Transfer',
      signature: '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
      raw: [Object]
    },
    Approval: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 585558,
      transactionHash: '0xbcb5bbce024293e0abb152c1b1d88b2adfc17958ba6b0e79b52aca212c45fec4',
      transactionIndex: 0,
      blockHash: '0x4826ccf629c565546c050e58cf8c464a3ba0105dd46c9f69e63f38cf30b48db5',
      logIndex: 1,
      removed: false,
      id: 'log_a4e7164e',
      returnValues: [Result],
      event: 'Approval',
      signature: '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->

To transfer an amount from an ERC20 contract token (e.g. Liquid Newton) to a recipient specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token transfer-from --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37  --from 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 0x11a87b260dd85ff7189d848fd44b28cc8505fa9c 0xbf2f718f948de541123f3e0a06a9100ee1df128c 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x64a88723d7dd99e026029db531b6415e6e7a19fe131395059742065fcfe6575c
{{< /tab >}}
{{< /tabpane >}}


## unbond

Unbonds an amount of Liquid Newton stake token from a designated validator.

On successful execution of the method call the designated amount of Liquid Newton amount is burnt, the unbonding period begins, and an unbonding object for the necessary voting power change and tracked in memory until applied at the end of the epoch in which the unbonding period expires. At that block point  Newton redemption occurs and due Newton is minted to the staker's Newton account.

Constraint checks:

- the `validator` address is registered as a validator
- the Liquid Newton balance of the account submitting  the `unbond()` method call has a balance `>=` to the `amount` being unbonded

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator`  | `address` | the [validator identifier](/concepts/validator/#validator-identifier) address |
| `amount` | `uint256` | the amount of Liquid Newton to be unbonded from the validator |

### Response

No response object is returned on successful execution of the method call.

The pending voting power change is tracked in memory until applied and can be returned by calling:

- the [`tailUnbondingID`](/reference/api/aut/#tailunbondingid) method to return the ID of the unbonding request, and
- the [`getUnbondingReq`](/reference/api/aut/#getunbondingreq) method to return metadata including the start block when the unbonding will be applied.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator unbond [OPTIONS] AMOUNT
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.unbond('_validator', amount).send()
{{< /tab >}}
-->

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut validator unbond --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9  1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x3ac340e33f5ddfdab04ffe85ce4b564986b2f1a877720cb79bc9d31c11c8f318
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.unbond('0xC2B1be82bdC33b5bA3825Cf0A2036305E78a5afa', 10).send({from: myAddress, gas: gas})
{
  blockHash: '0x0684d2639e65d3051e67a322b9ec90e0f53cd5b7e6cb5c35f70a14bc5a5a7bdc',
  blockNumber: 587534,
  contractAddress: null,
  cumulativeGasUsed: 150977,
  from: '0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4',
  gasUsed: 150977,
  logsBloom: '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0xe8dce29963dc069c0c74eb10c4cea2fbf6d647c40a1e3c12001255963a45ea32',
  transactionIndex: 0,
  events: {}
}
{{< /tab >}}
-->
