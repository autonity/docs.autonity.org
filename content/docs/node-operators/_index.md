---
title: "Node Operators"
linkTitle: "Node Operators"
weight: 40
description: >
  How to setup and operate an Autonity Go Client node on an Autonity testnet
---

All nodes on the Autonity network exchange blocks and transactions with other nodes, keep track of the current start of the blockchain.  Running a node offers a dedicated RPC endpoint for querying and for accepting transactions.  DApps running on the network may take advantage of dedicates nodes for any "backend" or off-chain operations.

This guide describes the steps to install, configure and run an instance of the Autonity Go Client (AGC) on an Autonity testnet, and describes how to use the [`aut` CLI tool](/account-holders/setup-autcli/) to connect to the node and performing some basic operations.

It is assumed that you the reader has setup the `aut` CLI tool, has an [account](/account-holder/create-acct/) with [fund](/account-holder/fund-acct/) and is able to submit transactions to the network.  See the [Account Holder Guide](/account-holder/) for details.

The approach taken in this guide is to run the Autonity Go Client on a dedicated _host_ machine (a VPS or other host that is _always-on_ and persistently available).  Transactions and queries are expected to be created (and signed) on a distinct _local_ machine, and then sent to the Autonity Go Client running on the _host_ via the RPC endpoint.  This setup may be adjusted to suit each specific deployment.

{{< alert title="Note" >}}
This guide is intended for use on _testnets_ (see [Networks](/networks/)), on which there is no real-world value at stake.  A production setup will likely have requirements not covered by this guide, such as node availability and security.  For example, the configuration outlined here exposes an unencrypted `http` RPC end-point. For production an operator may wish to configure authentication and encryption (for example using a reverse-proxy such as NGINX).
{{< /alert >}}

Further information about Autonity [concepts](/concepts/) and [terminology](/glossary/) are available in this documentation.

------------------------------------------------

If you need help, you can chat to us on [Discord Server](https://discord.gg/autonity)!
