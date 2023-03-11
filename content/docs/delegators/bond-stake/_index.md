---
title: "Bond and unbond stake"
linkTitle: "Bond and unbond stake"
weight: 80
description: >
  How to bond and unbond stake to validators in an Autonity network
---

See the [staking section](/concepts/staking/) to understand the concepts behind bonding and unbonding.

## Prerequisites

- A running instance of [`aut`](https://github.com/autonity/aut) configured to [submit a transaction from your account](/account-holders/submit-trans-aut/).
- An [account](/account-holders/create-acct/) that has been [funded](/account-holders/fund-acct/) with auton to pay for transaction gas costs.
- A Newton stake token balance >= to the amount being bonded.

## Discover registered validators

The `validator` command is used for operations that interact with validators.

The current set of registered validators in the Autonity network can be queried using the `list` subcommand:

```bash
aut validator list
```
```bash
0x32F3493Ef14c28419a98Ff20dE8A033cf9e6aB97
0x31870f96212787D181B3B2771F58AF2BeD0019Aa
0x6EBb5A45728be7Cd9fE9c007aDD1e8b3DaFF6B3B
0xb3A3808c698d82790Ac52a42C05E4BCb3dfCd3db
0x467D99EA9DACC495E6D1174b8f3Dd20DDd531335
0x1114fE559b302403BB3a89806bC08F7fA5299E99
0x9fd408Bdb83Be1c8504Ff13eBcCe7f490DCCC2cF
0xE03D1DE3A2Fb5FEc85041655F218f18c9d4dac55
0x52b89AFA0D1dEe274bb5e4395eE102AaFbF372EA
```

Details about a specific validator can be queried with the `info` subcommand:

```bash
aut validator info --validator 0x9fd408Bdb83Be1c8504Ff13eBcCe7f490DCCC2cF
{
  "treasury": "0x040803C4767A28A65e0cc15E4626DF1f7977109c",
  "addr": "0x9fd408Bdb83Be1c8504Ff13eBcCe7f490DCCC2cF",
  "enode": "enode://ad9972b7b23ecfc229323cd243f50c3caf980f5825a6765b102d9e28be2a760b7fd3045790246d1a5836af9a8ea5d2dbcc9b56864f6391504ab376d91d99b13e@77.68.90.188:30303",
  "commission_rate": 1000,
  "bonded_stake": 95,
  "total_slashed": 0,
  "liquid_contract": "0x7A4C3b88B944fA2702F19625e9A38107FcbE1db8",
  "liquid_supply": 95,
  "registration_block": 5657271,
  "state": 0
}
```

{{< alert name="Note" >}}
If you interact with a specific validator very frequently, you might consider making it the default by adding an entry such as

```
validator=0x9fd408Bdb83Be1c8504Ff13eBcCe7f490DCCC2cF
```

to your `.autrc` file.
{{< /alert >}}

{{% pageinfo %}}
As described in [Committee member selection](/concepts/consensus/committee/#committee-member-selection) the set of validators in the consensus committee is changed at every block epoch. [Voting power changes](/concepts/consensus/committee/#voting-power-changes) caused by bonding and unbonding stake to a validator are applied at the end of an epoch before the committee selection algorithm for the next epoch's committee is run.

To get the validators in the current consensus committee use the `protocol` command `get-committee` to call:

```bash
aut protocol get-committee
```
{{% /pageinfo %}}


## Bond Newton to validator

The `aut validator bond` command creates a transaction that bonds the caller's newton to a specific validator.

```bash
aut validator bond --validator <VALIDATOR_IDENTIFIER_ADDRESS> <AMOUNT> | aut tx sign - | aut tx send -
```

{{< alert name="Note" >}}
Bonding requests are not processed until the end of the current epoch.  The newton to be bonded will be deducted from your balance, but your [liquid newton balance](/delegators/transfer-lntn) will not be affected until the epoch

(Pending and historical bonding requests can be queried using the [getBondingReq](/reference/api/) api call or the `aut protocol get-bonding-req` command)
{{< /alert >}}

## Unbond Newton from validator

The `aut validator unbond` command creates a transaction that unbonds the caller's newton from a specific validator.

```bash
aut validator unbond --validator <VALIDATOR_IDENTIFIER_ADDRESS> <AMOUNT> | aut tx sign - | aut tx send -
```

{{< alert name="Note" >}}
Like bonding requests, unbonding does not complete immediately.  After an unbonding period, the Newton will be returned to the caller.  See the [staking section](/concepts/staking/) for further details.
{{< /alert >}}
