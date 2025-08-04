---
title: "Inflation Controller Contract Interface"

description: >
  Autonity Inflation Controller Contract functions
---

Interface for interacting with Autonity Inflation Controller Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

::: {.callout-note title="Protocol contract calls" collapse="false"}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Inflation Controller Contract's generated ABI and the `aut` tool's `contract` command to call the Inflation Controller Contract address `0x3BB898B4Bbe24f68A4e9bE46cFE72D1787FD74F4`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `InflationController` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/InflationController`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).

:::

##  getParams

Returns the current parameters of the inflation controller.

### Parameters
   
None.

### Response

Returns a `Params` object with properties of:

| Field | Datatype | Description |
| --| --| --|
| `inflationRateInitial` | `SD59x18` | Initial inflation rate |
| `inflationRateTransition` | `SD59x18` | Transition inflation rate |
| `inflationCurveConvexity` | `SD59x18` | Convexity Parameter |
| `inflationTransitionPeriod` | `SD59x18` | Transition | `inflationReserveDecayRate` (denominated in seconds) |
| `inflationReserveDecayRate` | `SD59x18` | Constant IR post T (denominated in seconds) |

### Usage

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x3BB898B4Bbe24f68A4e9bE46cFE72D1787FD74F4 getParams
```
:::

### Example

::: {.panel-tabset}
## aut
``` {.aut}
aut contract call --address 0x3BB898B4Bbe24f68A4e9bE46cFE72D1787FD74F4 getParams
```
```console
{"inflationRateInitial": 2378234398, "inflationRateTransition": 1744038559, "inflationCurveConvexity": 2765000000000000000, "inflationTransitionPeriod": 126230400000000000000000000, "inflationReserveDecayRate": 5491184677}
```
:::

