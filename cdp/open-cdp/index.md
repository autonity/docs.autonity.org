---
title: "Open and manage a CDP"
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
- amount of interest to pay on the borrowing

### Step 1. Get collateral price

Query for current collateral price calling the [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice) function of the Stabilization Contract using the `aut contract call` command:

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f collateralPrice
```

The current collateral price is returned denominated in `ton`, Autonity’s equivalent of `wei`. For example:

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

- `<PRINCIPAL>` - the amount of ATN to borrow, specified in `ton`, Autonity's equivalent of `wei`
- `<PRICE>` - set to the collateral price returned in [Step 1](/cdp/open-cdp/#step-1-get-collateral-price).
- `<MCR>` - the minimum collateralization ratio set for the ASM at genesis. Set to `2000000000000000000` (i.e. 2). (For the default value set for `mcr` see [Reference, Genesis, ASM stabilization config `minCollateralizationRatio`](/reference/genesis/#configasmstabilization-object)).


```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f minimumCollateral <PRINCIPAL> <PRICE> <MCR>
```

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

- `<COLLATERAL>` - the amount of collateral token deposited to back the debt
- `<PRICE>` - the collateral token price. Set as for the  preceding [example](/cdp/open-cdp/#minimum-collateral).
- `<TARGETPRICE>` - the [ACU](/concepts/asm/#acu) value of 1 unit of debt set for the ASM at genesis. Set to `1000000000000000000` (i.e. 1). (For the default value set for `targetPrice` see [Reference, Genesis, ASM stabilization config `minCollateralizationRatio`](/reference/genesis/#configasmstabilization-object)).
- `<MCR>` - the minimum collateralization ratio. Set as for the preceding [example](/cdp/open-cdp/#minimum-collateral).


```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrowLimit <COLLATERAL> <PRICE> <TARGETPRICE> <MCR>
```

In this example the `0.35...` NTN value returned by the other method is set as the collateral token amount.

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f borrowLimit 350321307696993528 9990828200000000000 1000000000000000000 2000000000000000000
```

Returning:

```
1749999999999999997
```

At the given collateral price, `1.749999999999999997` ATN can be borrowed for deposited collateral token of `0.350321307696993528` NTN.


### Step 3. Calculate borrowing interest

Determine the interest that will charged on the borrowed Auton over time.

Query for the borrowing costs by calling the [`interestDue()`](http://localhost:1313/reference/api/asm/stabilization/#interestdue) function of the Stabilization Contract using the `aut contract call` command. Pass in parameters for:
  
  - `<DEBT>`: the amount of Auton you want to borrow
  - `<RATE>`: the borrow interest rate. For the default value set for `rate` see Reference, Genesis, [ASM stabilization config](/reference/genesis/#configasmstabilization-object). Set to 5%, `50000000000000000`
  - `<TIMEBORROW>`: the time point at which you will take out the borrowing. The timestamp is provided as a [Unix time](/glossary/#unix-time) value
  - `<TIMEDUE>`: the time point at which you will repay the borrowing, to specify the time point at which the interest is due. The timestamp is provided as a [Unix time](/glossary/#unix-time) value.

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f interestDue <DEBT> <RATE> <TIMEBORROW> <TIMEDUE>
```

In this example interest for borrowing 1.75 ATN over the calendar month of October is requested.

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f interestDue 1750000000000000000 50000000000000000 1696114800 1698710400
```

Returning:

```bash
7216608464428718
```

Borrowing interest costs over the 31 day period are `7216608464428718` [`ton`](/glossary/#ton), or `0.007216608464428718` ATN.

### Step 4. Determine collateral requirements

Finally, for ongoing management of your CDP you need to maintain a sufficient collateral buffer to manage the risk of the CDP entering a liquidatable state. Factors that could lead to a CDP becoming liquidatable include collateral withdrawals, increased principal borrowing, accrued interest increasing the debt, or collateral-to-Auton price fluctuation.

::: {.callout-note title="Note" collapse="false"}
If a debt position is under collateralized or not is determined by calculating `(collateral * price) / debt`. If this returns a value `< liquidationRatio`, then the CDP is under collateralised and can be liquidated.
:::

To mitigate this risk you can run different collateralization, debt, and price scenarios to simulate liquidation risk and determine how much collateral you post for your borrowing.

To support this simulation you can use the [`underCollateralized()`](/reference/api/asm/stabilization/#undercollateralized) function of the Stabilization Contract.  Use the `aut contract call` command to do this, passing in parameters:

- `<COLLATERAL>`: the amount of collateral backing the debt
- `<PRICE>`: the price of the collateral in Auton. The actual price can be retrieved by calling [`collateralPrice()`](/reference/api/asm/stabilization/#collateralprice). For how to do this see [Step 1. Get collateral price](/cdp/open-cdp/#step-1-get-collateral-price).
- `<DEBT>`: the debt amount
- `<LIQUIDATIONRATIO>`: the liquidation ratio  set for the ASM at genesis. Set to `1800000000000000000` (i.e. 1.8). (For the default value set for `liquidationRatio` see [Reference, Genesis, ASM stabilization config `liquidationRatio`](/reference/genesis/#configasmstabilization-object)).

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized <COLLATERAL> <PRICE> <DEBT> <LIQUIDATIONRATIO>
```

In this example, values for borrowing 1.75 ATN per other Steps in this example are used for the parameterisation: 

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized 350321307696993528 9990828200000000000 1750000000000000000 1800000000000000000
```

Returning:

```bash
false
```

If the borrowing amount is increased from 1.75 to 1.95 ATN, then the position becomes under collateralized:

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized 350321307696993528 9990828200000000000 1950000000000000000 1800000000000000000
```

Returning:

```bash
true
```

However, if collateral is increased from `350321307696993528` to `352000000000000000`, then the position is no longer under collateralized:


```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f underCollateralized 352000000000000000 9990828200000000000 1950000000000000000 1800000000000000000
```
Returning:

```bash
false
```

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

### Get current CDP debt amount

The debt of a CDP consists of the Auton borrowed (the 'principal') and accrued interest due charged at the borrow interest rate.

To determine the current debt owed on a CDP call [`debtAmount()`](/reference/api/asm/stabilization/#debtamount)function of the Stabilization Contract using the `aut contract call` command.

1. Call `debtAmount()` passing in parameters for:

  - `<ACCOUNT>`: the CDP account address
  - `<TIMESTAMP>`: the timestamp at which you want to  value the debt. The timestamp is provided as a [Unix time](/glossary/#unix-time) value.

  ```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount <ACCOUNT> <TIMESTAMP>
```
  
  The call will return the total amount owed on the CDP, `debt + accrued interest`. The result is returned as an integer value in [`ton`](/glossary/#ton), Autonity's equivalent of Ethereum's `wei`.

In this example the debt amount is returned as `1.75...` ATN at time point October 17 2023 14:16:37 GMT:

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount 0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa 1697552197
1750217362321414404
```

### Repay borrowing

Repay an amount of borrowed Auton by submitting a transaction to the [`repay()`](/reference/api/asm/stabilization/#repay) function of the Stabilization Contract using the `aut contract tx` command.  Pass in parameters for:

- `<AMOUNT>` - the amount of Auton to repay to the CDP.

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value <AMOUNT> repay | aut tx sign - | aut tx send -
```

In this example 0.25 ATN is repaid to reduce the principal:

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value 250000000000000000 repay | aut tx sign - | aut tx send -

```

{{% alert title="Note" %}}
A repayment can be a partial or full repayment of the borrowed amount.

If you want to repay all borrowed ATN in a CDP and clear the debt position completely, then slightly overpay - this covers accrued interest and the protocol will return any surplus payment to your account immediately.

For example, you are repaying the entire debt and call [`interestDue()`](http://localhost:1313/reference/api/asm/stabilization/#interestdue) and [`debtAmount()`](/reference/api/asm/stabilization/#debtamount) to determine the amount owed. You then make a repayment for that exact amount. In the time interval before the [`repay()`](/reference/api/asm/stabilization/#repay) transaction is submitted a `dust` amount of interest can then accrue. In this scenario, overpayment will settle that interest due and surplus ATN from the repayment is returned.
{{% /alert %}}

### Withdraw collateral

Withdraw an amount of deposited collateral token by submitting a transaction to the [`withdraw()`](/reference/api/asm/stabilization/#withdraw) function of the Stabilization Contract using the `aut contract tx` command.  Pass in parameters for:

- `<AMOUNT>` - the amount of Auton to repay to the CDP.

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw <AMOUNT> | aut tx sign - | aut tx send -
```

In this example 0.1 NTN collateral token is withdrawn to reduce the deposited collateral amount:

```bash
aut contract tx --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f withdraw 100000000000000000 | aut tx sign - | aut tx send -

```

