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
```yaml {.aut}
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

To return an ERC-20 contract token (e.g. Liquid Newton) balance for an account specify the `--token` option:


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
aut contract call [OPTIONS] circulatingSupply [PARAMETERS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 circulating
Supply
48376978018975530850560921
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
aut contract call [OPTIONS] decimals [PARAMETERS]
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 decimals
18
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
aut contract call [OPTIONS] getCurrentEpochPeriod [PARAMETERS]
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 getCurrentEpochPeriod
1800
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
aut protocol epoch-by-height [OPTIONS] BLOCK_HEIGHT
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-by-height 53690
{
  "committee": [
    {
      "addr": "0x551f3300FCFE0e392178b3542c009948008B2a9F",
      "voting_power": 100776717436166282286338,
      "consensus_key": "0xa3aa75e42e99275f7d7985538fedc06e7f128b138a5311702afc0dc129484763645c40c36fdd97ff0d0293b00a031714"
    },
    {
      "addr": "0x1Be7f70BCf8393a7e4A5BcC66F6f15d6e35cfBBC",
      "voting_power": 100194147663096345519089,
      "consensus_key": "0x8e37252fc62b32896b522150a020170fbd937a9871967e3a17cc4c9941a5dceeca881eb21316e42c7cc56e3dc3fc099a"
    },
    {
      "addr": "0x94470A842Ea4f44e668EB9C2AB81367b6Ce01772",
      "voting_power": 100193401001979275366620,
      "consensus_key": "0x93d58b3114509a592c321250cb5a512f42aa19e59dfa29aec90a262fa0dbb9364e138caff57bc4efe5fe27c05bfe6d4a"
    },
    {
      "addr": "0x23b4Be9536F93b8D550214912fD0e38417Ff7209",
      "voting_power": 100193013182019732813600,
      "consensus_key": "0xa75b87984e7fe44699c94e5cdaf43036b9b3ddd358e7d84d319ca5b8c892abf466f73139d4940b0753fb135d7d574856"
    },
    {
      "addr": "0xE4686A4C6E63A8ab51B458c52EB779AEcf0B74f7",
      "voting_power": 100192881584008137395470,
      "consensus_key": "0x8375584b6108dc57307d8b2335d01286f96198b829bcaa1c2ad30545cacbdf7886b1cf12e8af1cc4e585fa189b8f3995"
    },
    {
      "addr": "0x6747c02DE7eb2099265e55715Ba2E03e8563D051",
      "voting_power": 100192771145915284462532,
      "consensus_key": "0xa286ee63600c630ce7c63d86c2eb83355e4025684b37cc3b00e835a02b7a430638f3c245c06c34a85ee259fe0ccf60ef"
    },
    {
      "addr": "0xBE287C82A786218E008FF97320b08244BE4A282c",
      "voting_power": 100192509567409538105218,
      "consensus_key": "0x8afe7050848e51433a30561efc0eb1d40698e3880b496b6cbcce1c35ca748575345605877298b480b4adde5bc96c9767"
    },
    {
      "addr": "0xcdEed21b471b0Dc54faF74480A0E700fCc42a7b6",
      "voting_power": 100192494168506938500884,
      "consensus_key": "0x86d048b1a123a2e74c7e4998bafcecb49fd16f366d5709478e654a85ac3c8add474653b39f8fc32614e567b52fba0d85"
    },
    {
      "addr": "0xDCA5DFF3D42f2db3C18dBE823380A0A81db49A7E",
      "voting_power": 100192240707848920660520,
      "consensus_key": "0xb49dfa4ce7fdddbd99e6c80fc1f52bc57c732cbe2793d60d4930455153a78c53d96450e0c209b59fdfe1f535d59d7987"
    },
    {
      "addr": "0xe877FcB4b26036Baa44d3E037117b9e428B1Aa65",
      "voting_power": 100192188118587594864026,
      "consensus_key": "0xb96706e536cdc9a38d3d9e570cd1bc2bb2316a04e3d9c5a042970128833dfc8a8585222ed2c8ba86cbfd1e9477a4cf10"
    },
    {
      "addr": "0x9C7dAABb5101623340C925CFD6fF74088ff5672e",
      "voting_power": 100192180670513853594399,
      "consensus_key": "0xb579a7df6f44c54413e344657c4bf07117904b25361218b32414ff509fc5b199a1ab5fac7f50d2cfe46193c7e9f5abb5"
    },
    {
      "addr": "0x5E17e837DcBa2728C94f95c38fA8a47CB9C8818F",
      "voting_power": 100191999541506839051184,
      "consensus_key": "0xb92b96a0bdd7d57836e326af33b40f5532f10e0268a61205acf568efc63a62391ac0debeeb04b1cdffaf9c58057d00e6"
    },
    {
      "addr": "0xcf716b3930d7cf6f2ADAD90A27c39fDc9D643BBd",
      "voting_power": 100191792873629428927880,
      "consensus_key": "0xb55ff748491cc9f24725e6db2ac4e5393a8d0428de9c84cedd48d908c19ad4c3ab5160999f0fbaa2db044bf9f1ca1ded"
    },
    {
      "addr": "0x3597d2D42f8Fbbc82E8b1046048773aD6DDB717E",
      "voting_power": 100186536210576955928066,
      "consensus_key": "0x987e729178b455c34051ba097a3a61e0a6164abc00e48bd24bc6dbe23b33571555691071f475145b4fce09a1d8c6f60b"
    },
    {
      "addr": "0xBBf36374eb23968F25aecAEbb97BF3118f3c2fEC",
      "voting_power": 100186526218057432059192,
      "consensus_key": "0xa70a21a1d5896ad8b348c931e24810c1238d100db876d686105796d1a9af77d0c93b52d8070e0fd65cc12c7ed74c0401"
    },
    {
      "addr": "0x197B2c44b887c4aC01243BDE7E4bBa8bd95BC3a8",
      "voting_power": 100186479172217178636676,
      "consensus_key": "0xae1b49d79c320203b526e79a82f744b3c0ab2a270f1f8bc30db9e54e0ad08053e94bd0848b515175985d62f5105c7403"
    },
    {
      "addr": "0x725fC5416BDb173642D21DfC401519B0DCBf7f3b",
      "voting_power": 100185379453450332004581,
      "consensus_key": "0x88dfd07a93c63943841d66698c52b3f5197aaf3af6dcc538edd5a4ea653290fee64c8ceafda84d81bf5ab0a0e384d594"
    },
    {
      "addr": "0xEf0Ba5e345C2C3937df5667A870Aae5105CAa3a5",
      "voting_power": 100184584034931204307553,
      "consensus_key": "0xb30755eb557b8908b7ed46669b814189615fd7428de1c5d53eae7459aa34cbc308a7731abfeca02d2e2ee6dfa298f463"
    },
    {
      "addr": "0x527192F3D2408C84087607b7feE1d0f907821E17",
      "voting_power": 100184478183353864817137,
      "consensus_key": "0xad6575bb260db0b73572ad023d41fdb101a52f2e6be302cd0a79cb6dc23a5d8cce9195033cfb76d2933a55fb34bd7b48"
    },
    {
      "addr": "0xA284470fa70D8A2A8402054e40A36077fEAdCF51",
      "voting_power": 100184462895207243291210,
      "consensus_key": "0xb22e3a21177e85b6a37bf039ac795859091087131c3cc51491c4fe8c4fdf920cf7dce804cbd88190af57615ae8dd4854"
    },
    {
      "addr": "0x36142A4f36974e2935192A1111C39330aA296D3C",
      "voting_power": 100184376822139424148901,
      "consensus_key": "0xb4658589fd31bafa3f1c91057c002546faa13f0129e9336402f87144f9ce143e88c6f9caffe7382a08b7447845567ad4"
    },
    {
      "addr": "0x94d28f08Ff81A80f4716C0a8EfC6CAC2Ec74d09E",
      "voting_power": 100184112727810050430253,
      "consensus_key": "0x86f21aa126b2bae0aca1926ae5ed55f2d0207917ca6995bd48755f809868b8903e56e4cfe48bee22224e854f2e7ffb2e"
    },
    {
      "addr": "0x8f91e0ADF8065C3fFF92297267E02DF32C2978FF",
      "voting_power": 100184012010509351697978,
      "consensus_key": "0xa6c19cc2771aee5bb4e21c9c7a234046dbd1b45b330294ca02445eedebab3f02d16a0b5602e1f1403078e97c00d29bd2"
    },
    {
      "addr": "0x100E38f7BCEc53937BDd79ADE46F34362470577B",
      "voting_power": 100183904974426457056635,
      "consensus_key": "0xa6b9f7113a95aa40a26571f4e26f2a971910c6ff8b067dccee61e53108868f36afc0c79ed4f8dd972c5d0085181abfdb"
    },
    {
      "addr": "0x383A3c437d3F12f60E5fC990119468D3561EfBfc",
      "voting_power": 100183821357007074081774,
      "consensus_key": "0x89f62c1858723ed3d027d31026e37d6edfdf730e21a9315a1f4e54c50b363f341f88ee5b420606cce4ab124bfaa6c496"
    },
    {
      "addr": "0x9d28e40E9Ec4789f9A0D17e421F76D8D0868EA44",
      "voting_power": 100183707173309737349542,
      "consensus_key": "0xae6013d1ad0f8e1a1ed62c68ff3ef09461e32e95a7f5f4ded6b9fb4dc7f866a5984727e8214fc92e85906df4627625a2"
    },
    {
      "addr": "0x3fe573552E14a0FC11Da25E43Fef11e16a785068",
      "voting_power": 100183640771710575053864,
      "consensus_key": "0x96843bfb82f6b5860aaa93d59b81ac8e08e0ff9f5a76c25e5e5e3bb127ca06d0cffb19fabb4e25305c6be4ad18c7ac7b"
    },
    {
      "addr": "0x99E2B4B27BDe92b42D04B6CF302cF564D2C13b74",
      "voting_power": 100183205992233464410356,
      "consensus_key": "0xb2eed3ac8ec307e0862cdf7b8435049a98d8c83721a6066308ec57a1d9ec7f9c4e4725872dbfc96a83d102a77b430eb0"
    }
  ],
  "previous_epoch_block": 50400,
  "epoch_block": 52200,
  "next_epoch_block": 54000,
  "delta": 5
}
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
aut protocol epoch-info [OPTIONS]
```

:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol epoch-info
{
  "committee": [
    {
      "addr": "0x551f3300FCFE0e392178b3542c009948008B2a9F",
      "voting_power": 123083753308886850895904,
      "consensus_key": "0xa3aa75e42e99275f7d7985538fedc06e7f128b138a5311702afc0dc129484763645c40c36fdd97ff0d0293b00a031714"
    },
    {
      "addr": "0x6747c02DE7eb2099265e55715Ba2E03e8563D051",
      "voting_power": 122416942558988963360818,
      "consensus_key": "0xa286ee63600c630ce7c63d86c2eb83355e4025684b37cc3b00e835a02b7a430638f3c245c06c34a85ee259fe0ccf60ef"
    },
    {
      "addr": "0xcdEed21b471b0Dc54faF74480A0E700fCc42a7b6",
      "voting_power": 122332297156857701144938,
      "consensus_key": "0x86d048b1a123a2e74c7e4998bafcecb49fd16f366d5709478e654a85ac3c8add474653b39f8fc32614e567b52fba0d85"
    },
    {
      "addr": "0xBE287C82A786218E008FF97320b08244BE4A282c",
      "voting_power": 122234531160894732588111,
      "consensus_key": "0x8afe7050848e51433a30561efc0eb1d40698e3880b496b6cbcce1c35ca748575345605877298b480b4adde5bc96c9767"
    },
    {
      "addr": "0xcf716b3930d7cf6f2ADAD90A27c39fDc9D643BBd",
      "voting_power": 121896709962514093141021,
      "consensus_key": "0xb55ff748491cc9f24725e6db2ac4e5393a8d0428de9c84cedd48d908c19ad4c3ab5160999f0fbaa2db044bf9f1ca1ded"
    },
    {
      "addr": "0xE4686A4C6E63A8ab51B458c52EB779AEcf0B74f7",
      "voting_power": 121878674528987341547224,
      "consensus_key": "0x8375584b6108dc57307d8b2335d01286f96198b829bcaa1c2ad30545cacbdf7886b1cf12e8af1cc4e585fa189b8f3995"
    },
    {
      "addr": "0x94470A842Ea4f44e668EB9C2AB81367b6Ce01772",
      "voting_power": 121703615027951096441258,
      "consensus_key": "0x93d58b3114509a592c321250cb5a512f42aa19e59dfa29aec90a262fa0dbb9364e138caff57bc4efe5fe27c05bfe6d4a"
    },
    {
      "addr": "0x383A3c437d3F12f60E5fC990119468D3561EfBfc",
      "voting_power": 121650043438421923798666,
      "consensus_key": "0x89f62c1858723ed3d027d31026e37d6edfdf730e21a9315a1f4e54c50b363f341f88ee5b420606cce4ab124bfaa6c496"
    },
    {
      "addr": "0x197B2c44b887c4aC01243BDE7E4bBa8bd95BC3a8",
      "voting_power": 121493456192220658064901,
      "consensus_key": "0xae1b49d79c320203b526e79a82f744b3c0ab2a270f1f8bc30db9e54e0ad08053e94bd0848b515175985d62f5105c7403"
    },
    {
      "addr": "0x36142A4f36974e2935192A1111C39330aA296D3C",
      "voting_power": 121431801886707582343871,
      "consensus_key": "0xb4658589fd31bafa3f1c91057c002546faa13f0129e9336402f87144f9ce143e88c6f9caffe7382a08b7447845567ad4"
    },
    {
      "addr": "0xBBf36374eb23968F25aecAEbb97BF3118f3c2fEC",
      "voting_power": 121091983741817617611461,
      "consensus_key": "0xa70a21a1d5896ad8b348c931e24810c1238d100db876d686105796d1a9af77d0c93b52d8070e0fd65cc12c7ed74c0401"
    },
    {
      "addr": "0x8f91e0ADF8065C3fFF92297267E02DF32C2978FF",
      "voting_power": 120980483385059300983556,
      "consensus_key": "0xa6c19cc2771aee5bb4e21c9c7a234046dbd1b45b330294ca02445eedebab3f02d16a0b5602e1f1403078e97c00d29bd2"
    },
    {
      "addr": "0xEf0Ba5e345C2C3937df5667A870Aae5105CAa3a5",
      "voting_power": 120973723078782527115278,
      "consensus_key": "0xb30755eb557b8908b7ed46669b814189615fd7428de1c5d53eae7459aa34cbc308a7731abfeca02d2e2ee6dfa298f463"
    },
    {
      "addr": "0x527192F3D2408C84087607b7feE1d0f907821E17",
      "voting_power": 120935934216452534331643,
      "consensus_key": "0xad6575bb260db0b73572ad023d41fdb101a52f2e6be302cd0a79cb6dc23a5d8cce9195033cfb76d2933a55fb34bd7b48"
    },
    {
      "addr": "0x3fe573552E14a0FC11Da25E43Fef11e16a785068",
      "voting_power": 120126098576170255706269,
      "consensus_key": "0x96843bfb82f6b5860aaa93d59b81ac8e08e0ff9f5a76c25e5e5e3bb127ca06d0cffb19fabb4e25305c6be4ad18c7ac7b"
    },
    {
      "addr": "0x99E2B4B27BDe92b42D04B6CF302cF564D2C13b74",
      "voting_power": 119981390170318179492552,
      "consensus_key": "0xb2eed3ac8ec307e0862cdf7b8435049a98d8c83721a6066308ec57a1d9ec7f9c4e4725872dbfc96a83d102a77b430eb0"
    },
    {
      "addr": "0x100E38f7BCEc53937BDd79ADE46F34362470577B",
      "voting_power": 119947673064847811117728,
      "consensus_key": "0xa6b9f7113a95aa40a26571f4e26f2a971910c6ff8b067dccee61e53108868f36afc0c79ed4f8dd972c5d0085181abfdb"
    },
    {
      "addr": "0x3597d2D42f8Fbbc82E8b1046048773aD6DDB717E",
      "voting_power": 118202618241243717830926,
      "consensus_key": "0x987e729178b455c34051ba097a3a61e0a6164abc00e48bd24bc6dbe23b33571555691071f475145b4fce09a1d8c6f60b"
    },
    {
      "addr": "0x725fC5416BDb173642D21DfC401519B0DCBf7f3b",
      "voting_power": 117833129350250564532001,
      "consensus_key": "0x88dfd07a93c63943841d66698c52b3f5197aaf3af6dcc538edd5a4ea653290fee64c8ceafda84d81bf5ab0a0e384d594"
    },
    {
      "addr": "0xe877FcB4b26036Baa44d3E037117b9e428B1Aa65",
      "voting_power": 115537459453908055783479,
      "consensus_key": "0xb96706e536cdc9a38d3d9e570cd1bc2bb2316a04e3d9c5a042970128833dfc8a8585222ed2c8ba86cbfd1e9477a4cf10"
    },
    {
      "addr": "0x9C7dAABb5101623340C925CFD6fF74088ff5672e",
      "voting_power": 112853580575750633754599,
      "consensus_key": "0xb579a7df6f44c54413e344657c4bf07117904b25361218b32414ff509fc5b199a1ab5fac7f50d2cfe46193c7e9f5abb5"
    },
    {
      "addr": "0xA284470fa70D8A2A8402054e40A36077fEAdCF51",
      "voting_power": 106497662658815289678415,
      "consensus_key": "0xb22e3a21177e85b6a37bf039ac795859091087131c3cc51491c4fe8c4fdf920cf7dce804cbd88190af57615ae8dd4854"
    },
    {
      "addr": "0xf34CD6c09a59d7D3d1a6C3dC231a7834E5615D6A",
      "voting_power": 2555523421469923930961,
      "consensus_key": "0x88157be3f8b1e532720701be71caccb599268fccf770ed4deab265ac4d4f5bdb8bc442c853dfd058c074c31b8a4b1f1d"
    },
    {
      "addr": "0x6a395dE946c0493157404E2b1947493c633f569E",
      "voting_power": 1731502787448693863699,
      "consensus_key": "0x8a156efa2e0eb15c347ddb6c3084bc7329a8a020d5c88b9e440a6c22cc1635674711385da28e31631eb0fcd65864878c"
    },
    {
      "addr": "0xD9fDab408dF7Ae751691BeC2efE3b713ba3f9C36",
      "voting_power": 1656852041364490318131,
      "consensus_key": "0xa0e5fada867ef428f95b1cca91fd1d9c25fd3413b5c45aae65da453a890400e1149ad24fbdc542c316cdc779764e6a2f"
    },
    {
      "addr": "0xE9FFF86CAdC3136b3D94948B8Fd23631EDaa2dE3",
      "voting_power": 1559297876847583109436,
      "consensus_key": "0xa5fc50fa0353b63905b3e3f5d5021a09d590b0de543d2c407f398c0d8646908fcfb05e29af4f85d233c55dae49de5acd"
    },
    {
      "addr": "0x59031767f20EA8F4a3d90d33aB0DAA2ca469Fd9a",
      "voting_power": 1553173366529063670250,
      "consensus_key": "0xb2831b7a6e4aec62d84c9163d66279f33b71287d9d3655de0145450f24cb247cd03e0c3e2192d0fcfcef0526b1c39194"
    },
    {
      "addr": "0x8584A78A9b94f332A34BBf24D2AF83367Da31894",
      "voting_power": 1485607390701290070504,
      "consensus_key": "0x92e378b76d88032cb0965bfe9932f01e8fd793d4dc9a00ecbaa7bc8bd66e01a020cf82beba88dafe4a85518f72737c6c"
    },
    {
      "addr": "0x3AaF7817618728ffEF81898E11A3171C33faAE41",
      "voting_power": 1484888028546905346574,
      "consensus_key": "0xb7111a7b2b676efd372de84dd149785eabf96ec4259ec78526f5920abb3429b3a9a97c0b464d8710d8bb9f61d30620da"
    },
    {
      "addr": "0x7232e75a8bFd8c9ab002BB3A00eAa885BC72A6dd",
      "voting_power": 1451683326444207046090,
      "consensus_key": "0xa878d3ba3e721c5d011bd03e10a7554f9c07221193c0b0a8cf889c4c5ddb0d2aba055e8b0e2ff9ac5b74d6468910cc84"
    },
    {
      "addr": "0x23b4Be9536F93b8D550214912fD0e38417Ff7209",
      "voting_power": 1433771132446945203831,
      "consensus_key": "0xa75b87984e7fe44699c94e5cdaf43036b9b3ddd358e7d84d319ca5b8c892abf466f73139d4940b0753fb135d7d574856"
    },
    {
      "addr": "0x94d28f08Ff81A80f4716C0a8EfC6CAC2Ec74d09E",
      "voting_power": 1404157574664495741670,
      "consensus_key": "0x86f21aa126b2bae0aca1926ae5ed55f2d0207917ca6995bd48755f809868b8903e56e4cfe48bee22224e854f2e7ffb2e"
    },
    {
      "addr": "0x19E356ebC20283fc74AF0BA4C179502A1F62fA7B",
      "voting_power": 1369982219103531894657,
      "consensus_key": "0x98e104feba56c19a59feac468b9e1589334cab43e823b93c2276da79453e7d9b21c1c7848d59150d73687ae56bcd9735"
    },
    {
      "addr": "0x831B837C3DA1B6c2AB68a690206bDfF368877E19",
      "voting_power": 1341903468818160918520,
      "consensus_key": "0xaaad12202c5a1d6ec21ebc9c2cfcd31aa601dd93aff04b492307554506c7ca70bfcf78ae12de60c3e345889fe87d068c"
    },
    {
      "addr": "0x5E17e837DcBa2728C94f95c38fA8a47CB9C8818F",
      "voting_power": 1303056370629516544975,
      "consensus_key": "0xb92b96a0bdd7d57836e326af33b40f5532f10e0268a61205acf568efc63a62391ac0debeeb04b1cdffaf9c58057d00e6"
    },
    {
      "addr": "0xc5B9d978715F081E226cb28bADB7Ba4cde5f9775",
      "voting_power": 1260575363317412211512,
      "consensus_key": "0xaac3f5dafbb22c5a4cf1db61614b36a90cd1fdd49921c1f2bc563f9e87ee85a9250e99cdedddcd6dc740f63ac501ce39"
    },
    {
      "addr": "0x00a96aaED75015Bb44cED878D927dcb15ec1FF54",
      "voting_power": 1250084090735046245714,
      "consensus_key": "0x97553f552e7488978bc6d3994ad05c757d12ce057e5cfc73f08b990186742b9e9e8ea172ec3b7029206fc0a2eac2ebcf"
    },
    {
      "addr": "0x2928FE5b911BCAf837cAd93eB9626E86a189f1dd",
      "voting_power": 1139653920688923901072,
      "consensus_key": "0xade8043500bd7354f5a5b688968d42c00ad24a6d0eea686d9ac98cff17e395ec8f3a9f52e55505bd90a3ebec4c0d1bac"
    },
    {
      "addr": "0xC1F9acAF1824F6C906b35A0D2584D6E25077C7f5",
      "voting_power": 1035883182541089359926,
      "consensus_key": "0xa10ec7e5591e3c9b57468ee5df68297edaac9f735d4c2e70c34b597d3df7c15347a0589b2fb59ab00b7bbaf006618def"
    },
    {
      "addr": "0x4cD134001EEF0843B9c69Ba9569d11fDcF4bd495",
      "voting_power": 1021069754466867358221,
      "consensus_key": "0xb12493c37a4616a96bb8a7e9da887cdbe5148d2e367ae54a47c3a9cc58b9cde66ccc9c9a51800a083ea509fb5f8ee83a"
    },
    {
      "addr": "0xDF2D0052ea56A860443039619f6DAe4434bc0Ac4",
      "voting_power": 1017604988918897061023,
      "consensus_key": "0x9544baa4ca4d4936c1c8534896c7d9e37fa9bb8d3190025712165e472542ca8c057d02d0825edbf95842247006f2dd38"
    },
    {
      "addr": "0xF9B38D02959379d43C764064dE201324d5e12931",
      "voting_power": 999150816791643061059,
      "consensus_key": "0x9419d4cef10e853c4b70e37188f2c08842a1bafdae118cdd500d9f5491cdf7f1207b9f2406e4cfa0a11695cf051a1c0e"
    },
    {
      "addr": "0x791A7F840ac11841cCB0FaA968B2e3a0Db930fCe",
      "voting_power": 954990106587103055113,
      "consensus_key": "0x98b34366132b6f53ca1168563e34d21f2610cd50c946e14b84ea071c0cd892006ac44f6958e66ce7b290798500e5fd6b"
    },
    {
      "addr": "0xfD97FB8835d25740A2Da27c69762D74F6A931858",
      "voting_power": 954949881126533527226,
      "consensus_key": "0xaabd8265d3b7a94a31b92c48c85ebbdf63895af6ec1527e2702b1af1187725916c260f2cef73e52a862c87dd0be72bb1"
    },
    {
      "addr": "0x24915749B793375a8C93090AF19928aFF1CAEcb6",
      "voting_power": 953884333034329372039,
      "consensus_key": "0x928396560c57addd279125c790b77fcb8dd8a111f9e640f821b65c7991f30d75111f980f837b4b284cbe2b28af6aa1f9"
    },
    {
      "addr": "0x718361fc3637199F24a2437331677D6B89a40519",
      "voting_power": 948962123381175564190,
      "consensus_key": "0xa5e5189151fd06c91c11943cd1c861a0bf801f4feffe290284edec8d848d6078b2f216e6098efb1c4b4d615c735facc8"
    },
    {
      "addr": "0x358488a4EdCA493FCD87610dcd50c62c8A3Dd658",
      "voting_power": 942774633442875073948,
      "consensus_key": "0xa8f645828e38bcd8fb9497a0884bab7f88df18c78da97ce111ddb17d651a45b9aeca7d8aeb2e32361d77caedd2429f33"
    },
    {
      "addr": "0x01F788E4371a70D579C178Ea7F48E04e8B2CD743",
      "voting_power": 909668015730283926860,
      "consensus_key": "0x8b0bfc8e6a2ba1c361ff9efa9bae7c9a401310faad58253d78947cced7720ae88b9e4b4a699be5ad79d87fb9e57d7e58"
    },
    {
      "addr": "0xf10f56Bf0A28E0737c7e6bB0aF92f3DDad34aE6a",
      "voting_power": 908173682553488319565,
      "consensus_key": "0x8b036f85b05cd5f08419fc694651b559030e136d3d9039b911367561d18454e8fc7bcafe1eaa1493122c2abf77899e4a"
    },
    {
      "addr": "0x22A76e194A49c9e5508Cd4A3E1cD555D088ECB08",
      "voting_power": 868676714999913271672,
      "consensus_key": "0xb3073c3332b30a607847e00a3f83a0abc5be860fe140ab07b0cb8a4ddff47a66c2a9f2652552844c3ebfb4afb8485b77"
    },
    {
      "addr": "0x783B7e7862c691405591633444CE662d4f0eCdC8",
      "voting_power": 815413115816136967343,
      "consensus_key": "0xaadfa42378feeb033c2429c51cabe39843740a5df27f28a466add11dd6a0a9046247f0100665e7f61bac5689b1ba6cb4"
    },
    {
      "addr": "0x64F83c2538A646A550Ad9bEEb63427a377359DEE",
      "voting_power": 792126042218933363738,
      "consensus_key": "0x86c4fca0dea7e1249a2a801b6d36f1f2d5168ef1c20452833e79680b34e272a34f30b67642c72698006149f510f83999"
    },
    {
      "addr": "0xd61a48b0e11B0Dc6b7Bd713B1012563c52591BAA",
      "voting_power": 753658940158723787227,
      "consensus_key": "0x93161d72e966d1705b5dcafcf0038a7c5d1f2d33ba7f1a351da6ef52c0d559b7c8687a60fa480e57e2f76a7f85d51094"
    },
    {
      "addr": "0x1Be7f70BCf8393a7e4A5BcC66F6f15d6e35cfBBC",
      "voting_power": 647287196080258522213,
      "consensus_key": "0x8e37252fc62b32896b522150a020170fbd937a9871967e3a17cc4c9941a5dceeca881eb21316e42c7cc56e3dc3fc099a"
    },
    {
      "addr": "0xDCA5DFF3D42f2db3C18dBE823380A0A81db49A7E",
      "voting_power": 647076943244552285915,
      "consensus_key": "0xb49dfa4ce7fdddbd99e6c80fc1f52bc57c732cbe2793d60d4930455153a78c53d96450e0c209b59fdfe1f535d59d7987"
    },
    {
      "addr": "0xdF239e0D5b4E6e820B0cFEF6972A90893c2073AB",
      "voting_power": 644738538771238323816,
      "consensus_key": "0xa26db57926432ff5691ab043feaa2225405e77d275ca279fb6ae27ec9f74af5af85aa652ae8f1ef3ae065e925ac3ea77"
    },
    {
      "addr": "0xB5d8be2AB4b6d7E6be7Ea28E91b370223a06289f",
      "voting_power": 613834521777030723111,
      "consensus_key": "0xa26ce7cf5d0bf122fcb7789c5b9d1f93c05513179424f142f66cd0dd4a208c8bd4895dcdb81bc669567e38c93d357333"
    },
    {
      "addr": "0xbfDcAF35f52F9ef423ac8F2621F9eef8be6dEd17",
      "voting_power": 584987300890720577138,
      "consensus_key": "0x90ff5175d92728e08610a60156da416a1fedff0662a45d7c5f57d614a47c0ec696c42bab4b015d4e288b7b11481999fc"
    },
    {
      "addr": "0x1c248C281c7aAc47B2E266Bc16B305df73CF6acB",
      "voting_power": 457099908515066240586,
      "consensus_key": "0x8b1f27e4d5946c99c1d247c0b5af869de55caf841ac96bd6426e17cf38c6b2817eb60252cc31b911c14aa6a376178992"
    },
    {
      "addr": "0x22C052b7f19fe4eEb7c87BaadE60E712b0743A55",
      "voting_power": 452769368046774912999,
      "consensus_key": "0xa6d2cf91eed8cf4ca4bbc7d132ed76bcc5a0bd00b0bf70a42e9506138d1b2c050adb8d26f47e2a72f146878d3f891556"
    },
    {
      "addr": "0x17321B2eE5f275ac2f5fb7fa3D10Fe1C789a503c",
      "voting_power": 354062939906105603087,
      "consensus_key": "0xb564451a6258e281524f26d9b4bcd35477b6fc13ec2d5bfcaf2ad5fd3624c0de98b6fd58d8e5931aa2ad10d5778ec69e"
    },
    {
      "addr": "0x26E2724dBD14Fbd52be430B97043AA4c83F05852",
      "voting_power": 307911464329777214419,
      "consensus_key": "0x8d3c82069ccf79e48b6a788f086d785ba224641a0d1934713d93ccfa1d721c156dda496994b70ed64558df3e80cd7913"
    },
    {
      "addr": "0x7E9269C66EcdDbaB4Daa8BC4b051984E66feE8B5",
      "voting_power": 295704951756375226954,
      "consensus_key": "0xb29bf614597350318a64888ca6298cb831c963992c2d6aea340895dfa0dceb1bbea73123ac7775a91735001cc1ef0e48"
    },
    {
      "addr": "0xd625d50B0d087861c286d726eC51Cf4Bd9c54357",
      "voting_power": 85962322385684277735,
      "consensus_key": "0xb47075e6d5d473c619d6b61b33cd103044c74cf83b2eea246f28318b958f8313fdbf113b179e8fbef178b35143cecc83"
    },
    {
      "addr": "0x4d09048d2C4e315664D658505C2630290ca59DdA",
      "voting_power": 60863574739211072874,
      "consensus_key": "0xaa7ddc4b43f545918fd1f660f5a108afdc05eaf9dd1a6f3f32f59373eb7c51f3e5e7a92a87140332b645ba702024146b"
    },
    {
      "addr": "0xbb0cD1D46733E115c4a570aDB3213e016EeABDAa",
      "voting_power": 1113986779259832229,
      "consensus_key": "0xb437412ef36192a11cb184b84961bdd9dd1dd3c360f8960110cf2213488fb5359b7c9d047bfbc819956f03f907115a8c"
    },
    {
      "addr": "0x7f8FaB294d861E4ED8660f3Bf4ED4B0910878f3B",
      "voting_power": 1,
      "consensus_key": "0xad7893cf6c3fa1d2b29882b3f7f271c3f461c032c59de81acbb5ecb10fa9577f1d1d8f6b1047f4fbc02608d0c2c8e875"
    }
  ],
  "previous_epoch_block": 4149000,
  "epoch_block": 4150800,
  "next_epoch_block": 4152600,
  "delta": 5
}
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


## get inflation reserve

Returns the amount of Newton remaining in the [inflation reserve](/glossary/#inflation-mechanism) at the block height of the call.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `_inflationReserve` | `uint256` | the amount of Newton in the inflation reserve. The value is returned in Newton's smallest unit `10^-18` (i.e. Newton's equivalent of ATN's [ton](/glossary/#ton)).  |

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol inflation-reserve
```

:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol inflation-reserve
38973492993331263556522187
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
aut protocol max-schedule-duration [OPTIONS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol max-schedule-duration
126230400
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
aut contract call [OPTIONS] getNextEpochBlock
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 getNextEpoc
hBlock
4154400
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
aut contract call [OPTIONS] getOracle
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.rpc}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 getOracle
"0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D"
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

### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol unbonding-share [OPTIONS] UNBONDING_ID
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut protocol unbonding-share 2
10153556909316523
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
aut contract call [OPTIONS] getValidatorState [PARAMETERS]
```
:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1  getValidatorState 0x7b06f608aB874E21f8FFC35D04B32bc03D8dCE1f
4
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
aut contract call [OPTIONS] isUnbondingReleased [PARAMETERS]
```

:::

### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1  isUnbondin
gReleased 2
true
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

Total supply is the total amount of Newton that has been minted. Circulating supply is simply the total supply minus the sum of any minted NTN that is locked and released into circulation over time according to a schedule.

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

If the validator has a [slashing](/concepts/afd/#slashing) event before this period expires, then the released Newton stake token amount may or may not correspond to the amount requested.

See Concept [Accountability and fault detection (AFD)](/concepts/afd/) for Autonity's slashing mechanism.
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
