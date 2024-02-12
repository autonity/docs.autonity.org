---
title: "Claim Staking Rewards using NodeJS Console"
description: >
  How to view and claim available staking rewards using Autonity NodeJS Console
draft: true
---

## Prerequisites

To claim fees using the Autonity NodeJS Console you need:

- an account on an Autonity network funded with auton to pay for transaction gas costs
- this account has been used to bond stake to a validator: this account is your _Staking Wallet_ account
- a running instance of the Autonity NodeJS Console as described in [Submit a transaction from Autonity NodeJS Console](/account-holders/submit-trans-nodejsconsole/). The console has been configured for submitting transactions from your _Staking Wallet_ account

## Get claimable reward balance

1. To return the current balance of your claimable rewards for all of your stake delegations:

   Call the console function [`wal()` _Print Staking Wallet_](/reference/api/liquid-newton/#wal-_print-staking-wallet_), passing in the address of your _Staking Wallet_ account as argument:

    ```bash
    wal(account)
    ```

    This will return an index-sorted list of all the stake delegations from your account (i.e. your _Staking Wallet'), showing:

    - `Account`: your _staking Wallet_ account address
    - `(index)`: the validator index, i.e. if the 1st or nth validator registered in the network
    - `validator`: the unique [validator identifier](/concepts/validator/#validator-identifier)
    - `lntn`: the amount of Liquid Newton the staker owns for that validator
    - `claimableRewards`: the amount of rewards the staker can claim from the stake delegation, denominated in [ton](/glossary/#ton), Auton's wei equivalent.

    You should see something like beneath. In this example, truncated to show the first 4 validators returned, the sender has bonded stake to 2 separate validators:

    ```bash

    > wal('0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C')

    __________________________Staking Wallet__________________________

    Account:       0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C

	________________________________________________________________________________________
	| (index) │                 validator                    │   lntn  │  claimableRewards  |
	|---------|----------------------------------------------|---------|--------------------|
	|    0    │ '0x07d872935972Aa0848d0cec9c67b270E5291D7e8' │ '10000' │ '1436124008436346' │
	│    1    │ '0x45998C7d6341CD32256E9eeEdd9865450d4aCB18' │  '150'  │ '29094266920200'   │
	│    2    │ '0xe32d53E4d077F7ADE8CDB6Ff3Cf857Be40Ab1516' │   '0'   │        '0'         │
	│    3    │ '0xAbbA1C48341755558E85A01e293Db94179dF9bcd' │   '0'   │        '0'         │

    ```



## Claim staking rewards

Rewards can be claimed individually or collectively.

### Claim rewards for a specific stake delegation

1. To claim rewards from a specific validator, call the console function [`rclm()` _Claim staking rewards_](/reference/api/liquid-newton/#rclm-_claim-staking-rewards_), passing in your _Staking Wallet_ account address and the validator identifier as arguments:

    ```bash
    rclm(account,validator)
    ```

    This will return the validator and staker addresses, the amount of claimable rewards from that valdiator, and the transaction receipt.  You should see something like beneath:

    ```bash
    > rclm('0x11a87b260dd85ff7189d848fd44b28cc8505fa9c','0x07d872935972Aa0848d0cec9c67b270E5291D7e8')
    validator:      0x07d872935972Aa0848d0cec9c67b270E5291D7e8
    staker:         0x11a87b260dd85ff7189d848fd44b28cc8505fa9c
    claimable rewards: 1436124008436346
	{
  		blockHash: '0xb99026335707e71d8663f5918386f7b8039ae706ec1e104e3a601080191747ff',
  		blockNumber: 33594,
  		contractAddress: null,
  		cumulativeGasUsed: 49156,
  		effectiveGasPrice: 12500000000,
  		from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  		gasUsed: 49156,
  		logsBloom: 		'0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  		status: true,
  		to: '0xf4d9599afd90b5038b18e3b551bc21a97ed21c37',
  		transactionHash: '0x6abe00db9b3beef9c40fe0b03e0f64dc6370c4b282f9136468b1259a1f6c77e8',
  		transactionIndex: 0,
  		type: '0x2',
  		events: {}
	}

    ```

    Calling `wal()` again will show rewards from the validator are claimed:

    ```bash

    > wal('0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C')

    __________________________Staking Wallet__________________________

    Account:       0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C

	________________________________________________________________________________________
	| (index) │                 validator                    │   lntn  │  claimableRewards  |
	|---------|----------------------------------------------|---------|--------------------|
	|    0    │ '0x07d872935972Aa0848d0cec9c67b270E5291D7e8' │ '10000' │        '0'         │
	│    1    │ '0x45998C7d6341CD32256E9eeEdd9865450d4aCB18' │  '150'  │ '29094266920200'   │
	│    2    │ '0xe32d53E4d077F7ADE8CDB6Ff3Cf857Be40Ab1516' │   '0'   │        '0'         │
	│    3    │ '0xAbbA1C48341755558E85A01e293Db94179dF9bcd' │   '0'   │        '0'         │

    ```


### Claim rewards for all stake delegations

1. To claim rewards from all validators, call the console function [`rclm_a()` _Claim all staking rewards_](/reference/api/liquid-newton/#rclm_a-_claim-all-staking-rewards_), passing in your _Staking Wallet_ account address as argument:

    ```bash
    rclm_a(account)
    ```

    This will return a listing of each validator you have delegated to, your claimable reward for each validator stake delegation, and the total amount of rewards claimed.  You should see something like beneath:

    ```bash
    > rclm_a(myAddress)
    validator:          0x07d872935972Aa0848d0cec9c67b270E5291D7e8
    claimable reward:   213928433236770

    validator:          0x45998C7d6341CD32256E9eeEdd9865450d4aCB18
    claimable reward:   29094266920200


    total claimed:        243022700156970

    ```

    Calling `wal()` again will show rewards are claimed:

    ```bash

    > wal('0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C')

    __________________________Staking Wallet__________________________

    Account:       0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C

	________________________________________________________________________________________
	| (index) │                 validator                    │   lntn  │  claimableRewards  |
	|---------|----------------------------------------------|---------|--------------------|
	|    0    │ '0x07d872935972Aa0848d0cec9c67b270E5291D7e8' │ '10000' │        '0'         │
	│    1    │ '0x45998C7d6341CD32256E9eeEdd9865450d4aCB18' │  '150'  │        '0'         │
	│    2    │ '0xe32d53E4d077F7ADE8CDB6Ff3Cf857Be40Ab1516' │   '0'   │        '0'         │
	│    3    │ '0xAbbA1C48341755558E85A01e293Db94179dF9bcd' │   '0'   │        '0'         │

    ```


### Claim costs

Note that claiming rewards is a state-affecting transaction that incurs gas costs. After claiming rewards, the user's Auton balance will only increase by _amount of rewards claimed - claim transaction cost_. Fees should not be claimed until the gain outweighs the cost! The gas cost of a claim transaction can be calculated simply as _gas used by transaction * gas price per unit of gas_.


{{% pageinfo %}}
See the Reference Node JS Console Staking management functions reference

and the How to [Transfer Liquid Newton](/delegators/transfer-lntn/)

{{% /pageinfo %}}
