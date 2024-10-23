---
title: "Transfer Liquid Newton"
description: >
  How to view your Liquid Newton holding and send Liquid Newton to another account using `aut`
---

## Prerequisites

To send Liquid Newton (LNTN) to another account you need:

- A running instance of `aut` for submitting transactions from your account configured as described in [Submit a transaction with Autonity CLI](/account-holders/submit-trans-aut/).
- An [account](/account-holders/create-acct/) [funded](/account-holders/fund-acct/) with auton to pay for transaction gas costs, and a Liquid Newton stake token balance >= to the amount being transferred.
- You have already [bonded stake](/delegators/bond-stake/) to one or more validators and so have Liquid Newton token balance(s).


## Get Liquid Newton holdings

Before transferring LNTN, verify your liquid newton holdings and the liquid newton contract address of the validator-specific stake delegation you are transferring LNTN from.

1. To return a listing of your current LNTN holdings for all of your stake delegations, use the `account` command `lntn-balances` to call:

	```bash
    aut account lntn-balances
    ```

	It will return an array of the liquid newton holdings for your account.
	
	You should see something like beneath. In this example, the calling account has staked a single validator whose identifier address `0xA9F070101236476fe077F4A058C0C22E81b8A6C9 ` and has a liquid newton holding of `9901`:
    
    ```bash
    aut account lntn-balances
    {
    	"0xA9F070101236476fe077F4A058C0C22E81b8A6C9": 9901
    }
    ```

2. To return the liquid newton contract address of a validator, use the `validator` command `info` to submit a call to query for validator metadata. Specify:
	- `<VALIDATOR_IDENTIFIER_ADDRESS>`: the validator identifier address of the validator you are querying for.

	It will return the validator metadata from system state, including the liquid newton contract address:

	```bash
    aut validator info --validator <VALIDATOR_IDENTIFIER_ADDRESS>
    ```

    You should see something like beneath. In this example, the liquid newton contract address is `0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37`:
    
    ```bash
    aut validator info --validator 0xA9F070101236476fe077F4A058C0C22E81b8A6C9
    {
    	"treasury": "0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C",
    	"addr": "0xA9F070101236476fe077F4A058C0C22E81b8A6C9",
    	"enode": "enode://11e025123dc489f30c26f2f46cef177de2c72d07c3b0f6aa948a2575e2b4be362b8098c14ec4720e4e46daceb390caeb1ad273f3adbfca8c4150e58c0c71f24b@51.89.151.55:30303",
    	"commission_rate": 1000,
    	"bonded_stake": 9901,
    	"total_slashed": 0,
    	"liquid_contract": "0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37",
    	"liquid_supply": 9901,
    	"registration_block": 0,
    	"state": 0
    }
    ```

## Transfer Liquid Newton to another account

3. To transfer an amount of LNTN to another account, use the `tx` command `make`, passing in as arguments:

- `--to`: `<RECIPIENT_ACCOUNT_ADDRESS>`the recipient account address.
- `--token`: `<LIQUID_CONTRACT>` the liquid newton contract address of the validator-specific stake delegation you are transferring LNTN from; returned from Step 2 above in the `liquid_contract` property.
- `--value`: `<AMOUNT>` the amount of LNTN you are transferring to the `to` account.

    ```bash
    aut tx make --to <RECIPIENT_ACCOUNT_ADDRESS> --token <LIQUID_CONTRACT> --value <AMOUNT> | aut tx sign - | aut tx send -
    ```
    
    You will be prompted for your passphrase for the key file. Having entered the password, the transaction hash will be returned on success.
    
    You should see something like beneath. In this example, the liquid newton holder transfers `111` LNTN from their account validator liquid newton contract address `0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37` to the recipient address `0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4`. The returned hash is `0x0aee45...29c67725`:
    
    ```bash
    aut tx make --to 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 --token 0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37 --value 111 | aut tx sign - | aut tx send -
    (consider using 'KEYFILEPWD' env var).
    Enter passphrase (or CTRL-d to exit): 
    0x0aee457755874ff776e36ec2d76955fcd4856d6753d5e75e1ba125d029c67725
    ```

::: {.callout-note title="Note" collapse="false"}
The Liquid Newton contract is ERC20 so you can also transfer LNTN using the ERC20 `transfer` command in the `token` command group.
:::

If using `transfer`, pass in as arguments:

- `--token`: `<LIQUID_CONTRACT>` the liquid newton contract address of the validator-specific stake delegation you are transferring LNTN from; returned from Step 2 above in the `liquid_contract` property.
- `RECIPIENT`: the recipient account address.
- `AMOUNT`: `<AMOUNT>` the amount of LNTN you are transferring to the `to` account. The `AMOUNT` is specified in decimal notation if fractional.

    ```bash
    aut token transfer --token <LIQUID_CONTRACT>  <RECIPIENT_ACCOUNT_ADDRESS> <AMOUNT>  | aut tx sign - | aut tx send -
    ```
