---
title: "Change Validator Commission Rate"
description: >
  How to change the stake delegation commission rate of your Validator node on an Autonity network
---

## Prerequisites

- An Autonity Go Client registered as a validator (the validator can be in a paused or an active state - see [validator lifecycle](/concepts/validator/#validator-lifecycle)).
- A running instance of `aut` for submitting transactions from your account configured as described in [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-aut/).
- Your validator's [`treasury account`](/concepts/validator/#treasury-account) is [funded](/account-holders/fund-acct/) with auton to pay for transaction gas costs.

{{< alert title="Note" >}}See the [Validator economics](/concepts/validator/#validator-economics) section for more information on commission rate and its default setting on an Autonity Network.{{< /alert >}}


## Change validator commission rate

1. To specify a new commission rate for a validator, use the `validator` command `change-commission-rate`. Specify:

	- `--validator`: `<VALIDATOR_IDENTIFIER_ADDRESS>` of the validator node you are pausing.
	- `<RATE>`: the new commission rate value. The commission rate precision is expressed in basis points as an integer value in the range `0-10000` (`10000` = 100%). Specify a decimal value between `0-1` For example, `0.078` would set a commission rate of 780 bps or 7.8%.

    ```bash
    aut validator change-commission-rate --validator <VALIDATOR_IDENTIFIER_ADDRESS> <RATE> | aut tx sign - | aut tx send -
    ```

    You will be prompted for your passphrase for the key file. Having entered the password, the transaction hash will be returned on success.
    
    You should see something like beneath. In this example the validator node with identifier `0x49454f01a8F1Fbab21785a57114Ed955212006be` is paused. The returned hash is `0xdbc9a2...6674d725`:
    
    ```bash
    aut validator change-commission-rate --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be 0.078 | aut tx sign - | aut tx send -
    (consider using 'KEYFILEPWD' env var).
    Enter passphrase (or CTRL-d to exit): 
    0xdbc9a27a2f7b53d9eaa660add917ed61fe7213d1cdd826065d0e7af96674d725
	```

{{< alert title="Note" >}}
Commission rate changes are subject to the same temporal [unbonding period](/concepts/staking/#unbondingperiod) constraint as staking transitions. On commit of the rate change transaction, the unbonding period is tracked and the rate change is applied at the end of the epoch in which the unbonding period expires.
{{< /alert >}}


2. (Optional) To verify the updated rate, use the `validator` command `info` to submit a call to query for validator metadata. It will return the validator metadata from system state, including the validator status:

	```bash
    aut validator info --validator <VALIDATOR_IDENTIFIER_ADDRESS>
    ```

    This will return a `Validator` object. The `commission_rate` property will show the new rate. You should see something like this:

    ```bash
	aut validator info --validator 0x49454f01a8F1Fbab21785a57114Ed955212006be
	{
		"treasury": "0xd4EdDdE5D1D0d7129a7f9C35Ec55254f43b8E6d4",
		"addr": "0x49454f01a8F1Fbab21785a57114Ed955212006be",
		"enode": "enode://c746ded15b4fa7e398a8925d8a2e4c76d9fc8007eb8a6b8ad408a18bf66266b9d03dd9aa26c902a4ac02eb465d205c0c58b6f5063963fc752806f2681287a915@51.89.151.55:30304",
		"commission_rate": 780,
		"bonded_stake": 0,
		"total_slashed": 0,
		"liquid_contract": "0x109F93893aF4C4b0afC7A9e97B59991260F98313",
		"liquid_supply": 0,
		"registration_block": 3505,
		"state": 1
	}
    ```
