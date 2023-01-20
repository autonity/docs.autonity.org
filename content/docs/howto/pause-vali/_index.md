---
title: "Pause and reactivate a Validator"
linkTitle: "Pause and Reactivate Validator"
weight: 130
description: >
  How to pause an active Validator, and reactivate a paused validator node.
---

## Prerequisites

- An Autonity Go Client registered as a validator in an active state.
- A running instance of `autcli` for submitting transactions from your account configured as described in [Submit a transaction from `autcli`](/howto/submit-trans-autcli/).
- Your validator's validator's [`treasury account`](/autonity/validator/#treasury-account) is [funded](/howto/fund-acct) with auton to pay for transaction gas costs.

{{< alert title="Note" >}}See the [Validator](/autonity/validator/) section for an explanation of the validator, a description of the [validator lifecycle](/autonity/validator/#validator-lifecycle), and [validator pausing](/autonity/validator/#validator-pausing).{{< /alert >}}

## Pause as a validator

1. To pause a validator from active to a paused, inactive state, use the `validator` command `pause`. Specify:

	- `--validator`: `<VALIDATOR_IDENTIFIER_ADDRESS>` of the validator node you are pausing.

    ```bash
    aut validator pause --validator <VALIDATOR_IDENTIFIER_ADDRESS> | aut tx sign - | aut tx send -
    ```

    You will be prompted for your passphrase for the key file. Having entered the password, the transaction hash will be returned on success.

    You should see something like beneath. In this example the validator node with identifier `0x49454f01a8F1Fbab21785a57114Ed955212006be` is paused. The returned hash is `0x942328...baec2d20`:

    ```bash
    aut validator pause --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
    (consider using 'KEYFILEPWD' env var).
    Enter passphrase (or CTRL-d to exit):
    0x942328bea54a0096ca9b2fb88acd337c883f7923c2ef6b8290a340c5baec2d20
	```

2. (Optional) To verify the validator is paused, use the `validator` command `info` to submit a call to query for validator metadata. It will return the validator metadata from system state, including the validator status:

	```bash
    aut validator info --validator <VALIDATOR_IDENTIFIER_ADDRESS>
    ```

    This will return a `Validator` object. The `state` property will be `1` (paused). You should see something like this:

    ```bash
	aut validator info --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be
	{
		"treasury": "0xd4EdDdE5D1D0d7129a7f9C35Ec55254f43b8E6d4",
		"addr": "0x49454f01a8F1Fbab21785a57114Ed955212006be",
		"enode": "enode://c746ded15b4fa7e398a8925d8a2e4c76d9fc8007eb8a6b8ad408a18bf66266b9d03dd9aa26c902a4ac02eb465d205c0c58b6f5063963fc752806f2681287a915@51.89.151.55:30304",
		"commission_rate": 1000,
		"bonded_stake": 0,
		"total_slashed": 0,
		"liquid_contract": "0x109F93893aF4C4b0afC7A9e97B59991260F98313",
		"liquid_supply": 0,
		"registration_block": 3505,
		"state": 1
	}
    ```

## Re-activate a validator

1. To resume a validator from a paused to an active state, use the `validator` command `activate`. Specify:

	- `--validator`: `<VALIDATOR_IDENTIFIER_ADDRESS>` of the validator node you are pausing.

    ```bash
    aut validator activate --validator <VALIDATOR_IDENTIFIER_ADDRESS> | aut tx sign - | aut tx send -
    ```

    You will be prompted for your passphrase for the key file. Having entered the password, the transaction hash will be returned on success.

    You should see something like beneath. In this example the validator node with identifier `0x49454f01a8F1Fbab21785a57114Ed955212006be` is re-activated. The returned hash is `0x0849c0...f1eb2a5b`:

    ```bash
    aut validator activate --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be | aut tx sign - | aut tx send -
    (consider using 'KEYFILEPWD' env var).
    Enter passphrase (or CTRL-d to exit):
    0x0849c0307bc446bb3fbb61b5c1518847574356aedb0b986248158d36f1eb2a5b
	```

2. (Optional) To verify the validator is re-activated, use the `validator` command `info` to submit a call to query for validator metadata. It will return the validator metadata from system state, including the validator status:

	```bash
    aut validator info --validator <VALIDATOR_IDENTIFIER_ADDRESS>
    ```

    This will return a `Validator` object. The `state` property will be `0` (active). You should see something like this:

    ```bash
	aut validator info --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be
	{
		"treasury": "0xd4EdDdE5D1D0d7129a7f9C35Ec55254f43b8E6d4",
		"addr": "0x49454f01a8F1Fbab21785a57114Ed955212006be",
		"enode": "enode://c746ded15b4fa7e398a8925d8a2e4c76d9fc8007eb8a6b8ad408a18bf66266b9d03dd9aa26c902a4ac02eb465d205c0c58b6f5063963fc752806f2681287a915@51.89.151.55:30304",
		"commission_rate": 1000,
		"bonded_stake": 0,
		"total_slashed": 0,
		"liquid_contract": "0x109F93893aF4C4b0afC7A9e97B59991260F98313",
		"liquid_supply": 0,
		"registration_block": 3505,
		"state": 0
	}
    ```
