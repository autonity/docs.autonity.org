---
title: "Use the DAX"
description: >
  Recipes for how to interact with the Decentralized Auton Exchange (DAX)
hide_summary: false
draft: false
---

## Synopsis

This page provides a collection of resources and how-to guide for the on-chain exchange DAX. DAX is a Uniswap V2 Protocol AMM.

This page details:

- resources for how to interact with the on-chain exchange DAX
- how to submit a trade swap

## Exchange resource links

### Uniswap Docs 

- [V2 Protocol Overview ](https://docs.uniswap.org/contracts/v2/overview)
- [API Overview ](https://docs.uniswap.org/contracts/v2/reference/API/overview)

### DAX Uniswap Contract Addresses

Decentralized Auton Exchange (DAX) Contract Addresses deployed on the Autonity Network Piccadilly:

| Contract | Address |
| :-- | :--: |
| DAX **UniswapV2Factory** contract | [`TO ADD`]( TO ADD) |
| DAX **UniswapV2Router02** contract | [`TO ADD`](TO DO) |
| **Wrapped Auton (WATN)** ERC20 token  | [`TO ADD`](TO DO) |
| **WATN-USDC pool** contract "Decentralized Auton Exchange (DAX)"| [`TO ADD`](TO DO) |

### Uniswap Contract ABI

This can be downloaded from the Uniswap V2 docs links for Solidity and ABI source on unpkg.com for the [Factory ](https://unpkg.com/browse/@uniswap/v2-core@1.0.1/) and [Periphery ](https://unpkg.com/browse/@uniswap/v2-periphery@1.1.0-beta.0/) smart contracts. 

The compiled ABI is in `.json` files in the `/build` directories. You will need to import the interface ABI.

| Contract Interface file | Contract ABI file Link on Unpkg.com |
| :-- | :-- |
| Uniswap V2 Factory [`IUniswapV2Factory.sol` ](https://unpkg.com/browse/@uniswap/v2-core@1.0.1/contracts/UniswapV2Factory.sol) | [IUniswapV2Factory.json ](https://unpkg.com/browse/@uniswap/v2-core@1.0.1/build/IUniswapV2Factory.json) |
| Uniswap V2 Router02 [`IUniswapV2Router02.sol` ](https://unpkg.com/browse/@uniswap/v2-periphery@1.1.0-beta.0/contracts/interfaces/IUniswapV2Router02.sol) | [IUniswapV2Router02.json ](https://unpkg.com/browse/@uniswap/v2-periphery@1.1.0-beta.0/build/IUniswapV2Router02.json) | 
| Uniswap V2 Wrapped ETH (WETH) [`IWETH.sol` ](https://unpkg.com/browse/@uniswap/v2-periphery@1.1.0-beta.0/contracts/interfaces/IWETH.sol) (to interact with the Wrapped Auton (WATN) ERC-20 token contract) | [`IWETH.json` ](https://unpkg.com/browse/@uniswap/v2-periphery@1.1.0-beta.0/build/IWETH.json) |

Alternatively, you can manually generate the ABI yourself using tooling. For example, using:

- Ethereum REMIX IDE. This is online at https://remix.ethereum.org/. See the docs for how to [compile the ABI from Solidity ](https://remix-ide.readthedocs.io/en/latest/compile.html).
- Solidity Compiler `solc`. See the docs to [install ](https://docs.soliditylang.org/en/latest/installing-solidity.html) and how to use the [compiler ](https://docs.soliditylang.org/en/latest/using-the-compiler.html#).

## WIP TESTING ON BAKERLOO HERE START

### FUNCTION TO USE & Uniswap V2 DOCS LINKS

- when function name has ETH you can swap for native token
- to swap USDC for ATN: swapExactTokenForEth
- converse: swapExactEthForToken
- remove the ones for add liquidity / create pair
- i.e. keep this simple and minimal

https://docs.uniswap.org/contracts/v2/reference/smart-contracts/factory

https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02

### ABI DOWNLOADED BUT NEED TO EDIT

- you've edited the factory but need to do the router json to abi conversion to. Also on the IWETH if you use that.

### BAKERLOO DEPLOYMENT ADDRESSES:


https://github.com/autonity/mainnet-and-bakerloo-runbook/blob/master/bakerloo-config/account-addresses.csv


- Factory deployed at: 0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944
- WATN deployed at: 0x7152e69E173D631ee7B8df89b98fd25decb7263D
- Router deployed at: 0x13a3a74463218D123596386D3E36bd1aC13DCFE2
- USDCx deployed at: 0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E

### AUT COMMANDS BEING USED

Note using aut not autdev is fine for this test.

jay@Jays-MacBook-Pro autcli % aut contract call --abi IUniswapV2Factory.abi --address 0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944 allPairs 0

- returns the address at index 0 i.e. WATN-USDCx - i.e. "0xe5bC134ae83DD0885eEe6942BB52337d55A3cAb2"

jay@Jays-MacBook-Pro autcli % aut contract call --abi IUniswapV2Factory.abi --address 0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944 getPair 0x7152e69E173D631ee7B8df89b98fd25decb7263D 0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E

- returns the address by using the token contract addresses - which is ofc that at index 0 i.e. WATN-USDCx - i.e. "0xe5bC134ae83DD0885eEe6942BB52337d55A3cAb2"

Approve by Alice on USDCx contract to Router for 1 USDCx for the swap:
```console
aut token approve --token 0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 1 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit):
0x34defcacea7943306a597c82221d6f6ca17d1da5f1ee84c3d52a751b0d479b72
```

Alice then traded 0.5 ATN for USDCx and sent the USDCx to the test account for Dave `0xF6e02381184E13Cbe0222eEDe0D12B61E2DF8bE5`:  


```bash
aut contract tx --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 \
--value 0.5 \
swapExactETHForTokens \
400000 \
'["0x7152e69E173D631ee7B8df89b98fd25decb7263D","0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E"]' \
0xF6e02381184E13Cbe0222eEDe0D12B61E2DF8bE5 \
1754911643 \
| aut tx sign - \
| aut tx send -
```



## WIP TESTING ON BAKERLOO HERE END

## Get setup to trade on the DAX

You will need to setup your tooling to submit transactions to the DAX from your [account](/account-holders/create-acct/).

This guide assumes you will use the `aut` command line tool (see [Setup Autonity CLI](/account-holders/setup-aut/)) and the `aut contract` command group. To use `aut contract` for this you will need to get the ABI for the DAX Uniswap contract functions. See [Exchange resource links](/networks/testnet-piccadilly/dax.html#exchange-resource-links) for how to get (or generate) the [Uniswap Contract ABI](/getting-started/exchange-dax.html#uniswap-contract-abi).

Alternatively, develop your own custom scripting for interacting with the DAX Uniswap contracts! For example, using: `web3.py` ([docs ](https://web3py.readthedocs.io/en/stable/), [GitHub ](https://github.com/ethereum/web3.py)) or use the [uniswap-python library ](https://uniswap-python.com/index.html) [command line interface ](https://uniswap-python.com/cli.html).


## Getting DAX pair information

There is currently one pair created on the DAX for an ATN-USDC liquidity pool, the `WATN-USDC` token pair. The contract address for this pair is listed in the [Exchange resource links above](/networks/testnet-piccadilly/dax.html#exchange-resource-links).

To check if additional pairs have been created, you can query using the Uniswap `Factory` smart contract's `getPair`, `allPairs`, and `allPairsLength` functions, see docs [Factory ](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/factory). You can use the ABI for the Factory interface `IUniswapV2Factory` to do this.

To see if there is a pair on the DAX for 2 specific token contracts use the `aut contract call` command to call `getPair` where:

- `--abi`: is the path to the `IUniswapV2Factory.abi` ABI file
- `--address `: is the DAX Factory contract address `0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944`
- `<TOKENA>` and `<TOKENB>`: are the contract addresses for the requested tokens (order is insignificant)
  - `<TOKENA>`: is the WATN contract address `TO ADD`
  - `<TOKENB>`: is the USDC contract address `TO ADD`


```bash
aut contract call --abi IUniswapV2Factory.abi \
--address 0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944 getPair <TOKENA> <TOKENB>
```

For example, passing in the `WATN` and `USDC` contract addresses returns the contract address for the `WATN-USDC` pair:

```bash
aut contract call --abi ../abi/IUniswapV2Factory.abi \
--address 0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944 getPair 0x7152e69E173D631ee7B8df89b98fd25decb7263D 0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E
```
```console
"0xe5bC134ae83DD0885eEe6942BB52337d55A3cAb2"
```

::: {.callout-tip title="Discovering pairs if you don't know the token contract addresses" collapse="true"}
To discover new pairs where you don't know the token contract addresses, use `allPairs` to pass in an index number to return the first, second pair created etc.

Use the `aut contract call` command to call `allPairs` where:

- `--abi`: is the path to the `IUniswapV2Factory.abi` ABI file
- `--address `: is the Factory contract address `0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944`
- `<INDEX>`: is an integer index number for the pair beginning at `0`. Pass in `0` to return the first pair created, `1` for the second, etc. 


```bash
aut contract call --abi IUniswapV2Factory.abi \
--address 0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944 allPairs <INDEX>
```
For example, passing in the index `0` returns the contract address for the first pair created, the `NTN-WATN` pair:

```bash
aut contract call --abi ../build/IUniswapV2Factory.abi \
--address 0x9709D1709bDE7C59716FE74D3EEad0b1f12D3944 allPairs 0
```
```console
"0xe5bC134ae83DD0885eEe6942BB52337d55A3cAb2"
```

To return the total number of pairs created, you can call `allPairsLength`. It will return an integer reflecting the number of pairs created.  `1`, i.e. the `WATN-USDC` pair. 
:::

## Getting a quote for trading

::: {.callout-tip title="Note" collapse="false"}
See the Uniswap docs advanced topic [Pricing](https://docs.uniswap.org/contracts/v2/concepts/advanced-topics/pricing) for an explanation of Uniswap V2 pricing and the risks of front running.
:::

::: {.callout-note title="Note" collapse="false"}
To get a quote for trading use the `getAmountsIn` and `getAmountsOut` rather than `quote` functions. This is because the result returned by `getAmounts*` includes the swap fees in the result. The `quote` function result does not - `quote` is useful to get quantities when minting.
:::

To price your trade and discover the amount of token you will get for trading an exact amount of the base or quote token of a pair, use the Uniswap `UniswapV2Router02` smart contract's `getAmountsIn` and `getAmountsOut` functions:

- Exact input amount use `getAmountsOut`: specify an _input_ token amount to provide, the function will calculate how much of the _output_ asset you would get for the swap
- Exact output amount use `getAmountsIn`: specify an _output_ token amount to receive, the function will calculate the minimum amount of the _input_ token you would need to provide for the swap

See docs [Router02 ](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02). You can use the ABI for the Router02 interface `IUniswapV2Router02 ` to do this.


Use the `aut contract call` command to call `getAmountsIn` and `getAmountsOut` where:

- `--abi`: is the path to the `IUniswapV2Router02` ABI file
- `--address `: is the Router02 contract address `0x13a3a74463218D123596386D3E36bd1aC13DCFE2`
- `<amountIn>` or `<amountOut>`: is the input / output asset amount to be traded, passed in using `10^18` denomination
- an array of token address pairs `<TOKENA>` and `<TOKENB>` to specify the contract addresses for the requested tokens (order is insignificant)

```bash
aut contract call --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 getAmountsIn <amountIn> '["<TOKENA>", "<TOKENB>"]'
```

```bash
aut contract call --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 getAmountsOut <amountOut> '["<TOKENA>", "<TOKENB>"]'
```


### Exact input quote example (`getAmoutsOut`)
To calculate how much output token you receive for an input of `0.1` ATN, pass as `amountOut` `0.1` ATN in `10^18` denomination (`100000000000000000`) and the token contract addresses for the `WATN-USDC` pair:


```bash
aut contract call --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 getAmountsOut 100000000000000000 '["0x7152e69E173D631ee7B8df89b98fd25decb7263D", "0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E"]'
```

Returns something like:

```bash
[100000000000000000, 127615]
```

I.e. `0.000000000000127615` USDC output is the amount received for `0.1` ATN input.

### Exact output quote example (`getAmoutsIn`)

To calculate how much input ATN to provide for an output of `0.005` USDC, pass as `amountIn` `0.005` USDC in `10^18` denomination (`5000000000000000`) and the token contract addresses for the `WATN-USDC` pair:

```bash
aut contract call --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 getAmountsIn 5000000000000000 '["0x7152e69E173D631ee7B8df89b98fd25decb7263D", "0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E"]'
```

Returns something like:

```bash
[100300902708205406, 5000000000000000]
```

I.e. `0.100300902708205406` ATN input is the amount to provide for `0.005` USDC output.


## Executing a swap

To execute a swap between ATN and USDC involves the steps below:

1. (Optional) Approve the DAX Router as a spender for the USDC contract if you intend to swap USDC for ATN
2. Swap between USDC and ATN

### Step 1: approve the router to spend USDC (if swapping USDC for ATN)
If swapping a token for ATN, then you will need to approve the UniswapV2 Router Contract as a `spender` of that token. To do this you will need to call the standard ERC-20 `approve()` method of the NTN contract. The NTN contract address is listed in the [Exchange resource links above](/getting-started/exchange-dax.html#exchange-resource-links) above.

 
#### 1. Verify your token balances

(Optional.) Verify you have the necessary ATN and USDC balances for the desired swap.

For ATN simply call your account balance:

```bash
aut account info
```

Or if you already have WATN, call the WATN contract to call your account balance:


```bash
 aut contract call [OPTIONS] METHOD [PARAMETERS]...
```

Example for WATN using `aut contract call`:

```bash
aut contract call --abi WATN.abi --address 0x7152e69E173D631ee7B8df89b98fd25decb7263D balanceOf <MY_ADDRESS>
```

Example for WATN using `aut tokcn balance-of`:

```bash
aut token balance-of --token 0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E <MY_AD
DRESS>
```

For the USDC contract simply call your account balance:

Example for USDC:

```bash
aut token balance-of --token 0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E 0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa
1000.000000
```

The amount approved in Step 2 must be `<=` to your USDC balances, otherwise the approval transaction will revert.

#### Step 2. Approve the Router Contract

Approve the Router Contract as a `spender` of USDC tokens. Call the USDC ERC-20 `approve()` contract functions (see the [docs.autonity.org ](https://docs.autonity.org/) Autonity Contract Interface [approve() ](https://docs.autonity.org/reference/api/aut/#approve).)

Use the `aut token approve` command where:

- `--token `: is `<ERC-20_CONTRACT_ADDRESS> ` of the `USDC` contract address 
- `<SPENDER>` is the Router02 Contract address, listed in [Exchange resource links above](/getting-started/exchange-dax.html#exchange-resource-links)
- `<AMOUNT>` is the amount of USDC that you are allowing the contract to spend on your behalf. 

For ERC-20 calls use the `aut token` command group:

```bash
aut token approve --token <ERC-20_CONTRACT_ADDRESS> <SPENDER> <AMOUNT>
```

In this example, , approval is given for `1` USDC:

```bash
aut token approve --token 0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 1 | aut tx sign - | aut tx send -
```

### Step 2: swap between USDC and ATN

::: {.callout-note title="Info" collapse="false"}
As an EVM-compatible chain, Autonity's equivalent to Ether is Auton (ATN). You can trade with Auton directly using Uniswap functions supporting ETH. For example, `swapExactETHForTokens` or `addLiquidityETH`.

You can, of course, trade using generic Uniswap functions for trading ERC-20 tokens. For example, to swap the ERC-20 tokens Wrapped Auton (WATN) and USDC using `swapExactTokensForTokens`.
:::

You can make swap trades using the Uniswap `UniswapV2Router02` smart contract's swap functions - see docs [`swapExactETHForTokens` ](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02#swapexactethfortokens) and [`swapTokensForExactETH` ](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02#swaptokensforexacteth). You can use the ABI for the Router02 interface `IUniswapV2Router02` to do this.

::: {.callout-warning title="USDC decimals is 6 not 18!" collapse="false"}
The uniswap swap in and out amounts are specified in exponent format. For an ERC-20 with a decimals setting of 18, then this would be 10^18. USDC uses 6 decimals so is 10^6.

Note that for the WATN and USDC contracts it is:

| Token | Decimals | Exponent | Example |
|:-- |:-- |:-- |:-- |
| WATN | 18 | 10^18 | 1 WATN = `1 * 10^18` = `1000000000000000000` in base units |
| USDC | 6 | 10^6 | 1 USDC = `1 * 10^6` = `1000000` in base units |

:::
#### ATN to USDC using `swapExactETHForTokens`

Swap an exact amount of ATN for USDC.  Use the `aut contract tx` command to call `swapExactETHForTokens` where:

- `--abi`: is the path to the `IUniswapV2Router02` ABI file
- `--address `: is the Router02 contract address
- `--value`: is the amount of ATN to swap, passed in using `10^18` denomination
- `<amountOutMin>`: is the minimum amount of output tokens to receive from the swap, passed in using `10^18` denomination. This sets a floor limit beneath which the swap will not take place and the transaction will revert
- `<path>`: is an array of addresses for the token pairs to swap - The WATN and USDC contract addresses, `'["<WATN_CONTRACT_ADDRESS>","<USDC_CONTRACT_ADDRESS>"]'`
- `<to>`: is the address of the swapped tokens. I.e. let's assume you want them sent to your account address
- `<deadline>`: the time point by which the trade must be executed, after which the transaction will revert. The timestamp is provided as a [Unix time](/glossary/#unix-time) value

```bash
aut contract tx --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 --value \
swapExactETHForTokens \
<amountOutMin> \
<path> \
<to> \
<deadline> \
| aut tx sign \
| aut tx send -
```

For example, for a trade on the `WATN-USDC` pair, passing in an amount of `0.5` ATN to swap for at minimum `0.4` USDC, the swap output token transferred to account `0xF6e02381184E13Cbe0222eEDe0D12B61E2DF8bE5`:


```bash
aut contract tx --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 \
--value 0.5 \
swapExactETHForTokens \
400000 \
'["0x7152e69E173D631ee7B8df89b98fd25decb7263D","0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E"]' \
0xF6e02381184E13Cbe0222eEDe0D12B61E2DF8bE5 \
1754911643 \
| aut tx sign - \
| aut tx send -
```



#### USDC to ATN using `swapExactTokensForEth`

Swap an exact amount of USDC for ATN.  Use the `aut contract tx` command to call `swapExactTokensForEth` where:

- `--abi`: is the path to the `IUniswapV2Router02` ABI file
- `--address `: is the Router02 contract address
- `<amountIn>`: is the amount of USDC to swap, passed in using `10^18` denomination
- `<amountOutMin>`: is the minimum amount of output tokens to receive from the swap, passed in using `10^18` denomination. This sets a floor limit beneath which the swap will not take place and the transaction will revert
- `<path>`: is an array of addresses for the token pairs to swap - The USDC and WATN contract addresses, `'["<USDC_CONTRACT_ADDRESS>","<WATN_CONTRACT_ADDRESS>"]'`
- `<to>`: is the address of the swapped tokens. I.e. let's assume you want them sent to your account address
- `<deadline>`: the time point by which the trade must be executed, after which the transaction will revert. The timestamp is provided as a [Unix time](/glossary/#unix-time) value

```bash
aut contract tx --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 \
swapExactTokensForETH \
<amountIn> \
<amountOutMin> \
<path> \
<to> \
<deadline> \
| aut tx sign \
| aut tx send -
```

For example, for a trade on the `WATN-USDC` pair, passing in an amount of `1` USDC to swap for at minimum `0.5` ATN, the swap output token transferred to account `0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa`:


```bash
aut contract tx --abi IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 \
swapExactTokensForETH \
1000000 \
500000000000000000 \
'["0x90488152F52e1aDc63CaA2CDb6Ad84F3AEC1df3E","0x7152e69E173D631ee7B8df89b98fd25decb7263D"]' \
0xF47FDD88C8f6F80239E177386cC5AE3d6BCdEeEa \
1754911643 \
| aut tx sign - \
| aut tx send -
```

## DELETE FROM HERE ON

## Add or remove liquidity to and from the NTN-WATN pool

You can add or remove liquidity from the NTN-WATN-USDC pool using the Uniswap `UniswapV2Router02` smart contract's liquidity functions - see docs [`addLiquidityETH` ](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02#addliquidityeth) and [`removeLiquidityETH` ](https://docs.uniswap.org/contracts/v2/reference/smart-contracts/router-02#removeliquidityeth). You can use the ABI for the Router02 interface `IUniswapV2Router02 ` to do this.

For providing liquidity, you will receive liquidity tokens in the NTN-WATN pool contract "Decentralized Auton Exchange (DAX)".

As example, let's add an amount of ATN liquidity to the NTN-WATN pool with ATN. Use the `aut contract tx` command to call `addLiquidityEth` where:

- `--abi`: is the path to the `IUniswapV2Router02` ABI file
- `--address `: is the Router02 contract address

- `--value`: is the amount of ATN to add as liquidity if the NTN-WATN price is `<= amountTokenDesired/msg.value` (WATN depreciates).
- `<token>`: is the contract address of the NTN token
- `<amountTokenDesired>`: is the amount of NTN token to add as liquidity if the WATN/NTN token price is `<= msg.value/amountTokenDesired` (token depreciates).
- `<amountTokenMin>`: is an amount that bounds the extent to which the WATN/NTN token price can go up before the transaction reverts. Must be `<= amountTokenDesired`.
- `<amountETHMin>`: is an amount that bounds the extent to which the token/WATN price can go up before the transaction reverts. Must be `<= msg.value`. Passed in using `10^18` denomination.
- `<to>`: is the recipient address of the liquidity tokens. I.e. let's assume you want them sent to your registered participant account address
- `<deadline>`: the time point by which the liquidity deposit transaction must be executed, after which the transaction will revert. The timestamp is provided as a [Unix time](/glossary/#unix-time) value


```bash
aut contract tx --abi ../build/IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 \
--value \
addLiquidityETH \
<token> \
<amountTokenDesired> \
<amountTokenMin> \
<amountETHMin> \
<to> \
<deadline> \
| aut tx sign - \
| aut tx send -
```

For example, to add `10` WATN liquidity to the `NTN-WATN` pair, passing in an amount of `10` WATN to add liquidity for `1` NTN (the pair has a ratio of 10 ATN to 1 NTN). The `amountTokenDesired` is set to `1`, the liquidity tokens received are transferred to (registered participant) account `0xF6e02381184E13Cbe0222eEDe0D12B61E2DF8bE5`:


```bash
aut contract tx --abi ../build/IUniswapV2Router02.abi \
--address 0x13a3a74463218D123596386D3E36bd1aC13DCFE2 \
--value 12.0 \
addLiquidityETH \
0x7152e69E173D631ee7B8df89b98fd25decb7263D \
1000000000000000000 \
0 \
0 \
0xF6e02381184E13Cbe0222eEDe0D12B61E2DF8bE5 \
1700139337 \
| aut tx sign - \
| aut tx send -
```
On success, the recipient address will appear as a token holder address for the `DAX` liquidity tokens. You can view your token holdings on the Block Explorer by navigating to inspect the recipient account address and viewing the "Tokens" tab, or navigating to the "DAX" token contract address and viewing the "Token Holders" tab.
