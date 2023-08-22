---
title: "ACU Contract Interface"
linkTitle: "ACU Contract Interface"
weight: 10

description: >
  Auton Currency Unit Contract functions
---

Interfaces for interacting with the ASM Auton Currency Unit Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

{{% pageinfo %}}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the ACU Contract's generated ABI and the `aut` tool's `contract` command to call the ACU Contract address `0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `ACU.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./params/generated/ACU.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).

{{% /pageinfo %}}

## value

Returns the latest value computed for the ACU index.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `_value ` | `int256` | the ACU value in fixed-point integer representation |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA value
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA value
98410
{{< /tab >}}
{{< /tabpane >}}

## symbols

Returns the currency pair symbols used to compute the ACU index.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `_symbols` | `string` array | a comma-separated list of the currency pair symbols used to compute the ACU index value |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA symbols
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA symbols
["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "USD-USD", "SEK-USD"]
{{< /tab >}}
{{< /tabpane >}}

## quantities

Returns the basket quantities used to compute the ACU index value.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `_quantities` | `uint256` array | an array of the quantities |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA quantities
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA quantities
[21300, 18700, 14300, 10400, 1760000, 18000, 141000]
{{< /tab >}}
{{< /tabpane >}}
