---
title: "Node Operators"
linkTitle: "Node Operators"
weight: 40
description: >
  How to setup and operate an Autonity Go Client node on an Autonity testnet
---

This section outlines how to:

1. Install the Autonity Go Client as a binary or a Docker image, pre-configured for an Autonity testnet.
2. Add your node to an Autonity testnet.
3. Interact with the testnet using your node.


This guide uses the Autonity [Piccadilly Testnet](https://docs.autonity.org/networks/testnet-piccadilly/) as an example.

## Useful to know

* Autonity is derived from Ethereum protocols. **_This guide assumes a basic understanding of the principles behind Ethereum_**.
* **_Basic Unix command-line skills_** are also assumed. You should be able to obtain or set up a simple Linux host with a static internet IP address, and root access.
* Knowledge of Docker is not assumed. Explanations will be given as required, but it may be **_helpful to know more about how Docker works_**.

Setting up and maintaining an Autonity node is relatively simple in the context of a testnet (such the [Piccadilly Testnet](https://docs.autonity.org/networks/testnet-piccadilly/)), as no real value is at stake. A production setup will likely have requirements not covered by this guide, such as node availability and security.  For example, the configuration outlined here exposes an unencrypted `http` RPC end-point. For production an operator may wish to configure authentication and encryption (for example using a reverse-proxy such as NGINX).

------------------------------------------------

If you need help, you can chat to us on [Discord Server](https://discord.gg/autonity)!
