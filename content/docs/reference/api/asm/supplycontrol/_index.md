---
title: "Supply Control Contract Interface"
linkTitle: "Supply Control Contract Interface"
weight: 20

description: >
  Supply Control Contract functions
---

Interfaces for interacting with the ASM Supply Control Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

{{% pageinfo %}}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Supply Control Contract's generated ABI and the `aut` tool's `contract` command to call the Supply Control Contract address `0x47c5e40890bcE4a473A49D7501808b9633F29782`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `SupplyControl.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./common/acdefault/generated/SupplyControl.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
{{% /pageinfo %}}


## availableSupply

Returns the supply of Auton available for minting.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| `availableSupply` | `uint` | the amount of Auton available for minting as an integer value |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut contract call --address 0x47c5e40890bcE4a473A49D7501808b9633F29782 availableSupply
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}


## stabilizer

Returns the Stabilization Contract address, the `stabilizer` account that is authorized to mint and burn Auton.
    
### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| `address` | `address` | the Stabilization Contract address |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< tab header="RPC" >}}

{{< /tab >}}
{{< /tabpane >}}


### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< tab header="RPC" >}}

{{< /tab >}}
{{< /tabpane >}}


## totalSupply

Returns the total supply of Auton under management.

### Parameters

None.

### Response

| Field | Datatype| Description |
| --| --| --|
| Auton Supply | `uint256` | the total supply of Auton under management |

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< tab header="RPC" >}}

{{< /tab >}}
{{< /tabpane >}}


### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< tab header="RPC" >}}

{{< /tab >}}
{{< /tabpane >}}

