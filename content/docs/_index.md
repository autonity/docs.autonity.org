
---
# title: "Welcome to Autonity!"
linkTitle: "Documentation"
type: docs

# Use target-specific front matter cascade to create a "docs only" site.
cascade:
    - _target:
        path: "/**"
        kind: "page"
      type: "docs"
    - _target:
        path: "/**"
        kind: "section"
      type: "docs"
resources:
- src: "**logo-autonity*.{png,svg}"
---

![logo-autonity](/logo-autonity.png)

Welcome to the documentation site for the Autonity Go Client (AGC). AGC is the main client software run by peer nodes in an Autonity network. 

AGC is a fork of [Geth](https://geth.ethereum.org/) and is the reference implementation of the Autonity Protocol. The protocol provides an EVM-based blockchain that utilises Tendermint BFT for delegated proof of stake consensus, has a dual native coin design for tokenomics, and provides liquid staking for capital efficiency.

This documentation describes key concepts and functionality of the protocol and client. It explains how to use the software and connect to an Autonity network.

## Getting started

### Autonity protocol and platform

- See [Autonity](/autonity/) for key concepts of the Autonity protocol and tokenomics, technical architecture of the platform, and available networks.

### Usage

- See [How to's](/howto/) for client installation, running and connecting to an Autonity Network, and examples for submitting transactions and calls to Autonity.
- See [Networks](/networks/) for publicly accessible Autonity Networks.

### Reference

- See [Reference](/reference/) for technical reference documentation of the codebase and API's.

### Terminology

- Explanations of terminology used throughout the documentation can be found in the [Glossary](/glossary/).
