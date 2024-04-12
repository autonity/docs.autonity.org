
---
# title: "Welcome to Autonity!"

---

![](/_assets/images/text-logo-autonity.svg)

Welcome to the documentation site for the [Autonity Go Client (AGC)](https://github.com/autonity/autonity) and [Autonity Oracle Server (AOS)](https://github.com/autonity/autonity-oracle)! AGC is the main client software run by peer nodes in an Autonity network. AOS is the oracle software run by validator nodes to source price data from external data providers and submit price reports on-chain.

AGC is a fork of [Geth <i class='fas fa-external-link-alt'></i>](https://geth.ethereum.org/) and is the reference implementation of the Autonity Protocol. The protocol provides an EVM-based blockchain that utilises Tendermint BFT for delegated proof of stake consensus, has a dual native coin design for tokenomics, and provides liquid staking for capital efficiency.

This documentation describes key concepts and functionality of the Autonity protocol, main client, and oracle server. It explains how to use the software and connect to an Autonity network.

## Getting started

### Autonity protocol and platform

- See [Concepts](/concepts/) for key concepts of the Autonity protocol and tokenomics, technical architecture of the platform, and available networks.

### Usage

- See the user-oriented guides for how to use the system:

  - [Account Holders](/account-holders/) for how to set up an account on the network: set up the Autonity `aut` command-line tool, create and fund accounts, submit transactions.
  
  - [Staking](/delegators/) for how to delegate stake in Autonity's liquid staking model: bond and unbond stake to validators, claim staking rewards, and transfer Liquid Newton.

  - [Running a Node](/node-operators/) for how to install and run the Autonity Go Client, connect to an Autonity Network, and setup node monitoring.

  - [Running a Validator](/validators/) and [Running an Oracle Server](/oracle/) for how to operate your node as a validator node: 
    - Setting up the validator's oracle server
    - Registering, pausing and reactivating validator operations, and setting your validator commission rate.

  - [Development](/developer/) for how to set up a custom network for development and deploy contracts to your local or a public Autonity network.

- See [Networks](/networks/) for publicly accessible Autonity Networks you can connect your node to.

### Reference

- See [Reference](/reference/) for technical reference documentation of the codebase and API's.

### Terminology

- Explanations of terminology used throughout the documentation can be found in the [Glossary](/glossary/).