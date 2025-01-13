---
title: "Non Stakeable Vesting Contract Interface"

description: >
  Non Stakeable Vesting Contract functions
---

Interfaces for interacting with the Non Stakeable Vesting Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Non Stakeable Vesting Contract's generated ABI and the `aut` tool's `contract` command to call the Non Stakeable Vesting Contract address `0x6901F7206A34E441Ac5020b5fB53598A65547A23`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `NonStakeableVesting.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/NonStakeableVesting.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::

## Operator only
### newContract (Non Stakeable Vesting Manager Contract)

Creates a new non stakeable vesting contract for a beneficiary. The non stakeable vesting contract subscribes to a vesting schedule which sets the vesting terms for the contract.

::: {.callout-tip title="Non stakeable vesting contract `Schedule` - what is it and why" collapse="true"}

Non-stakeable vesting contracts subscribe to a vesting schedule which has a set amount of NTN funding available for unlocking according to the unlocking constraints defined in the Schedule. The NTN is held in a vault contrct and unlocked

Each new non stakeable contract is for a set amount of NTN. Logically it is subscribing to an amount of the schedule's total available amount. Once the schedule is fully subscribed new vesting contracts cannot be taken out in the schedule.

Note that if a contract is created before the start timestamp, the beneficiary is entitled to NTN as it unlocks. Otherwise, the contract already has some unlocked NTN to which the beneficiary is not entitled to a share of and which goes to the protocol `treasury` account. The beneficiary is entitled to receive NTN that unlocks in the future after their contract start time.

:::

Constraint checks are applied:

- the amount of unsubscribed funds available in the referenced schedule is greater than or equal to the amount of the new contract
- the identifier for the new vesting contract will be a valid contract ID.

The new non stakeable vesting contract is then created for the stated amount of Newton stake token. The state of non stakeable vesting schedules is tracked in memory in a `ScheduleTracker` object. Following contract creation this is updated.

::: {.callout-tip title="`Schedule Tracker` - what is tracked and why" collapse="true"}

Tracking schedule state ensures funds are correctly distributed and new non stakeable vesting contracts correctly funded. Schedule state is tracked in memory in a `ScheduleTracker` object by three properties:

| Field | Datatype | Description |
| --| --| --|
| `unsubscribedAmount` | `uint256` | the amount of NTN that is locked in the schedule and available for vesting in new non stakeable vesting contracts |
| `expiredFromContract` | `uint256` | the amount of NTN that was locked in the contract but has expired and is no longer available to the vesting schedule |
| `initialized` | `bool` | Boolean flag indicating if the vesting schedule has been initialised (`true`) or not (`false`) | 

A schedule is initialised once the start time is reached. At this point unlocking of NTN will be initiated and begin per schedule.

Unsubscribed funds records the amount of locked NTN remaining in the schedule and available to new non stakeable vesting contracts.

Expired funds records the amount of locked NTN that would have unlocked between the schedule start time and the creation time of a non stakeable vesting contract in the case of a new vesting contract being created _after_ the schedule's start time. Logically these funds have expired and are not due to the contract `beneficiary`. Expired funds go to the protocol `treasury` account where they are available for community funding.

_Expiry only occurs in the case that a contract is created **after** the schedule's start time. In the case of a new non stakeable vesting contract being created **before** the schedule's start time there is no expiry. I.e. the schedule has not been initialised and so expiry cannot occur_.

On new contract creation the schedule tracker is updated:

- `unsubscribedAmount`: the amount of the new contract is subtracted
- `expiredFromContract`: the amount of expired funds computed for the new contract is added

:::

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the address of the contract beneficiary |
| `_amount` | `uint256` | the total amount of NTN to be vested |
| `_scheduleID` | `uint256` | identifier of the vesting schedule that the contract subscribes to |
| `_cliffDuration` | `uint256` | the cliff duration of the contract |

#### Response

None.

#### Event

None.


### createSchedule (Autonity Contract)

Creates a new schedule setting the vesting terms for a non stakeable vesting contract.

The schedule is utilised by creating new non stakeable vesting contract(s) that subscribe to the new vesting schedule.

Constraint checks are applied:

- the amount of unsubscribed funds available in the referenced schedule is greater than or equal to the amount of the new contract
- the identifier for the new vesting contract will be a valid contract ID.

Note that NTN token locked in schedules does not contribute to the circulating supply of NTN. On creating a new schedule the amount of NTN minted to the new schedule is subtracted from the circulating supply of NTN (see [`circulatingSupply()`](/reference/api/aut/#circulatingsupply)).

Constraint checks are applied:

- the schedule vault address cannot be the zero address
- the total duration specified for the schedule does not exceed maximum  allowed duration specified by the protocol parameter setting for `maxScheduleDuration`
- the total duration must be greater than `0` and cannot be zero
- the start time must be greater than or equal to the block timestamp; the schedule cannot start before its creation
- the amount of NTN locked in the schedule must be a positive value greater than `0`

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_scheduleVault` | `address` | the address of the vault contract holding the NTN token locked by the schedule |
| `_amount` | `uint256` | the total amount of NTN locked in the schedule vault  |
| `_startTime` | `uint256` | the start time at which the schedule will begin to unlock NTN from the vault contract; the start time is in Unix Timestamp format |
| `_totalDuration` | `uint256` | the length of time over which the contract will unlock; the duration is in seconds |

#### Response

None.

#### Event

On a successful call the function emits a `NewSchedule` event, logging `_scheduleVault`, `_amount`, `_startTime`, `_totalDuration`.


### changeContractBeneficiary (Non Stakeable Vesting Manager Contract)

Changes the beneficiary of a non stakeable vesting contract to a new recipient address.

On successful processing of the transaction the beneficiary address change is applied.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the beneficiary address whose contract will be canceled |
| `_contractID` | `uint256` | new contract id numbered from `0` to `(n-1)`; `n` = the total number of contracts entitled to the beneficiary (excluding already canceled ones)
| `_recipient` | `address` | the new beneficiary to whom the contract is being transferred |

#### Response

None.

#### Event

On a successful call the function emits a `BeneficiaryChanged` event, logging: `_recipient`, `_beneficiary`, `_contractID`.

## Beneficiary

### releaseAllNTN

Used by a beneficiary to release all unlocked NTN from a non stakeable vesting contract and transfer the NTN to the beneficiary's address.

A beneficiary can have multiple non stakeable vesting contracts. The identifier of the contract from which funds are to be released is passed in as the identifier argument.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_id` | `uint256` | Unique id of the contract numbered from `0` to `(n-1)` where `n` = the total number of contracts entitled to the beneficiary (excluding canceled ones). |

#### Response

None

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] releaseAllNTN [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 releaseAllNTN 0
```
:::

### releaseNTN

Used by a beneficiary to release a specific amount of unlocked NTN from a non stakeable vesting contract and transfer the NTN to the beneficiary's address.

A beneficiary can have multiple non stakeable vesting contracts. The identifier of the contract from which funds are to be released and the required amount are passed in as arguments.

Constraint checks are applied:

- the requested amount is less than or equal to the amount of withdrawable vested funds available to the beneficiary from the contract.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_amount` | `uint256` | The amount of NTN to release from the contract |
| `_id` | `uint256` | Unique id of the contract numbered from `0` to `(n-1)` where `n` = the total number of contracts entitled to the beneficiary (excluding canceled ones). |

#### Response

None

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] releaseNTN [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 releaseNTN 100 0
```
:::

### withdrawableVestedFunds

Returns the amount of funds vested and withdrawable by the beneficiary upto the end time of the last epoch.

A beneficiary can have multiple non stakeable vesting contracts. The beneficiary address and the identifier of the contract from which funds are to be released are passed in as arguments.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the address of the contract beneficiary |
| `_contractID` | `uint256` | new contract id numbered from `0` to `(n-1)`; `n` = the total number of contracts entitled to the beneficiary (excluding already canceled ones)

#### Response

None

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] withdrawableVestedFunds [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 withdrawableVestedFunds 0x3F3FeE9C908c43138d7e892CE33cAF85BDEc83e6 0
184119648021308980213089
```
:::


### vestedFunds

Returns the amount of funds vested upto the end time of the last epoch.

A beneficiary can have multiple non stakeable vesting contracts. The beneficiary address and the identifier of the contract are passed in as arguments.
   
#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the address of the contract beneficiary |
| `_contractID` | `uint256` | new contract id numbered from `0` to `(n-1)`; `n` = the total number of contracts entitled to the beneficiary (excluding already canceled ones)

#### Response

None

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] vestedFunds [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 vestedFunds 0x3F3FeE9C908c43138d7e892CE33cAF85BDEc83e6 0
184119648021308980213089
```
:::

### getExpiredFunds

Returns the amount of funds vested and withdrawable by the beneficiary upto the end time of the last epoch.

Returns the amount of funds that have expired from the contract due to creation of the contract being after the non stakeable vesting contract's schedule has started.

The expired funds are not due to the beneficiary but belong to autonity treasury account instead.

A beneficiary can have multiple non stakeable vesting contracts. The beneficiary address and the identifier of the contract from which funds are to be released are passed in as arguments.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the address of the contract beneficiary |
| `_contractID` | `uint256` | new contract id numbered from `0` to `(n-1)`; `n` = the total number of contracts entitled to the beneficiary (excluding already canceled ones)

#### Response

None

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getExpiredFunds [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 getExpiredFunds 0x3F3FeE9C908c43138d7e892CE33cAF85BDEc83e6 0
0
```
:::

### getContract

Returns metadata about a non stakeable vesting contract(s) that a given beneficiary has Newton locked in.

A beneficiary can have multiple non stakeable vesting contracts. The beneficiary address and the identifier of the contract from which funds are to be released are passed in as arguments.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_beneficiary` | `address` | the address of the contract beneficiary |
| `_contractID` | `uint256` | new contract id numbered from `0` to `(n-1)`; `n` = the total number of contracts entitled to the beneficiary (excluding already canceled ones)

#### Response

Returns a `Contract` object object consisting of:

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
aut contract call [OPTIONS] getContract [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 getContract 0x3F3FeE9C908c43138d7e892CE33cAF85BDEc83e6 0
{"currentNTNAmount": 3895625000000000000000000, "withdrawnValue": 0, "start": 1733922000, "cliffDuration": 0, "totalDuration": 60444000, "canStake": false}
```
:::


### getContracts

Returns metadata about the non stakeable vesting contract(s) that a given beneficiary has Newton locked in.

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
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 getContracts 0x6d49071fb4D3eC08b99e89Bb06208B5FA8cF7907
[{"currentNTNAmount": 9089791666666700000000000, "withdrawnValue": 0, "start": 1733922000, "cliffDuration": 0, "totalDuration": 60444000, "canStake": false}]
```
:::


### getSchedule (ScheduleController Contract imported into Autonity Contract)

Returns the schedule with the provided identifier and vault contract address.
    
#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_vault` | `address` | the address of the schedule's vault contract |
| `_id` | `uint256` | unique identifier of the schedule |

#### Response

Returns a `Schedule` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `totalAmount` | `uint256` | the total amount of NTN locked in the contract vault |
| `unlockedAmount` | `uint256` | the amount of NTN that has been unlocked from the contract to date |
| `start` | `uint256` | the start time at which the contract unlocking schedule will begin; the start time is in Unix Timestamp format |
| `totalDuration` | `uint256` | the length of time over which the contract will unlock; the duration is in seconds |
| `lastUnlockTime` | `uint256` | the last time at which the contract unlocked NTN; the last unlock time is in Unix Timestamp format |

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getSchedule [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 getSchedule 0x6901F7206A34E441Ac5020b5fB53598A65547A23 0
{"totalAmount": 12985416666666700000000000, "unlockedAmount": 615665664637241560108530, "start": 1733922000, "totalDuration": 60444000, "lastUnlockTime": 1736787776}
```
:::


### getScheduleTracker

Returns the schedule tracker for a non stakeable vesting schedule.
    
#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_id` | `uint256` | unique identifier of the non stakeable vesting contract schedule |

#### Response

Returns a `ScheduleTracker` object consisting of:

| Field | Datatype | Description |
| --| --| --|
| `unsubscribedAmount` | `uint256` | the amount of NTN that is locked in the schedule and available for vesting in new non stakeable vesting contracts |
| `expiredFromContract` | `uint256` | the amount of NTN that was locked in the contract but has expired and is no longer available to the vesting schedule |
| `initialized` | `bool` | Boolean flag indicating if the vesting schedule has been initialised (`true`) or not (`false`) | 

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getScheduleTracker [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/NonStakeableVesting.abi  --address 0x6901F7206A34E441Ac5020b5fB53598A65547A23 getScheduleTracker 1
{"unsubscribedAmount": 0, "expiredFromContract": 0, "initialized": false}
```
:::


### getTotalSchedules (ScheduleController Contract imported into Autonity Contract)

Returns the total number of schedules for the vault contract at the provided address.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_vault` | `address` | the address of the vault contract |

#### Response

Returns the number of schedules that are making use of the vault contract as an integer value.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call [OPTIONS] getTotalSchedules [PARAMETERS]
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --abi ../scripts/abi/v1.0.2-alpha/Autonity.abi  --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 getTotalSchedules 0x6901F7206A34E441Ac5020b5fB53598A65547A23
1
```
:::
