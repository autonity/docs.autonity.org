
---
title: "Development with Autonity"
linkTitle: "Development"
weight: 90
description: >
  Start developing on the Autonity network, spin up a local development testnet and deploy contracts.
draft: false
---

The steps in this section describe how to set up a local testnet for development and deploy contracts to your local or a public Autonity network.

It is assumed that you have:

- [Setup the Autonity Utility Tool (aut)](/account-holders/setup-aut/).

- Have an [account](/account-holders//create-acct/) that has been [funded](/account-holders/fund-acct/) with auton, to pay for transaction gas costs:
	
	- If deploying to a public network you will need to [fund](/account-holders/fund-acct/) your account from the testnet faucet.
	
	- If deploying to a custom network you will need to:
		
		- Fund your dev account(s) in the [genesis configuration file](/reference/genesis/#genesis-configuration-file)'s [`alloc`](/reference/genesis/#alloc-object) data structure.
		
		- If you are running the client in dev mode, there is a pre-funded developer account. See [Command line options](/reference/cli/#command-line-options) `--dev`, `--dev.gaslimit`, `--dev.etherbase`.

- An installation of the Autonity Go Client. See the [Running a node](/node-operators) guide for details of how to [install Autonity in your environment](/node-operators/install-aut/) and [run](/node-operators/run-aut/) it.

