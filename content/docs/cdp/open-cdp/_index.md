---
title: "Open and manage a CDP"
linkTitle: "Open and manage a CDP"
weight: 10
description: >
  How to use a CDP to borrow Auton in the Auton Stabilization Mechanism.
---

## Prerequisites

To open a CDP and borrow ATN you need:

- An [account](/account-holders//create-acct/) that has been [funded](/account-holders/fund-acct/) with:
  - Auton: to pay for transaction gas costs
  - Newton: to deposit as collateral token in the CDP.
  
  Note that this account address will be also be used as the [CDP identifier](/concepts/asm/#cdp-identifiers) account address as well as the [CDP Owner](/concepts/asm/#roles) address used to open and service the CDP.

- A running instance of [`aut` <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/aut) configured to [submit a transaction from your account](/account-holders/submit-trans-aut/).

{{% pageinfo %}}
The guide uses the `aut contract call` and `aut contract tx` commands for contract interactions.

`aut contract` usage requires that you specify the [ABI](/glossary/#application-binary-interface-abi) file and the protocol contract address of the contract being called. To complete the guide you will need to call 2 protocol contracts:

- the Autonity Protocol Contract (`Autonity.abi`)  with the protocol contract address `0xBd770416a3345F91E4B34576cb804a576fa48EB1`
- the Stabilization Contract (`Stabilization.abi`) with the protocol contract address `0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f`.

The [Autonity Protocol Contract Interfaces](/reference/api/aut/) is called to approve the Stabilization Contract as a spender of the CDP Owner's NTN token. The primary interface for CDP interactions is the [Stabilization Contract Interface](/reference/api/asm/stabilization/).

The `abi` files are generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Autonity.abi` and `./params/generated/Stabilization.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built the utility when building from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).

The guide explicitly sets the path to the ABI file and contract address to be clear which contract is being called. Note that the ABI file and contract address can be set as defaults in `aut`'s configuration file `.autrc` using the `contract_address` and `contract_abi` flags as appropriate:

```
#contract_abi = Autonity.abi
#contract_address = 0xBd770416a3345F91E4B34576cb804a576fa48EB1
```

or

```
contract_abi = Stabilization.abi
contract_address = 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f

```

The guide assumes the ABI files are in the directory from which the `aut` command is run.
{{% /pageinfo %}}

## Determine borrowing limit

As prerequisite to opening a CDP, verify your borrowing limit.  This is done based on:

- collateral price
- amount of collateral to be deposited

### Step 1. Get collateral price

Query for current collateral price calling the [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice) function of the Stabilization Contract using the `aut contract call` command:

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f collateralPrice
```

The current collateral price is returned. For example:

```bash
9990828200000000000
```

### Step 2. Get borrowing ceiling

Next, determine your borrowing limits. There are two ways to do this:

- [By Auton borrowing amount](/#minimum-collateral), to calculate the amount of collateral token that must be deposited to borrow a stated amount of Auton (ATN). Call `minimumCollateral()`.
- [By collateral token amount](/#borrow-limit), to calculate the amount of Auton that can be borrowed for a stated amount of collateral token (NTN). Call `borrowLimit()`.


#### By amount of Auton to be borrowed {#minimum-collateral}

Determine how much collateral token (NTN) you will need to deposit for the amount of auton (ATN) you want to borrow.

Query for the minimum collateral amount by calling the [`minimumCollateral()`](/reference/api/asm/stabilization/#minimumcollateral) function of the Stabilization Contract using the `aut contract call` command.  Pass in parameters for:

- `principal` - the amount of ATN to borrow, specified in `ton`, Autonity's equivalent of `wei`
- `price` - set to the collateral price returned in Step 1.
- `mcr` - the minimum collateralization ratio set for the ASM at genesis. Set to `2000000000000000000` (i.e. 2). (For the default value set for `mcr` see [Reference, Genesis, ASM stabilization config `minCollateralizationRatio`](/reference/genesis/#configasmstabilization-object)).

In this example 1.75 ATN is set as the principal
```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f minimumCollateral 1750000000000000000 9990828200000000000 2000000000000000000
```

Returning:

```
350321307696993528
```

At the given collateral price, `0.350321307696993528` NTN must be deposited to borrow `1.75` ATN.


#### By amount of Newton collateral token deposited {#borrow-limit}

Determine the maximum amount of Auton (ATN) that can be borrowed for a given amount of collateral token (NTN).

Query for the borrowing limit by calling the [`borrowLimit()`](/reference/api/asm/stabilization/#borrowlimit) function of the Stabilization Contract using the `aut contract call` command.  Pass in parameters for:

- `collateral` - the amount of collateral token deposited to back the debt
- `price` - the collateral token price. Set as for Step 2 above
- `targetPrice`	- the [ACU](/concepts/asm/#acu) value of 1 unit of debt set for the ASM at genesis. Set to `1000000000000000000` (i.e. 1). (For the default value set for `targetPrice` see [Reference, Genesis, ASM stabilization config `minCollateralizationRatio`](/reference/genesis/#configasmstabilization-object)).
- `mcr` - the minimum collateralization ratio. Set as for Step 2 above.

In this example the `0.35...` NTN value returned by the other method is set as the collateral token amount.

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrowLimit 350321307696993528 9990828200000000000 1000000000000000000 2000000000000000000
```

Returning:

```
1749999999999999997
```

At the given collateral price, `1.749999999999999997` ATN can be borrowed for deposited collateral token of `0.350321307696993528` NTN.

## Approve the Stabilization Contract as a collateral token spender

Before depositing collateral token to open a cdp, the collateral token contract must be called to approve the Stabilization Contract as a `spender` of collateral token using the standard ERC-20 "approve" method.

<!-- Note on Step 2 approve() and allowance().

`aut contract tx` is being used instead of `aut token approve` because:

- consistent use of one command group throughout the tutorial
- `aut token allowance` returns the allowance granted by the owner to the caller...not to the spender. You can't call as the Stabilization Contract... `aut contract tx` allows you to specify the spender and owner.
-->

### Step 1. Verify your collateral token balance

(Optional.) Verify you have the necessary NTN balance for the desired borrowing:

```
aut account balance --ntn
```

The amount approved in Step 2 must be `<=` to your NTN balance, otherwise the transaction will revert.

### Step 2. Approve the Stabilization Contract

Approve the Stabilization Contract as a `spender` of collateral token. Call the Autonity Protocol Contract [`approve()`](/reference/api/aut/#approve) function, using the `aut contract tx` command.  Pass in parameters for:

- `<SPENDER>` is the Stabilization Contract address
- `<AMOUNT>` is the amount of NTN that you are allowing the contract to spend on your behalf.

```bash
aut contract tx --abi Autonity.abi --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 approve  <SPENDER> <AMOUNT>
```

In this example, approval is given for `0.75` NTN:

```bash
aut contract tx --abi Autonity.abi --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 approve  0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f 750000000000000000 | aut tx sign - | aut tx send -
```

Optionally, verify the Stabilization Contract approval has succeeded by calling the Autonity Protocol Contract [`allowance()`](/reference/api/aut/#allowance) function, using the `aut contract call` command.  Pass in parameters for:

- `<OWNER>` is your account address
- `<SPENDER>` is the Stabilization Contract address.

```bash
aut contract call --abi Autonity.abi --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 allowance <OWNER> <SPENDER>
```

For example:

```bash
aut contract call --abi Autonity.abi --address 0xBd770416a3345F91E4B34576cb804a576fa48EB1 allowance 0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f
750000000000000000
```

## Open a CDP

It is only possible to have one CDP open at a time. This prevents users opening multiple CDP's to borrow Auton without maintaining collateralization ratios.

Open a CDP by depositing collateral token. Auton can then be borrowed against that collateral, creating the debt position. The debt of a CDP is then composed of:

- `principal`: the amount of ATN borrowed, which must be above a minimum debt requirement
- `accrued interest`: the borrowing interest rate charged to the debt, continuously compounding.

(For the default values set for `borrowInterestRate` and `minDebtRequirement`  see [Reference, Genesis, ASM stabilization config](/reference/genesis/#configasmstabilization-object)).

## Deposit collateral token

Deposit collateral token (NTN) by submitting a transaction to the [`deposit()`](/reference/api/asm/stabilization/#deposit) function of the Stabilization Contract using the `aut contract tx` command.  Pass in parameters for:

- `<AMOUNT>` - the amount of collateral token to deposit.

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f deposit <AMOUNT> | aut tx sign - | aut tx send -
```

In this example 0.75 NTN is deposited:

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f deposit 750000000000000000 | aut tx sign - | aut tx send -

```

Optionally, verify the deposit has succeeded and the CDP opened by calling the Stabilization Contract [`accounts()`](/reference/api/asm/stabilization/#accounts) function to return an array of open CDP's. The account address you used to submit the transaction will be included in the array of [CDP identifier](/concepts/asm/#cdp-identifiers) addresses returned.

For example:

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f accounts
["0x1f790c60D974F5A8f88558CA90F743a71F009641", "0xfd1ac0e99E9BD153F49080A96eb44843211E5C9f", "0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa"]
```

## Borrow against collateral

Borrow Auton against deposited CDP collateral by submitting a transaction to the [`borrow()`](/reference/api/asm/stabilization/#borrow) function of the Stabilization Contract using the `aut contract tx` command.  Pass in parameters for:

- `<AMOUNT>` - the amount of Auton to borrow.

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrow <AMOUNT> | aut tx sign - | aut tx send -
```

The borrowed Auton will be transferred to your account.  To view your new ATN account balance run `aut account balance`.

In this example 1.75 ATN is borrowed as the principal:

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrow 1750000000000000000 | aut tx sign - | aut tx send -

```

## Manage your CDP

### repay

Repay an amount of borrowed Auton by submitting a transaction to the [`repay()`](/reference/api/asm/stabilization/#repay) function of the Stabilization Contract using the `aut contract tx` command.  Pass in parameters for:

- `<AMOUNT>` - the amount of Auton to repay to the CDP.

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value <AMOUNT> repay | aut tx sign - | aut tx send -
```

In this example 0.25 ATN is repaid to reduce the principal:

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value 250000000000000000 repay | aut tx sign - | aut tx send -

```

### withdraw

Withdraw an amount of deposited collateral token by submitting a transaction to the [`withdraw()`](/reference/api/asm/stabilization/#withdraw) function of the Stabilization Contract using the `aut contract tx` command.  Pass in parameters for:

- `<AMOUNT>` - the amount of Auton to repay to the CDP.

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw <AMOUNT> | aut tx sign - | aut tx send -
```

In this example 0.1 NTN collateral token is withdrawn to reduce the deposited collateral amount:

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw 100000000000000000 | aut tx sign - | aut tx send -

```

