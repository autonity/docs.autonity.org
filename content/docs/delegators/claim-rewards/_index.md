---
title: "Claim Staking Rewards"
linkTitle: "Claim Staking Rewards"
weight: 100
description: >
  How to view and claim available staking rewards using `aut`
---

## Prerequisites

To claim staking rewards you need:

- A running instance of `aut` for submitting transactions from your account configured as described in [Submit a transaction from Autonity Utility Tool (aut)](/account-holders/submit-trans-autcli/)
- An [account](/account-holders//create-acct/) [funded](/account-holders/fund-acct/) with auton to pay for transaction gas costs, and a Newton stake token balance >= to the amount being bonded.
- You have already [bonded stake](/delegators/bond-stake/) to a validator and have a Liquid Newton token balance that may have accrued claimable rewards.


## Get claimable reward balance {#get-reward-balance}

1. To return the current balance of your claimable rewards for a validator, use the `unclaimed-rewards` command to submit a call to query for claimable rewards. Specify:
	- `<VALIDATOR_IDENTIFIER_ADDRESS>`: the validator identifier address of the validator you are querying for your claimable rewards balance.

	It will return the amount of staking rewards you have available to claim, denominated in [attoton](/glossary/#attoton):

	```bash
    aut validator unclaimed-rewards --validator <VALIDATOR_IDENTIFIER_ADDRESS>
    ```

    You should see something like beneath. In this example, claimable rewards are `259885349961020`:

    ```bash
    aut validator unclaimed-rewards --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9
    259885349961020
    ```


## Claim staking rewards {#claim-rewards}

1. To claim rewards from a validator, submit a claim-rewards transaction. Specify:
	- `<VALIDATOR_IDENTIFIER_ADDRESS>`: the validator identifier address of the validator you are querying for your claimable rewards balance.

	```bash
    aut validator claim-rewards --validator <VALIDATOR_IDENTIFIER_ADDRESS> | aut tx sign - | aut tx send -
    ```

    You will be prompted for your passphrase for the key file. Having entered the password, the transaction hash will be returned on success.

    You should see something like beneath. In this example, the returned hash is rewards are `0xb0daf5...a6bcf12d`:

    ```bash
    aut validator claim-rewards --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9 | aut tx sign - | aut tx send -
    (consider using 'KEYFILEPWD' env var).
    Enter passphrase (or CTRL-d to exit):
    0xb0daf5a584d192ab5e38940bac38acf672507fa7322f60ef7a6bd59ca6bcf12d
    ```


## Claim costs

Note that claiming rewards is a state-affecting transaction that incurs gas costs. After claiming rewards, the user's auton balance will only increase by _amount of rewards claimed - claim transaction cost_. Fees should not be claimed until the gain outweighs the cost! The gas cost of a claim transaction can be calculated simply as _gas used by transaction * gas price per unit of gas_.


{{% pageinfo %}}
See also the How to [Transfer Liquid Newton](/delegators/transfer-lntn/).{{% /pageinfo %}}
