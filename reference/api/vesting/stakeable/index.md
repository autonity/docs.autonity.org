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


The new stakeable vesting contract is then created with the deposited amount of Newton stake token.

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
| `_contractID` | `uint256` | new contract id numbered from 0 to (n-1); n = total contracts entitled to the beneficiary (excluding already canceled ones)
| `_recipient` | `address` | the new beneficiary to whom the contract is being transferred |

#### Response

None.

#### Event

On a successful call the function emits a `BeneficiaryChanged` event, logging: `_recipient`, `_beneficiary`, `_contractID`.

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
| `_id` | `uint256` | contract id numbered from 0 to (n-1); n = total contracts entitled to the beneficiary (excluding already canceled ones) |

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
| `cliffDuration` | `uint256` | the length of time over which the contract will unlock; the duration is in seconds |
| `totalDuration` | `uint256` | the length of time between the contract `start` time and the time at which the contract unlocking schedule will begin to unlock; the cliff is in seconds |
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
