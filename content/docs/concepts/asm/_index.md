
---
title: "Auton Stability Mechanism (ASM)"
linkTitle: "Auton Stability Mechanism (ASM)"
weight: 10
description: >
  Auton Stability Mechanism: elements, the functions they perform, and the lifecycle for Auton and Newton supply.
---

## Overview

This section describes the Auton Stability Mechanism (ASM) protocol, the elements composing the mechanism, the functions it provides for computing and maintaining a stable price for Auton, and the lifecycle for Auton and Newton supply.

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

CDP-based stabilization mechanism.

...

#### ASM configuration

...

### Protocol primitives

- CDP - CDP-based stabilization mechanism and the core attributes thereof - principal, etc
- Protocol Assets - Auton, Newton, Liquid Newton - Auton supply, price stability, collateral token
- ACU - ACU value derived from weighted currency basket, to minimize FX exposure for borderless markets.
- Oracle. Oracle data from oracle contract - or subsume this into ACU?
- CDP liquidation - of under collateralized debt positions

...

#### xyz

...

#### xyz

...

### CDP lifecycle

CDP lifecycle events.
...

### CDP ownership

...


### CDP liquidation

...


## ASM economics

- for protocol - Auton supply control
- for borrower - collateralized borrowing using protocol asset as collateral token; borrow interest payment, risk of liquidation
- for liquidator - returns from liquidation, remaining collateral after settlement of debt and interest outstanding