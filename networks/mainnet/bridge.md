---
title: "Bridge USDC to Mainnet"
description: >
  Recipes for how to bridge USDC from Polygon Mainnet to your account on Autonity Mainnet!
hide_summary: false
draft: false
---

## Synopsis

This page details:

- resources for how to get set up and interact with the Polygon Mainnet to bridge USDC to Autonity Mainnet

## Resource links

- Mainnet USDC Bridge Frontend UI URL:
  - [`TO ADD`]( TO ADD)
- USDC Bridge Contract addresses:
  - On Autonity Mainnet: [`TO ADD`]( TO ADD)
  - On Polygon Mainnet: [`TO ADD`]( TO ADD)

::: {.callout-tip title="What is USDC?" collapse="true"}

If you want to find out more about what USDC from Polygon is, here are some resources:

  - Circle [Introducing Bridged USDC Standard](https://www.circle.com/blog/bridged-usdc-standard)
  - Polygon [Bridged USDC Standard Contracts Are Live on Polygon zkEVM](https://polygon.technology/blog/bridged-usdc-standard-contracts-are-live-on-polygon-zkevm)
  - Polygon [Native USDC now available on Polygon PoS](https://www.circle.com/blog/native-usdc-now-available-on-polygon-pos)
<!--
- About Polygon Amoy Testnet [Introducing the Amoy Testnet for Polygon PoS](https://polygon.technology/blog/introducing-the-amoy-testnet-for-polygon-pos)
-->
:::

## Get setup 

Bridging is simple with a frontend UI provided. The bridge UI requires you connect a wallet, so you will need to have your wallet software setup to use the address you registered for the game.

### Set up your wallet

To setup your chosen wallet you will need to:

- create and import your [account](/account-holders/create-acct/) into your wallet if you don't already have one
- add the Autonity Mainnet network to your wallet. The network details you will need to enter for this can be found at [Mainnet Details](/networks/mainnet/#mainnet-details).

## Bridge USDC from Polygon to Autonity

Simply navigate to the USDC Bridge Frontend UI URL (see [Resource links](/networks/mainnet/bridge.html#resource-links)). Connect your wallet and execute the bridge transfer on the UI.

Note that there will be 2 transactions - 1 to approve a spending cap on the USDC token contract, 1 to execute the bridge transfer over to Autonity.

To view your USDC token balance on Autonity, simply navigate to the [https://autonityscan.org](https://autonityscan.org)
 block Explorer and view the Token tab for your account address.

### Trading with your USDC on Autonity

To trade on-chain in the DAX simply use your bridged USDC to trade in an on-chain ATN market. For how to do this see the guide [Use the DAX](/networks/mainnet/dax.md).
