---
title: "ASM Contract Interface"

description: >
  Auton Stabilization Mechanism Contract functions
---

Interfaces for interacting with Auton Stabilization Mechanism Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Info" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the ASM Contracts' generated ABI and the `aut` tool's `contract` command to call the ASM Contract functions. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The contract `.abi` files are generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
:::
