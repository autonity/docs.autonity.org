
---
title: "Auton Stabilization Mechanism (ASM)"
linkTitle: "Auton Stabilization Mechanism (ASM)"
weight: 10
description: >
  Auton Stabilization Mechanism: elements, the functions they perform, and the lifecycle for Auton and Newton supply.
---

## Overview

This section describes the Auton Stabilization Mechanism (ASM) protocol, the elements composing the mechanism, the functions it provides for computing and maintaining a stable price for Auton, and the lifecycle for Auton and Newton supply.

...

## CDP identity, accounts

...

### CDP identifier

The CDP Owner account address is used as a unique identifier for the CDP.

...


## Stabilization protocol

### CDP roles

- Owners (Borrowers)
- Liquidators (Keepers)
- Stabilizer (ASM Protocol)

### Auton Stability Mechanism

Mechanism

3 main elements - ACU, Supply Control, Stabilization 

...


#### ACU

...

#### Supply control

...

#### Stabilization

/// @title ASM Stabilization Contract
/// @notice A CDP-based stabilization mechanism for the Auton.
/// @dev Intended to be deployed by the protocol at genesis. Note that all
/// rates, ratios, prices, and amounts are represented as fixed-point integers
/// with `SCALE` decimal places.

...

#### ASM configuration


Values are set in params config. `autonity/params/` and are the default used at network genesis for acu,supply control, stabilization contracts.
 
/// Stabilization Configuration.


- `borrowInterestRate`: the annual continuously-compounded interest rate for borrowing.

- `liquidationRatio`: the minimum ACU value of collateral required to maintain 1 ACU value of debt.

- `minCollateralizationRatio`: the minimum ACU value of collateral required to borrow 1 ACU value of debt.

- `minDebtRequirement`: the minimum amount of debt required to maintain a CDP.

- `targetPrice`: the ACU value of 1 unit of debt.
    
...

### Protocol primitives

- CDP - CDP-based stabilization mechanism and the core attributes thereof - principal, etc
- Protocol Assets - Auton, Newton, Liquid Newton - Auton supply, price stability, collateral token
- ACU - ACU value derived from weighted currency basket, to minimize FX exposure for borderless markets.
- Oracle. Oracle data from oracle contract - or subsume this into ACU?
- CDP liquidation - of under collateralized debt positions

...

#### CDP

Collateralized Debt Position (CDP) attributes:

- `timestamp`: the timestamp of the last borrow or repayment.
- `collateral`: the collateral deposited with the Stabilization Contract.
- `principal`: the principal debt outstanding as of `timestamp`.
- `interest`: the interest debt that is due at the `timestamp`.


   /// The decimal places in fixed-point integer representation.
    uint256 public constant SCALE = 18; // Match UD60x18
    /// The multiplier for scaling numbers to the required scale.
    uint256 public constant SCALE_FACTOR = 10 ** SCALE;
    /// A year is assumed to have 365 days for interest rate calculations.
    uint256 public constant SECONDS_IN_YEAR = 365 days;
    /// The Config object that stores Stabilization Contract parameters.
    Config public config;
    /// A mapping to retrieve the CDP for an account address.
    mapping(address => CDP) public cdps;

...

#### xyz

...

### CDP lifecycle

CDP lifecycle events.

    /// Collateral Token was deposited into a CDP
    /// @param account The CDP account address
    /// @param amount Collateral Token deposited
    event Deposit(address indexed account, uint256 amount);
    /// Collateral Token was withdrawn from a CDP
    /// @param account The CDP account address
    /// @param amount Collateral Token withdrawn
    event Withdraw(address indexed account, uint256 amount);
    /// Auton was borrowed from a CDP
    /// @param account The CDP account address
    /// @param amount Auton amount borrowed
    event Borrow(address indexed account, uint256 amount);
    /// Auton debt was paid into a CDP
    /// @param account The CDP account address
    /// @param amount Auton amount repaid
    event Repay(address indexed account, uint256 amount);
    /// A CDP was liquidated
    /// @param account The CDP account address
    /// @param liquidator The liquidator address
    event Liquidate(address indexed account, address liquidator);

...



### CDP ownership

...


### CDP liquidation

...


## ASM economics

- for protocol - Auton supply control
- for borrower - collateralized borrowing using protocol asset as collateral token; borrow interest payment, risk of liquidation
- for liquidator - returns from liquidation, remaining collateral after settlement of debt and interest outstanding