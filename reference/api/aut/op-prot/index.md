---
title: "Governance and Protocol Only Reference"

description: >
  Autonity Protocol Contract functions callable by governance operator and by protocol only 
---

## Operator only

Functions with the `onlyOperator` access constraint that can only be called by the governance operator account.

::: {.callout-tip title="Semantics for events emitted by operator updates to protocol configuration parameters" collapse="false"}

A standard set of events is used for events emitted by operator only transactions setting new values for protocol configuration parameters of data types `int`, `uint`, `address`, and `bool`.

The events are named `ConfigUpdateUint`, `ConfigUpdateInt`, `ConfigUpdateAddress`, `ConfigUpdateBool`. They have a standard set of event parameters.

For events  the parameters logged are:

| Parameter | Datatype | Description |
|:-- |:-- |:-- |:-- |
| `name` | `string` | name of the configuration parameter |
| `oldValue` | `uint256` | old value of the configuration parameter |
| `newValue` | `uint256` | new value of the configuration parameter |
| `appliesAtHeight` | `uint256` | block height at which the change will apply to the configuration parameter |

:::


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

Modifies the symbols, quantities, or scale of the ACU currency basket.

Constraint checks are applied:

- `InvalidBasket`: the number of new `symbols_` and `quantities_` correspond. I.e. for each symbol there is a quantity.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `symbols_` | `string` | the symbols used to retrieve prices |
| `quantities_` | `uint256` | the basket quantity corresponding to each symbol |
| `scale_` | `uint256` | the scale for quantities and the ACU value |

#### Response

None.

#### Event

On a successful call the function emits a `BasketModified` event, logging: `symbols_`, `quantities_`, `scale_`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ACU Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  removeCDPRestrictions (ASM Stabilization Contract)

Transitions out of the CDP restricted state. Transitioning has two effects:

- lifts restrictions on CDP opening and borrowing: any Autonity network user is able to open a CDP in the ASM.
- sets the CDP `BorrowInterestRate` to the default genesis configuration setting, i.e. to the value documented in Reference, Protocol Parameters, ASM [Stabilization Config](/reference/protocol/#stabilization-config).

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- `NotRestricted`: CDP Restrictions are enabled.
            
#### Parameters
   
None.

#### Response

None.

#### Event

On a successful call the function emits:

- a `ConfigUpdateUint` event, logging: configuration parameter `name` ("borrowInterestRate"), `oldValue`, `newValue`, `appliesAtHeight`.
- an `ConfigUpdateBool` event, logging: configuration parameter `name` ("restricted"), `oldValue`, `newValue`, `appliesAtHeight`
- a `CDPRestrictionsRemoved` event, no logging.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

### rescale (ACU Contract)

Rescale the quantity multiplier for the ACU basket.

Constraint checks are applied:

- `ZeroValue`: the new quantity multiplier value is not `0`.

::: {.callout-note title="Note" collapse="false"}

The `rescale()` function sets a new value for the ACU basket quantity multiplier.

The basket quantity multiplier for the ACU basket is scaled to the ACU's scaled representation. is used to set a new value for the basket `quantityMultiplier`.

If the ACU basket is modified, `modifyBasket()`, the modify basket logic rescales quantity multiplier to the correct precision for scaling numbers to the ACU's scaled representation. This check ensures that if `rescale()` has been called a subsequent call to `modifyBasket()` will ensure the ACU basket's quantity multiplier is kept scaled to the correct precision.

:::


#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `newQuantityMultiplier` | `uint256` | the new quantity multiplier |

#### Response

None.

#### Event

On a successful call the function emits a `Rescaled` event, logging: `newQuantityMultiplier`, `oldQuantityMultiplier`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ACU Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setAccountabilityContract

Sets a new value for the [Autonity Accountability Contract](/concepts/architecture/#autonity-accountability-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Accountability Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("accountabilityContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-accountability-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setAcuContract

Sets a new value for the [ASM Autonomous Currency Unit (ACU) Contract](/concepts/architecture/#asm-acu-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the ACU Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("acuContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-acu-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


### setAtnSupplyOperator (ASM Stabilization Contract)

Sets a new value for the `atnSupplyOperator` protocol parameter value, a governance address permissioned to open CDPs in the ASM [Stabilization Contract](/concepts/architecture/#protocol-contracts). The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `atnSupplyOperator` | `address` | the ethereum formatted address of the `_atnSupplyOperator` |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setAuctioneerContract

Sets a new value for the [ASM Auctioneer Contract](/concepts/architecture/#asm-auctioneer-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Auctioneer Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-auctioneer-contract [OPTIONS] CONTRACT-ADDRESS
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
| `_rates` | `uint256` | comma separated list of the new `low`, `mid` and `high` values for the base slashing rates |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `BaseSlashingRateUpdate` event, logging: old `config.baseSlashingRates`, new `_rates`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setBaseSlashingRates()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setClusteringThreshold

Sets the clustering threshold for consensus messaging. The clustering threshold will take effect when committee size reaches the threshold.

Constraint checks are applied:

- the new clustering `threshold` must be greater than `0`.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_threshold` | `uint256` | the committee size at which clustering becomes active (positive integer) |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("clusteringThreshold"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-clustering-threshold [OPTIONS] THRESHOLD
```
:::


###  setCommitRevealConfig (Oracle Contract)

Sets the commit-reveal penalty mechanism configuration for `nonRevealThreshold` and `revealResetInterval`.

::: {.callout-note title="Note" collapse="false"}
For more detail on commit-reveal in oracle voting see the Concepts:

- Oracle network, Oracle protocol, [Commit and reveal](/concepts/oracle-network/#commit-and-reveal) scheme.
- Oracle Accountability Fault Detection (OAFD), [Protocol configuration](/concepts/oafd/#protocol-configuration) commit-reveal penalty mechanism.
:::

Constraint checks are applied:

- `invalid config`: the `threshold` cannot be less than the `reset interval` and the `reset interval` must be greater than `0`.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_threshold` | `uint256` | Threshold for missed reveals | 
| `_resetInterval` | `uint256` | Number of rounds after which the missed reveal counter is reset |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits `ConfigUpdateUint` events, logging:

- configuration parameter `name` ("revealResetInterval"), `oldValue`, `newValue`, `appliesAtHeight`.
- configuration parameter `name` ("nonRevealThreshold"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setCommitRevealConfig()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setCommitteeSize

Sets the maximum size of the consensus committee. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- the new committee size must be greater than 0.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_size` | `uint256` | a positive integer value for the maximum committee size |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by calling the [`getMaxCommitteeSize()`](/reference/api/aut/#getmaxcommitteesize) method.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("committeeSize"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-committee-size [OPTIONS] COMMITTEE_SIZE
```
:::


###  setDefaultACUUSDPrice (ASM Stabilization Contract)

Set the default ACU-USD price for use when fixed prices are enabled. (See [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract).)

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `defaultACUUSDPrice` | `uint256` | the new default ACU-USD price |

#### Response

None.

#### Event

On a successful call the function emits:

- an `IConfigEvents.ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setDefaultNTNATNPrice (ASM Stabilization Contract)

Set the default NTN-ATN price for use when fixed prices are enabled. (See [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract).)

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `defaultNTNATNPrice` | `uint256` | the new default NTN-ATN price |

#### Response

None.

#### Event

On a successful call the function emits:

- an `IConfigEvents.ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setDefaultNTNUSDPrice (ASM Stabilization Contract)

Set the default NTN-USD price for use when fixed prices are enabled. (See [`useFixedGenesisPrices()`](/reference/api/aut/op-prot/#usefixedgenesisprices-asm-stabilization-contract).)

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `defaultNTNUSDPrice` | `uint256` | the new default NTN-USD price |

#### Response

None.

#### Event

On a successful call the function emits:

- an `IConfigEvents.ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setDelta (Accountability Contract)

Sets the `delta` protocol parameter of the Accountability protocol's configuration. The configuration change will take effect at epoch end (the end of epoch block height is logged in the function's `appliesAtHeight` event parameter).

Constraint checks are applied:

- the `delta` must be less than the `newRange` configuration value.

::: {.callout-note title="Note" collapse="false"}
Accountability Contract configuration updates are applied at the same time. Therefore the new values for `delta`, `range`, and `gracePeriod` are checked for logical consistency.
:::

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_delta` | `uint256` | the new value for delta |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("delta"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setDelta (Omission Accountability Contract)

Sets the `delta` protocol parameter of the Omission Accountability protocol's configuration. The configuration change will take effect at epoch end (the end of epoch block height is logged in the function's `appliesAtHeight` event parameter).

Constraint checks are applied:

- the `delta` needs to be at least `2` (it cannot be 1 due to optimistic block building).
- the epoch period needs to be greater than `delta+lookbackWindow-1`.
    
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_delta` | `uint256` | the new value for delta |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("newOmissionDelta"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setEip1559Params

Sets the EIP-1559 parameters for the next epoch: `minBaseFee`, `gasLimitBoundDivisor`, `elasticityMultiplier` and `baseFeeChangeDenominator`.

::: {.callout-note title="Note" collapse="false"}
For detail on Autonity's implementation of EIP-1559 see the Concept [System model](/concepts/system-model/), [EIP 1559 Transaction fee mechanism (TFM)](/concepts/system-model/#eip-1559-transaction-fee-mechanism-tfm).
:::

Constraint checks are applied:

- the new `gas limit bound divisor` must be a positive integer greater than `0`.
- the new `base fee change denominator` must be a positive integer greater than `0`.
- the new `elasticity multiplier` must be a positive integer greater than `0`.
       
#### Parameters

A `_params` object with fields:
   
| Field | Datatype | Description |
| --| --| --| 
| `minBaseFee ` | `uint256` | the new minimum base fee |
| `gasLimitBoundDivisor ` | `uint256` | the new block gas limit bound divisor |
| `elasticityMultiplier ` | `uint256` | the new elasticity multiplier |
| `baseFeeChangeDenominator ` | `uint256` | the new base fee change  denominator |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits am `Eip1559ParamsUpdate` event, logging the new `minBaseFee`, `gasLimitBoundDivisor`, `elasticityMultiplier` and `baseFeeChangeDenominator`.
   
#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-eip1559-params [OPTIONS] MIN_BASE_FEE
                                         BASE_FEE_CHANGE_DENOMINATOR
                                         ELASTICITY_MULTIPLIER
                                         GAS_LIMIT_BOUND_DIVISOR
```
:::


###  setEpochPeriod

Sets a new value for the `epochPeriod` protocol parameter. The change will be applied at epoch end.

The `epochPeriod` period value must be less than the `unbondingPeriod` protocol parameter.


Constraint checks are applied:

- The new epoch period value cannot be `0`.
- If the new value is decreasing the current epoch period, checks the current chain head has not already exceeded the new epoch period window.
- The new epoch period value must be greater than the [OFD](/concepts/ofd/) `[Delta](/concepts/ofd/#delta-delta)+[lookbackWindow](/concepts/ofd/#lookback-window)-1`.
-   The new epoch period is less than or equal to `votePeriod * 2` (a check to ensure there is sufficient time for any oracle voter changes before epoch end).
        
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


###  setFactors (Accountability Contract)

Sets the `collusion`, `history`, and `jail` punishment factor protocol parameters.

The new collusion and history factor values must not exceed the [slashing rate scale factor](/concepts/afd/#slashing-protocol-configuration) of the Accountability Fault Detection protocol's configuration. The jail factor is specified as a number of epochs.

Constraint checks are applied:

- the `collusion factor` cannot exceed the slashing rate scale factor.
- the `history factor` cannot exceed the slashing rate scale factor.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_rates` | `uint256` | comma separated list of the new `CollusionFactor`, `HistoryFactor` and `JailFactor` values for the base slashing rates |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits an `AccountabilityFactorsUpdate` event, logging: old `config.factors`, new `_factors`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setFactors()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setGasLimit

Sets the block gas limit.

Constraint checks are applied:

- the new `gas limit` must be a positive integer greater than `0`.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_gasLimit` | `uint256` | the new gas limit; a positive integer value |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("gasLimit"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-gas-limit [OPTIONS] GAS_LIMIT
```
:::


###  setInactivityThreshold (Omission Accountability Contract)

Sets the `inactivityThreshold` protocol parameter of the Omission Accountability protocol's configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

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

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("inactivityThreshold"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setInflationControllerContract

Sets a new value for the [Inflation Controller Contract](/concepts/architecture/#inflation-controller-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Stabilization Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("inflationControllerContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-inflation-controller-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


### setInitialJailingPeriod (Omission Accountability Contract)

Sets the `initialJailingPeriod` protocol parameter of the Omission Accountability protocol's configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_initialJailingPeriod` | `uint256` | the new value for the initial jailing period |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("initialJailingPeriod"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setInitialProbationPeriod (Omission Accountability Contract)

Sets the `initialProbationPeriod` protocol parameter of the Omission Accountability protocol's configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.
     
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_initialProbationPeriod` | `uint256` | the new value for the initial probation period |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("initialProbationPeriod"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setInitialSlashingRate (Omission Accountability Contract)

Sets the `initialSlashingRate` protocol parameter of the Omission Accountability protocol's configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- the initial slashing rate  cannot exceed the slashing rate scale factor.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_initialSlashingRate` | `uint256` | the new value for the initial slashing rate |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("initialSlashingRate"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setInnocenceProofSubmissionWindow (Accountability Contract)

Sets the innocence proof submission window protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.
       
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_window ` | `uint256` | the new value for the window (in blocks) |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setInnocenceProofSubmissionWindow()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setInterestAuctionDiscount (ASM Auctioneer Contract)

Sets a new value for the `interestAuctionDiscount` protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

The `interestAuctionDiscount` value is set as a value between $[0,1)$ with $10 \hat{\ } 18$ precision.

Constraint checks are applied:

- `InvalidParameter`: the new interest auction `discount` value cannot be `>= 10^18`.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `discount ` | `uint256` | an integer value specifying the discount rate for the starting price of an interest auction |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

### setInterestAuctionDuration (ASM Auctioneer Contract)

Sets a new value for the `interestAuctionDuration` protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

The `interestAuctionDuration` value is set as a number of blocks.

Constraint checks are applied:

- `InvalidParameter`: the new interest auction `duration` value cannot be `0`.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `duration ` | `uint256` | a positive integer value specifying the duration in blocks  |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setInterestAuctionThreshold (ASM Auctioneer Contract)

Sets a new value for the `interestAuctionThreshold` protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

The `interestAuctionThreshold` value is set as a value in Auton `>0`.

Constraint checks are applied:

- `InvalidParameter`: the new interest auction `threshold` value cannot be `0`.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `threshold ` | `uint256` | a positive integer value specifying the total amount of ATN accumulated from interest payments required to trigger an interest auction |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setLiquidationAuctionDuration (ASM Auctioneer Contract)

Sets a new value for the `liquidationAuctionDuration` protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

The `liquidationAuctionDuration` value is set as a number of blocks.

Constraint checks are applied:

- `InvalidParameter`: the new liquidation auction `duration` value cannot be `0`.
   
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `duration ` | `uint256` | a positive integer value specifying the duration in blocks |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setLiquidationRatio (ASM Stabilization Contract)

Sets a new value for the `liquidationRatio` protocol parameter in the ASM Stabilization Contract configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.
    
Constraint checks are applied:

- the ratio must be less than the minimum collateralization ratio parameter.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `ratio` | `uint256` | an integer value specifying the liquidation ratio for ASM CDP's |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setLiquidLogicContract

Sets a new value for the liquid newton logic contract address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

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

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("liquidLogicContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-liquid-logic-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


### setLookbackWindow (Omission Accountability Contract)

Sets the `lookbackWindow` protocol parameter of the Omission Accountability protocol's configuration. The configuration change will take effect at epoch end (the end of epoch block height is logged in the function's `appliesAtHeight` event parameter).

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

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("newLookbackWindow"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setMaxScheduleDuration

Sets the max allowed duration of the protocol schedules. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.
       
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_newMaxDuration` | `uint256` | a positive integer value specifying the duration in seconds |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by calling the [`getMaxScheduleDuration()`](/reference/api/aut/#getmaxscheduleduration) method.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("maxScheduleDuration"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-max-schedule-duration [OPTIONS] DURATION
```
:::


###  setMinCollateralizationRatio (ASM Stabilization Contract)

Sets a new value for the `minCollateralizationRatio` protocol parameter in the ASM Stabilization Contract configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.
    
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

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setMinDebtRequirement (ASM Stabilization Contract)

Sets a new value for the `minDebtRequirement` protocol parameter in the ASM Stabilization Contract configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.
            
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `amount` | `uint256` |  an integer value specifying the minimum debt requirement for ASM CDP's |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

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

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("minBaseFee"), `oldValue`, `newValue`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-minimum-base-fee [OPTIONS] base-fee
```
:::


###  setOmissionAccountabilityContract

Sets a new value for the [Autonity Omission Accountability Contract](/concepts/architecture/#autonity-omission-accountability-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Omission Accountability Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("omissionAccountabilityContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-omission-accountability-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setOperatorAccount

Sets a new governance account address as the protocol parameter for the [Autonity Protocol Contracts](/concepts/architecture/#protocol-contracts). The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_account` | `address` | the ethereum formatted  address of the operator governance account |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to the [`operatorAccount()`](/reference/api/aut/#operatoraccount) public variable.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("operatorAccount"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-operator-account [OPTIONS] OPERATOR-ADDRESS
```
:::


###  setOracleContract

Sets a new value for the [Autonity Oracle Contract](/concepts/architecture/#autonity-oracle-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

The Oracle Contract is called by the [Autonity Protocol Contracts](/concepts/architecture/#protocol-contracts):

- [Autonity Protocol Contract](/concepts/architecture/#autonity-protocol-contract)
- [ASM ACU Contract](/concepts/architecture/#asm-acu-contract)
- [ASM Stabilization Contract](/concepts/architecture/#asm-stabilization-contract).
- [ASM Auctioneer Contract](/concepts/architecture/#asm-auctioneer-contract).

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address` | `address` | the ethereum formatted address of the Oracle Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("oracleContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-oracle-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setOracleRewardRate

Sets the oracle reward rate for the protocol policy configuration.  The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- The reward rate must not exceed 100%.
- The proposer reward rate plus the oracle reward rate must not exceed 100%.

See [`config()`](/reference/api/aut/#config) for policy properties.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_oracleRewardRate` | `uint256` | the new reward rate for oracles (scaled by `10^4`). |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("oracleRewardRate"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-oracle-reward-rate [OPTIONS] ORACLE_REWARD_RATE
```
:::


###  setPastPerformanceWeight (Omission Accountability Contract)

Sets the `pastPerformanceWeight` protocol parameter of the Omission Accountability protocol's configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

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

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("pastPerformanceWeight"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Omission Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


### setProceedAddress (ASM Auctioneer Contract)

Sets a new value for the `proceedAddress` protocol parameter value, the address to which auction proceeds are sent by the ASM [Auctioneer Contract](/concepts/architecture/#protocol-contracts). The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `proceedAddress_` | `address` | the ethereum formatted address to send proceeds to |

#### Response

No response object is returned on successful execution of the method call.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name`, `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Auctioneer Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setProposerRewardRate

Sets the block proposer reward rate for the protocol policy configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- The reward rate must not exceed 100%.
- The proposer reward rate plus the oracle reward rate must not exceed 100%.

See [`config()`](/reference/api/aut/#config) for policy properties.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_proposerRewardRate` | `uint256` | the new reward rate for the block proposer (scaled by `10^4`). |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("proposerRewardRate"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-proposer-reward-rate [OPTIONS] PROPOSER_REWARD_RATE
```
:::


### setRange (Accountability Contract)

Sets the `range` protocol parameter of the Accountability protocol's configuration. The configuration change will take effect at epoch end (the end of epoch block height is logged in the function's `appliesAtHeight` event parameter).

Constraint checks are applied:

- the `gracePeriod == 0`, the height range change is already in progress
- the new `range` modulo `4 == 0`, the height range must be a multiple of 4
- the new `range` is greater than `newDelta`, the height range needs to be greater than `delta`

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_range` | `uint256` | the new value for the height range (in blocks) |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("range"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Accountability Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setSlasher

Sets a new value for the Accountability Slasher Contract address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Slasher Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("slasher"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-slasher [OPTIONS] SLASHER-ADDRESS
```
:::



###  setSlashingConfig (Oracle Contract)

Sets the internal slashing and outlier detection penalty mechanism configuration for `outlierSlashingThreshold`, `outlierDetectionThreshold`, `baseSlashingRate`, and `slashingRateCap`.

::: {.callout-note title="Note" collapse="false"}
For more detail on slashing in oracle voting see the Concept:

- Oracle Accountability Fault Detection (OAFD), [Protocol configuration](/concepts/oafd/#protocol-configuration) slashing penalty mechanism.
:::
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_outlierSlashingThreshold` | `int256` | Threshold for flagging outliers |
| `_outlierDetectionThreshold` | `int256` | Threshold for outlier slashing penalties, controlling the sensitivity of the penalty mode |
| `_baseSlashingRate` | `uint256` | The base slashing rate for outlier slashing penalties |
| `_slashingRateCap` | `uint256` | The maximum % slashing rate for oracle accountability slashing penalties |

#### Response

No response object is returned on successful execution of the call.

#### Event

On a successful call the function emits events:

- a `ConfigUpdateInt` event, logging: configuration parameter `name` ("outlierSlashingThreshold"), `oldValue`, `newValue`, `appliesAtHeight`
- a `ConfigUpdateInt` event, logging: configuration parameter `name` ("outlierDetectionThreshold"), `oldValue`, `newValue`, `appliesAtHeight`
- a `ConfigUpdateUint` event, logging: configuration parameter `name` ("baseSlashingRate"), `oldValue`, `newValue`, `appliesAtHeight`
- a `ConfigUpdateUint` event, logging: configuration parameter `name` ("slashingRateCap"), `oldValue`, `newValue`, `appliesAtHeight`

#### Usage

::: {.callout-note title="Note" collapse="false"}
The `setCommitRevealConfig()` function is not currently supported by the `aut governance` command group.

You can interact with the Accountability Contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setStabilizationContract

Sets a new value for the [ASM Stabilization Contract](/concepts/architecture/#asm-stabilization-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_address ` | `address` | the ethereum formatted address of the Stabilization Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("stabilizationContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-stabilization-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setSupplyControlContract

Sets a new value for the [ASM Supply Control Contract](/concepts/architecture/#asm-supply-control-contract) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `supplyControl` | `address` |  the ethereum formatted address of the Supply Control Contract |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("supplyControlContract"), `oldValue`, `newValue`, `appliesAtHeight`.

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
- the current `round` number is not equal to the current symbol update (a) round number, and (b) round number + 1.

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

<!--
#### Example

::: {.panel-tabset}
## aut

``` {.aut}
aut contract tx --address 0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D setSymbols '["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "NTN-ATN"]' | aut tx sign - | aut tx send -
```
:::
-->

###  setTreasuryAccount

Sets a new account address as the value of the `treasuryAccount` protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_account` | `address payable` | the ethereum formatted  address of the Autonity Treasury Account for community funds |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to [`config()`](/reference/api/aut/#config) to get the Autonity network configuration.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("treasuryAccount"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-treasury-account [OPTIONS] treasury-address
```
:::


### setTreasuryFee

Sets a new value for the `treasuryFee` protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_treasuryFee ` | `uint256` | a positive integer value specifying the percentage fee levied on staking rewards before redistribution |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to [`config()`](/reference/api/aut/#config) to get the Autonity network configuration.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("treasuryFee"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-treasury-fee [OPTIONS] TREASURY-FEE
```
:::


### setVotePeriod (Oracle Contract)

Sets a new value set for the oracle voting round duration.

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

-  The new `votePeriod * 2` is less than or equal to the current or a new pending epoch period value (a check to ensure there is sufficient time for any oracle voter changes before epoch end).

The vote period update is applied and is applied at the end of the voting rouond.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `_votePeriod` | `uint` | the new vote period as a number of blocks |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("votePeriod"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The Oracle Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::


###  setUnbondingPeriod

Sets a new value for the `unbondingPeriod` protocol parameter. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

The unbonding period specifies the length of time that bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction. The period of time is defined as a number of blocks.

The `unbondingPeriod` period value must be greater than the `epochPeriod` protocol parameter. When the last block of an epoch is finalised, logic checks if the unbonding period for any pending unbonding requests for unbonding has expired and if so applies the staking transitions.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_period` | `uint256` | a positive integer value specifying the number of blocks defining the duration of an unbonding period |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to [`config()`](/reference/api/aut/#config) to get the Autonity network configuration or [`getUnbondingPeriod()`](/reference/api/aut/#getunbondingperiod).

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("unbondingPeriod"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-unbonding-period [OPTIONS] UNBONDING_PERIOD
```
:::


###  setUpgradeManagerContract

Sets a new value for the [Upgrade Manager Contract](/concepts/architecture/#protocol-contract-upgrade) address. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

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

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("upgradeManagerContract"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-upgrade-manager-contract [OPTIONS] CONTRACT-ADDRESS
```
:::


###  setWithheldRewardsPool

Sets the address of the pool to which withheld Newton inflation rewards will be sent. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- The provided address must not be the zero address.

See [`config()`](/reference/api/aut/#config) for policy properties.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_pool ` | `address payable` | the address of the withheld rewards pool |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateAddress` event, logging: configuration parameter `name` ("setWithheldRewardsPool"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-withheld-rewards-pool -h
Usage: aut governance set-withheld-rewards-pool [OPTIONS] POOL_ADDRESS
```
:::

###  setWithholdingThreshold

Sets the withholding threshold for the policy configuration. The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- The threshold must not exceed 100%.

See [`config()`](/reference/api/aut/#config) for policy properties.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_withholdingThreshold` | `uint256` | the new withholding threshold (scaled by `10^4`). |

#### Response

None.

#### Event

On a successful call the function emits a `ConfigUpdateUint` event, logging: configuration parameter `name` ("setWithholdingThreshold"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.panel-tabset}
## aut

``` {.aut}
aut governance set-withholding-threshold [OPTIONS] WITHHOLDING_THRESHOLD
```
:::

### updateBorrowInterestRate (ASM Stabilization Contract)

Updates the borrow interest rate. The new rate `newInterestRate` will take affect after the `config.announcementWindow` (in seconds). (See Reference, Protocol Parameters, ASM [Stabilization Config](/reference/protocol/#stabilization-config).)

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- `NotRestricted`: CDP Restrictions are enabled.
            
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `newInterestRate ` | `uint256` | the new interest rate multiplied by $10 \hat{\ } 18$. If it is 5% then it should be `(5/100)*(10^18) = 50_000_000_000_000_000` |

#### Response

None.

#### Event

On a successful call the function emits:

- an `InterestRateUpdateAnnounced` event, logging `newInterestRate`, `_borrowInterestRate.nextActiveFrom`, `overridden`.
- a `ConfigUpdateUint` event, logging: configuration parameter `name` ("borrowInterestRate"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

### updateAnnouncementWindow (ASM Stabilization Contract)

Updates the announcement window. The new `window` will take affect after the `config.announcementWindow` (in seconds). (See Reference, Protocol Parameters, ASM [Stabilization Config](/reference/protocol/#stabilization-config).)

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- the new `window` value is not equal to `0`
- `AnnouncementWindowPending`: there is not a pending announcement `window` update.
            
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `window` | `uint256` | the new announcement window measured in seconds |

#### Response

None.

#### Event

On a successful call the function emits:

- an `AnnouncementWindowUpdateAnnounced` event, logging `window`, `_announcementWindow.nextActiveFrom`, `overridden`.
- a `ConfigUpdateUint` event, logging: configuration parameter `name` ("announcementWindow"), `oldValue`, `newValue`, `appliesAtHeight`.
    
#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

### updateRatios (ASM Stabilization Contract)

Updates the minimum collateralization ratio and liquidation ratio for a CDP. The new ratios will take affect after the `config.announcementWindow` (in seconds). (See Reference, Protocol Parameters, ASM [Stabilization Config](/reference/protocol/#stabilization-config).)

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Constraint checks are applied:

- `lrOverridden`: there is not a pending new `liquidationRatio` update
- `mcrOverridden`: there is not a pending new `minCollateralizationRatio` update
- `InvalidParameter`: the ratios are valid. The `newLiquidationRatio`must be `<` the `newMinCollateralizationRatio` and `>= 1`

#### Parameters
   
| Field | Datatype | Description |
| --| --| --|
| `newLiquidationRatio` | `uint256` | the new liquidation ratio |
| `newMinCollateralizationRatio` | `uint256` | the new minimum collateralization ratio |    

#### Response

None.

#### Event

On a successful call the function emits:

- a `LiquidationRatioUpdateAnnounced` event, logging `newLiquidationRatio`, `_liquidationRatio.nextActiveFrom, `lrOverridden`.
- a `MinCollateralizationRatioUpdateAnnounced` event, logging `newMinCollateralizationRatio`, `_minCollateralizationRatio.nextActiveFrom`, `mcrOverridden`.
- a `ConfigUpdateUint` event, logging: configuration parameter `name` ("liquidationRatio"), `oldValue`, `newValue`, `appliesAtHeight`.
- a `ConfigUpdateUint` event, logging: configuration parameter `name` ("minCollateralizationRatio"), `oldValue`, `newValue`, `appliesAtHeight`.
    
#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
:::

### upgrade

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

On a successful call the function emits:

- an `upgradeResult` event, logging: `_target` the upgrade target contract address, `success` boolean indicating successful or failed upgrade.


###  useFixedGenesisPrices (ASM Stabilization Contract)

Toggles the use of the fixed genesis price state. Fixed genesis prices may be set for: NTN-ATN, NTN-USD, ACU-USD. For the default values set in the genesis configuration for the Stabilization Contract see Reference, Protocol Parameters, ASM [Stabilization Config](/reference/protocol/#stabilization-config) and `DefaultNTNATNPrice`, `DefaultNTNUSDPrice`, `DefaultACUUSDPrice`.

The configuration change will take effect at the block height logged in the function's `appliesAtHeight` event parameter.

Note that governance can update the default values and set new fixed prices. See [`setDefaultNTNATNPrice()`](/reference/api/aut/op-prot/#setdefaultntnatnprice-asm-stabilization-contract),[`setDefaultNTNUSDPrice()`](/reference/api/aut/op-prot/#setdefaultntnusdprice-asm-stabilization-contract), [`setDefaultACUUSDPrice()`](/reference/api/aut/op-prot/#setdefaultacuusdprice-asm-stabilization-contract).
            
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `useFixed ` | `bool` | whether to use fixed genesis prices (`true`) or not (`false`) |

#### Response

None.

#### Event

On a successful call the function emits:

- an `ConfigUpdateBool` event, logging: configuration parameter `name` ("fixedGenesisPrices"), `oldValue`, `newValue`, `appliesAtHeight`.

#### Usage

::: {.callout-note title="Note" collapse="false"}
The ASM Stabilization Contract Interface is not currently supported by `aut`.

You can interact with the contract using the `aut contract` command group. See `aut contract tx -h` for how to submit a transaction calling the interface function.
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

On successful reward distribution the function emits:

- for [AFD](/concepts/afd/) [slashing rewards](/concepts/afd/#slashing-rewards) distribution, a `ReporterRewarded` event for each slashing reward distribution, logging: reporting validator identifier `_reporter.nodeAddress`, `_offender` validator identifier node address, slashed `_ntnReward` amount, slashed `_atnReward` amount.
- for [OFD](/concepts/ofd/) [slashing rewards](/concepts/ofd/#slashing-rewards) distribution, a `TotalProposerRewards` event for the block proposer reward distribution, logging: `_ntnReward` amount, `_atnReward` amount.


###  finalize

The block finalisation function, invoked each block after processing every transaction within it. The function:

- tests if the `bytecode` protocol parameter is `0` length to determine if an Autonity Protocol Contract upgrade is available. If the `bytecode` length is `>0`, the `contractUpgradeReady` protocol parameter is set to `true`

- tests if the block number is the last epoch block number (equal to `lastEpochBlock + epochPeriod` config) and if so sets the `epochEnded` boolean variable to `true` or `false` accordingly
- invokes finalize on the auxiliary protocol contracts, triggering the compute and apply of penalties for provable accountability and omission faults committed by validators, and distribute rewards for submitting provable fault accusations:
  - Accountability Contract [`finalize()`](/reference/api/aut/op-prot/#finalize-accountability-contract) 
  - Omission Accountability Contract [`finalize()`](/reference/api/aut/op-prot/#finalize-omission-accountability-contract)
  - Oracle Contract [`finalize()`](/reference/api/aut/op-prot/#finalize-oracle-contract)

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
- a `NewEpoch` event signalling the beginning of a new epoch, logging: `epochID`, `inflationReserve`, `stakeCirculating`.


###  finalize (Accountability Contract)

The Accountability Contract finalisation function, called at each block finalisation as part of the state finalisation function [`finalize()`](/reference/api/aut/op-prot/#finalize). The function checks if it is the last block of the epoch, then:

- On each block, tries to [promote `Accusations`](/reference/api/aut/op-prot/#promote-guilty-accusations) without proof of innocence into misconducts. `Accusations` without a valid innocence proof are considered guilty of the reported misconduct and a new fault proof is created if the fault severity is higher than that of any previous fault already committed by the validator in the current epoch.

::: {.callout-note title="Note" collapse="false"}
A validator can, of course, have more than one fault proven against it in an epoch. For example, a first fault is proven and then another fault for a higher severity is proven. Note that the protocol will only apply an accountability slashing to a validator for the fault with the highest severity committed in an epoch.
:::

- On epoch end, [performs slashing tasks](/reference/api/aut/op-prot/#perform-slashing-tasks) and [updates configuration](/reference/api/aut/op-prot/#update-configuration).

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

#### update configuration

Checks to see if there are new values for `gracePeriod`, `delta`, `range` and updates the accountability configuration if so.

Changes to delta and range are applied at block finalization to avoid inconsistencies when processing multiple accusations in a block.

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

- checks for voters failing to commit-reveal, updates oracle voter non reveal count for any no reveal penalties, applies any no reveal slashing penalties, and resets the no reveal counter to `0`
- executes the Oracle Contract's on-chain aggregation routine to calculate the median of all price data points for each symbol submitted to the oracle, invoking the Oracle Contract `aggregateSymbol` function
- checks oracle voting performance during the round and updates the oracles' voting performance score for the reward (epoch) period
- checks if there have been any oracle voter changes, if so then updates the oracle voter set for the following oracle voting round
- resets the `lastRoundBlock` to the current `block.number`
- increments the `round` counter by `1`
- checks if there is a pending new vote period config change, if so then updates the oracle `votePeriod` for the following oracle voting round.

#### Parameters

None.

#### Response

Returns `true` if there is a new voting round and new symbol prices are available, `false` if not.

#### Event

On success the function emits:

- a `NewRound` event for the new oracle voting period, logging: round number `round`, `block.timestamp`, and vote period duration `votePeriod`
- a `NoRevealPenalty` event for each non reveal penalty, logging validator oracle address `_voter`, `round`, `nonRevealCount`
- a `CommitRevealMissed` event for each missed commit reveal, logging validator oracle address `_address`, `round`, `nonRevealCount`
- a `Penalized` event for each price outlier penalty, logging validator oracle address `voter`, `_slashingAmount`, `_symbol`, `_priceMedian`, `price`
- a `TotalOracleRewards` event for the total oracle ATN and NTN rewards distributed in the reward period (i.e. for the voting round), logging `_totalNTN`, `_totalATN`
- a `PriceUpdated` event for the oracle median price aggregation, logging `_price`, `round`, `_symbol`, boolean (`true`|`false`) if the symbol was updated or not, `block.timestamp`


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
