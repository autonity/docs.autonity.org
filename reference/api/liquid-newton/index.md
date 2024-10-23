---
title: "Liquid Newton Contract Interface"

description: >
  Autonity Liquid Newton Contract functions
---

The LiquidNewton contract is deployed by the Autonity contract in response to validator registration.  It implements the Liquid Newton token for that validator, and handles the distribution of staking rewards to all delegators.

The address of the Liquid Newton contract for a given validator can be determined by the information returned from the Autonity contract [`getValidator`](/reference/api/aut/#getvalidator) method (see [here](/delegators/transfer-lntn/) for details of how to query this using Autonity CLI).

Liquid Newton tokens implement the ERC20 interface, and so all ERC20 calls are implemented.  The following public methods are also available for handling the reward distribution and querying Liquid Newton balances.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Autonity implements a 'pull-based' model for staking rewards where delegators must manually retrieve their rewards.
:::

::: {.callout-note title="Protocol contract calls" collapse="false"}
Some Usage and Examples illustrate using the Liquid Newton  Contracts' generated ABI and the `aut` tool's `contract` command to call the Liquid Newton Contract functions. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The contract `.abi` files are generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Liquid.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).

You will need to specify the validator's Liquid Newton contract address. This can be retrieved using the `aut` command `aut validator info` - for usage see Autonity Contract Interface and [`getValidator()`](/reference/api/aut/#getvalidator).
:::

## unclaimedRewards

Queries the contract and returns the total rewards owed to a given account.

This function is used by the `aut validator unclaimed-rewards` command of [`aut`](/account-holders/setup-aut/).  Further details are given in the ["Claiming staking rewards"](/delegators/claim-rewards/#get-reward-balance) section.

## claimRewards

Computes the total rewards owed to the caller, and sends the appropriate amount of auton.

The `aut validator claim-rewards` command uses this function.  Usage details and examples are given in the ["Claiming staking rewards"](/delegators/claim-rewards/#claim-rewards) section.

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
