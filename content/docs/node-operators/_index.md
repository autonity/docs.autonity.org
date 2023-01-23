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

## Key concepts

In addition to Ethereum concepts such as `address`, `gas`, and `node`, the distinction between participant and validator nodes is key in the Autonity context:

| **Concept** | **Meaning** |
| --------- | --------- |
| [Auton (_XTN_)](/architecture/protocol-assets/auton/) | Autonity's native account coin (intrinsic balance of an account, like "Ether" in Ethereum). |
| [participant](/architecture/system-model/#participants) node | A node running Autonity Go Client software and connected to other nodes in an Autonity network. A participant node maintains a copy of system state and may become a _validator_. |
| [validator](/architecture/validator/) node | A participant node that has registered as a validator on an Autonity network. A validator node may be selected to the _Consensus Committee_ if it has sufficient stake _bonded_ to it by a stake delegator. |
| [Consensus Committee](/architecture/consensus/committee/) | The subset of _validator_ nodes that participate in the consensus protocol. The Consensus Committee is updated periodically (every epoch), according to an algorithm prescribed by protocol. |

In a production setting, requirements for _participant_ nodes and _validator_ nodes may be significantly different, depending on the needs and role(s) of their owners.

For example, a _participant_ node may be used to submit transactions to the network and be provided as a public endpoint, making it necessary to meet high availability criteria.  In contrast, _validator_ nodes will generally be configured to NOT provide a public endpoint, in order to mitigate the risk of denial of service attacks while participating in the consensus protocol. Failing to remain active and responsive on the network while being part of the consensus committee can incur [slashing penalties](https://docs.autonity.org/glossary/#slashing-penalty).

For a reference of Autonity terminology and concepts see the [Glossary](https://docs.autonity.org/glossary/).

------------------------------------------------

If you need help, you can chat to us on [Discord Server](https://discord.gg/autonity)!
