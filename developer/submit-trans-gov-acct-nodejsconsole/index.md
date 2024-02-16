---
title: "Submit governance transaction from Autonity NodeJS Console"
description: >
  How to call operator only functions as the governance account using the NodeJS interface to the RPC API's
draft: true
---

::: {.callout-note title="Info" collapse="false"}
Governance functions are only callable from the governance operator account of an Autonity network. See the Autonity Interfaces Reference section [Operator only](/reference/api/aut/op-prot/#operator-only) for the listing of governance API methods.
:::

## Prerequisites

To submit transactions restricted to the governance account from the Autonity NodeJS Console you need:

- an [installed NodeJS Console](/node-operators/install-aut/)
- the governance account is funded with auton to pay for transaction gas costs
- configuration details for the local Autonity network you are connecting your console to
- to provide the following constants:

  - the private key of the governance account (to unlock the account in the JavaScript environment)
  - gas (the amount of gas you are providing for the transaction)
  - gas price (the amount of gas you are willing to pay for computing the transaction)


## Setup

1. Navigate to your Autonity NodeJS Console install directory  and initialise a console session, specifying the IP address of the node you will connect to. The connection is made over WebSockets to port 8546:

    ```bash
    ./console ws://<IP-ADDRESS>:8546
    ```

::: {.callout-note title="Note" collapse="false"}
If the transport is over WebSockets or WebSockets Secure will depend on your local network setup. If the node you are connecting to is public, then WebSockets Secure (`wss`) is advised.
:::

2. Unlock the governance account private key in the NodeJS Console. Enter the following in the NodeJS Console, specifying the private key of the governance account:

    ```javascript
    const privatekey = '<PRIVATE_KEY>';
    const account = web3.eth.accounts.wallet.add(privatekey);
    const governanceAccount = web3.utils.toChecksumAddress(account.address);
    const gas = 10000000;
    ```

    You are now configured to submit transactions to your local Autonity network from the governance account. Transactions must be appended with `.send({from: governanceAccount, gas: gas})`

    When a transaction is successful, you will receive a transaction receipt.


## Examples

Here are some examples of calling Autonity Protocol Contract governance functionality.

For a listing of all operator only functions and the parameter definitions see the Autonity Interfaces Reference [Operator only](/reference/api/aut/op-prot/#operator-only) section.

### Mint Newton stake token:
    
Call the Autonity contract to mint Newton stake token to a recipient account, specifying the recipient account address and the amount of token to be minted:

```bash
autonity.mint('<_addr>', <_amount>).send({from: governanceOperator, gas: gas})
```

On success a `MintedStake` event is emitted and you will receive a transaction receipt resembling this:

```javascript
    { blockHash:
    '0xa62ea814027d4e244859fa804e0b26ae3034ff829ec35fcbfa7a7bd31682e1d2',
    blockNumber: 2729631,
    contractAddress: null,
    cumulativeGasUsed: 36892,
    from: '0x2f3bce2d6c2602de594d9a6662f0b93416cfb4d7',
    gasUsed: 36892,
    logsBloom:
    '0x00004000000000000000000000020000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    status: true,
    to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
    transactionHash:
    '0x105d5470c48ce77f6375b3282e0fde78b4d30a23c429861651fca03d277d0422',
    transactionIndex: 0,
    events:
    { MintedStake:
        { address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
            blockNumber: 2729631,
            transactionHash:
            '0x105d5470c48ce77f6375b3282e0fde78b4d30a23c429861651fca03d277d0422',
            transactionIndex: 0,
            blockHash:
            '0xa62ea814027d4e244859fa804e0b26ae3034ff829ec35fcbfa7a7bd31682e1d2',
            logIndex: 0,
            removed: false,
            id: 'log_5ae937eb',
            returnValues: [Result],
            event: 'MintedStake',
            signature:
            '0x48490b4407bb949b708ec5f514b4167f08f4969baaf78d53b05028adf369bfcf',
            raw: [Object] } } }
```

You can confirm the Newton has been successfully minted by checking the balance of the recipient account has been augmented by the minted amount, and by checking the total supply of Newton in circulation:

```bash
autonity.balanceOf('<_addr>').call()
    
autonity.totalSupply().call()
```

### Burn Newton stake token:
    
Specify the account address from which Newton stake token is to be burnt and the amount of token to be burnt from that account:

```bash
autonity.burn('<_addr>', <_amount>).send({from: governanceOperator, gas: gas})
```

On success a `BurnedStake` event is emitted and you will receive a transaction receipt resembling this:

```javascript
{ blockHash:
   '0x78580bcbcbf6f65402a6db11e1ec28eadf3b7c03d019549739b439df7cc9607f',
  blockNumber: 1094785,
  contractAddress: null,
  cumulativeGasUsed: 37773,
  from: '0x2f3bce2d6c2602de594d9a6662f0b93416cfb4d7',
  gasUsed: 37773,
  logsBloom:
   '0x00004000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash:
   '0xf1326cb488fa8cd337852b5e1ad70e5fad08929488666ac1d37c5c81099527c1',
  transactionIndex: 0,
  events:
   { BurnedStake:
      { address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
        blockNumber: 1094785,
        transactionHash:
         '0xf1326cb488fa8cd337852b5e1ad70e5fad08929488666ac1d37c5c81099527c1',
        transactionIndex: 0,
        blockHash:
         '0x78580bcbcbf6f65402a6db11e1ec28eadf3b7c03d019549739b439df7cc9607f',
        logIndex: 0,
        removed: false,
        id: 'log_b67b42e4',
        returnValues: [Result],
        event: 'BurnedStake',
        signature:
         '0x5024dbeedf0c06664c9bd7be836915730c955e936972c020683dadf11d5488a3',
        raw: [Object] } } }
```


### Set minimum base fee:
    
Specify the new minimum base fee as an integer denominated in `Auton`:

```bash
autonity.setMinimumBaseFee(_price).send({from: governanceOperator, gas: gas})
```

On success a `MinimumBaseFeeUpdated` event is emitted and you will receive a transaction receipt resembling this:

```javascript
{ blockHash:
   '0x31ff42b44dd8acc78251cd9e1aecdd145e949ce5edc288585232b237a7c6a510',
  blockNumber: 1095787,
  contractAddress: null,
  cumulativeGasUsed: 28764,
  from: '0x2f3bce2d6c2602de594d9a6662f0b93416cfb4d7',
  gasUsed: 28764,
  logsBloom:
   '0x00004000000000000000000000020000000400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000008000000000000000000000008000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash:
   '0xb18e41fa0b043964f32414a1dd04cbd98d19b9705f473ef4ec36cc8dabbce363',
  transactionIndex: 0,
  events:
   { MinimumBaseFeeUpdated:
      { address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
        blockNumber: 1095787,
        transactionHash:
         '0xb18e41fa0b043964f32414a1dd04cbd98d19b9705f473ef4ec36cc8dabbce363',
        transactionIndex: 0,
        blockHash:
         '0x31ff42b44dd8acc78251cd9e1aecdd145e949ce5edc288585232b237a7c6a510',
        logIndex: 0,
        removed: false,
        id: 'log_3c960360',
        returnValues: [Result],
        event: 'MinimumBaseFeeUpdated',
        signature:
         '0x58841da31675d02939f5efa0add356e7af0a24703fe398e1eba9ea4ea4db253a',
        raw: [Object] } } }
```

You can view the updated value has been updated by a call to return the protocol parameter, returning the variable's value. For example:

```bash
> autonity.getMinimumBaseFee().call()
'5000000'
```
