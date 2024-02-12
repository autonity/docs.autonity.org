---
title: "Autonity Contract Interface"

description: >
  Autonity Protocol Contract functions
---

Interface for interacting with Autonity Contract functions using:

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
- the validator state must not be `active`; it must be `paused` or `jailed`
- if the validator state is `jailed`, the validator's `jailReleaseBlock` is less than the current block number at the time of the call

Validator re-activation is executed on transaction commit. New stake delegations to the validator are accepted and the validator is included in the consensus committee selection algorithm at epoch end.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_address` | `address` | the validator identifier account address |

### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits an `ActivatedValidator` event, logging: `val.treasury`, `_address`, `effectiveBlock`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator activate --validator _address
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator activate --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 

0x0849c0307bc446bb3fbb61b5c1518847574356aedb0b986248158d36f1eb2a5b
{{< /tab >}}
{{< /tabpane >}}


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

To return an ERC20 contract token (e.g. Liquid Newton) balance for an account specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token balance-of --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 0x11a87b260dd85ff7189d848fd44b28cc8505fa9c
999.000000000000000000
{{< /tab >}}
{{< /tabpane >}}

{{< alert title="Info" >}}
All Liquid Newton balances for an account can be returned in one call using the `aut` command `aut account lntn-balances [OPTIONS] ACCOUNT`.
{{< /alert >}}


## bond

Delegates an amount of Newton stake token to a designated validator. If the delegator's `msg.Sender` address is the validator `treasury` account then the stake is self-bonded and no Liquid Newton will be issued.

Constraint checks:

- the `validator` address is registered as a validator
- the `validator` state is `active`. A bonding operation submitted to a validator in a `paused`, `jailed` or `jailbound` state will revert
- the `amount` is a positive integer value `> 0`
- the Newton balance of the account submitting  the `bond()` method call has a Newton balance`>=` to the `amount` being bonded.

On successful processing of the method call:

- the bonded Newton amount is locked in the `msg.Sender`'s Newton account
- a `BondingRequest` object for the necessary voting power change is created:

| Field | Datatype | Description |
| --| --| --|
| `delegator` | `address payable` | account address of the account bonding stake |
| `delegatee` | `address` | validator identifier account address of the validator to which stake is being bonded |
| `amount` | `uint256` | the amount of Newton stake token being bonded to the `delegatee` account |
| `requestBlock` | `uint256` | the block number at which a bonding transaction was committed |

The `BondingRequest` is tracked in memory until applied at epoch end. At that block point, if the stake delegation is [delegated](/glossary/#delegated) and not [self-bonded](/glossary/#self-bonded), then Liquid Newton will be minted to the delegator for the bonded stake amount.

{{< alert title="Note" >}}
Liquid Newton is *not* issued for self-bonded stake. See Concept [Staking](/concepts/staking/) and [Penalty Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas).
{{< /alert >}}

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `validator`  | `address` | the [validator identifier](/concepts/validator/#validator-identifier) address |
| `amount` | `uint256` | the amount of Newton bonded to the validator |

### Response

No response object is returned on successful execution of the method call.

The pending voting power change is tracked in memory until applied.

### Event

The function emits events:

- on success, a `NewBondingRequest` event, logging: `validator` address, `delegator` address, `selfBonded` (boolean), `amount` bonded.
- on revert, a `BondingRejected` event, logging: `delegator` address, `delegatee` address, `amount` bonded, validator `state`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator bond [OPTIONS] AMOUNT
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator bond --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xaa3705ef2d38cf2d98925660e6ca55de8948e8a075e7ee9edf6be7fa540ffe51
{{< /tab >}}
{{< /tabpane >}}


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

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator change-commission-rate --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9 900 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x7a4c6bb2e19eb8a4a160723b07eeb538e835db512541621aef0062cd9e1e15f2
{{< /tab >}}
{{< /tabpane >}}


## config

Returns the Autonity Network configuration at the block height the call was submitted.

### Parameters

None.

### Response

Returns a `Config` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `treasuryFee` | `uint256` | the percentage of staking rewards deducted from staking rewards and sent to the Autonity Treasury account for community funding before staking rewards are distributed |
| `minBaseFee` | `uint256` | the minimum gas price for a unit of gas used to compute a transaction on the network, denominated in [ton](/glossary/#ton) |
| `delegationRate` | `uint256` | the percentage of staking rewards deducted by validators as a commission from delegated stake |
| `unbondingPeriod` | `uint256` | the period of time for which bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction, defined as a number of blocks |
| `treasuryAccount` | `address payable` | the address of the Autonity Treasury account for community funds |
| `accountabilityContract` | `address` | the address of the Autonity Accountability Contract |
| `oracleContract` | `address` | the address of the Autonity Oracle Contract |
| `acuContract` | `address` | the address of the Autonity ASM ACU Contract |
| `supplyControlContract` | `address` | the address of the Autonity ASM Supply Control Contract |
| `stabilizationContract` | `address` | the address of the Autonity ASM Stabilization Contract |
| `operatorAccount` | `address` | the address of the Autonity governance account |
| `epochPeriod` | `uint256` | the period of time for which a consensus committee is elected, defined as a number of blocks |
| `blockPeriod` | `uint256` | the minimum time interval between two consecutive blocks, measured in seconds |
| `committeeSize` | `uint256` | the maximum number of validators that may be members of a consensus committee on the network |
| `contractVersion` | `uint256 ` | the version number of the Autonity Protocol Contract. An integer value set by default to `1` and incremented by `1` on contract upgrade |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol config [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_config", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol config -r https://rpc1.piccadilly.autonity.org
{
  "policy": {
    "treasury_fee": 10000000000000000,
    "min_basefee": 500000000,
    "delegation_rate": 1000,
    "unbonding_period": 21600,
    "treasury_account": "0xF74c34Fed10cD9518293634C6f7C12638a808Ad5"
  },
  "contracts": {
    "accountability_contract": "0x5a443704dd4B594B382c22a083e2BD3090A6feF3",
    "oracle_contract": "0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D",
    "acu_contract": "0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA",
    "supply_control_contract": "0x47c5e40890bcE4a473A49D7501808b9633F29782",
    "stabilization_contract": "0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f"
  },
  "protocol": {
    "operator_account": "0xd32C0812Fa1296F082671D5Be4CbB6bEeedC2397",
    "epoch_period": 1800,
    "block_period": 1,
    "committee_size": 100
  },
  "contract_version": 1
}
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_config", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":[{"treasuryFee":10000000000000000,"minBaseFee":500000000,"delegationRate":1000,"unbondingPeriod":21600,"treasuryAccount":"0xf74c34fed10cd9518293634c6f7c12638a808ad5"},{"accountabilityContract":"0x5a443704dd4b594b382c22a083e2bd3090a6fef3","oracleContract":"0x47e9fbef8c83a1714f1951f142132e6e90f5fa5d","acuContract":"0x8be503bcded90ed42eff31f56199399b2b0154ca","supplyControlContract":"0x47c5e40890bce4a473a49d7501808b9633f29782","stabilizationContract":"0x29b2440db4a256b0c1e6d3b4cdcaa68e2440a08f"},{"operatorAccount":"0xd32c0812fa1296f082671d5be4cbb6beeedc2397","epochPeriod":1800,"blockPeriod":1,"committeeSize":100},1]}
{{< /tab >}}
{{< /tabpane >}}


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

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol epoch-total-bonded-stake --rpc-endpoint https://rpc1.piccadilly.autonity.org
61338
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_epochTotalBondedStake", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":61338}
{{< /tab >}}
{{< /tabpane >}}



## getBlockPeriod

Returns the block period from the protocol configuration.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `blockPeriod` | `uint256` | the minimum time interval between two consecutive blocks, measured in seconds |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-block-period [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getBlockPeriod", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-block-period --rpc-endpoint https://rpc1.piccadilly.autonity.org
1
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_getBlockPeriod", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":1}
{{< /tab >}}
{{< /tabpane >}}


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
{"jsonrpc":"2.0","id":1,"result":[{"addr":"0x4b7275d5f5292c3027a16e0eb891d75a0ef39cc7","votingPower":10000},{"addr":"0x5e08564ee99e96e690e9b25591191ae0c78351a3","votingPower":10000},{"addr":"0x33bf54630991f0a1a23b9f102873b3b54c4b94b3","votingPower":10000},{"addr":"0x1ae9b1b3207195430a36d82fc0bda1f857d0aa72","votingPower":10000},{"addr":"0x0c7dc2ab00c7b5934eda097a8585f56367a94da4","votingPower":10000},{"addr":"0xf5a48b1df2a3a616adb92e57d6ce36e17c3c2a0b","votingPower":10000},{"addr":"0x5fe87ee4f61da6e640aec02ce818cdcd30b8cb13","votingPower":10000},{"addr":"0xebf9dd85cc99a15f1afb78a6a7cb28a9103e9a12","votingPower":10000},{"addr":"0x9f26942a9710099a7f2b4b64e53522bb16d2af7d","votingPower":10005}]}
{{< /tab >}}
{{< /tabpane >}}


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

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-committee-enodes -r https://rpc1.bakerloo.autonity.org
['enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303', 'enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303', 'enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303', 'enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308', 'enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309', 'enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310', 'enode://c6ae16b58cf2e073649ec34ed59550c57389fcb949f51b806d6f7de26e7961cfc33794fde67b484ce9966a30e5ab5331c610b1b659249a6d66cc9e6d8a3d23d1@143.198.240.242:30303', 'enode://06facaec377a55fe8fd9e30cc922bedc7ee97e292294435635fa3b053c30215b87954daa27c79a73e3a5013124318b084907c81f518bcf36f88dad4d01e952ec@138.68.118.4:30303', 'enode://0c71d8076f0543505aae22901471d5437f1fd92b3d154d154edcec5baf0d7b121e6e8dc85ae725daf77cbc50ff5616727d59d36c2606751401000580e155e2bc@5.181.104.29:30303']
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getCommitteeEnodes", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":["enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303","enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303","enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303","enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308","enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309","enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310","enode://c6ae16b58cf2e073649ec34ed59550c57389fcb949f51b806d6f7de26e7961cfc33794fde67b484ce9966a30e5ab5331c610b1b659249a6d66cc9e6d8a3d23d1@143.198.240.242:30303","enode://06facaec377a55fe8fd9e30cc922bedc7ee97e292294435635fa3b053c30215b87954daa27c79a73e3a5013124318b084907c81f518bcf36f88dad4d01e952ec@138.68.118.4:30303","enode://0c71d8076f0543505aae22901471d5437f1fd92b3d154d154edcec5baf0d7b121e6e8dc85ae725daf77cbc50ff5616727d59d36c2606751401000580e155e2bc@5.181.104.29:30303"]}
{{< /tab >}}
{{< /tabpane >}}


## getEpochFromBlock

Returns the unique identifier of the epoch block epoch associated with a block as an integer value.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_block` | `uint256` | the input block number |

### Response

| Field | Datatype | Description |
| --| --| --|
| `epochID` | `uint256` | the identifier of the epoch in which the block was committed to state |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-epoch-from-block [OPTIONS] BLOCK
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getEpochFromBlock", "params":[_block]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-epoch-from-block --rpc-endpoint https://rpc1.piccadilly.autonity.org 3293857
1829
{{< /tab >}}
{{< tab header="RPC" >}}
curl --location --request GET 'https://rpc1.bakerloo.autonity.org/' \
--header 'Content-Type: application/json' \
--data-raw '{
        "jsonrpc":"2.0",
        "method":"aut_getEpochFromBlock",
        "params":[1900],
        "id":1500
}'
{"jsonrpc":"2.0","id":1,"result":1}
{{< /tab >}}
{{< /tabpane >}}


## getEpochPeriod

Returns the epoch period from the protocol configuration.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `epochPeriod` | `uint256` | the period of time for which a consensus committee is elected, defined as a number of blocks |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-epoch-period [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getEpochPeriod", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-epoch-period --rpc-endpoint https://rpc1.piccadilly.autonity.org
1800
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_getEpochPeriod", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":1800}
{{< /tab >}}
{{< /tabpane >}}


## getLastEpochBlock

Returns the number of the last block in the preceding epoch at the block height of the call.

### Response

| Field | Datatype | Description |
| --| --| --|
| `lastEpochBlock` | `uint256` | the number of the last block in the preceding epoch |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-last-epoch-block [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_getLastEpochBlock", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol get-last-epoch-block -r https://rpc1.piccadilly.autonity.org
12981684
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_getLastEpochBlock", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":12981684}
{{< /tab >}}
{{< /tabpane >}}


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


##  getMinimumBaseFee

Returns the protocol setting for the minimum price per unit of gas for computing a transaction on an Autonity network.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `minBaseFee` | `uint256` | the minimum price per unit of gas, denominated in [ton](/glossary/#ton) |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-minimum-base-fee [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getMinimumBaseFee", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

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

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-operator -r https://rpc1.bakerloo.autonity.org/
0x293039dDC627B1dF9562380c0E5377848F94325A
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.bakerloo.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getOperator", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":"0x293039dDC627B1dF9562380c0E5377848F94325A"}
{{< /tab >}}
{{< /tabpane >}}


## getOracle

Returns the address of the Autonity Oracle Contract.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the oracle contract account address |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="RPC" >}}
{"method": "aut_getOracle", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_getOracle", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":"0x47e9fbef8c83a1714f1951f142132e6e90f5fa5d"}
{{< /tab >}}
{{< /tabpane >}}


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

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-proposer -r https://rpc1.bakerloo.autonity.org/ 4576868 0
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


## getTreasuryAccount

Returns the address of the Autonity treasury account.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the Autonity treasury account address |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-treasury-account [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_getTreasuryAccount", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-treasury-account -r https://rpc1.piccadilly.autonity.org/
0xF74c34Fed10cD9518293634C6f7C12638a808Ad5
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getTreasuryAccount", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":"0xf74c34fed10cd9518293634c6f7c12638a808ad5"}
{{< /tab >}}
{{< /tabpane >}}

## getTreasuryFee

Returns the percentage of staking rewards deducted from staking rewards by the protocol. Treasury fees ared sent to the Autonity Treasury account for community funding before staking rewards are distributed.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `treasuryFee` | `uint256` | the Autonity treasury account address. The value is returned in `10^18` format. |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-treasury-fee [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method":"aut_getTreasuryFee", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-treasury-fee -r https://rpc1.piccadilly.autonity.org/
10000000000000000
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getTreasuryFee", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":10000000000000000}
{{< /tab >}}
{{< /tabpane >}}


## getUnbondingPeriod

Returns the unbonding period from the protocol configuration.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `unbondingPeriod` | `uint256` | the period of time for which bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction, defined as a number of blocks |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-unbonding-period [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getUnbondingPeriod", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol get-unbonding-period -r https://rpc1.piccadilly.autonity.org/
21600
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"method":"aut_getUnbondingPeriod", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":21600}
{{< /tab >}}
{{< /tabpane >}}


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
| `unbondingStake` | `uint256` | the total amount of NTN in the unbonding staking pool |
| `unbondingShares` | `uint256` | the total amount of shares issued for the unbonding staking pool |
| `selfBondedStake` | `uint256` | the total amount of 'self-bonded' stake that has been bonded to the validator by the validator operator |
| `selfUnbondingStake` | `uint256` | the total amount of NTN in the self-unbonding staking pool |
| `selfUnbondingShares` | `uint256` | the total amount of shares in the self-unbonding staking pool |
| `selfUnbondingStakeLocked` | `uint256` | the total amount of NTN in the self-unbonding staking pool that is locked pending unbonding |
| `liquidContract` | `Liquid` | the address of the validator's Liquid Newton contract |
| `liquidSupply` | `uint256` | the total amount of Liquid Newton in circulation |
| `registrationBlock` | `uint256` | the block number in which the registration of the validator was committed to state|
| `totalSlashed` | `uint256` | the total amount of stake that a validator has had slashed for accountability and omission faults since registration |
| `jailReleaseBlock` | `uint256` | the block number at which a validator jail period applied for an accountability or omission fault ends (the validator can be re-activated after this block height). Set to `0` when the validator is in an active or jailbound state |
| `provableFaultCount` | `uint256` | a counter of the number of times that a validator has been penalised for accountability and omission faults since registration |
| `ValidatorState` | `state` | the state of the validator. `ValidatorState` is an enumerated type with enumerations: `0`: active, `1`: paused, `2`: jailed, `3`: jailbound |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator info [OPTIONS]
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_getValidator", "params":[_addr]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut validator info --rpc-endpoint https://rpc1.piccadilly.autonity.org --validator 0x21bb01ae8eb831fff68ebe1d87b11c85a766c94c
{
  "treasury": "0x61EE7d3244642E5f6D654416a098DEabFBF5306e",
  "node_address": "0x21bb01Ae8EB831fFf68EbE1D87B11c85a766C94C",
  "oracle_address": "0x9b844631B7279576330B9B822bE79266696fF8C2",
  "enode": "enode://b2748268c31ebab8603058335bb4bed062e05b9ceaa3562f69868a01d1038a84136fc587fb913e1cb8ce821f1eb0bf9879e3249f18adcd39f1211a104ceb57a9@35.197.223.249:30303",
  "commission_rate": 1000,
  "bonded_stake": 10000000000000000000000,
  "unbonding_stake": 0,
  "unbonding_shares": 0,
  "self_bonded_stake": 10000000000000000000000,
  "self_unbonding_stake": 0,
  "self_unbonding_shares": 0,
  "liquid_contract": "0x0000000000000000000000000000000000000000",
  "liquid_supply": 1397840815523076466699159265359708166239426845751,
  "registration_block": 0,
  "total_slashed": 0,
  "jail_release_block": 0,
  "provable_fault_count": 0,
  "state": 0
}
{{< /tab >}}
{{< tab header="RPC" >}}
$ curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_getValidator", "params":["0x21bb01ae8eb831fff68ebe1d87b11c85a766c94c"], "id":1}'
{"jsonrpc":"2.0","id":1,"result":{"treasury":"0x61ee7d3244642e5f6d654416a098deabfbf5306e","nodeAddress":"0x21bb01ae8eb831fff68ebe1d87b11c85a766c94c","oracleAddress":"0x9b844631b7279576330b9b822be79266696ff8c2","enode":"enode://b2748268c31ebab8603058335bb4bed062e05b9ceaa3562f69868a01d1038a84136fc587fb913e1cb8ce821f1eb0bf9879e3249f18adcd39f1211a104ceb57a9@35.197.223.249:30303","commissionRate":1000,"bondedStake":10000000000000000000000,"unbondingStake":0,"unbondingShares":0,"selfBondedStake":10000000000000000000000,"selfUnbondingStake":0,"selfUnbondingShares":0,"selfUnbondingStakeLocked":0,"liquidContract":"0xf4d9599afd90b5038b18e3b551bc21a97ed21c37","liquidSupply":0,"registrationBlock":0,"totalSlashed":0,"jailReleaseBlock":0,"provableFaultCount":0,"state":0}}
{{< /tab >}}
{{< /tabpane >}}


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


{{< alert title="Info" >}}
`getValidators` can also be called using the `aut` command `aut protocol get-validators`.
{{< /alert >}}

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

To return the `name` for an ERC20 (e.g. a Liquid Newton token) token contract specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token name --rpc-endpoint https://rpc1.piccadilly.autonity.org --token 0xC500751c4F96d49B954D20EAE42Fa29278B96beB
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

Validator pausing is executed on transaction commit. New stake delegations are reverted from submission of the pausing transaction. Exclusion of the validator from the consensus committee selection algorithm takes effect at epoch end (i.e. the 'effective block').

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_address` | `address` | the validator identifier account address |

### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits a `PausedValidator` event, logging: `val.treasury`, `_address`, `effectiveBlock`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator pause [OPTIONS]
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator pause --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x942328bea54a0096ca9b2fb88acd337c883f7923c2ef6b8290a340c5baec2d20
{{< /tab >}}
{{< /tabpane >}}


## registerValidator

Registers a validator on an Autonity Network.

The `registerValidator` method provides as argument the [enode](/glossary/#enode) URL of the validator node, the validator's oracle server address, and a proof of node ownership generated using the private key of the validator node's [P2P node key](/concepts/validator/#p2p-node-key) and the validator's [oracle server key](/concepts/oracle-network/#oracle-server-key).

On method execution a `Validator` object data structure is constructed in memory, populated with method arguments and default values ready for validator registration processing:

| Field | Datatype | Description |
| --| --| --|
| `treasury` | `address payable` | Set to the `msg.sender` address submitting the `registerValidator` method call transaction |
| `nodeAddress` | `address` | Set to temporary value of `0` before assignment of the actual validator node identifier address value|
| `oracleAddress`| `string` | Assigned the value of the `_oracleAddress` argument to the method call |
| `enode`| `string` | Assigned the value of the `_enode` argument to the method call |
| `commissionRate` | | Assigned the value of the `delegationRate` parameter in the genesis configuration file |
| `bondedStake` | `uint256` | Set to `0`. There is no stake bonded to the newly registered validator at this point. |
| `unbondingStake` | `uint256` | Set to `0`. There is no stake in the unbonding staking pool at this point |
| `unbondingShares` | `uint256` | Set to `0`. There are no  shares issued for the unbonding staking pool at this point |
| `selfBondedStake ` | `uint256` | Set to `0`. There is no self-bonded stake to the newly registered validator at this point |
| `selfUnbondingStake` | `uint256` | Set to `0`. There is no stake in the self-unbonding staking pool at this point |
| `selfUnbondingShares` | `uint256` | Set to `0`. There are no  shares issued for the self-unbonding staking pool at this point |
| `selfUnbondingStakeLocked` | `uint256` | Set to `0`. There is no stake in the self-unbonding staking pool at this point that is locked pending unbonding |
| `liquidContract` | `address` | Set to the contract address of the newly registered validator's Liquid Newton Contract |
| `liquidSupply` | `uint256` | Set to `0`. There is no liquid token supply until stake is bonded to the newly registered validator |
| `registrationBlock` | `uint256` | Set to current block number (the number of the block that the register validator transaction will be committed in) |
| `totalSlashed` | `uint256` | Set to `0`. (The total amount of stake that a validator has had slashed for accountability and omission faults since registration.) |
| `jailReleaseBlock` | `uint256` | Set to `0`. (The block number at which a validator jail period applied for an accountability or omission fault ends.) |
| `provableFaultCount` | `uint256` | Set to `0`. (Counter recording the number of times the validator has been penalised for accountability and omission faults.) |
| `ValidatorState` | `state` | Set to `active`. |


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
aut validator register [OPTIONS] ENODE ORACLE PROOF
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator register enode://a3b821f89d8ea172421dedacdb00e76d8d6a929e4c5ff3c2b30ec84144a7405698ce30ba2ed482770ad2df94d050311b350c036d7f2cef3c9ef32be3f635d62e@51.89.151.55:30303 0xFd91928d58Af4AFbD78C96821D3147ef1f517072 0x62a44f56a617520ebc7c73414df7b8ae5b8133ebdbc0715d66ca0522fe26788873c7e774ed8a7702e16311e6ee8f149c4ef70cfb261fbdd3d375401375209a3000a5189e8d50880faf97ad42501375b216b89304c3fd4acf548a1d7fd7136e74771791422819134e2e3fbf720c35652d8c163e3d4f22c798a3c648958f7abcda2c00 | aut tx sign - | aut tx send -
{{< /tab >}}
{{< /tabpane >}}


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
{{< tab header="RPC" >}}
{"method":"aut_symbol", "params":[]}
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token symbol --ntn --rpc-endpoint https://rpc1.piccadilly.autonity.org
NTN
{{< /tab >}}
{{< tab header="RPC" >}}
curl -X GET 'https://rpc1.piccadilly.autonity.org/'  --header 'Content-Type: application/json' --data '{"jsonrpc":"2.0", "method":"aut_symbol", "params":[], "id":1}'
{"jsonrpc":"2.0","id":1,"result":"NTN"}
{{< /tab >}}
{{< /tabpane >}}

To return the `symbol` for an ERC20 (e.g. a Liquid Newton token) token contract specify the `--token` option:

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut token symbol --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37
LNTN-0
{{< /tab >}}
{{< /tabpane >}}

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

Unbonds an amount of bonded stake from a designated validator.

The amount specifies Newton stake token if the delegator is unbonding [self-bonded](/glossary/#self-bonded) stake, else Liquid Newton if [delegated](/glossary/#delegated) stake is being unbonded.

::: {.callout-important title="Warning" collapse="false"}
The unbonding request will only be effective after the unbonding period, rounded to the next epoch.

If the validator has a [slashing](/concepts/accountability/#slashing) event before this period expires, then the released Newton stake token amount may or may not correspond to the amount requested.

See Concept [Accountability and fault detection (AFD)](/concepts/accountability/) for Autonity's slashing mechanism.
:::

Constraint checks are applied. The  `validator` address provided is verified as a registered validator address and the requested unbonding amount is checked to verify it is `<=` to the `msg.sender`'s bonded stake amount. For delegated stake this is done by checking the `msg.Sender`'s Liquid Newton balance is `>=` to the requested amount, and for self-bonded stake this is done by checking the validator's `selfBondedStake` balance is`>=` to the requested unbonding amount.

{{< alert title="Note" >}}
If `msg.Sender` is the validator `treasury` account, then Liquid Newton balance and supply checks are not required.

This is because Liquid Newton is *not* issued for self-bonded stake. See Concept [Staking](/concepts/staking/) and [Penalty Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas).
{{< /alert >}}

On successful processing of the method call, an `UnbondingRequest` object for the necessary voting power change is created:

| Field | Datatype | Description |
| --| --| --|
| `delegator` | `address payable` | account address of the account unbonding stake |
| `delegatee` | `address` | validator identifier account address of the validator from which stake is being unbonded |
| `amount` | `uint256` | the amount of stake being unbonded from the `delegatee` account. It records the amount unbound in (a) Newton stake token for [self-bonded](/glossary/#self-bonded) stake, or (b) Liquid Newton for [delegated](/glossary/#delegated) stake  |
| `unbondingShare` | `uint256` | the amount of shares issued for the unbonding staking pool that the unbonding amount represents |
| `requestBlock` | `uint256` | the block number at which an unbonding transaction was committed and from which the unbonding period begins |
| `unlocked` | `bool` | Boolean value indicating if the stake being unbonded is subject to a lock or not |
| `selfDelegation` | `bool` | Boolean value indicating if the unbonding is for [self-bonded](/glossary/#self-bonded) stake |

The [unbonding period](/glossary/#unbonding-period) begins in the next block. The `UnbondingRequest` is tracked in memory. At the end of the epoch in which the unbond request was processed:
  - the designated amount of Liquid Newton amount is unlocked and burnt if the stake being unbonded is [delegated](/glossary/#delegated) and *not* [self-bonded](/glossary/#self-bonded) stake
  - calculation of the amount of stake to deduct from the unbonding pool, as well as the delegator's share of the unbonding pool
  - the amount of Newton bonded to the validator is reduced by the unbonding amount

Then, at the end of the epoch in which the unbonding period expires Newton redemption occurs and the Newton that is due is minted to the staker's Newton account.

::: {.callout-important title="Warning" collapse="false"}
The amount of Newton released may be less than the unbonded amount if the validator has been slashed.
:::

- due Newton is minted to the delegator's Newton account.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator`  | `address` | the [validator identifier](/concepts/validator/#validator-identifier) address |
| `amount` | `uint256` | the amount of stake to be unbonded from the validator. Depending on the `msg.Sender` address the amount is for: (a) Newton stake token if the `msg.Sender` is the validator `treasury` and the unbond request is for [self-bonded](/glossary/#self-bonded) stake, or (b) Liquid Newton and the unbond request is for [delegated](/glossary/#delegated) stake |

### Response

No response object is returned on successful execution of the method call.

The pending voting power change is tracked in memory until applied.

### Event

On a successful call the function emits a `NewUnbondingRequest` event, logging: `validator` address, `delegator` address, `selfBonded` (boolean), `amount` unbonded.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut validator unbond [OPTIONS] AMOUNT
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut validator unbond --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9  1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x3ac340e33f5ddfdab04ffe85ce4b564986b2f1a877720cb79bc9d31c11c8f318
{{< /tab >}}
{{< /tabpane >}}
