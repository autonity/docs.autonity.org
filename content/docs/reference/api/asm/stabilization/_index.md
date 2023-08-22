---
title: "Stabilization Contract Interface"
linkTitle: "Stabilization Contract Interface"
weight: 30

description: >
  Stabilization Contract functions
---

Interfaces for interacting with the ASM Stabilization Contract functions using:

- The `aut` command-line RPC client to submit calls to inspect state and state-affecting transactions.

{{% pageinfo %}}
Examples for calling functions from `aut` use the setup described in the How to [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).

Usage and Examples illustrate using the Stabilization Contract's generated ABI and the `aut` tool's `contract` command to call the Stabilization Contract address `0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f`. See `aut contract call --help`.

Usage and Examples assume the path to the ABI file has been set in `aut`'s configuration file `.autrc`. The `Stabilization.abi` file is generated when building the client from source and can be found in your `autonity` installation directory at `./common/acdefault/generated/Stabilization.abi`. Alternatively, you can generate the ABI using the `abigen` `cmd` utility if you built from source (See [Install Autonity, Build from source code](/node-operators/install-aut/#install-source)).
{{% /pageinfo %}}

## CDP Owner
### deposit

Deposit Collateral Token to a CDP using the ERC20 allowance mechanism.

Before calling this function, the CDP owner must approve the Stabilization contract to spend Collateral Token on their behalf for the full amount to be deposited.

Constraint checks are applied:

- the `amount` deposited is a non-zero amount
- the `amount` deposited is `<` the `allowance` amount that the CDP owner has approved the CDP contract to transfer.

The CDP's collateral balance is then incremented by the deposited amount.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | Units of Collateral Token to deposit (non-zero) |

#### Response

None.

#### Event

On a successful call the function emits a `Deposit` event, logging: `msg.sender`, `amount`.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}


### withdraw

Request a withdrawal of Collateral Token from a CDP.

On method execution, state is inspected to retrieve:

- the CDP principal, collateral, and debt amounts
- the minimum collateralization and liquidation ratios from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- invalid amount: the `amount` withdrawn is `<` the CDP's collateral amount 
- insufficient collateral: the withdrawn `amount` must not reduce the remaining Collateral Token amount below the minimum collateral ratio.
- liquidatable: withdrawal does not make the CDP liquidatable. The withdrawn amount value must not reduce the CDP to an under collateralized state below the liquidation ratio.

The CDP's collateral balance is then decremented by the withdrawn amount and Collateral Token is transferred to the CDP owner.


#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | Units of Collateral Token to withdraw (non-zero) |

#### Response

None.

#### Event

On a successful call the function emits a `Withdraw` event, logging: `msg.sender`, `amount`.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

### borrow

Borrow Auton against CDP Collateral.

On method execution, state is inspected to retrieve:

- the current CDP borrow limit, and debt and accrued interest amounts
- the minimum collateralization and liquidation ratios, and the minimum debt requirement from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- invalid debt position: the `debt` after borrowing must satisfy the minimum debt requirement.
- liquidatable: borrowing does not make the CDP liquidatable. The `debt` after borrowing amount value must not reduce the CDP to an under collateralized state below the liquidation ratio.
- insufficient collateral: the borrowed `amount` must not exceed the borrow `limit` for the CDP. The `debt` after borrowing must not reduce the CDP to an under collateralized state below the minimum collateral ratio.

The CDP's debt is then incremented by the borrowed amount and Auton is minted to the CDP owner.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `amount` | `uint256` | Amount of Auton to borrow (non-zero) |

#### Response

None.

#### Event

On a successful call the function emits a `Borrow` event, logging: `msg.sender`, `amount`.


#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}


### repay

Make a payment towards a CDP debt. The transaction value is the payment amount.

On method execution, state is inspected to retrieve:

- the current CDP principal amount, and debt and accrued interest amounts
- the minimum collateralization and liquidation ratios, and the minimum debt requirement from the Stabilization Contract config
- the current Collateral Token price.

Constraint checks are applied:

- no debt position: there is a debt; the CDP `principal` is `> 0`.
- invalid debt position: the debt after payment must satisfy the minimum debt requirement. The payment amount is `<` the `debt` and the `debt` after the payment amount satisfies the minimum debt requirement.

The payment first covers the outstanding interest debt before the principal debt. If there is a surplus after repayment, then the surplus is returned to the CDP Owner.

#### Parameters

| Field | Datatype | Description |
| --| --| --|
| `msg.value` | `uint256` | The payment amount |

#### Response

None.

#### Event

On a successful call the function emits a `Repay` event, logging: `msg.sender`, `msg.value`.


#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}

{{< /tab >}}
{{< /tabpane >}}

