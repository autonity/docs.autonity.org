---
title: "Governance and Protocol Only Reference"

description: >
  Autonity Protocol Contract functions callable by governance operator and by protocol only 
---

## Operator only

Functions with the `onlyOperator` access constraint that can only be called by the governance operator account.

### burn

Burns the specified amount of Newton stake token from an account. When `x` amount of newton is burned, then `x` is simply deducted from the account’s balance and from the total supply of newton in circulation.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_addr ` | `address` | the account address from which newton is being burned |
| `_amount ` | `uint256` | a positive integer value for the value amount being burned, denominated in Newton |

#### Response

No response object is returned on successful execution of the method call.

The new Newton balance of the account can be retrieved from state by calling the [`balanceOf()`](/reference/api/aut/#balanceof) method.

The new total supply of Newton in circulation can be retrieved from state by calling the [`totalSupply()`](/reference/api/aut/#totalsupply) method.

#### Event

On a successful call the function emits a `BurnedStake` event, logging: `_addr`, `_amount`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut governance burn [OPTIONS] AMOUNT ACCOUNT
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut governance burn 1 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x3e86062cca9fa263acb7076f8287117e9ee2c5570e0f4e4bd2ff4db21895796e
```
:::


###  createSchedule

Creates a new schedule for a non-stakeable vesting contract, specifying how much Newton is to be locked, when the schedule will begin to release Newton into circulation, and the total duration of the locking schedule.

Constraint checks are applied:

- the `maxScheduleDuration` protocol parameter value is greater than or equal to the new schedule's `_totalDuration`

On success the designated amount of Newton is minted to the vesting contract address and the amount of Newton in the circulating supply reduced by that amount.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_scheduleVault` | `address` | the contract account address of the vesting contract (or 'vault') that will hold the locked Newton |
| `_amount ` | `uint256` | a positive integer value for the total value amount of the schedule, denominated in Newton |
| `_startTime ` | `uint256` | the start time of the schedule in seconds |
| `_totalDuration ` | `uint256` | the total duration of the schedule in seconds |

#### Response

No response object is returned on successful execution of the method call.

The new supply of Newton in circulation can be retrieved from state by calling the [`circulatingSupply()`](/reference/api/aut/#circulatingsupply) method.

#### Event

On a successful call the function emits a `NewSchedule` event, logging: `_scheduleVault`, `_amount`, `_startTime`, `_totalDuration`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut governance create-schedule [OPTIONS] ADDRESS AMOUNT START_TIME TOTAL_DURATION
```
:::


### mint

Mints new stake token and adds it to the recipient's account balance. When `x` amount of newton is minted, then `x` is simply added to the account’s balance and to the total supply of newton in circulation.       
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_addr ` | `address` | the recipient account address |
| `_amount ` | `uint256` | a positive integer value for the value amount being minted, denominated in `Newton` |

#### Response

No response object is returned on successful execution of the method call.

The new Newton balance of the recipient account can be retrieved from state by calling the [`balanceOf()`](/reference/api/aut/#balanceof) method.

The new total supply of newton in circulation can be retrieved from state by calling the [`totalSupply()`](/reference/api/aut/#totalsupply) method.

#### Event

On a successful call the function emits a `MintedStake` event, logging: `_addr`, `_amount`.

#### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut governance mint [OPTIONS] AMOUNT RECIPIENT
```
:::

#### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut governance mint 1 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xbd9e604372cc922c4594b0fce94919f933734e29b0043c5af3c4a7774ed99ad7
```
:::


###  mint (Supply Control Contract)

The Auton mint function, called by the Stabilization Contract to mint Auton to recipients while processing a CDP borrowing. 

The protocol calls the function using by the `stabilizer` account, the Stabilization Contract address
The recipient cannot be the `stabilizer` account or the zero address. The minted `amount` cannot be equal to `0` or greater than the Supply Control Contract's available auton `balance`.
    
When `x` amount of auton is minted, then `x` is simply added to the account’s balance, increasing the total supply of Auton in circulation and reducing the supply of Auton available for minting.       
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `recipient ` | `address` | the recipient account address |
| `amount ` | `uint256` | amount of Auton to mint (non-zero) |

#### Response

No response object is returned on successful execution of the method call.

The new Auton balance of the recipient account can be returned from state using `aut` to [Get the auton balance](/account-holders/submit-trans-aut/#get-auton-balance).

The new total supply of auton available for minting can be retrieved from state by calling the [`availableSupply()`](/reference/api/asm/supplycontrol/#availablesupply) method.

#### Event

On a successful call the function emits a `Mint` event, logging: `recipient`, `amount`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Supply Control Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

###  modifyBasket (ACU Contract)

Modifies the ACU symbols, quantities, or scale of the ACU currency basket.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `symbols_` | `string` | the symbols used to retrieve prices |
| `quantities_` | `uint256` | the basket quantity corresponding to each symbol |
| `scale_` | `uint256` | the scale for quantities and the ACU value |

#### Response

None.

#### Event

None.

#### Usage




###  setAccountabilityContract

Sets a new value for the [Autonity Accountability Contract](/concepts/architecture/#autonity-accountability-contract) address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Accountability Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-accountability-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setAcuContract

Sets a new value for the [ASM Autonomous Currency Unit (ACU) Contract](/concepts/architecture/#asm-acu-contract) address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the ACU Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-acu-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setBaseSlashingRates (Accountability Contract)

Sets the `low`, `mid`, and `high` base slashing rates protocol parameters.

The new base slashing rate values must be scaled per the [slashing rate scale factor](/concepts/afd/#slashing-protocol-configuration) of the Accountability Fault Detection protocol's configuration.

Constraint checks are applied:

- the `low` slashing rate cannot exceed the `mid` slashing rate
- the `mid` slashing rate cannot exceed the `high` slashing rate
- the `high` slashing rate cannot exceed the slashing rate scale factor.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_rates ` | `uint256` | comma separated list of the new `low`, `mid` and `high` values for the base slashing rates |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setBaseSlashingRates()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setCommitteeSize

Sets the maximum size of the consensus committee. 

Constraint checks are applied:

- the new committee size must be greater than 0.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_size` | `uint256` | a positive integer value for the maximum committee size |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by calling the [`getMaxCommitteeSize()`](/reference/api/aut/#getmaxcommitteesize) method.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-committee-size [OPTIONS] COMMITTEE_SIZE
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
$ aut governance set-committee-size 50 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x3dbe5afbb89267b1549f735d09ac3acd6a4894eccbab8dca125497806c8fdc2d
```
:::


### setDelta (Omission Accountability Contract)

Sets the `delta` protocol parameter of the Omission Accountability protocol's configuration. It will get updated at epoch end.

Constraint checks are applied:

- the `delta` needs to be at least `2` (it cannot be 1 due to optimistic block building).
- the epoch period needs to be greater than `delta+lookbackWindow-1`.
    
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_delta ` | `uint256` | the new value for delta |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setEpochPeriod

Sets a new value for the `epochPeriod` protocol parameter. The change will be applied at epoch end.

The `epochPeriod` period value must be less than the `unbondingPeriod` protocol parameter.

Constraint checks are applied:

- The new epoch period value cannot be `0`.
- If the new value is decreasing the current epoch period, checks the current chain head has not already exceeded the new epoch period window. The new epoch period needs to be greater than `delta+lookbackWindow-1`.
-  The new epoch period is less than or equal to `votePeriod * 2` (a check to ensure there is sufficient time for any oracle voter changes before epoch end).
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_period` | `uint256` | a positive integer value specifying the number of blocks defining the duration of an epoch on the network. Value must respect the equation `epochPeriod > delta+lookback-1` |

#### Response

No response object is returned on successful execution of the call.

The updated parameter can be retrieved using [`getEpochPeriod()`](/reference/api/aut/#getepochperiod).

#### Event

On a successful call the function emits an `EpochPeriodUpdated` event, logging: `period`, `appliedAtBlock`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-epoch-period [OPTIONS] EPOCH_PERIOD
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-epoch-period 1000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xdf3b3eb316a3070a591621d8cc450ca6d1af3a6d57a0455714b5bff72eb06b92
```
:::


###  setFactors (Accountability Contract)

Sets the `collusion`, `history`, and `jail` punishment factor protocol parameters.

The new collusion and history factor values must not exceed the [slashing rate scale factor](/concepts/afd/#slashing-protocol-configuration) of the Accountability Fault Detection protocol's configuration. The jail factor is specified as a number of epochs.

Constraint checks are applied:

- the `collusion factor` cannot exceed the slashing rate scale factor.
- the `history factor` cannot exceed the slashing rate scale factor.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_rates ` | `uint256` | comma separated list of the new `CollusionFactor`, `HistoryFactor` and `JailFactor` values for the base slashing rates |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setFactors()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setInactivityThreshold (Omission Accountability Contract)

Sets the `inactivityThreshold` protocol parameter of the Omission Accountability protocol's configuration.

Constraint checks are applied:

- the `inactivity threshold` cannot exceed the omission accountability scale factor.
- the `inactivity threshold` needs to be greater or equal to `pastPerformanceWeight`.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_inactivityThreshold` | `uint256` | the new value for  inactivity threshold |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setInflationControllerContract

Sets a new value for the [Inflation Controller Contract](/concepts/architecture/#inflation-controller-contract) address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Stabilization Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-inflation-controller-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


### setInitialJailingPeriod (Omission Accountability Contract)

Sets the `initialJailingPeriod` protocol parameter of the Omission Accountability protocol's configuration.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_initialJailingPeriod` | `uint256` | the new value for the initial jailing period |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setInitialProbationPeriod (Omission Accountability Contract)

Sets the `initialProbationPeriod` protocol parameter of the Omission Accountability protocol's configuration.
     
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_initialProbationPeriod` | `uint256` | the new value for the initial probation period |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setInitialSlashingRate (Omission Accountability Contract)

Sets the `initialSlashingRate` protocol parameter of the Omission Accountability protocol's configuration.

Constraint checks are applied:

- the initial slashing rate  cannot exceed the slashing rate scale factor.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_initialSlashingRate` | `uint256` | the new value for the initial slashing rate |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setInnocenceProofSubmissionWindow (Accountability Contract)

Sets the innocence proof submission window protocol parameter. 
       
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_window ` | `uint256` | the new value for the window (in blocks) |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setInnocenceProofSubmissionWindow()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setLiquidationRatio (ASM Stabilization Contract)

Sets a new value for the `liquidationRatio` protocol parameter in the ASM Stabilization Contract configuration. 
    
Constraint checks are applied:

- the ratio must be less than the minimum collateralization ratio parameter.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `ratio` | `uint256` | an integer value specifying the liquidation ratio for ASM CDP's |

#### Response

None.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setLiquidLogicContract

Sets a new value for the liquid newton logic contract address.

Constraint checks are applied:

- The provided address must not be the zero address.

   
::: {.callout-note title="Liquid Newton contract architecture" collapse="false"}
The Liquid Newton contract implements a Proxy Pattern to ensure upgradability. The logic and state are separated in two separate contracts.

For more information on the Proxy Pattern, see <https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies>.
:::
     
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_contract` | `address` |  the ethereum formatted address of the liquid logic contract|

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-liquid-logic-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


### setLookbackWindow (Omission Accountability Contract)

Sets the `lookbackWindow` protocol parameter of the Omission Accountability protocol's configuration. It will get updated at epoch end.

Constraint checks are applied:

- the lookback window cannot be `0`.
- the epoch period needs to be greater than `delta+lookbackWindow-1`.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_lookbackWindow` | `uint256` | the new value for the lookback window |

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setMaxScheduleDuration

Sets the max allowed duration of any schedule or vesting contract.
       
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_newMaxDuration` | `uint256` | a positive integer value specifying the duration in seconds |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by calling the [`getMaxScheduleDuration()`](/reference/api/aut/#getmaxscheduleduration) method.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-max-schedule-duration [OPTIONS] DURATION
```
:::


###  setMinCollateralizationRatio (ASM Stabilization Contract)

Sets a new value for the `minCollateralizationRatio` protocol parameter in the ASM Stabilization Contract configuration.
    
Constraint checks are applied:

- the ratio must be a positive value
- the ratio must be greater than the liquidation ratio
- minimum collateralization ratio parameter.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `ratio` | `uint256` | a positive integer value specifying the minimum collateralization ratio for ASM CDP's |

#### Response

None.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setMinDebtRequirement (ASM Stabilization Contract)

Sets a new value for the `minDebtRequirement` protocol parameter in the ASM Stabilization Contract configuration. 
            
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `amount` | `uint256` |  an integer value specifying the minimum debt requirement for ASM CDP's |

#### Response

None.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setMinimumBaseFee

Sets a new value for the `minBaseFee` protocol parameter. The value is denominated in [`ton`](/glossary/#ton). 

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_price` | `uint256` | a positive integer value for the minimum gas price, denominated in [`ton`](/glossary/#ton) |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by calling the [`getMinimumBaseFee()`](/reference/api/aut/#getminimumbasefee) method.

#### Event

On a successful call the function emits a `MinimumBaseFeeUpdated` event, logging: `gasPrice`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-minimum-base-fee [OPTIONS] base-fee
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-minimum-base-fee 50000000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x4d1abc6881f63d7856b3b2d6f0b9865a4a9c2b1378dd824e36e9ac194fd8da52
```
:::


###  setOmissionAccountabilityContract

Sets a new value for the [Autonity Omission Accountability Contract](/concepts/architecture/#autonity-omission-accountability-contract) address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Omission Accountability Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-omission-accountability-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setOperatorAccount

Sets a new governance account address as the protocol parameter for the [Autonity Protocol Contracts](/concepts/architecture/#application-layer-protocol-contracts):

- [Autonity Protocol Contract](/concepts/architecture/#autonity-protocol-contract)
- [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract)
- [ASM ACU Contract](/concepts/architecture/#asm-acu-contract)
- [ASM Supply Control Contract](/concepts/architecture/#asm-supply-control-contract)
- [ASM Stabilization Contract](/concepts/architecture/#asm-stabilization-contract)
- [upgradeManagerContract](/concepts/architecture/#protocol-contract-upgrade)
- [Omission Accountability Contract](/concepts/architecture/#autonity-omission-accountability-contract).

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_account` | `address` | the ethereum formatted  address of the operator governance account |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to the [`operatorAccount()`](/reference/api/aut/#operatoraccount) public variable.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-operator-account [OPTIONS] OPERATOR-ADDRESS
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-operator-account 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xee513f48b4ad4cd24cfc5bb0fe0c1402a5e03ae030b6c73824bae253f56efd51
```
:::


###  setOracleContract

Sets a new value for the [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract) address.

The Oracle Contract is called by the [Autonity Protocol Contracts](/concepts/architecture/#application-layer-protocol-contracts):

- [Autonity Protocol Contract](/concepts/architecture/#autonity-protocol-contract)
- [ASM ACU Contract](/concepts/architecture/#asm-acu-contract)
- [ASM Stabilization Contract](/concepts/architecture/#asm-stabilization-contract).

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address` | `address` | the ethereum formatted address of the Oracle Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-oracle-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setOracleRewardRate

Sets the oracle reward rate for the protocol policy configuration. See [`config()`](/reference/api/aut/#config) for policy properties.

Constraint checks are applied:

- The reward rate must not exceed 100%.
- The proposer reward rate plus the oracle reward rate must not exceed 100%.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_oracleRewardRate` | `uint256` | the new reward rate for oracles (scaled by `10^4`). |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-oracle-reward-rate [OPTIONS] ORACLE_REWARD_RATE
```
:::


###  setPastPerformanceWeight (Omission Accountability Contract)

Sets the `pastPerformanceWeight` protocol parameter of the Omission Accountability protocol's configuration.

Constraint checks are applied:

- the `past performance weight` cannot exceed the omission accountability scale factor.
- the `past performance weight` cannot be greater than the `inactivity threshold`.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_pastPerformanceWeight` | `uint256` | the new value for the past performance weight|

#### Response

No response object is returned on successful execution of the call.

#### Event

None.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setProposerRewardRate

Sets the block proposer reward rate for the protocol policy configuration. See [`config()`](/reference/api/aut/#config) for policy properties.

Constraint checks are applied:

- The reward rate must not exceed 100%.
- The proposer reward rate plus the oracle reward rate must not exceed 100%.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_proposerRewardRate` | `uint256` | the new reward rate for the block proposer (scaled by `10^4`). |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-proposer-reward-rate [OPTIONS] PROPOSER_REWARD_RATE
```
:::


###  setSlasher

Sets a new value for the Accountability Slasher Contract address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Slasher Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-slasher [OPTIONS] SLASHER-ADDRESS
```
:::


###  setStabilizationContract

Sets a new value for the [ASM Stabilization Contract](/concepts/architecture/#asm-stabilization-contract) address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Stabilization Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-stabilization-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setSupplyControlContract

Sets a new value for the [ASM Supply Control Contract](/concepts/architecture/#asm-supply-control-contract) address.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `supplyControl` | `address` |  the ethereum formatted address of the Supply Control Contract |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-supply-control-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


### setSymbols (Oracle Contract)

Sets a new value set for the [currency pair](/glossary/#currency-pair) symbols for which the Oracle Contract computes median price.

Note that the function overwrites the existing symbols; and does not update; the complete set of symbols for which oracles shall provide price reports must be provided.

Constraint checks are applied:

- the `_symbols` parameter cannot be empty; new symbols are provided
- the current `round` number is not equal to the current symbol update (a) round number, and (b) round number +1.

The symbol update is applied and oracle submissions for the new symbols are effective from the next round `round+1`.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `symbols` | `string` array | a comma-separated list of the new currency pair symbols for which price reports are generated |

#### Response

None.

#### Event

On a successful call the function emits a `NewSymbols` event, logging: a string array of the new currency pair `_symbol` and the following round number at which the new symbols become effective  `round+1`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Oracle Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

::: {.panel-tabset}
## aut

``` {.aut}
aut contract tx --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D setSymbols '["_symbol"]' | aut tx sign - | aut tx send -
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract tx --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D setSymbols '["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "NTN-ATN"]' | aut tx sign - | aut tx send -
```
:::


###  setTreasuryAccount

Sets a new account address as the value of the `treasuryAccount` protocol parameter. 

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_account` | `address payable` | the ethereum formatted  address of the Autonity Treasury Account for community funds |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to [`config()`](/reference/api/aut/#config) to get the Autonity network configuration.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-treasury-account [OPTIONS] treasury-address
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-treasury-account 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xffe8725f6988668700896f335ecb5db75bb48c9dfb7caef90acecef85d0a2520
```
:::


### setTreasuryFee

Sets a new value for the `treasuryFee` protocol parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_treasuryFee ` | `uint256` | a positive integer value specifying the percentage fee levied on staking rewards before redistribution |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to [`config()`](/reference/api/aut/#config) to get the Autonity network configuration.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-treasury-fee [OPTIONS] TREASURY-FEE
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-treasury-fee 100000000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x513f36338720545a8f2c1111e0c2f4b5eebe9582e39493c6cd587ababe1e2e08
```
:::


###  setUnbondingPeriod

Sets a new value for the `unbondingPeriod` protocol parameter. The unbonding period specifies the length of time that bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction. The period of time is defined as a number of blocks.

The `unbondingPeriod` period value must be greater than the `epochPeriod` protocol parameter. When the last block of an epoch is finalised, logic checks if the unbonding period for any pending unbonding requests for unbonding has expired and if so applies the staking transitions.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_period` | `uint256` | a positive integer value specifying the number of blocks defining the duration of an unbonding period |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to [`config()`](/reference/api/aut/#config) to get the Autonity network configuration or [`getUnbondingPeriod()`](/reference/api/aut/#getunbondingperiod).

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-unbonding-period [OPTIONS] UNBONDING_PERIOD
```
:::

#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-unbonding-period 1000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x1057bf2525ee910b393ea8d54d0ec9b362355e5dbeb14235ed5eba92750a4bdd
```
:::


###  setUpgradeManagerContract

Sets a new value for the [Upgrade Manager Contract](/concepts/architecture/#protocol-contract-upgrade) address.

::: {.callout-note title="Note" collapse="false"}
This is a development function only used for internal testing purposes. A value other than `0x3C368B86AF00565Df7a3897Cfa9195B9434A59f9` will break the upgrade function.
:::

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `UpgradeManager` | `_address` |  the ethereum formatted address of the Upgrade Manager Contract|

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-upgrade-manager-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  upgrade

Provides new contract creation code for an Autonity Protocol Contract.

The function calls an in-protocol EVM replace mechanism. The contract creation code is compiled and the new contract bytecode and abi appended to the contract storage buffer.

::: {.callout-note title="How upgrade works" collapse="true"}
The contract storage buffer length is checked during block finalization and if a contract upgrade is ready it is applied - see [`finalize()`](/reference/api/aut/op-prot/#finalize).

When an upgrade is initiated a `getNewContract()` method retrieves the compiled EVM bytecode and Contract ABI of the new Autonity Protocol Contract, and performs an upgrade.

:::

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_target ` | `address` | the target contract address to be updated |
| `_data` | `string` | the contract creation code |

#### Response

None.

#### Event

None.


###  setWithheldRewardsPool

Sets the address of the pool to which withheld Newton inflation rewards will be sent. See [`config()`](/reference/api/aut/#config) for policy properties.

Constraint checks are applied:

- The provided address must not be the zero address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_pool ` | `address payable` | the address of the withheld rewards pool |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-withheld-rewards-pool -h
Usage: aut governance set-withheld-rewards-pool [OPTIONS] POOL_ADDRESS
```
:::

###  setWithholdingThreshold

Sets the withholding threshold for the policy configuration. See [`config()`](/reference/api/aut/#config) for policy properties.

Constraint checks are applied:

- The threshold must not exceed 100%.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_withholdingThreshold` | `uint256` | the new withholding threshold (scaled by `10^4`). |

#### Response

None.

#### Event

None.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-withholding-threshold [OPTIONS] WITHHOLDING_THRESHOLD
```
:::


## Protocol only

Functions with protocol contract access constraints can only be invoked by the Autonity protocol itself:

- Autonity Protocol Contract: for state finalization and committee selection
- Autonity Stabilization Contract: for Auton mint and burn.

###  burn (Supply Control Contract)

The Auton burn function, called by the Stabilization Contract `stabilizer` account address to burn Auton while processing a CDP repayment. 

Burns the specified amount of Auton, taking it out of circulation.

Constraint checks are applied:

- the caller is the `stabilizer` account, the Stabilization Contract address.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `amount ` | `uint256` | a non-zero integer value for the value amount being burned, denominated in Auton |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `Burn` event, logging: `value`, the amount of Auton burned.


###  computeCommittee

Selects the consensus committee for the following epoch by selecting the validators with the highest amount of bonded stake.

The algorithm reads from the `validatorList`  state variable to select the set of registered validators that are in an `enabled` state and with bonded stake greater than `0`. 

If the number of selected validators exceeds the maximum committee size, then the selected validators are sorted by bonded stake amount in ascending order. The top `N` where `N` is the maximum committee size, are then selected to be members of the consensus committee for the next epoch.

The consensus committee variables maintained in persistent storage are deleted and recreated:

- `committee` is assigned the array of new `CommitteeMember`'s, each `CommitteeMember` struct recording the validator's account address (`_addr`) and bonded stake amount (`votingPower`)
- `committeeNodes` is assigned the array of enode URL's for the committee members
- `epochTotalBondedStake` is assigned the total amount of the stake bonded to the committee members.

Constraint checks:

- `validatorList.length > 0`. A committee cannot be selected without registered validators.
- `ValidatorState = 0` (i.e. active). Validators must be in an active state to be included in the selection algorithm (validators in a paused, jailed, or jailbound state are excluded).
- `bondedStake > 0`. Validators must have a non-zero amount of bonded stake to be included in the selection algorithm.

#### Parameters

None.

#### Response

No response object is returned on successful execution of the method invocation.

The new committee can be retrieved from state by calling the [`getCommittee()`](/reference/api/aut/#getcommittee) method.

The new committee enode URL's can be retrieved from state by calling the [`getCommitteeEnodes()`](/reference/api/aut/#getcommitteeenodes) method.

Returns the amount of stake token bonded to the new consensus committee members and securing the network during the epoch can be retrieved from state by a call to the [`epochTotalBondedStake()`](/reference/api/aut/#epochtotalbondedstake) method.

### distributeRewards (Accountability Contract)

The Accountability Contract reward distribution function, called at epoch finalisation as part of the state finalisation function [`finalize`](/reference/api/aut/op-prot/#finalize). 

The function:

- distributes rewards for reporting provable faults committed by an offending validator to the reporting validator.
- if multiple slashing events are committed by the same offending validator during the same epoch, then rewards are only distributed to the last reporter.
- if funds can't be transferred to the reporter's `treasury` account, then rewards go to the autonity protocol `treasury` account for community funds (see also [Protocol Parameters](/reference/protocol/#parameters) Reference).

After distribution, the reporting validator is removed from the `beneficiaries` array.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_validator` | `address` | the address of the validator node being slashed |

#### Response

None.

#### Event

None.


###  finalize

The block finalisation function, invoked each block after processing every transaction within it. The function:

- tests if the `bytecode` protocol parameter is `0` length to determine if an Autonity Protocol Contract upgrade is available. If the `bytecode` length is `>0`, the `contractUpgradeReady` protocol parameter is set to `true`

- tests if the block number is the last epoch block number (equal to `lastEpochBlock + epochPeriod` config) and if so sets the `epochEnded` boolean variable to `true` or `false` accordingly
- invokes the Accountability Contract [`finalize()`](/reference/api/aut/op-prot/#finalize-accountability-contract) function, triggering the Accountability Contract to compute and apply penalties for provable accountability and omission faults committed by validators, and distribute rewards for submitting provable fault accusations
- then, if `epochEnded` is `true`:

    - performs the staking rewards redistribution, redistributing the available reward amount per protocol and emitting a `Rewarded` event for each distribution
    - applies any staking transitions - pending bonding and unbonding requests tracked in `BondingRequest` and `UnbondingRequest` data structures in memory
    - applies any validator commission rate changes - pending rate change requests tracked in `CommissionRateChangeRequest` data structures in memory
    - selects the consensus committee for the following epoch, invoking the [`computeCommittee()`](/reference/api/aut/op-prot/#computecommittee) function
    - assigns the `lastEpochBlock` state variable the value of the current block number
    - increments the `epochID` by `1`
    - emits a `NewEpoch` event logging the `epochID` of the new epoch
- invokes the Oracle Contract [`finalize()`](/reference/api/aut/op-prot/#finalize-oracle-contract) function, triggering the Oracle Contract to check it is the end of a voting round and if so:
  - calculate the median price of [currency pairs](/glossary/#currency-pair)
  - re-set oracle voters and parameters ready for the next oracle voting round.
- then, if the oracle has computed data and started a new voting round (`newRound` is `true`), invokes the ACU Contract [`update()`](/reference/api/aut/op-prot/#update-acu-contract) function to recompute the ACU value using the new price data.

#### Parameters

None.

#### Response

| Field | Datatype | Description |
| --| --| --| 
| `contractUpgradeReady` | `bool` | Set to `true` if an Autonity Protocol Contract upgrade is available |
| `committee`| `CommitteeMember[]` array | the consensus committee that approved the block, each `CommitteeMember` struct recording the validator's account address (`_addr`) and bonded stake amount (`votingPower`)|

::: {.callout-note title="Note" collapse="false"}
If an upgrade is available for a protocol contract, this is executed by the protocol at epoch finalisation. After an upgrade has been completed the new Autonity Protocol Contract version can be retrieved from state by calling the [`getVersion()`](/reference/api/aut/#getversion) method.
:::

#### Event

On successful reward distribution the function emits:

- a `Rewarded` event for each staking reward distribution, logging: recipient address `addr`, `atnAmount` and `ntnAmount`.
- a `NewEpoch` event signalling the beginning of a new epoch, logging: `epoch`, the unique identifier for the new epoch.


###  finalize (Accountability Contract)

The Accountability Contract finalisation function, called at each block finalisation as part of the state finalisation function [`finalize()`](/reference/api/aut/op-prot/#finalize). The function checks if it is the last block of the epoch, then:

- On each block, tries to [promote `Accusations`](/reference/api/aut/op-prot/#promote-guilty-accusations) without proof of innocence into misconducts. `Accusations` without a valid innocence proof are considered guilty of the reported misconduct and a new fault proof is created if the fault severity is higher than that of any previous fault already committed by the validator in the current epoch.

::: {.callout-note title="Note" collapse="false"}
A validator can, of course, have more than one fault proven against it in an epoch. For example, a first fault is proven and then another fault for a higher severity is proven. Note that the protocol will only apply an accountability slashing to a validator for the fault with the highest severity committed in an epoch.
:::

- On epoch end, [performs slashing tasks](/reference/api/aut/op-prot/#perform-slashing-tasks).

#### promote guilty accusations

`Accusations` are placed into an `accusation` queue stored in memory. For each `Accusation` in the queue, the protocol checks if the proof submission window for the `Accusation` has expired and, if so, it attempts to promote the `Accusation` into a misbehaviour fault. If a fault with a higher severity than the `Accusation` already exists for the epoch, then the `Accusation` is dropped. Otherwise, a new `FaultProof` is created from the `Accusation` and the slashing history of the validator is updated to record this as the highest severity fault committed in the epoch.

The function takes each `Accusation` proof from the accusations queue and:

- Checks if the proof innocence window has closed. If the window is still open, the `Accusation`  remains in the queue. If the window has closed (the sum of the block number at which the `Accusation` was reported and the number of blocks in the proof innocence window is greater than the current block number (`_ev.reportingBlock + INNOCENCE_PROOF_SUBMISSION_WINDOW > block.number`)), then the `Accusation` is removed from the queue (i.e. deleted) to determine if the `Accusation's` should be promoted to a fault.
- Tries to promote the `Accusation` to a fault or discards. The slashing history of the validator is checked to see if the validator already has a proven offence (i.e. a `FaultProof`) for the epoch with a severity `>=` to the `Accusation`. If true, then the `Accusation` is skipped as a `FaultProof` with a higher severity has already been reported during the epoch. If false, then the validator's slashing history is updated to record the new fault as the highest severity for the epoch. A new `FaultProof` is created for the validator and added to the slashing queue.
- A `FaultProof` event is emitted logging the event.

The reported validator will be silenced and slashed for the fault at the end of the current epoch.

#### perform slashing tasks

For each fault the protocol performs slashing over faulty validators at the end of an epoch.

The function checks the total number of faults committed by **all**  validators in the epoch, counting the number of fault proofs in the slashing queue, to quantify validator collusion. It then applies slashing for each fault in the slashing queue:

- Computes the slashing. The slashing rate and amount are computed taking into account the number of fault offences committed in the epoch by the offending validator and all validators globally. The slashing amount is calculated by the formula `(slashing rate * validator bonded stake)/slashing rate scale factor`.
- Applies the slashing penalty. Slashing is applied to the offending validator's stake, subtracting the slashing amount from the validator's bonded stake according to the protocol's [Penalty Absorbing Stake (PAS)](/concepts/afd/#penalty-absorbing-stake-pas) model ([self-bonded](/glossary/#self-bonded) stake before [delegated](/glossary/#delegated) stake)
- Computes the jail period of the offending validator. If the validator stake slashing is 100% of bonded stake, permanent validator jailing is applied and the validator state is set to `jailbound`. Else, jailing is temporary and a jail period is calculated, using the formula `current block number + jail factor * proven offence fault count * epoch period` to compute a jail release block number. The validator state is set to `jailed`.
- Updates validator state. The validator's proven fault counter is incremented by `1` to record the slashing occurrence in the validator's reputational slashing history. The jail release block number is recorded, set to the computed value if `jailed` or set to `0` if `jailbound`. Bonded stake amounts are adjusted for the slashing amount and the slashed stake token are transferred to the Autonity Protocol global `treasury` account for community funding.
- Updates global slashing state. The pending slashing fault queue is reset ready for the next epoch, and the reporting validator is added to the array of reward beneficiaries that will receive rewards for offence reporting
- A `SlashingEvent` event is emitted for each validator that has been slashed.

Rewards for fault reporting are distributed to the `treasury` account of the reporting validator as the last block of the epoch is finalised. Reporting validator [self-bonded](/glossary/#self-bonded) and [delegated](/glossary/#delegated) stakeholders receive a share of the rewards _pro rata_ to their bonded stake amount. If the rewards transfer to the validator `treasury` account fails, then the rewards are sent to the Autonity Protocol's community `treasury` account.

::: {.callout-note title="Note" collapse="false"}
The protocol adjusts the slashing rate according to the total number of fault offences committed in an epoch across all validators.

This mechanism applies a dynamic slashing rate mitigating collusion risk by Byzantine agents in an epoch.
:::    

#### Parameters

| Field | Datatype | Description |
| --| --| --| 
| `epochEnd` | `Bool` | boolean value indicating if the current block is the last block of the epoch (`true`) or not (`false`) |

#### Response

None.

#### Event

The function emits events:

- on submission of a fault proof, a `NewFaultProof` event, logging: `_offender`, `_severity`, `_id`.
- after a successful slashing, a `SlashingEvent` logging: `_val.nodeAddress`, `_slashingAmount`, `_val.jailReleaseBlock`, `isJailbound`.


###  finalize (Oracle Contract)

The Oracle Contract finalisation function, called once per `VotePeriod` as part of the state finalisation function [`finalize()`](/reference/api/aut/op-prot/#finalize). The function checks if it is the last block of the vote period, if so then:

- executes the Oracle Contract's on-chain aggregation routine to calculate the median of all price data points for each symbol submitted to the oracle, invoking the Oracle Contract `aggregateSymbol` function
- checks if there have been any oracle voter changes, if so then updates the oracle voter set for the following oracle voting round
- resets the `lastRoundBlock` to the current `block.number`
- increments the `round` counter by `1`
- checks if there have been any oracle symbol changes, if so then updates the oracle symbol set for the following oracle voting round.

#### Parameters

None.

#### Response

Returns `true` if there is a new voting round and new symbol prices are available, `false` if not.

#### Event

On success the function emits a `NewRound` event for the new oracle voting period, logging: round number `round`, `block.number`, `block.timestamp` and vote period duration `votePeriod`.


### handleEvent (Accountability Contract)

The accountability event handling function, invoked by protocol on submission of accountability event data to handle event processing.

Constraint checks are applied:
 
 - the `msg.sender` caller is a registered [validator identifier](/concepts/validator/#validator-identifier), else the transaction reverts. (Rewards for reporting a successful slashing event are distributed to the validator's [`treasury` account](/concepts/validator/#treasury-account).)
 - the `msg.sender` calling the function and the slashing event reporter addresses are the same.
 - chunk segments are contiguous for oversize events that have been chunked for storage into a map. If an event's raw proof data is above a floor byte size, then the event is `chunked` into `16kb` size chunks and stored in a map. Chunk id's must be contiguous; i.e. a map can only contain chunks from one and not multiple events.

The function checks the event data:

- If the raw proof contains `>1` chunk, then the function stores the event into a map and then returns.

The function then processes the event according to event type.

The function validates the accountability event proof, passing the event's `rawProof` data to a precompiled contract for verification. The precompiled contract returns verification outcome to the method:

- `_success` - boolean flag indicating if proof verification succeeded or failed
- `_offender` - validator identifier address of the fault offender
- `_ruleId` - ID of the accountability rule tested
- `_block` - number of the block in which the fault occurred
- `_messageHash` - cryptographic hash of the main fault evidence, the `rawProof`.

Based on the verification outcome, constraint checks are applied:

- the raw proof verification passed: `_success` is `true`
- there are no mismatches between the event data and the verified raw proof data fields:
  - the returned `_offender` and event `offender` address values match
  - the returned `_ruleId` and event `rule` identifier values match
- the`_block` number returned by the verification is less than the current `block.number` - the proof is for a historical and not future event

- depending on event type, specific constraint checks are applied:

  - if `FaultProof`, then:
    - the severity of the fault event is greater than the severity of the offender's current slashing history for the epoch.

  - if `Accusation`, then:
    - the severity of the fault event is greater than the severity of the offender's current slashing history for the epoch
    - the validator does not have a pending accusation being processed.

  - if `InnocenceProof`, then:
    - the validator has an associated pending accusation being processed
    - the innocence proof and associated accusation proof have matching: rule identifiers, block number, message hash.

On successful constraint checking:

- The `event` data object is updated using data returned by processing of the raw proof during proof verification processing:

| Field | Datatype | Description |
| --| --| --|
| `block ` | `uint256` | assigned block number returned from verification in `_block`|
| `epoch` | `uint256` | assigned the identifier of the epoch in which the accountability event `_block` occurred |
| `reportingBlock` | `uint256` | assigned the current block number |
| `messageHash` | `uint256` | assigned the hash of the main evidence for the accountability event returned from verification in `_messageHash` |

- The event is added to the events queue and assigned an `_eventId` value reflecting its position in the event queue.

Then, depending on event type:

- If `FaultProof`, then:
  - The record of validator faults is updated to add the new event ID.
  - The event is added to the slashing queue.
  - The slashing history of the validator for the epoch is updated to record the fault's severity.

- If `Accusation`, then:
  - The event is recorded as the validator's pending accusation.
  - The event is added to the accusation queue.

- If `InnocenceProof`, then:
  - The accusation queue is checked and the associated accusation is removed.
  - The validator's pending accusation is reset to `0`, indicating the validator has no pending accusations (so a new accusation can now be submitted against the validator).


#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_event` | `Event` | event data object |

On proof submission an `_event` object data structure is constructed in memory, populated with fields ready for proof processing:

| Field | Datatype | Description |
| --| --| --|
| `chunks` | `uint8` | counter of the number of chunks in the accountability event (for oversize accountability event) |
| `chunkId` | `uint8` | chunk index to construct the oversize accountability event |
| `eventType` | `EventType` | the accountability event type, one of: `FaultProof` (proven misbehaviour), `Accusation` (pending accusation), `InnocenceProof` (proven innocence) |
| `rule` | `Rule` | the identifier of the accountability Rule defined in the Accountability Fault Detector (AFD) rule engine. Enumerated values are defined for each AFD Rule ID. |
| `reporter` | `address` | the node address of the validator that reported this accountability event |
| `offender` | `address` | the node address of the validator accused of the accountability event |
| `rawProof` | `bytes` | the `rlp` encoded bytes of the accountability proof object |
| `block ` | `uint256` | the number of the block at which the accountability event occurred. Assigned by protocol after proof verification. |
| `epoch` | `uint256` | the identifier of the epoch in which the accountability event occurred. Assigned by protocol after proof verification. |
| `reportingBlock` | `uint256` | the number of the block at which the accountability event was reported. Assigned by protocol after proof verification. |
| `messageHash` | `uint256` | hash of the main evidence for the accountability event. Assigned by protocol after proof verification. |
| `_validator` | `address` | the address of the validator node being slashed |


#### Response

None.

#### Event

On success the function emits events for handling of:

- Fault proof: a `NewFaultProof` event, logging: round `_offender` validator address, `_severity` of the fault, and `_eventId`.
- Accusation proof: a `NewAccusation` event, logging: round `_offender` validator address, `_severity` of the fault, and `_eventId`.
- Innocence proof: an `InnocenceProven` event, logging: `_offender` validator address, `0` indicating there are no pending accusations against the validator.


###  mint (Supply Control Contract)

The Auton mint function, called by the Stabilization Contract to mint Auton to recipients while processing a CDP borrowing. 

Mints Auton and sends it to a recipient account, increasing the amount of Auton in circulation. 

Constraint checks are applied:

- the caller is the `stabilizer` account, the Stabilization Contract address
- invalid recipient: the `recipient` cannot be the `stabilizer` account, the Stabilization Contract address, or the zero address
- invalid amount: the `amount` is not equal to `0` or greater than the Supply Control Contract's available Auton `balance`.
    
When `x` amount of Auton is minted, then `x` is simply added to the account’s balance, increasing the total supply of Auton in circulation and reducing the supply of Auton available for minting.       
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `recipient ` | `address` | the recipient account address |
| `amount ` | `uint256` | amount of Auton to mint (non-zero) |

#### Response

No response object is returned on successful execution of the method call.

The new Auton balance of the recipient account can be returned from state using `aut` to [Get the auton balance](/account-holders/submit-trans-aut/#get-auton-balance).

The new total supply of auton available for minting can be retrieved from state by calling the [`availableSupply()`](/reference/api/asm/supplycontrol/#availablesupply) method.

#### Event

On a successful call the function emits a `Mint` event, logging: `recipient`, `amount`.


###  update (ACU Contract)

The Autonomous Currency Unit (ACU) Contract finalization function, called once per Oracle voting round as part of the state finalization function [`finalize()`](/reference/api/aut/op-prot/#finalize). The function checks if the Oracle Contract [`finalize()`](/reference/api/aut/op-prot/#finalize-oracle-contract) has initiated a new oracle voting round, if so then:

- it retrieves the latest prices from the Oracle Contract (i.e. the latest round data)
- checks price data completeness:
  - if latest prices have been returned for all symbols in the ACU currency basket, then:
    - computes the ACU index value
    - resets the `round` to the index number of the oracle voting round that computed the retrieved latest prices.
    - returns status of `true` to the calling Autonity Protocol Contract
  - else if one or more prices are unavailable from the Oracle, it will not compute the ACU value for that round, and returns status of `false` to the calling Autonity Protocol Contract.

#### Parameters

None.

#### Response

None.

#### Event

On success the function emits an `Updated` event for the new ACU value, logging: `block.number`, `block.timestamp`, oracle voting round number `round`, and the ACU index value calculated `_value`.
