---
title: "Liquid Newton Contract Interface"
linkTitle: "Liquid Newton Contract Interface"

description: >
  Autonity Liquid Newton Contract functions
---

The LiquidNewton contract is deployed by the Autonity contract in response to validator registration.  It implements the Liquid Newton token for that validator, and handles the distribution of staking rewards to all delegators.

The address of the Liquid Newton contract for a given validator can be determined by the information returned from the Autonity contract [`getValidator`](/reference/api/aut/#getvalidator) method (see [here](/delegators/transfer-lntn/) for details of how to query this using the Autonity Utility Tool `aut`).

Liquid Newton tokens implement the ERC20 interface, and so all ERC20 calls are implemented.  The following public methods are also available for handling the reward distribution.

{{% pageinfo %}}
Autonity implements a 'pull-based' model for staking rewards where delegators must manually retrieve their rewards.
{{% /pageinfo %}}

## unclaimedRewards

Queries the contract and returns the total rewards owed to the a given account.

This function is used by the `aut validator unclaimed-rewards` command of [`aut`](/account-holders/setup-autcli/).  Further details are given in the ["Claiming staking rewards"](/delegators/claim-rewards/#get-reward-balance) section.

## claimRewards

Computes the total rewards owed to the caller, and sends the appropriate amount of auton.

The `aut validator claim-rewards` command uses this function.  Usage details and examples are given in the ["Claiming staking rewards"](/delegators/claim-rewards/#claim-rewards) section.
