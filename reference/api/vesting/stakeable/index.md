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

::: {.callout-tip title="How to: call `getLinkedValidators()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

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
aut contract call --abi ../scripts/abi/v1.0.2-alpha/StakeableVestingLogic.abi --address 0x2456ea48f393F71dE908CE099716215CC5d421c6 getLinkedValidators
["0x551f3300FCFE0e392178b3542c009948008B2a9F"]
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

::: {.callout-tip title="How to: call `releaseAllLNTN()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

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

::: {.callout-tip title="How to: call `releaseAllNTN()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

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
 
#### Event

On a successful call the function emits a `FundsReleased` event, logging `beneficiary`, `_validator`, `_amount`.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator |
| `_amount` | `uint256` | the amount of LNTN to transfer |

#### Response

None.

#### Usage

::: {.callout-tip title="How to: call `releaseLNTN()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

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

::: {.callout-tip title="How to: call `releaseNTN()` on the vesting contract you are releasing funds from using the `StakeableVestingLogic.abi` file" collapse="true" }

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

