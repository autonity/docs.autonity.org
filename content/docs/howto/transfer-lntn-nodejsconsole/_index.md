---
title: "Transfer Liquid Newton using NodeJS Console"
linkTitle: "Transfer Liquid Newton using NodeJS Console"
weight: 110
description: >
  How to view your Liquid Newton holding and send Liquid Newton to another account using Autonity NodeJS Console
draft: true
---

## Prerequisites

To send Liquid Newton (LNTN) to another account using the Autonity NodeJS Console you need:

- a running instance of the Autonity NodeJS Console configured for submitting transactions from your _Staking Wallet_ account, as described in [Claim Staking Rewards](/howto/claim-rewards/).

## View your Liquid Newton holdings

1. To return a listing of your current LNTN holdings for all of your stake delegations:

   Call the console function [`wal()` _Print Staking Wallet_](/reference/api/liquid-newton/#wal-_print-staking-wallet_), passing in the address of your _Staking Wallet_ account as argument:

    ```bash
    wal(account)
    ```
    
    This will return an index-sorted list of all the stake delegations from your account (i.e. your _Staking Wallet'), showing:
    
    - `Account`: your _Staking Wallet_ account address.
    - `(index)`: the validator index, i.e. if the 1st or nth validator registered in the network.
    - `validator`: the unique [validator identifier](/autonity/validator/#validator-identifier).
    - `lntn`: the amount of Liquid Newton the staker owns for that validator.
    - `claimableRewards`: the amount of rewards the staker can claim from the stake delegation, denominated in [attoton](/glossary/#attoton), Auton's wei equivalent.
    
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


## Transfer Liquid Newton to another account

1. To transfer an amount of LNTN to another account, call the console function [`lsend()` _Send Liquid Newton_](/reference/api/liquid-newton/#lsend-_send-liquid-newton_), passing in as arguments:

- `from`: your _Staking Wallet_ account address.
- `to`: the recipient account address.
- `val`: the validator identifier for the validator-specific stake delegation you are transferring LNTN from.
- `value`: the amount of LNTN you are transferring to the `to` account.

    ```bash
    lsend({from, to, val, value})
    ```
    
    On successful processing, the function will return a transaction receipt and event. You should see something like beneath:
    
    ```bash
    > lsend({from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c', to: '0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4', val: '0x45998C7d6341CD32256E9eeEdd9865450d4aCB18', value: 100})
	Sending 100 LNTN - Validator 0x45998C7d6341CD32256E9eeEdd9865450d4aCB18
	{
  		blockHash: 		'0x87fec89e8c91784a12ecf9f21941d58c2c9a7b32cc5b446d52c833e6fef632d1',
  		blockNumber: 34331,
  		contractAddress: null,
  		cumulativeGasUsed: 63512,
  		effectiveGasPrice: 12500000000,
  		from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  		gasUsed: 63512,
  		logsBloom: 		'0x00000000000000000000000000000400000000010000000000000000000000000000000000000000000000000000000004000000000000000000000001000000000000000000000000040008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000002000000000000000000000000000000000000000000000002000000000000000000000000000000000000000080000000000000000000001000000000',
  		status: true,
  		to: '0x109f93893af4c4b0afc7a9e97b59991260f98313',
  		transactionHash: '0xaea4f62e5a5ed703bf084c78a4eca65d125a078045c5076c76fc8c3226cc4340',
  		transactionIndex: 0,
  		type: '0x2',
  		events: {
    		Transfer: {
     		 	address: '0x109F93893aF4C4b0afC7A9e97B59991260F98313',
      			blockNumber: 34331,
      			transactionHash: '0xaea4f62e5a5ed703bf084c78a4eca65d125a078045c5076c76fc8c3226cc4340',
      			transactionIndex: 0,
      			blockHash: '0x87fec89e8c91784a12ecf9f21941d58c2c9a7b32cc5b446d52c833e6fef632d1',
      			logIndex: 0,
      			removed: false,
      			id: 'log_af2225aa',
      			returnValues: [Result],
      			event: 'Transfer',
      			signature: '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
      			raw: [Object]
    		}
  		}
	}
    ```
    
    Calling `wal()` again will show the LNTN holding for the stake delegation has reduced by the sent amount:
    
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
