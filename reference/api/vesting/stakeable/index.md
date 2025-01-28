---
title: "Stakeable Vesting Contract Interface"

description: >
  Stakeable Vesting Contract functions
---

Interfaces for interacting with the Stakeable Vesting Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Stakeable Vesting Manager Contract's generated ABI and the `aut` tool's `contract` command to call the Stakeable Vesting Manager Contract address `0x117814AF22Cb83D8Ad6e8489e9477d28265bc105`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `StakeableVestingManager.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/StakeableVestingManager.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::

## Operator only


### changeContractBeneficiary (Stakeable Vesting Manager Contract)

Changes the beneficiary of a stakeable vesting contract to a new recipient address.

On successful processing of the transaction the beneficiary address change is applied and:

- The new beneficiary (i.e. recipient address) is able to release and stake tokens from the contract
- Staking rewards earned before the beneficiary change was applied are transferred to the old beneficiary address (not the new beneficiary).

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the beneficiary address whose contract will be canceled |
| `_contractID` | `uint256` | new contract id numbered from `0` to `(n-1)`; `n` = the  total number of contracts entitled to the beneficiary (excluding already canceled ones) |
| `_recipient` | `address` | the new beneficiary to whom the contract is being transferred |

#### Response

None.

#### Event

None.


### newContract (Stakeable Vesting Manager Contract)

Creates a new stakeable vesting contract for a beneficiary.

Constraint checks are applied:

- the vesting contract start time is greater than or equal to the block timestamp. I.e. the contract cannot start before the contract is created.
- the vesting contract cliff duration is not already past.
- the `msg.sender` address has a Newton balance greater than  or equal to the amount deposited to the new vesting contract.
- the identifier for the new vesting contract will be a valid contract ID.

The new stakeable vesting contract is then created for the stated amount of Newton stake token.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | address of the beneficiary |
| `_amount` | `uint256` | the total amount of NTN to be vested |
| `_startTime` | `uint256` | the start time of the contract|
| `_cliffDuration` | `uint256` | the cliff duration of the contract |
| `_totalDuration` | `uint256` | the total duration of the contract |

#### Response

None.

#### Event

None.


### setManagerContract (Stakeable Vesting Manager Contract)

Sets a new value for the Stakeable Vesting Manager Contract address.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_managerContract` | `address` | the ethereum formatted address of the Stakeable Vesting Manager Contract |


#### Response

None.

#### Event

None.


## Beneficiary

### bond

Used by a beneficiary to delegate an amount of Newton stake token from a stakeable vesting contract to a designated validator.

All bondings of stakeable vesting Newton are treated as [delegated](/glossary/#delegated) and [Liquid Newton](/glossary/#liquid-newton) will be issued for the bonding.

::: {.callout-note title="Locking and vesting of Liquid Newton from stake delegations" collapse="true"}

When a beneficiary bonds Newton locked in a stakeable vesting contract then the stake [delegation](/glossary/#delegation) is always treated as [delegated](/glossary/#delegated) and [Liquid Newton](/glossary/#liquid-newton) is issued. 

The stake [delegation](/glossary/#delegation) is technically made by the stakeable vesting contract and the Liquid Newton is locked in the vesting contract until it has vested, just as the locked Newton is.

After NTN and LNTN token has vested and become unlocked, the beneficiary is able to release their unlocked Newton and Liquid Newton from the vesting contract and transfer it to their beneficiary account. For how to do this see [`releaseFunds()`](/reference/api/vesting/stakeable/#releasefunds) and the other `release...()` and `update...()` functions on this page.
:::

The bonding request will be tracked in memory and applied at epoch end. 

On successful processing of the method call:

- a `PendingStakingRequest` object for the necessary voting power change is created:

| Field | Datatype | Description |
| --| --| --|
| `epochID` | `uint256` | the unique identifier of the block epoch in which the bonding request was created |
| `validator` | `address` | the validator identifier address |
| `amount` | `uint256` | the amount of Newton bonded to the validator |
| `requestID` | `uint256` | the unique identifier of the staking request; `0` for a bonding request |

The `PendingStakingRequest` is enqueued to an indexed `StakingRequestQueue` and tracked in memory by the stakeable vesting contract logic until applied at epoch end. 

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |
| `_amount` | `uint256` | the amount of NTN to bond |

#### Response

Returns the unique identifier for the bonding request in the Autonity Contract on successful execution of the method call.

The pending staking request is enqueued to a staking request queue and tracked in memory until applied at the epoch end.

#### Event

None.

The bonding is executed by the Autonity Protocol Contract, which will emit on success, a `NewBondingRequest` event or on revert, a `BondingRejected` event. See [Autonity Contract Interface](/reference/api/aut/), [`bond()`](/reference/api/aut/#bond) for details.

#### Usage

::: {.callout-tip title="How to: call `bond()` on the vesting contract you are bonding Newton from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `bond()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is bonding Newton stake token from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to bond Newton from, call the `unbond()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract
- and the `bond()` parameters of `validator` address and `amount`

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] bond [PARAMETERS] \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 bond 0x551f3300FCFE0e392178b3542c009948008B2a9F 100 | aut tx sign - | aut tx send -
```
:::

<!--

<!--
Duplicate naming interface function:

- claimRewards (by specific validator))
- claimRewards (all validators)

"claimRewards (by specific validator)" is documented but hidden in anticipation of renaming and unhiding for the next documentation release. See issue https://github.com/autonity/docs.autonity.org/issues/263

### claimRewards (specific validator) 

Used by a beneficiary to claim rewards from bonding Newton stake token from a stakeable vesting contract to a designated validator.

The function claims all earned ATN staking rewards from the validator and transfers the rewards to the beneficiary address. 

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |

#### Response

None.

#### Event

None.

#### Usage

::: {.callout-tip title="How to: call `claimRewards()` on the vesting contract you are bonding Newton from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `claimRewards()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is claiming rewards for bonded Newton stake token from. The function is called using the contract beneficiary address.

For how to return a list of the validators you are able to claim rewards from, see [`getLinkedValidators()`](/reference/api/vesting/stakeable/#getlinkedvalidators) on this page.

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] claimRewards [PARAMETERS] \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 claimRewards 0x551f3300FCFE0e392178b3542c009948008B2a9F | aut tx sign - | aut tx send -
```
:::
-->

### claimRewards 

Used by a beneficiary to claim rewards from bonding Newton stake token from a stakeable vesting contract to one or more validators.

The function claims earned ATN staking rewards from all validator(s) staked to from the contract and transfers the rewards to the beneficiary address. 

#### Parameters

None.

#### Response

None.

#### Event

None.

#### Usage

::: {.callout-tip title="How to: call `claimRewards()` on the vesting contract you are claiming ATN staking rewards from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `claimRewards()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is claiming rewards for bonded Newton stake token from. The function is called using the contract beneficiary address.

For how to return a list of the validators you are able to claim rewards from, see [`getLinkedValidators()`](/reference/api/vesting/stakeable/#getlinkedvalidators) on this page.

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] claimRewards \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 claimRewards | aut tx sign - | aut tx send -
```
:::


### contractTotalValue

Returns the current total value in NTN of a stakeable vesting contract.

#### Parameters

None.

#### Response

Returns the value in NTN stake token as an integer value.

#### Event

None.

#### Usage

::: {.callout-tip title="How to: call `contractTotalValue()` on a stakeable vesting contract using the `StakeableVestingLogic.abi` file" collapse="true" }

The `contractTotalValue()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return the total value a stakeable vesting contract in NTN.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return vested funds  for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `contractTotalValue()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] contractTotalValue
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 contractTotalValue
1090578595890410958904542
```


### getBeneficiary

Returns the account address of the beneficiary to a stakeable vesting contract.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the beneficiary account address |

#### Usage

::: {.callout-tip title="How to: call `getBeneficiary()` on a stakeable vesting contract using the `StakeableVestingLogic.abi` file" collapse="true" }

The `getBeneficiary()` function is called against the _specific_ stakeable vesting contract instance to return the account address of the beneficiary to the stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return the beneficiary address for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `getBeneficiary()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::


::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getBeneficiary
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.rpc}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 getBeneficiary
"0x25B456f817B645B8f8Fd9d2A5C499B279aA12a2f"
```
:::


### getContract

Returns metadata about a stakeable vesting contract that a given beneficiary has Newton locked in.

#### Parameters

None.

#### Response

Returns a `stakeableContract` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `currentNTNAmount` | `uint256` | the amount of NTN currently locked in the contract |
| `withdrawnValue` | `uint256` | the amount of NTN that has been withdrawn from the contract to date |
| `start` | `uint256` | the start time at which the contract unlocking schedule will begin; the start time is in Unix Timestamp format |
| `cliffDuration` | `uint256` | the length of time after the contract `start` time that must elapse before unlocked funds can be withdrawn; the cliff is in seconds |
| `totalDuration` | `uint256` | the length of time over which the contract will unlock; the duration is in seconds |
| `canStake` | `bool` | Boolean flag indicating if the Newton locked in the contract can be staked or not (`true`: yes, `false`: no) |

#### Usage

::: {.callout-tip title="How to: call `getContract()` on a stakeable vesting contract using the `StakeableVestingLogic.abi` file" collapse="true" }

The `getContract()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return metadata about the stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return metadata for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `getContract()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::


::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getContract
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 getContract
{"currentNTNAmount": 1090578595890410958904011, "withdrawnValue": 59421404109589041095890, "start": 1733922000, "cliffDuration": 0, "totalDuration": 60444000, "canStake": true}
```
:::


### getContractAccount

Returns the address of the stakeable vesting contract with the provided contract ID.

Constraint checks are applied:

- The contract account identifier is a valid contract ID.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_uniqueContractID` | `uint256` | Unique id of the contract |

#### Response

Returns the stakeable vesting contract account address.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getContractAccount [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingManager.abi  --address 0x117814AF22Cb83D8Ad6e8489e9477d28265bc105 getContractAccount 0
"0xD4EfaB5b47a36E4dFBc5CC60D2812AeF807F76c9"
```
:::


<!--
Duplicate naming interface function:

- getContractAccount (by uniqueContractID)
- getContractAccount (by beneficiary and contract ID)

"getContractAccount (by beneficiary and contract ID)" is documented but hidden in anticipation of renaming and unhiding for the next documentation release. See issue https://github.com/autonity/docs.autonity.org/issues/263

### getContractAccount (by beneficiary and contract ID)

Returns the address of the stakeable vesting contract for the provided beneficiary address and contract ID.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address =` | the address of the beneficiary of the contract |
| `_id` | `uint256` | contract id numbered from `0` to `(n-1)`; `n` = the total number of contracts entitled to the beneficiary (excluding already canceled ones) |

#### Response

Returns the stakeable vesting contract account address.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getContractAccount [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingManager.abi  --address 0x117814AF22Cb83D8Ad6e8489e9477d28265bc105 getContractAccount 0xb5678C419aB603cFdf2a33589Bb7E5B73c7d2dC6 0
"0x6dA198FC324b62eb36E4DDcF9E86B61023bd5fA5"
```
:::

-->


### getContractAccounts

Returns a list of the stakeable vesting contract account(s) that a given beneficiary has Newton locked in.

Metadata about a vesting contract is returned in a `Contract` object.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | address of the beneficiary  |

#### Response

Returns a list of the stakeable vesting contract account address(es) that a given beneficiary has Newton locked in.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getContractAccounts [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingManager.abi  --address 0x117814AF22Cb83D8Ad6e8489e9477d28265bc105 getContractAccounts 0xb5678C419aB603cFdf2a33589Bb7E5B73c7d2dC6
["0x6dA198FC324b62eb36E4DDcF9E86B61023bd5fA5"]
```
:::


### getContracts

Returns metadata about the stakeable vesting contract(s) that a given beneficiary has Newton locked in.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the address of the beneficiary of the contract  |

#### Response

Returns an array of `Contract` objects, each object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `currentNTNAmount` | `uint256` | the amount of NTN currently locked in the contract |
| `withdrawnValue` | `uint256` | the amount of NTN that has been withdrawn from the contract to date |
| `start` | `uint256` | the start time at which the contract unlocking schedule will begin; the start time is in Unix Timestamp format |
| `cliffDuration` | `uint256` | the length of time after the contract `start` time that must elapse before unlocked funds can be withdrawn; the cliff is in seconds |
| `totalDuration` | `uint256` | the length of time over which the contract will unlock; the duration is in seconds |
| `canStake` | `bool` | Boolean flag indicating if the Newton locked in the contract can be staked or not (`true`: yes, `false`: no) |

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getContracts [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingManager.abi  --address 0x117814AF22Cb83D8Ad6e8489e9477d28265bc105 getContracts 0xb5678C419aB603cFdf2a33589Bb7E5B73c7d2dC6
[{"currentNTNAmount": 383333333333330000000000, "withdrawnValue": 0, "start": 1733922000, "cliffDuration": 0, "totalDuration": 60444000, "canStake": true}]
```
:::


### getLinkedValidators

Returns the list of validators that are bonded to or have some unclaimed rewards due to NTN stake token that has been bonded from a stakeable vesting contract.

#### Parameters

None.

#### Response

Returns a `linkedValidators` object, consisting of an array of validator addresses.

#### Usage

::: {.callout-tip title="How to: call `getLinkedValidators()` on a stakeable  vesting contract you have made stake delegations from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `getLinkedValidators()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return a list of validators that have been bonded to using NTN from a stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return linked validators for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract to get linked validators for, call the `getLinkedValidators()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getLinkedValidators
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 getLinkedValidators
["0x551f3300FCFE0e392178b3542c009948008B2a9F", "0x7f8FaB294d861E4ED8660f3Bf4ED4B0910878f3B", "0xB5d8be2AB4b6d7E6be7Ea28E91b370223a06289f", "0x19E356ebC20283fc74AF0BA4C179502A1F62fA7B", "0x00a96aaED75015Bb44cED878D927dcb15ec1FF54"]
```
:::


### getManagerContractAddress

Returns the address of the `StakeableVestingManager` smart contract.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the `StakeableVestingManager` contract account address |

#### Usage

::: {.callout-tip title="How to: call `getManagerContractAddress()` on a stakeable vesting contract using the `StakeableVestingLogic.abi` file" collapse="true" }

The `getManagerContractAddress()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return metadata about the stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return metadata for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `getManagerContractAddress()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::


::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getManagerContractAddress
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.rpc}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 getManagerContractAddress
"0x117814AF22Cb83D8Ad6e8489e9477d28265bc105"
```
:::


### liquidBalance

Returns the amount of Liquid Newton stake token bonded to a designated validator from a stakeable vesting contract.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |

#### Response

| Field | Datatype | Description |
| --| --| --|
| value | `_liquidBalance` | the amount of the beneficiary's Liquid Newton stake token balance for the designated validator as an integer value |

#### Usage

::: {.callout-tip title="How to: call `liquidBalance()` on a stakeable vesting contract using the `StakeableVestingLogic.abi` file" collapse="true" }

The `liquidBalance()` function is called against the _specific_ stakeable vesting contract instance to return the amount of LNTN held by a beneficiary for stake delegation to a validator using NTN from the stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return the LNTN balance for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `liquidBalance()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::


::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] liquidBalance [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.rpc}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 liquidBalance 0x551f3300FCFE0e392178b3542c009948008B2a9F
181
```
:::


### lockedLiquidBalance

Returns the amount of locked (unbonding) Liquid Newton stake token bonded to a designated validator from a stakeable vesting contract.

::: {.callout-note title="Unbonding constraints" collapse="false" }
During unbonding staked NTN is subject to locking as described in concept [Staking, unbonding period](/concepts/staking/#unbondingperiod).

During this period the liquid stake token is locked and cannot be transferred. Calling `lockedLiquidBalance()` queries the vesting contract and returns the amount of locked Liquid Newton held by the vesting contract for the beneficiary.
:::

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |

#### Response

| Field | Datatype | Description |
| --| --| --|
| value | `_lockedLiquidBalance` | the amount of the beneficiary's locked Liquid Newton stake token balance for the designated validator as an integer value |

#### Usage

::: {.callout-tip title="How to: call `lockedLiquidBalance()` on a stakeable vesting contract using the `StakeableVestingLogic.abi` file" collapse="true" }

The `lockedLiquidBalance()` function is called against the _specific_ stakeable vesting contract instance to return the amount of locked LNTN held by a beneficiary for stake delegation to a validator using NTN from the stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return the locked LNTN balance for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `lockedLiquidBalance()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::


::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] lockedLiquidBalance [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.rpc}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 lockedLiquidBalance 0x551f3300FCFE0e392178b3542c009948008B2a9F
0
```
:::


### releaseAllLNTN

Used by beneficiary to transfer all vested LNTN to the beneficiary's own address.

Unlocked LNTN is released in the order in which it was bonded until the equivalent amount of withdrawable vested funds in NTN is obtained. LNTN is released from validators in the order in which it was bonded. A list of validator addresses to which stake delegations have been made by the beneficiary is maintained as an indexed `linkedValidators` list. LNTN is released from validators beginning at index `0`. If there is insufficient unlocked LNTN for the validator at index `0`, then the logic will proceed to release LNTN at the following index(es) until the required amount of LNTN is obtained.


#### Parameters

None.

#### Response

None.

#### Usage

::: {.callout-tip title="How to: call `releaseAllLNTN()` on the vesting contract you are releasing LNTN funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `releaseAllLNTN()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is releasing withdrawable funds from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to release funds from, call the `releaseAllLNTN()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] releaseAllLNTN \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x6dA198FC324b62eb36E4DDcF9E86B61023bd5fA5 releaseAllLNTN | aut tx sign - | aut tx send -
```
:::

### releaseAllNTN

Used by beneficiary to transfer all vested NTN to the beneficiary's own address.

#### Parameters

None.

#### Response

None.

#### Usage

::: {.callout-tip title="How to: call `releaseAllNTN()` on the vesting contract you are releasing NTN funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `releaseAllNTN()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is releasing withdrawable funds from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to release funds from, call the `releaseAllNTN()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] releaseAllNTN \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x6dA198FC324b62eb36E4DDcF9E86B61023bd5fA5 releaseAllNTN | aut tx sign - | aut tx send -
```
:::

### releaseFunds

Used by a beneficiary to transfer all withdrawable funds (i.e. unlocked, vested NTN and LNTN) from a stakeable vesting contract to the beneficiary's own address.

When releasing unlocked funds, the function will attempt to release the unlocked funds from the withdrawable NTN balance first. If that NTN balance is insufficient, withdrawable LNTN will then be released until the amount of withdrawable unlocked funds is attained. Withdrawable LNTN is released in bonding order

- If the NTN balance of the contract is greater than or equal to the amount of withdrawable vested funds, then all of the vested funds will be released.
- Else, if the NTN balance of the contract is less than the amount of withdrawable vested funds, then the available NTN balance of the contract will be released and the remainder will be made up by releasing LNTN from locked NTN that has been staked. The withdrawable vested funds amount is updated to subtract the released amount of NTN. The remaining withdrawable vested funds amount due is taken by releasing LNTN from NTN that has been staked from the contract where that NTN has now vested and the LNTN has therefore become withdrawable. The LNTN is released and can then be transferred to the beneficiary's own address by the beneficiary calling by [`releaseAllLNTN()`](/reference/api/vesting/stakeable/#releasealllntn).


::: {.callout-tip title="Retrieve the order in which LNTN will be released by calling `getLinkedValidators()`" collapse="true"}

LNTN is released in the sequential order of priority by which it was originally staked. I.e. the first validator stake delegation to is released first until exhausted. LNTN is then released from the second validator stake delegation, _et cetera_.

Before calling `releaseFunds()` call [`getLinkedValidators()`](/reference/api/vesting/stakeable/#getlinkedvalidators) to return a `linkedValidators` list of the validators to which stake delegations using NTN from the stakeable vesting contract has been bonded. LNTN will be released in that order.

:::

#### Parameters

None.

#### Response

None.

#### Usage

::: {.callout-tip title="How to: call `releaseFunds()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `releaseFunds()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is releasing withdrawable funds from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to release funds from, call the `releaseFunds()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] releaseFunds \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0xD4EfaB5b47a36E4dFBc5CC60D2812AeF807F76c9 releaseFunds | aut tx sign - | aut tx send -
```
:::


### releaseLNTN

Used by a beneficiary to transfer an amount of vested LNTN from a stakeable vesting contract to the beneficiary's address.

Constraint checks are applied:

- the amount of unlocked LNTN for the validator stake delegation is greater than or equal to the requested amount
- the requested amount of LNTN is greater than `0`

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |
| `_amount` | `uint256` | the amount of LNTN to transfer |

#### Response

None.

#### Event

On a successful call the function emits a `FundsReleased` event, logging `beneficiary`, `_validator`, `_amount`.

#### Usage

::: {.callout-tip title="How to: call `releaseLNTN()` on the vesting contract you are transferring LNTN funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `releaseLNTN()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is releasing withdrawable funds from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to transfer funds from, call the `releaseLNTN()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] releaseLNTN [PARAMETERS] \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x6dA198FC324b62eb36E4DDcF9E86B61023bd5fA5 releaseLNTN 0x551f3300FCFE0e392178b3542c009948008B2a9F 50 | aut tx sign - | aut tx send -
```
:::


### releaseNTN

Used by a beneficiary to transfer an amount of vested NTN from a stakeable vesting contract to the beneficiary's address.

A beneficiary can have multiple stakeable vesting contracts. The contract from which funds are to be released is specified by addressing the contract call to the stakeable vesting contract address. See **Usage** beneath.

Constraint checks are applied:

- the requested amount is less than or equal to the amount of withdrawable vested funds available to the beneficiary from the contract.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_amount` | `uint256` | the amount of NTN to transfer |

#### Response

None.

#### Usage

::: {.callout-tip title="How to: call `releaseNTN()` on the vesting contract you are transferring funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `releaseNTN()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is releasing withdrawable funds from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to transfer funds from, call the `releaseNTN()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] releaseNTN [PARAMETERS] \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x6dA198FC324b62eb36E4DDcF9E86B61023bd5fA5 releaseNTN 100 | aut tx sign - | aut tx send -
```
:::


### unbond

Used by a beneficiary to unbond an amount of Liquid Newton stake token from a stakeable vesting contract from a designated validator.

The unbonding request is enqueued to a staking request queue and tracked in memory until applied at the end of the epoch in which the unbonding period expires.

::: {.callout-important title="Warning" collapse="false"}
The unbonding request will only be effective after the unbonding period, rounded to the next epoch.

If the validator has a [slashing](/concepts/accountability/#slashing) event before this period expires, then the released Newton stake token amount may or may not correspond to the amount requested.

See Concept [Accountability and fault detection (AFD)](/concepts/accountability/) for Autonity's slashing mechanism.
:::

On successful processing of the method call:

- a `PendingStakingRequest` object for the necessary voting power change is created:

| Field | Datatype | Description |
| --| --| --|
| `epochID` | `uint256` | the unique identifier of the block epoch in which the unbonding request was created |
| `validator` | `address` | the validator identifier address |
| `amount` | `uint256` | the amount of Liquid Newton to be unbonded from the validator `0` for an unbonding request |
| `requestID` | `uint256` | the unique identifier of the staking request; |

The `PendingStakingRequest` is enqueued to an indexed `StakingRequestQueue` and tracked in memory by the stakeable vesting contract logic until applied at epoch end. 

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |
| `_amount` | `uint256` | the amount of LNTN to unbond |

#### Response

Returns the unique identifier for the unbonding request in the Autonity Contract on successful execution of the method call.

The pending staking request is enqueued to a staking request queue and tracked in memory until applied in the following epoch.

#### Event

None.

The unbonding is executed by the Autonity Protocol Contract, which will emit on success, a `UnbondingRequest` event. See [Autonity Contract Interface](/reference/api/aut/), [`unbond()`](/reference/api/aut/#unbond) for details.

#### Usage

::: {.callout-tip title="How to: call `unbond()` on the vesting contract you are unbonding Liquid Newton from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `unbond()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is unbonding Liquid Newton from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to unbond Liquid Newton from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to unbond Liquid Newton from, call the `unbond()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract
- and the `unbond()` parameters of `validator` address and `amount`

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] unbond [PARAMETERS] \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 unbond 0x551f3300FCFE0e392178b3542c009948008B2a9F 1 | aut tx sign - | aut tx send -
```
:::


### unclaimedRewards

Returns unclaimed rewards from bonding Newton stake token from a stakeable vesting contract to a validator.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |

#### Response

Returns the amount of unclaimed rewards as an integer value

#### Event

None.

#### Usage

::: {.callout-tip title="How to: call `unclaimedRewards()` on a stakeable  vesting contract to discover the amount of claimable ATN staking rewards  that are available from stake delegation using the `StakeableVestingLogic.abi` file" collapse="true" }

The `unclaimedRewards()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return the available amount of unclaimed staking rewards from stake delegations using NTN from a stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return unclaimed rewards for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `unclaimedRewards()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] unclaimedRewards [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 unclaimedRewards 0x551f3300FCFE0e392178b3542c009948008B2a9F
0
```
:::

<!--
Duplicate naming interface function:

- unclaimedRewards (by specific validator))
- unclaimedRewards (all validators)

"unclaimedRewards (all validators)" is documented but hidden in anticipation of renaming and unhiding for the next documentation release. See issue https://github.com/autonity/docs.autonity.org/issues/263

### unclaimedRewards (all validators)

Returns unclaimed rewards from bonding Newton stake token from a stakeable vesting contract to one or more validators.

The function returns the amount of earned and claimable ATN staking rewards from all validator(s) the beneficiary has staked to from the contract. 


#### Parameters

None.

#### Response

Returns the amount of unclaimed rewards as an integer value

#### Event

None.

#### Usage

::: {.callout-tip title="How to: call `unclaimedRewards()` on a stakeable  vesting contract to discover the amount of claimable ATN staking rewards  that are available from stake delegation using the `StakeableVestingLogic.abi` file" collapse="true" }

The `unclaimedRewards()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return the available amount of unclaimed staking rewards from stake delegations using NTN from a stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return unclaimed rewards for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `unclaimedRewards()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] unclaimedRewards
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 unclaimedRewards
30
```

-->


### unlockedLiquidBalance

Returns the amount of unlocked (not vested) Liquid Newton stake token bonded to a designated validator from a stakeable vesting contract.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |

#### Response

| Field | Datatype | Description |
| --| --| --|
| value | `_unlockedLiquidBalance` | the amount of the beneficiary's unlocked Liquid Newton stake token balance for the designated validator as an integer value |

#### Usage

::: {.callout-tip title="How to: call `unlockedLiquidBalance()` on a stakeable vesting contract using the `StakeableVestingLogic.abi` file" collapse="true" }

The `unlockedLiquidBalance()` function is called against the _specific_ stakeable vesting contract instance to return the amount of unlocked LNTN held by a beneficiary for stake delegation to a validator using NTN from the stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return the unlocked LNTN balance for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `unlockedLiquidBalance()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::


::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] unlockedLiquidBalance [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.rpc}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 unlockedLiquidBalance 0x551f3300FCFE0e392178b3542c009948008B2a9F
181
```
:::


### updateFunds

Updates the NTN and LNTN funds of the stakeable vesting contract by triggering the processing of any pending staking requests.

Calling `updateFunds()` allows for the case where funds available for release are missing because of a pending staking operation that has failed. The function updates funds by triggering the handling of any pending bonding or unbonding requests.

#### Parameters

None.

#### Response

None.

#### Usage

::: {.callout-tip title="How to: call `updateFunds()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `updateFunds()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is releasing withdrawable funds from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to release funds from, call the `updateFunds()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] updateFunds \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x6dA198FC324b62eb36E4DDcF9E86B61023bd5fA5 updateFunds | aut tx sign - | aut tx send -
```
:::


### updateFundsAndGetContract

Updates the funds of the contract by invoking [`updateFunds()`](/reference/api/vesting/stakeable/#updatefunds) and returns the address of the stakeable vesting contract.

#### Parameters

None.

#### Response

Returns the address of the stakeable vesting contract whose funds have been updated by the function call.

#### Usage

::: {.callout-tip title="How to: call `updateFundsAndGetContract()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

The `updateFundsAndGetContract()` function is called against the _specific_ stakeable vesting contract instance that the beneficiary is releasing withdrawable funds from. The function is called using the contract beneficiary address.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract tx` command.

To determine the stakeable vesting contract you want to release funds from you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts
- view the state of your vesting contract(s) to verify your available funds amounts. Use [`getContracts()`](/reference/api/vesting/stakeable/#getcontracts) to return metadata about your vesting contract(s). 

Having determined which vesting contract to release funds from, call the `updateFundsAndGetContract()` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

Remember to send the transaction using your beneficiary address, otherwise the call will fail with the message "`execution reverted: caller is not beneficiary of the contract`".

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx [OPTIONS] updateFundsAndGetContract \
| aut tx sign - \
| aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract tx --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 updateFundsAndGetContract | aut tx sign - | aut tx send -
```
:::



### vestedFunds

Returns the amount of vested funds in NTN from a stakeable vesting contract.

Returns the amount of funds vested upto the end time of the last epoch.

#### Parameters

None.

#### Response

Returns the amount of vested NTN stake token as an integer value.

#### Event

None.

#### Usage

::: {.callout-tip title="How to: call `vestedFunds()` on a stakeable  vesting contract to discover the amount of vested funds that are available using the `StakeableVestingLogic.abi` file" collapse="true" }

The `vestedFunds()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return the available amount of vested funds from a stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return vested funds  for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `vestedFunds ` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] vestedFunds
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 vestedFunds
8185007610350076103504
```


### withdrawableVestedFunds

Returns the amount of vested funds and withdrawable in NTN from a stakeable vesting contract.

Returns the amount of funds vested and withdrawable by the beneficiary upto the end time of the last epoch.

#### Parameters

None.

#### Response

Returns the amount of withdrawable vested NTN stake token as an integer value.

#### Event

None.

#### Usage

::: {.callout-tip title="How to: call `withdrawableVestedFunds()` on a stakeable vesting contract to discover the amount of withdrawable vested funds that are available using the `StakeableVestingLogic.abi` file" collapse="true" }

The `withdrawableVestedFunds()` function is called against the _specific_ stakeable vesting contract instance that the contract beneficiary is calling to return the available amount of withdrawable vested funds from a stakeable vesting contract.

The function is defined in the Stakeable Vesting Logic Solidity contract. To call it you will need to use the `StakeableVestingLogic.abi` file and the vesting contract instance address as the `--abi` and `--address` OPTIONS in the `aut contract call` command.

To determine the stakeable vesting contract you want to return vested funds  for you can:

- retrieve your stakeable vesting contract address(es). Use [`getContractAccount()`](/reference/api/vesting/stakeable/#getcontractaccount). If you have multiple stakeable vesting contracts use [`getContractAccounts()`](/reference/api/vesting/stakeable/#getcontractaccounts) to return a list of your vesting contracts

Having determined which vesting contract, call the `withdrawableVestedFunds ` function specifying:

- for `--abi`: the path to `./StakeableVestingLogic.abi`
- for `--address`: the address of your stakeable vesting contract

:::

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] withdrawableVestedFunds
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi  --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 withdrawableVestedFunds
8150761035007610350079
```
