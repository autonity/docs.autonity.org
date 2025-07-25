---
title: "Liquid Newton Contract Interface"

description: >
  Autonity Liquid Newton Contract functions
---

The Liquid Newton contract is deployed by the Autonity contract in response to validator registration.  It implements the Liquid Newton token for that validator, and handles the distribution of staking rewards to all delegators.

The address of the Liquid Newton contract for a given validator can be determined by the information returned from the Autonity contract [`getValidator`](/reference/api/aut/#getvalidator) method (see [here](/delegators/transfer-lntn/) for details of how to query this using Autonity CLI).

Liquid Newton tokens implement the ERC20 interface, and so all ERC20 calls are implemented. The following public methods are also available for handling the reward distribution and querying Liquid Newton balances.

::: {.callout-note title="Claiming ATN staking rewards" collapse="false"}
Autonity implements a 'pull-based' model for staking rewards where delegators must manually retrieve their rewards.
:::

::: {.callout-note title="Claiming validator commission on ATN staking rewards" collapse="false"}

The validator `treasury` receives commission rewards automatically epoch end when the Autonity Contract [`finalize()`(/reference/api/aut/op-prot/#finalize) function is invoked to finalize the last block of the epoch.

`claimTreasuryATN()` is provided for a failure scenario if `finalize()` fails to send ATN rewards to the validator `treasury` end of epoch. To prevent reward loss the protocol tracks ATN rewards for the `treasury` and  the `treasury` can claim them by calling `claimTreasuryATN()`. A validator operator can check if there are commission rewards to claim by calling [`getTreasuryUnclaimedATN()`](/reference/api/liquid-newton/#gettreasuryunclaimedatn) from the validator `treasury` address.

The `claimRewards()` function is for stake delegators who don't receive their rewards automatically. 

:::

::: {.callout-note title="Protocol contract calls" collapse="false"}
Some Usage and Examples illustrate using the Liquid Newton  Contracts' generated ABI and the `aut` tool's `contract` command to call the Liquid Newton Contract functions. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The contract `.abi` files are generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Liquid.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).

You will need to specify the validator's Liquid Newton contract address. This can be retrieved using the `aut` command `aut validator info` - for usage see Autonity Contract Interface and [`getValidator()`](/reference/api/aut/#getvalidator).
:::


## claimRewards

Computes the total ATN rewards owed to the caller from a specific validator stake delegation, and sends the appropriate amount of Auton to the caller's [staking wallet account](/glossary/#staking-wallet-account).

::: {.callout-note title="Note" collapse="false"}

- The claim rewards function is used by _any_ stake delegator to claim ATN staking rewards, i.e. for [delegated](/glossary/#delegated) or [self-bonded](/glossary/#self-bonded) stake.
- Ir returns rewards for a designated validator. If the caller has stake delegations to _multiple_ validators, then `claimRewards()` will need to be called for each stake delegation.

:::

The `aut validator claim-rewards` command uses this function.  Usage details and examples are given in the ["Claiming staking rewards"](/delegators/claim-rewards/#claim-rewards) section.

## claimTreasuryATN

Used by a validator operator to claim ATN rewards accrued by the validator from the validator commission charged on stake [delegations](/glossary/#delegation). The rewards are sent to the validator `treasury` account.

Constraint checks are applied:

- the caller is the validator `treasury` address.

### Parameters
   
None.

### Response

None.

### Event

None.

### Usage

::: {.callout-note title="Note" collapse="false"}
The `claimTreasuryATN()` function in the Liquid Newton Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

## getTreasuryUnclaimedATN

Used by a validator operator to return the total unclaimed ATN rewards accrued by the validator via the commission charged on [delegated](/glossary/#delegated) stake. The rewards are sent to the validator `treasury` account.

The rewards can be claimed and sent to the validator's `treasury` by the validator operator calling [`claimTreasuryATN()`](/reference/api/liquid-newton/#claimtreasuryatn).

### Parameters
   
None.

### Response

None.

### Event

None.

### Usage

::: {.callout-note title="Note" collapse="false"}
The `getTreasuryUnclaimedATN()` function in the Liquid Newton Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract call -h` for how to submit a transaction calling the interface function.
:::

## balanceOf (ERC-20)

::: {.callout-note title="ERC-20 balanceOf()" collapse="false"}

Note that the ERC-20 `balanceOf()` will return the sum of locked and unlocked balances of LNTN in the contract. The locked and unlocked balances can be returned individually using `lockedBalanceOf()` and `unlockedBalanceOf()`.

:::

##  lockedBalanceOf

Queries the contract and returns the amount of locked Liquid Newton held by a stake delegator's account.

### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `delegator ` | `address` | the account address of the Liquid Newton holder for which the locked balance amount is requested |

### Response

| Field | Datatype | Description |
| --| --| --|
| `amount` |  `uint256`  | the account balance for Liquid Newton in a locked state |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address lockedBalanceOf delegator
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x109f93893af4c4b0afc7a9e97b59991260f98313  lockedBalanceOf 0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa
0
```
:::

## unclaimedRewards

Returns the total ATN rewards owed to a given account.
Computes the total ATN rewards owed to the caller for a specific validator stake delegation.

This function is used by the `aut validator unclaimed-rewards` command of [`aut`](/account-holders/setup-aut/).  Further details are given in the ["Claiming staking rewards"](/delegators/claim-rewards/#get-reward-balance) section.


##  unlockedBalanceOf

Queries the contract and returns the amount of unlocked Liquid Newton held by a stake delegator's account.

### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `delegator ` | `address` | the account address of the Liquid Newton holder for which the unlocked balance amount is requested |

### Response

| Field | Datatype | Description |
| --| --| --|
| `amount` |  `uint256`  | the account balance for Liquid Newton in an unlocked state |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address unlockedBalanceOf delegator
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x109f93893af4c4b0afc7a9e97b59991260f98313 unlockedBalanceOf 0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa
0
```
:::


