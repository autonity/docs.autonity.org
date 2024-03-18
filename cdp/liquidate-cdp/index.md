---
title: "Liquidate a CDP"
description: >
  How to identify and liquidate a CDP in the Auton Stabilization Mechanism.
---

## Prerequisites

- An [account](/account-holders/create-acct/) that has been [funded](/account-holders/fund-acct/) with Auton (to pay for transaction gas costs)

- A running instance of [`aut`](https://github.com/autonity/aut) configured to [submit a transaction from your account](/account-holders/submit-trans-aut/).

::: {.callout-note title="Protocol contract calls" collapse="false"}
The guide uses the `aut contract call` and `aut contract tx` commands for contract interactions.

`aut contract` usage requires that you specify the [ABI](/glossary/#application-binary-interface-abi) file and the protocol contract address of the contract being called. To complete the guide you will need to call the Stabilization Contract (`Stabilization.abi`) with the protocol contract address `0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f`.

The `abi` files are generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/Autonity.abi` and `./params/generated/Stabilization.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built the utility when building from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).

The guide explicitly sets the path to the ABI file and contract address to be clear the Stabilization Contract is being called. Note that the ABI file and contract address can be set as defaults in `aut`'s configuration file `.autrc` using the `contract_address` and `contract_abi` flags:


```
contract_abi = Stabilization.abi
contract_address = 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f

```

The guide assumes the ABI files are in the directory from which the `aut` command is run.
:::

## Discover if a CDP is liquidatable

- get the CDP's `accounts()`
- call `isLiquidatable()`
- call `underCollateralized()`
- can you call other functions to forecast if it will be liquidatable or under collateralised based on interest due/accruing, or?
  - e.g. if the collateralPrice falls etc
  - i.e. liquidationRatio
  - i.e. collateralizationRatio


### Step 1. Get CDP accounts

Query for open CDPs by calling the [`accounts()`](/reference/api/asm/stabilization/#accounts) function of the Stabilization Contract using the `aut contract call` command:

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f accounts
```

An array of open CDPs is returned. For example:

```bash
["0x1f790c60D974F5A8f88558CA90F743a71F009641", "0xfd1ac0e99E9BD153F49080A96eb44843211E5C9f", "0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa"]
```

### Step 2. Determine if a CDP is liquidatable

Determine if a CDP is liquidatable by calling the [`isLiquidatable()`](/reference/api/asm/stabilization/#isliquidatable) function of the Stabilization Contract using the `aut contract call` command. Pass in parameter:

  - `<ACCOUNT>`: the CDP account address

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f isLiquidatable <ACCOUNT>
```

The call will return a boolean value indicating if the CDP is liquidatable or not.

For example, using the results returned from Step 1:

```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f isLiquidatable 0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa
```

`false` is returned for `0x1f790c60D974F5A8f88558CA90F743a71F009641` - the CDP is not liquidatable.

### Step 3. Get CDP economic state

Next, inspect CDP state to understand the economic costs and returns of liquidation - i.e. cost of repaying the debt (principal, accrued interest) and the collateral token that will be transferred to the position's liquidator.

There are two steps to do this:

- [Get CDP debt amount](/#get-debt-amount), to calculate the current outstanding debt amount of Auton that must be repaid to liquidate the CDP.
- [Get CDP collateral amount](/#get-collateral), to return the amount of collateral token deposited to the CDP.


#### Get CDP collateral amount {#get-collateral}

As described in the Concept page for ASM [Stabilization](/concepts/asm/#stabilization) section, for each CDP, the Stabilization Contract records:

- `timestamp`: the timestamp of the last borrow or repayment
- `collateral`: the collateral deposited with the Stabilization Contract
- `principal`: the principal debt outstanding as of `timestamp`.
- `interest`: the interest debt that is due at the `timestamp`.

::: {.callout-important title="Warning" collapse="false"}
The important data point is the `collateral` amount value as this gives you the economic benefit of liquidating the CDP. 

The other data should be ignored. The `timestamp` reflects the time point that the CDP was last borrowed from or repaid to so the `principal` and `interest` data is out of date. To get the _current CDP debt amount_ due you will need to call [`debtAmount()`](/reference/api/asm/stabilization/#debtamount), which is done in the next step [Get CDP debt amount](/cdp/liquidate-cdp/#get-debt-amount).
:::

CDP state is maintained in memory as a public mapping `cdps` and may be inspected by calling the getter function automatically generated for it when the Stabilization Contract is compiled.

::: {.callout-note title="Note" collapse="false"}
The `cdps` getter function definition can be found in the `Stabilization.abi` file by searching for `"name": "cdps"`.
:::


::: {.callout-note title="Note" collapse="false"}
The `cdps` function cannot currently be called from `aut` using the `aut contract call` command. This is a known issue logged as an `autonity.py` GitHub issue [AssertionError on returning tuple
#37](https://github.com/autonity/autonity.py/issues/37). 
:::

The auto-generated `cdps` method can be called to return the CDP data, simply passing in the CDP account address as the parameter.

This can be done using a simple `web3.py` script using the `web3.eth.contract` module to call the `cdps` function. Where:

  - `<RPC_ENDPOINT>`: is the HTTP address for the node endpoint being called
  - `<ACCOUNT>`: is the [CDP account address](/concepts/asm/#cdp-identifiers) identifier.


```python

from web3 import Web3, HTTPProvider
import json

with open("Stabilization.abi") as f:
	abi = info_json = json.load(f)


w3 = Web3(HTTPProvider('<RPC_ENDPOINT>'))

stabilizationContractAddress = "0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f"
contract_instance = w3.eth.contract(address=stabilizationContractAddress, abi=abi)

# read state: call the cdps function passing in the CDP identifier address <ACCOUNT>:

print(contract_instance.functions.cdps("<ACCOUNT>").call())

```


For example, for the CDP account `0x1f790c60D974F5A8f88558CA90F743a71F009641` it returns:


```bash
% python3 aut_cdps.py
[1695737259, 410000024269118276, 300010815663118114, 0]
```

#### Get CDP debt amount {#get-debt-amount}

The debt of a CDP consists of the Auton borrowed (the 'principal') and accrued interest due charged at the borrow interest rate.

To get the current debt owed on a CDP and so the cost of liquidating the CDP, call [`debtAmount()`](/reference/api/asm/stabilization/#debtamount)function of the Stabilization Contract using the `aut contract call` command. Pass in parameters for:

  - `<ACCOUNT>`: the CDP account address
  - `<TIMESTAMP>`: the timestamp at which you want to value the debt. The timestamp is provided as a [Unix time](/glossary/#unix-time) value.

  ```bash
aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount <ACCOUNT> <TIMESTAMP>
```
  
  The call will return the total amount owed on the CDP, `debt + accrued interest`. The result is returned as an integer value in [`ton`](/glossary/#ton), Autonity's equivalent of Ethereum's `wei`.

In this example the debt amount for CDP `0x1f790c60D974F5A8f88558CA90F743a71F009641` is returned as `0.3008...` ATN at time point October 17 2023 14:16:37 GMT:

```bash
ubuntu@vps-c7c3e8c7:~/TEST/autcli$ aut contract call --abi Stabilization.abi --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f debtAmount 0x1f790c60D974F5A8f88558CA90F743a71F009641 1697552197
```

Returning:

```bash
300875359676920667
```

## Liquidate a CDP

To liquidate a CDP in a liquidatable state submit a `liquidate` transaction to the [`liquidate()`](/reference/api/asm/stabilization/#liquidate) function of the Stabilization Contract using the `aut contract call` command. Pass in parameter:

  - `<ACCOUNT>`: the CDP account address to liquidate
  - `<AMOUNT>`: the payment amount, sufficient to repay the outstanding debt of the CDP

```bash
aut contract tx --address 0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f --value <AMOUNT> liquidate <ACCOUNT>
```

The transaction will revert if the CDP is not liquidatable or the payment is insufficient to repay the debt.

On success, the CDP's collateral token and any surplus Auton remaining from the payment are transferred to your account.
