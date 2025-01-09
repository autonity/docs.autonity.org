---
title: "Autonity Contract Interface"

description: >
  Autonity Protocol Contract functions
---

Interface for interacting with Autonity Contract functions using:

- Autonity CLI to submit calls to inspect state and state-affecting transactions.
- JSON-RPC methods to submit calls to inspect state.

Given an `RPC_URL` from <https://chainlist.org/?testnets=true&search=autonity>.

::: {.callout-note title="Info" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).
:::

## activateValidator

Changes the state of a paused validator on an Autonity Network from `paused` to `active`. (See [`pauseValidator`](/reference/api/aut/#pausevalidator) method.)

The `activateValidator` method provides as argument the [validator identifier](/concepts/validator/#validator-identifier) address.

On method execution the `Validator.state` object data property is updated in memory and set to `active`.

Constraint checks are applied:

- the `address` of the validator is registered
- the `msg.sender` address of the transaction is equal to the validator's `treasury` address
- the validator state must not be `active`; it must be `paused`, `jailed`, or `jailedForInactivity`
- if the validator state is `jailed` or `jailedForInactivity`, the validator's `jailReleaseBlock` is less than the current block number at the time of the call
- the validator state must not be in a permanently jailed state of `jailbound` or `jailboundForInactivity`

Validator re-activation is executed on transaction commit. New stake delegations to the validator are accepted and the validator is included in the consensus committee selection algorithm at epoch end.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_address` | `address` | the [validator identifier](/concepts/validator/#validator-identifier) account address |

### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits an `ActivatedValidator` event, logging: `treasury`, `addr`, `effectiveBlock`.

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut validator activate --validator _address
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut validator activate --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 

0x0849c0307bc446bb3fbb61b5c1518847574356aedb0b986248158d36f1eb2a5b
```
:::


## address

Returns the address of the Autonity Protocol Contract.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the Autonity Protocol contract account address |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut protocol contract-address
```

## RPC

``` {.rpc}
{"method": "aut_address", "params":[]}
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut protocol contract-address
0xBd770416a3345F91E4B34576cb804a576fa48EB1
```

## RPC

``` {.rpc}
curl -X GET $RPC_URL --header 'Content-Type: application/json' --data '{"method":"aut_address", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":"0xbd770416a3345f91e4b34576cb804a576fa48eb1"}
```
:::


## allowance

Returns the amount of stake token that remains available for a spender to withdraw from a Newton stake token owner's account.

Using `aut` you can return the allowance for an ERC-20 token contract account, e.g. a Liquid Newton account.

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


::: {.panel-tabset}
## aut

``` {.aut}
aut token allowance [OPTIONS] OWNER
```
:::


### Example

To return a spender's allowance for a Newton stake token account specify the `--ntn` option:


::: {.panel-tabset}
## aut
``` {.aut}
$ aut token allowance --ntn 0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C
100.000000000000000000
```
:::

To return a spender's allowance for an ERC-20 contract token (e.g. Liquid Newton) account specify the `--token` option:

::: {.panel-tabset}
## aut
``` {.aut}
$ aut token allowance --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37  0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C
1000.000000000000000000
```
:::


## approve

Approves a `spender` account to withdraw Newton stake token from the token owner's account up to the  designated `amount`. The amount is set as the spender's allowance over the caller's tokens. The owner calls the function again to set a new `amount` allowance.

Constraint checks:

- The `owner` cannot be the zero address
- The `spender` cannot be the zero address

Using `aut` you can approve a `spender` account allowance for an ERC-20 token contract account, e.g. a Liquid Newton account.

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


::: {.panel-tabset}
## aut
``` {.aut}
aut token approve [OPTIONS] SPENDER AMOUNT
```
:::


### Example

To approve a spender for a Newton stake token account specify the `--ntn` option:

::: {.panel-tabset}
## aut
``` {.aut}
aut token approve --ntn 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 100 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x715749a9aed398da7f25e66767c2ed9d3cd00c02f7306453949b9203b9a034a6
```
:::


To approve a spender for an ERC-20 contract token (e.g. Liquid Newton) account specify the `--token` option:

::: {.panel-tabset}
## aut
``` {.aut}
aut token approve --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 1000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xa20ae3a75009fb967ed53897b980e6e88dd580fada133c08071183b5b452ca2c
```
:::

## atnTotalRedistributed

Returns the total amount of Auton staking rewards distributed since genesis minus treasury fee.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the amount of Auton utility token distributed as staking rewards |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol atn-total-redistributed [OPTIONS]
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol atn-total-redistributed -r $RPC_URL
47981813599875371606
```
:::


##  balanceOf

Returns the amount of unbonded Newton stake token held by an account (ERC-20).

You can return the account balance for an ERC-20 token contract account using the `aut token` command group, which is for interacting with ERC-20 token contracts. For example, of a Liquid Newton account.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_addr` | `address` | address of token account |

### Response

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | the amount of unbonded Newton token held by the account |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut token balance-of [OPTIONS] ACCOUNT
```
:::


### Example

To return the Newton stake token balance for an account specify the `--ntn` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token balance-of --ntn 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4
1000.000000000000000000
```
:::

To return an ERC2-0 contract token (e.g. Liquid Newton) balance for an account specify the `--token` option:


::: {.panel-tabset}
## aut

``` {.aut}
aut token balance-of --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 0x11a87b260dd85ff7189d848fd44b28cc8505fa9c
999.000000000000000000
```
:::

::: {.callout-note title="Note" collapse="false"}
All Liquid Newton balances for an account can be returned in one call using the `aut` command `aut account lntn-balances [OPTIONS] ACCOUNT`.
:::


## bond

Delegates an amount of Newton stake token to a designated validator. If the delegator's `msg.Sender` address is the validator `treasury` account then the stake is self-bonded and no Liquid Newton will be issued.

Constraint checks:

- the `validator` address is registered as a validator
- the `validator` state is `active`. A bonding operation submitted to a validator in a `paused`, `jailed` or `jailbound` state will revert
- the `amount` is a positive integer value `> 0`
- the Newton balance of the account submitting  the `bond()` method call has a Newton balance`>=` to the `amount` being bonded.

On successful processing of the method call:

- the bonded Newton amount is burned
- a `BondingRequest` object for the necessary voting power change is created:

| Field | Datatype | Description |
| --| --| --|
| `delegator` | `address payable` | account address of the account bonding stake |
| `delegatee` | `address` | [validator identifier](/concepts/validator/#validator-identifier) address of the validator to which stake is being bonded |
| `amount` | `uint256` | the amount of Newton stake token being bonded to the `delegatee` account |
| `requestBlock` | `uint256` | the block number at which a bonding transaction was committed |

The `BondingRequest` is tracked in memory until applied at epoch end. At that block point, if the stake delegation is [delegated](/glossary/#delegated) and not [self-bonded](/glossary/#self-bonded), then Liquid Newton will be minted to the delegator for the bonded stake amount.

::: {.callout-note title="Note" collapse="false"}
Liquid Newton is *not* issued for self-bonded stake. See Concept [Staking](/concepts/staking/) and [Penalty Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas).
:::

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


::: {.panel-tabset}
## aut
``` {.aut}
aut validator bond [OPTIONS] AMOUNT
```
:::


### Example


::: {.panel-tabset}
## aut
``` {.aut}
aut validator bond --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xaa3705ef2d38cf2d98925660e6ca55de8948e8a075e7ee9edf6be7fa540ffe51
```
:::


## changeCommissionRate

Changes the percentage fee of staking rewards deducted by a validator as commission from delegated stake. At registration all validators have commission set to a default rate specified by the Autonity network's genesis configuration. (See Reference [Genesis, `delegationRate`](/reference/genesis/#configautonity-object).)

Validators may change commission rate at any time after registration.

The `changeCommissionRate` method provides as arguments the [validator identifier](/concepts/validator/#validator-identifier) address and the new commission rate expressed as basis points (bps).

On method execution the `Validator.commissionRate` object data property is updated in memory and set to the new rate.

Constraint checks are applied:

- the `address` of the validator is registered
- the `msg.sender` address of the transaction is equal to the validator's `treasury` address
- the commission rate precision is correctly expressed in basis points as an integer value in the range `0`-`10000` (`10000` = 100%).

The rate change is applied at the next unbonding period modulo epoch.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the [validator identifier](/concepts/validator/#validator-identifier) account address |
| `_rate` | `uint256 ` | the new commission rate in basis points (bps), value range between 0-10000 (10000 = 100%) |

### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits a `CommissionRateChange` event, logging: `_validator`, `_rate`.

### Usage


::: {.panel-tabset}
## aut

``` {.aut}
aut validator change-commission-rate [OPTIONS] RATE
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut validator change-commission-rate --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9 900 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x7a4c6bb2e19eb8a4a160723b07eeb538e835db512541621aef0062cd9e1e15f2
```
:::


## circulatingSupply

Returns the amount of Newton stake token circulating in the network.

::: {.callout-note title="What is the difference between the total and circulating supply of Newton?" collapse="true"}

Total supply is the total amount of Newton that has been minted. Minted Newton may be locked in a contract and released into circulation over time by unlocking according to a schedule. 

Newton stake token that is locked in schedules does not contribute to circulating supply. 

Circulating supply is simply the total supply minus the sum of any minted NTN locked in a contract according to a schedule and pending unlocking. It becomes part of the circulating supply when it unlocks.

To return the total supply of NTN see [`totalSupply()`](/reference/api/aut/#totalsupply).
:::

### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| `stakeCirculating` | `uint256` | the supply of Newton in circulation on the network |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::


## config

Returns the Autonity Network configuration at the block height the call was submitted.

### Parameters

None.

### Response

Returns a `Config` object consisting of:

| Object | Field | Datatype | Description |
| --| --| --| --|
| `Policy` | n/a | `struct` | the Autonity network's configuration of economic and staking protocol parameters |
| | `treasuryFee` | `uint256` | the percentage of staking rewards deducted from staking rewards and sent to the Autonity Treasury account for community funding before staking rewards are distributed |
| | `minBaseFee` | `uint256` | the minimum gas price for a unit of gas used to compute a transaction on the network, denominated in [ton](/glossary/#ton) |
| | `delegationRate` | `uint256` | the percentage of staking rewards deducted by validators as a commission from delegated stake |
| | `unbondingPeriod` | `uint256` | the period of time for which bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction, defined as a number of blocks |
| | `initialInflationReserve` | `uint256` | the amount of Newton held in reserve for Newton inflation rewards |
| | `withholdingThreshold` | `uint256` | the inactivity threshold at which committee member Auton (staking) and Newton (Newton inflation) rewards are withheld and sent to the Withheld Rewards Pool account. Inactivity is based on omission accountability and the validator's inactivity score |
| | `proposerRewardRate` | `uint256` | the percentage of epoch staking rewards allocated for proposer rewarding based on activity proof |
| | `oracleRewardRate` | `uint256` | the percentage of staking rewards deducted for oracles as a reward for correct price reporting |
| | `withheldRewardsPool` | `address payable` | the address of the Autonity Withheld Rewards account, the pool to which withheld inflation rewards are sent for holding. Set to the Autonity Treasury account at genesis, but can be changed |
| | `treasuryAccount` | `address payable` | the address of the Autonity Treasury account for community funds |
| `contracts` | n/a | `struct` | the deployed contract addresses of the Autonity network's [Protocol contracts](/concepts/architecture/#protocol-contracts) |
| | `accountabilityContract` | `address` | the address of the Autonity accountable fault detection Accountability Contract |
| | `oracleContract` | `address` | the address of the Autonity Oracle Contract |
| | `acuContract` | `address` | the address of the Autonity ASM ACU Contract |
| | `supplyControlContract` | `address` | the address of the Autonity ASM Supply Control Contract |
| | `stabilizationContract` | `address` | the address of the Autonity ASM Stabilization Contract |
| | `upgradeManagerContract` | `address` | the address of the Autonity Protocol contract upgrade mechanism's Upgrade Manager Contract |
| | `inflationControllerContract` | `address` | the address of the Autonity Newton inflation reward mechanism Control Contract |
| | `omissionAccountabilityContract` | `address` | the address of the Autonity Accountability Contract |
| `Protocol` | n/a | `struct` | the Autonity network's configuration of governance, consensus committee, and duration (NTN unlocking schedule, epoch and block interval) protocol parameters |
| | `OperatorAccount` | `address` | the address of the Autonity governance account |
| | `EpochPeriod` | `uint256` | the period of time for which a consensus committee is elected, defined as a number of blocks |
| | `BlockPeriod` | `uint256` | the minimum time interval between two consecutive blocks, measured in seconds |
| | `CommitteeSize` | `uint256` | the maximum number of validators that may be members of a consensus committee on the network |
| | `MaxScheduleDuration` | `uint256` | the maximum allowed duration in seconds of an NTN locking schedule or contract |
| `ContractVersion` | `uint256 ` | the version number of the Autonity Protocol Contract. An integer value set by default to `1` and incremented by `1` on contract upgrade |



### Usage


::: {.panel-tabset}

## aut
``` {.aut}
aut protocol config [OPTIONS]
```

## RPC

``` {.rpc}
{"method":"aut_config", "params":[]}
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol config -r $RPC_URL
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
```

## RPC

``` {.rpc}
curl -X GET $RPC_URL  --header 'Content-Type: application/json' --data '{"method":"aut_config", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":{"Policy":{"TreasuryFee":10000000000000000,"MinBaseFee":500000000,"DelegationRate":1000,"UnbondingPeriod":21600,"InitialInflationReserve":40000000000000000000000000,"WithholdingThreshold":0,"ProposerRewardRate":1000,"OracleRewardRate":1000,"WithheldRewardsPool":"0xf74c34fed10cd9518293634c6f7c12638a808ad5","TreasuryAccount":"0xf74c34fed10cd9518293634c6f7c12638a808ad5"},"Contracts":{"AccountabilityContract":"0x5a443704dd4b594b382c22a083e2bd3090a6fef3","OracleContract":"0x47e9fbef8c83a1714f1951f142132e6e90f5fa5d","AcuContract":"0x8be503bcded90ed42eff31f56199399b2b0154ca","SupplyControlContract":"0x47c5e40890bce4a473a49d7501808b9633f29782","StabilizationContract":"0x29b2440db4a256b0c1e6d3b4cdcaa68e2440a08f","UpgradeManagerContract":"0x3c368b86af00565df7a3897cfa9195b9434a59f9","InflationControllerContract":"0x3bb898b4bbe24f68a4e9be46cfe72d1787fd74f4","OmissionAccountabilityContract":"0x684c903c66d69777377f0945052160c9f778d689"},"Protocol":{"OperatorAccount":"0xd32c0812fa1296f082671d5be4cbb6beeedc2397","EpochPeriod":1800,"BlockPeriod":1,"CommitteeSize":30,"MaxScheduleDuration":126230400},"ContractVersion":1}}
```
:::



## decimals

Returns the number of decimals the NTN token uses (ERC-20).

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint8` | the number of decimals set in the Newton ERC-20 contract |

### Usage


::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::


## deployer

Returns the address of the account deploying the contract. The address is used to restrict access to functions that can only be invoked by the protocol (the `msg.sender` of a transaction is checked against the `deployer` address by the `onlyProtocol` access modifier), bypassing transaction processing and signature verification. It is set to the zero address.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the address of the account deploying the Autonity contract |

### Usage


::: {.panel-tabset}
## aut

``` {.aut}
aut protocol deployer [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol deployer --rpc-endpoint $RPC_URL
0x0000000000000000000000000000000000000000
```
:::


## epochID

Returns the unique identifier of a block epoch as an integer value.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the identifier of a block epoch. Initial value is `0`. |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-id [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-id --rpc-endpoint $RPC_URL
7371
```
:::


## epochReward

Returns the amount of Auton transaction fees available for distribution as staking rewards for stake bonded to validators in the consensus committee at the block height of the call. Actual reward distribution takes place as the last block of an epoch is finalised.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the amount of Auton transaction fees available for distribution to consensus committee members at the block height of the call |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-reward [OPTIONS]
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-reward --rpc-endpoint $RPC_URL
121166000000000
```
:::


## epochTotalBondedStake

Returns the amount of Newton stake token bonded to consensus committee members and securing the network during the epoch of the call.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `uint256` | the amount of Newton stake token bonded to consensus committee validators in the epoch  of the call |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-total-bonded-stake [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-total-bonded-stake --rpc-endpoint $RPC_URL
61338
```
:::


## getBlockPeriod

Returns the block period from the protocol configuration.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `blockPeriod` | `uint256` | the minimum time interval between two consecutive blocks, measured in seconds |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol block-period [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol block-period --rpc-endpoint $RPC_URL
1
```
:::


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
| `addr` | `address` | the `nodeAddress` of the validator node, its unique [`validator identifier`](/concepts/validator/#validator-identifier) |
| `votingPower` | `uint256` | the amount of Newton stake token bonded to the validator |
| `consensusKey` | `bytes` | the bls public key in bytes that the validator node is using in consensus |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol committee [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol committee -r $RPC_URL
[
  {
    "address": "0xBaf935b88066021a0B0BD34cEB2Ba10389b6Aa0D",
    "voting_power": 114000000000000000000000,
    "consensus_key": "0xb0d287da6365b9ebcf69c84985877a75a59e7449699a2ada0abb42f3e3414fef3f1406dd11a1e9cb0ee2154c2983de77"
  },
  {
    "address": "0x889Dcd8Ca57AB1108e73E9B02B2C2Cb09Ea9b19e",
    "voting_power": 114000000000000000000000,
    "consensus_key": "0xa83a69fb0a0918985bea979812abf6d98b674d5fc6619b8b1fa67f8515aee63a024d8913eb45306645a6bc5c4964769c"
  },
  ...
]
```
:::


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

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol committee-enodes [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol committee-enodes -r $RPC_URL
['enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303', 'enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303', 'enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303', 'enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308', 'enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309', 'enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310', 'enode://c6ae16b58cf2e073649ec34ed59550c57389fcb949f51b806d6f7de26e7961cfc33794fde67b484ce9966a30e5ab5331c610b1b659249a6d66cc9e6d8a3d23d1@143.198.240.242:30303', 'enode://06facaec377a55fe8fd9e30cc922bedc7ee97e292294435635fa3b053c30215b87954daa27c79a73e3a5013124318b084907c81f518bcf36f88dad4d01e952ec@138.68.118.4:30303', 'enode://0c71d8076f0543505aae22901471d5437f1fd92b3d154d154edcec5baf0d7b121e6e8dc85ae725daf77cbc50ff5616727d59d36c2606751401000580e155e2bc@5.181.104.29:30303']
```
:::


## getCurrentEpochPeriod

Returns the epoch period from the protocol configuration.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `epochPeriod` | `uint256` | the period of time for which a consensus committee is elected, defined as a number of blocks |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::


## getEpochByHeight

Returns the epoch info for a given block height.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_height` | `uint256` | the input block number |

### Response

| Field | Datatype | Description |
| --| --| --|
| `epochInfos` | `EpochInfo` | epoch info object for the requested block height |

### Response

Returns an `epochInfo` object providing metadata about the consensus committee and epoch. See [`getEpochInfo()`](/reference/api/aut/#getepochinfo) for the description of `EpochInfo` object properties.

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::


## getEpochFromBlock

Returns the unique identifier of the epoch associated with a block height.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_block` | `uint256` | the input block number |

### Response

| Field | Datatype | Description |
| --| --| --|
| `epochID` | `uint256` | the identifier of the epoch in which the block was committed to state |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-from-block [OPTIONS] BLOCK
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-from-block --rpc-endpoint $RPC_URL 3293857
1829
```

:::

## getEpochInfo

Returns the current epoch info of the chain.    

### Parameters

None.

### Response

Returns an `epochInfo` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `committee` | `CommitteeMember[]` | an array of `CommitteeMember` objects recording the consensus committee of the epoch |
| `previousEpochBlock` | `uint256` | The previous epoch block number |
| `epochBlock` | `uint256` | The epoch block number |
| `nextEpochBlock` | `uint256` | The next epoch block number |
| `delta` | `uint256` | the current value for delta (omission failure) |

For each committee member [`validator identifier`](/concepts/validator/#validator-identifier) address, [voting power](/glossary/#voting-power), and [consensus key](/concepts/validator/#p2p-node-keys-autonitykeys) is returned. See [`getCommittee()`](/reference/api/aut/#getcommittee) for the description of `CommitteeMember` object properties.

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::


## getEpochPeriod

Returns the epoch period. If there will be an update at epoch end, the new epoch period is returned.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `newEpochPeriod` | `uint256` | the period of time for which a consensus committee is elected, defined as a number of blocks |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-period [OPTIONS]
```

:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-period --rpc-endpoint $RPC_URL
1800
```

:::


## getLastEpochBlock

Returns the last epoch's end block height.

### Response

| Field | Datatype | Description |
| --| --| --|
| `epochBlock` | `uint256` | the number of the last block in the preceding epoch |

### Usage


::: {.panel-tabset}
## aut

``` {.aut}
aut protocol last-epoch-block [OPTIONS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol last-epoch-block -r $RPC_URL
12981684
```

:::


##  getMaxCommitteeSize

Returns the protocol setting for the maximum number of validators that can be selected to the consensus committee.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `committeeSize` | `uint256` | the maximum number of validators allowed in the consensus committee |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol max-committee-size [OPTIONS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol max-committee-size --rpc-endpoint $RPC_URL
50
```

:::


## getMaxScheduleDuration

Returns the max allowed duration of any schedule or contract from the protocol configuration.

### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| `maxScheduleDuration` | `uint256` | the maximum duration allowed for a schedule or contract for locked Newton |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::


##  getMinimumBaseFee

Returns the protocol setting for the minimum price per unit of gas for computing a transaction on an Autonity network.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `minBaseFee` | `uint256` | the minimum price per unit of gas, denominated in [ton](/glossary/#ton) |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol minimum-base-fee [OPTIONS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol minimum-base-fee --rpc-endpoint $RPC_URL
500000000
```

:::


## getNextEpochBlock

Returns the next epoch's block.

### Response

| Field | Datatype | Description |
| --| --| --|
| `nextEpochBlock` | `uint256` | the number of the first block in the following epoch |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::


## getOperator

Returns the address of the Autonity governance account.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the operator governance account address |

### Usage


::: {.panel-tabset}
## aut

``` {.aut}
aut protocol operator [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol operator -r $RPC_URL
0x293039dDC627B1dF9562380c0E5377848F94325A
```
:::


## getOracle

Returns the address of the Autonity Oracle Contract.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the oracle contract account address |

### Usage

::: {.panel-tabset}
## aut

``` {.rpc}
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.rpc}
TO DO
```
:::


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

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol proposer [OPTIONS] HEIGHT ROUND
```

:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol proposer -r $RPC_URL 4576868 0
0x0c7dC2aB00c7b5934EDA097a8585f56367A94dA4
```

:::


## getTreasuryAccount

Returns the address of the Autonity treasury account.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the Autonity treasury account address |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol treasury-account [OPTIONS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol treasury-account -r $RPC_URL
0xF74c34Fed10cD9518293634C6f7C12638a808Ad5
```

:::


## getTreasuryFee

Returns the percentage of staking rewards deducted from staking rewards by the protocol. Treasury fees are sent to the Autonity Treasury account for community funding before staking rewards are distributed.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `treasuryFee` | `uint256` | the Autonity treasury account address. The value is returned in `10^18` format. |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol treasury-fee [OPTIONS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol treasury-fee -r $RPC_URL
10000000000000000
```

:::


## getUnbondingPeriod

Returns the unbonding period from the protocol configuration.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `unbondingPeriod` | `uint256` | the period of time for which bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction, defined as a number of blocks |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol unbonding-period [OPTIONS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol unbonding-period -r $RPC_URL
21600
```

:::


## getUnbondingShare

Returns the amount of unbonding shares for an unbonding request.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_unbondingID ` | `uint256` | the unique identifier of the unbonding request |

### Response

| Field | Datatype | Description |
| --| --| --|
| `unbondingShare` | `uint256` | the amount of shares issued for the unbonding staking pool that the unbonding amount represents. See [`unbond()`](/reference/api/aut/#unbond) |

### Response

Returns an `epochInfo` object providing metadata about the consensus committee and epoch. See [`getEpochInfo()`](/reference/api/aut/#getepochinfo) for the description of `EpochInfo` object properties.

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::


## getValidator

Returns the data for a designated [validator identifier](/concepts/validator/#validator-identifier) address from system state. The method response may be empty if there is no associated validator object for the address argument provided.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_addr` | `address` | the [validator identifier](/concepts/validator/#validator-identifier) account address |

### Response

Returns a `Validator` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `treasury` | `address payable` | the address that will receive staking rewards the validator earns |
| `nodeAddress` | `address` | the [validator identifier](/concepts/validator/#validator-identifier) account address |
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
| `liquidStateContract` | `Liquid` | the address of the validator's Liquid Newton contract |
| `liquidSupply` | `uint256` | the total amount of Liquid Newton in circulation |
| `registrationBlock` | `uint256` | the block number in which the registration of the validator was committed to state|
| `totalSlashed` | `uint256` | the total amount of stake that a validator has had slashed for accountability and omission faults since registration |
| `jailReleaseBlock` | `uint256` | the block number at which a validator jail period applied for an accountability or omission fault ends (the validator can be re-activated after this block height). Set to `0` when the validator is in an active or jailbound state |
| `consensusKey` | `bytes` | the public consensus key of the validator |
| `state` | `ValidatorState` | the state of the validator. `ValidatorState` is an enumerated type with enumerations: `0`: active, `1`: paused, `2`: jailed, `3`: jailbound, `4`:  jailedForInactivity, `5`:  jailboundForInactivity |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut validator info [OPTIONS]
```

:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut validator info --rpc-endpoint $RPC_URL --validator 0x21bb01ae8eb831fff68ebe1d87b11c85a766c94c
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
  "liquid_state_contract": "0x0000000000000000000000000000000000000000",
  "liquid_supply": 1397840815523076466699159265359708166239426845751,
  "registration_block": 0,
  "total_slashed": 0,
  "jail_release_block": 0,
  "state": 0
}
```

:::


##  getValidators

Returns the current list of validators from system state.

The response is returned as a list of [validator identifier](/concepts/validator/#validator-identifier) addresses, sorted by registration index in ascending order. I.E. the last value in the array is always the last processed registration request.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `validatorList` | `address` array | an array of registered validators, sorted by registration index in ascending order  |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut validator list [OPTIONS]
```
:::


::: {.callout-note title="Note" collapse="false"}
`getValidators` can also be called using the `aut` command `aut protocol validators`.
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut validator list --rpc-endpoint $RPC_URL
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
```
:::


## getValidatorState

Returns the state of a designated validator.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_addr` | `address` | the [validator identifier](/concepts/validator/#validator-identifier) account address |

### Response

| Field | Datatype| Description |
| --| --| --|
| `state` | `ValidatorState` | the state of the validator. `ValidatorState` is an enumerated type with enumerations: `0`: active, `1`: paused, `2`: jailed, `3`: jailbound, `4`: jailedForInactivity, `5`: jailboundForInactivity |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```
:::


##  getVersion

Returns the current Autonity Protocol Contract version.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `contractVersion` | `uint256 ` | the version number of the Autonity Protocol Contract. An integer value set by default to `1` and incremented by `1` on contract upgrade |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol version [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol version -r $RPC_URL
1
```
:::


## isUnbondingReleased

Returns a boolean flag specifying if stake for an unbonding request has been released or not.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_unbondingID ` | `uint256` | the unique identifier of the unbonding request |

### Response

Returns `true` if unbonding is released and `false` otherwise.

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
TO DO
```

:::


## name

Returns the name of the Newton stake token as a human-readable string (ERC-20). Set as contract metadata to the value of `Newton`.

Using `aut` you can return the name for an ERC-20 token contract account, e.g. a Liquid Newton contract.

### Parameters

None.

### Response

| Returns | Datatype | Description |
| --| --| --|
| value | `string` | the name of the Newton stake token |

### Usage


::: {.panel-tabset}
## aut

``` {.aut}
aut token name [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut token name --ntn -r $RPC_URL
Newton
```
:::

To return the `name` for an ERC-20 (e.g. a Liquid Newton token) token contract specify the `--token` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token name --rpc-endpoint $RPC_URL --token 0xC500751c4F96d49B954D20EAE42Fa29278B96beB
LNTN-4
```
:::


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
| `_addr` | `address` | the validator identifier account address |

### Response

No response object is returned on successful execution of the method call.

The updated state can be viewed by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits a `PausedValidator` event, logging: `treasury`, `addr`, `effectiveBlock`.

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut validator pause [OPTIONS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut validator pause --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x942328bea54a0096ca9b2fb88acd337c883f7923c2ef6b8290a340c5baec2d20
```
:::


## registerValidator

Registers a validator on an Autonity Network.

The `registerValidator` method provides as argument the [enode](/glossary/#enode) URL of the validator node, the validator's oracle server address, the validator's BLS public key used for consensus gossiping, and a proof of node ownership generated using the private key of the validator node's [P2P node keys, autonitykeys](/concepts/validator/#p2p-node-keys-autonitykeys) and the validator's [oracle server key](/concepts/oracle-network/#oracle-server-key).

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
| `consensusKey` | `bytes` | Set to the `_consensusKey` parameter value provided in the `registerValidator` method call transaction |
| `ValidatorState` | `state` | Set to `active`. |

Constraint checks are applied:

- the `enode` URL is not empty and is correctly formed
- the `address` of the validator is not already registered
- the `consensusKey` is valid
- the `proof` of node ownership is valid: a cryptographic proof containing the string of the validator's `treasury` account address signed by (a) the validator's private P2P node key and (2) the validator's oracle server private key. The two signatures are concatenated together to create the ownership proof. The validator's `treasury` account address is recovered from the proof using the public key of (1) the validator's P2P node key and (2) the oracle server key.

Validator registration is then executed, the temporary address assignments updated, and the new validator object appended to the indexed validator list recorded in system state. I.E. the most recently registered validator will always have the highest index identifier value and will always be the last item in the validator list returned by a call to get a network's registered validators (see [`getValidators`](/reference/api/aut/#getvalidators)).

A validator-specific Liquid Newton contract is deployed; the contract's `name` and `symbol` properties are both set to `LNTN-<ID>` where `<ID>` is the validator's registration index identifier.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_enode` | `string` | the enode url for the validator node  |
| `_oracleAddress` | `address` | the oracle server identifier account address |
| `_consensusKey` | `bytes` | the BLS public key from `autonitykeys` used for P2P consensus gossiping |
| `_signatures` | `bytes` | the proof of node ownership. A combination of two ECDSA signatures and a bls signature appended sequentially to provide the ownership proof of the validator node key (autonitykeys). The first two ECDSA signatures are in the order: (1) a message containing the treasury account address signed by the validator P2P autonitykeys private key; (2) a message containing the treasury account address signed by the Oracle Server account private key. |

### Response

No response object is returned on successful execution of the method call.

The validator registration entry can be retrieved from state by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

On a successful call the function emits a `RegisteredValidator` event, logging: `treasury`, `_addr` (validator identifier (nodeAddress)), `oracleAddress`, `enode`, `liquidStateContract`.

### Usage

::: {.panel-tabset}

## aut

``` {.aut}
aut validator register [OPTIONS] ENODE ORACLE CONSENSUS_KEY PROOF
```
:::

### Example

::: {.panel-tabset}

## aut

``` {.aut}
aut validator register enode://c36481d70943dd046d8013f3d302cf0d2a17f5f5f3398cd47fbcb38edfe4e5b4207ea4e762ec52efb65f72bede5cd5a65e8380eaf0db9ef39a77cb6ec5694af9@11.19.111.18:30303 0xFe91928d58Af4AFbD78C96121k3147ef1f517072 0x978191bff952cd9614b36ff2cc57a47820204bc71b0131625964e6801c304836a7fa11a9c47ca2561cbfc71eb0b314ab 0xfc93396148320f466f10f25abd312ed15ef31f6b29e8924b6f0592e585580f873f807304a540a8a436d92aed969aef0148ca8a2884fc7ad56f1cffa50bb7aa9a01a5189e8d50880faf97ad42501375b216b89304c3fd4acf548a1d7fd7136e74771791422819134e2e3fbf720c35652d8c163e3d4f22c798a3c648958f7abcda2c00b1e8cd80be821c23d41d4ccb6587685960519375762e9ccd8a95ba3fbeb7d47955990b33af65db5155d3d79d498152760d83ab8c92a132e94aeb458f556ff7ef9d5b78b2544a47939ae71a01faf5172c25b5102bc7eed886ff105e91283b3916 | aut tx sign - | aut tx send -
```
:::


## symbol

Returns the three-letter symbol of the Newton stake token as a string (ERC-20). Set as contract metadata to the value of `NTN`.

Using `aut` you can return the symbol for an ERC-20 token contract account, e.g. a Liquid Newton contract.

### Parameters

None.

### Response

| Returns | Datatype | Description |
| --| --| --|
| value | `string` | the symbol for the Newton stake token - `NTN` |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut token symbol [OPTIONS]
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut token symbol --ntn --rpc-endpoint $RPC_URL
NTN
```
:::

To return the `symbol` for an ERC-20 (e.g. a Liquid Newton token) token contract specify the `--token` option:


::: {.panel-tabset}
## aut

``` {.aut}
aut token symbol --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37
LNTN-0
```
:::


## totalSupply

Returns the amount of Newton stake token issued (ERC-20).

You can return the total supply for an ERC-20 token contract using the `aut token` command group, which is for interacting with ERC-20 token contracts. For example, of a Liquid Newton account.

::: {.callout-note title="What is the difference between the total and circulating supply of Newton?" collapse="true"}

Total supply is the total amount of Newton that has been minted. Circulating supply is simply the total supply minus the sum of any minted NTN that is locked and released into circulation over time by unlocking according to a schedule.

To return the circulating supply of NTN see [`circulatingSupply()`](/reference/api/aut/#circulatingsupply).
:::

### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| `stakeSupply` | `uint256` | the total supply of Newton in circulation |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut token total-supply [OPTIONS]
```

:::

### Example

To return total supply for the Newton stake token specify the `--ntn` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token total-supply --ntn -r $RPC_URL
63402
```
:::

To return the total supply for an ERC-20 contract token (e.g. Liquid Newton) specify the `--token` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token total-supply --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37   -r $RPC_URL
10087
```
:::


## transfer

Transfers a designated amount of Newton stake token from the caller account to a recipient account.

Constraint checks:

- the `amount` value is `>= 0`
- the caller's account balance is `>= amount`

Using `aut` you can transfer from an ERC-20 token contract account, e.g. a Liquid Newton account.

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

::: {.panel-tabset}
## aut

``` {.aut}
aut token transfer [OPTIONS] RECIPIENT AMOUNT
```
:::

### Example

To transfer an amount of Newton stake token to a recipient specify the `--ntn` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token transfer --ntn 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 1| aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x17092d181653c4f13642698233966010a83a39f34846f65cef7dc860ad13644d
```
:::

To transfer an amount from an ERC-20 contract token (e.g. Liquid Newton) to a recipient specify the contract address with the `--token` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token transfer --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 10 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x2d78e64d82d1e54aeb487c4c10834dc3a1e17fabbd1f5775a2d72c6390db7b26
```
:::


##  transferFrom

Transfers a designated amount of Newton stake token from a specified sender account to a recipient account using the ERC-20 [`approve()'](/reference/api/aut/#approve) and [`allowance()'](/reference/api/aut/#allowance) mechanisms.

The `transferFrom` method is used for withdraw workflows where the token owner account (the `sender`) has authorised the method caller, the `spender` (the `msg.sender`), to transfer tokens on the owner's behalf.

Constraint checks:

- `sender` and `recipient` accounts must be allowed to hold Newton stake token
- the `msg.sender` (`spender`) has been approved by the owner (the `sender`) to withdraw tokens from their account
- the `msg.sender`'s remaining allowance to withdraw the `owner`'s tokens is `>= amount`

Using `aut` you can call `transferFrom` on an ERC-20 token contract (e.g. Liquid Newton) account.

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

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut token transfer-from [OPTIONS] SENDER RECIPIENT AMOUNT
```
:::

### Example

To transfer an amount of Newton stake token to a recipient specify the `--ntn` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token transfer-from --ntn --from 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 0x11a87b260dd85ff7189d848fd44b28cc8505fa9c 0xbf2f718f948de541123f3e0a06a9100ee1df128c 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x2d277f8eee73d900f3cb3994796cfbb4ddef22ca78870344bf910bbd1b64f22c
```
:::

To transfer an amount from an ERC-20 contract token (e.g. Liquid Newton) to a recipient specify the contract address with the `--token` option:

::: {.panel-tabset}
## aut

``` {.aut}
aut token transfer-from --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37  --from 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 0x11a87b260dd85ff7189d848fd44b28cc8505fa9c 0xbf2f718f948de541123f3e0a06a9100ee1df128c 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x64a88723d7dd99e026029db531b6415e6e7a19fe131395059742065fcfe6575c
```
:::


## unbond

Unbonds an amount of bonded stake from a designated validator.

The amount specifies Newton stake token if the delegator is unbonding [self-bonded](/glossary/#self-bonded) stake, else Liquid Newton if [delegated](/glossary/#delegated) stake is being unbonded.

::: {.callout-important title="Warning" collapse="false"}
The unbonding request will only be effective after the unbonding period, rounded to the next epoch.

If the validator has a [slashing](/concepts/accountability/#slashing) event before this period expires, then the released Newton stake token amount may or may not correspond to the amount requested.

See Concept [Accountability and fault detection (AFD)](/concepts/accountability/) for Autonity's slashing mechanism.
:::

Constraint checks are applied. The  `validator` address provided is verified as a registered validator address and the requested unbonding amount is checked to verify it is `<=` to the `msg.sender`'s bonded stake amount. For delegated stake this is done by checking the `msg.Sender`'s Liquid Newton balance is `>=` to the requested amount, and for self-bonded stake this is done by checking the validator's `selfBondedStake` balance is`>=` to the requested unbonding amount.

::: {.callout-note title="Note" collapse="false"}
If `msg.Sender` is the validator `treasury` account, then Liquid Newton balance and supply checks are not required.

This is because Liquid Newton is *not* issued for self-bonded stake. See Concept [Staking](/concepts/staking/) and [Penalty Absorbing Stake (PAS)](/concepts/staking/#penalty-absorbing-stake-pas).
:::

On successful processing of the method call, an `UnbondingRequest` object for the necessary voting power change is created:

| Field | Datatype | Description |
| --| --| --|
| `delegator` | `address payable` | account address of the account unbonding stake |
| `delegatee` | `address` | validator identifier account address of the validator from which stake is being unbonded |
| `amount` | `uint256` | the amount of stake being unbonded from the `delegatee` account. It records the amount unbound in (a) Newton stake token for [self-bonded](/glossary/#self-bonded) stake, or (b) Liquid Newton for [delegated](/glossary/#delegated) stake  |
| `unbondingShare` | `uint256` | the amount of shares issued for the unbonding staking pool that the unbonding amount represents |
| `requestBlock` | `uint256` | the block number at which an unbonding transaction was committed and from which the unbonding period begins |
| `unlocked` | `bool` | Boolean value indicating if the stake being unbonded is subject to a lock or not |
| `released` | `bool` | Boolean value indicating if the stake being unbonded has been released or not |
| `selfDelegation` | `bool` | Boolean value indicating if the unbonding is for [self-bonded](/glossary/#self-bonded) stake |

The [unbonding period](/glossary/#unbonding-period) begins in the next block. The `UnbondingRequest` is tracked in memory. At the end of the epoch in which the unbond request was processed:

  - the designated amount of Liquid Newton amount is unlocked and burned if the stake being unbonded is [delegated](/glossary/#delegated) and *not* [self-bonded](/glossary/#self-bonded) stake
  - the amount of stake to deduct from the unbonding pool, as well as the delegator's share of the unbonding pool, is calculated
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

::: {.panel-tabset}
## aut

``` {.aut}
aut validator unbond [OPTIONS] AMOUNT
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut validator unbond --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9  1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x3ac340e33f5ddfdab04ffe85ce4b564986b2f1a877720cb79bc9d31c11c8f318
```
:::


## updateEnode

Updates the enode URL of a registered validator on an Autonity Network.

The `updateEnode` method provides as argument the [validator identifier](/concepts/validator/#validator-identifier) and the [enode](/glossary/#enode) URL of the validator node.

Constraint checks are applied:

- the `enode` URL is not empty, is correctly formed, the `PUBKEY` element of the enode has not been updated
- the `_nodeAddress` is a registered validator address
- the `msg.Sender` caller address of the `updateEnode()` transaction is the validator's registered [treasury account](/concepts/validator/#treasury-account)
- the `_nodeAddress` is not a member of the consensus committee

On method execution the `enode` property of the validator is updated in system state and assigned the value of the `_enode` argument to the method call.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_nodeAddress` | `address` | the validator node identifier account address |
| `_enode` | `string` | the enode url for the validator node  |


### Response

No response object is returned on successful execution of the method call.

The updated validator enode can be retrieved from state by calling the [`getValidator`](/reference/api/aut/#getvalidator) method.

### Event

None.

### Usage

::: {.panel-tabset}

## aut
``` {.aut}
aut validator update-enode [OPTIONS] ENODE
```
:::

### Example

::: {.panel-tabset}

## aut
```
aut validator update-enode --validator  0xbaf935b88066021a0b0bd34ceb2ba10389b6aa0d enode://0be363cfa0c81ee12cfc7e144cf6611a1418344a1fa6a0ca04aaa9b09f68dfe2a8d70b8de22026807728424122937721f8f3570bf296c8d445183e37c87b152d@35.197.223.249:30303
```
:::
