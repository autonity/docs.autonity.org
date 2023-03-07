---
title: "Governance and Protocol Only Reference"
linkTitle: "Governance and Protocol Only Reference"

description: >
  Autonity Protocol Contract functions callable by governance operator and by protocol only 
---

## Operator only

Functions with the `onlyOperator` access constraint that can only be called by the governance operator account.

###  burn

Burns the specified amount of Newton stake token from an account. When `x` amount of newton is burned, then `x` is simply deducted from the account’s balance and from the total supply of newton in circulation.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_addr ` | `address` | the account address from which newton is being burned |
| `_amount ` | `uint256` | a positive integer value for the value amount being burned, denominated in Newton |

#### Response

No response object is returned on successful execution of the method call.

The new Newton balance of the account can be retrieved from state by calling the [`balanceOf`](/reference/api/aut/#balanceof) method.

The new total supply of Newton in circulation can be retrieved from state by calling the [`totalSupply`](/reference/api/aut/#totalsupply) method.

#### Event

On a successful call the function emits a `BurnedStake` event, logging: `_addr`, `_amount`.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol burn [OPTIONS] AMOUNT ACCOUNT
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.burn(_addr, _amount).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_burn, "params":[_addr, _amount]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol burn 1 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x3e86062cca9fa263acb7076f8287117e9ee2c5570e0f4e4bd2ff4db21895796e
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.burn('0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4',1).send({from: myAddress, gas: gas})
{
  blockHash: '0x11d2d38328b3846c1b7df1a8873475881a4047a328e08716281b6766cd2ce618',
  blockNumber: 6295,
  contractAddress: null,
  cumulativeGasUsed: 36801,
  effectiveGasPrice: 3000000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 36801,
  logsBloom: '0x00004000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0xe7cf2d9a5e29f3eee71206194d65dd474a36984fd373b669f0df47e8ced9c3ed',
  transactionIndex: 0,
  type: '0x2',
  events: {
    BurnedStake: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 6295,
      transactionHash: '0xe7cf2d9a5e29f3eee71206194d65dd474a36984fd373b669f0df47e8ced9c3ed',
      transactionIndex: 0,
      blockHash: '0x11d2d38328b3846c1b7df1a8873475881a4047a328e08716281b6766cd2ce618',
      logIndex: 0,
      removed: false,
      id: 'log_5c08294b',
      returnValues: [Result],
      event: 'BurnedStake',
      signature: '0x5024dbeedf0c06664c9bd7be836915730c955e936972c020683dadf11d5488a3',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->

###  mint

Mints new stake token and adds it to the recipient's account balance. When `x` amount of newton is minted, then `x` is simply added to the account’s balance and to the total supply of newton in circulation.       
        
#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_addr ` | `address` | the recipient account address |
| `_amount ` | `uint256` | a positive integer value for the value amount being minted, denominated in `Newton` |

#### Response

No response object is returned on successful execution of the method call.

The new Newton balance of the recipient account can be retrieved from state by calling the [`balanceOf`](/reference/api/aut/#balanceof) method.

The new total supply of newton in circulation can be retrieved from state by calling the [`totalSupply`](/reference/api/aut/#totalsupply) method.

#### Event

On a successful call the function emits a `MintedStake` event, logging: `_addr`, `_amount`.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol mint [OPTIONS] AMOUNT RECIPIENT
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.mint(_addr, _amount).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_mint", "params":[_addr, _amount]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol mint 1 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xbd9e604372cc922c4594b0fce94919f933734e29b0043c5af3c4a7774ed99ad7
{{< /tab >}}
{{< /tabpane >}}


<!--
{{< tab header="NodeJS Console" >}}
> autonity.mint('0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4',1).send({from: myAddress, gas: gas})
{
  blockHash: '0x1e7f80a9af5cfc370ff2531c3e506c5b24529ea8041f20d1af69f8eee454ecab',
  blockNumber: 4675,
  contractAddress: null,
  cumulativeGasUsed: 36599,
  effectiveGasPrice: 3000000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 36599,
  logsBloom: '0x00004000000000000000000000020000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0xe15f0eb1ca93ea114073dee6850823f07e874771a2feb596f73a7265dec1e3fc',
  transactionIndex: 0,
  type: '0x2',
  events: {
    MintedStake: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 4675,
      transactionHash: '0xe15f0eb1ca93ea114073dee6850823f07e874771a2feb596f73a7265dec1e3fc',
      transactionIndex: 0,
      blockHash: '0x1e7f80a9af5cfc370ff2531c3e506c5b24529ea8041f20d1af69f8eee454ecab',
      logIndex: 0,
      removed: false,
      id: 'log_4e240327',
      returnValues: [Result],
      event: 'MintedStake',
      signature: '0x48490b4407bb949b708ec5f514b4167f08f4969baaf78d53b05028adf369bfcf',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->

###  setCommitteeSize

Sets a new value for the `committeeSize` protocol parameter. 

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_size` | `uint256` | a positive integer value for the maximum committee size |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by calling the [`getMaxCommitteeSize`](/reference/api/aut/#getmaxcommitteesize) method.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-committee-size [OPTIONS] COMMITTEE_SIZE
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.setCommitteeSize(_size).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_setCommitteeSize", "params":[_size]}
{{< /tab >}}
-->
#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol set-committee-size 50 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x3dbe5afbb89267b1549f735d09ac3acd6a4894eccbab8dca125497806c8fdc2d
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.setCommitteeSize(50).send({from: myAddress, gas: gas})
{
  blockHash: '0x56ba4e58d52a3297345c31ad437d44a4dd018f4498ffbf1fee27bf80ee03182b',
  blockNumber: 6379,
  contractAddress: null,
  cumulativeGasUsed: 28941,
  effectiveGasPrice: 3000000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 28941,
  logsBloom: '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0xf14a9ea24e7e27ea4e3453aa87aa0375dabb57743f5fa945e835552b593b6447',
  transactionIndex: 0,
  type: '0x2',
  events: {}
}
{{< /tab >}}
-->

###  setEpochPeriod

Sets a new value for the `epochPeriod` protocol parameter. 

The `epochPeriod` period value must be less than the `unbondingPeriod` protocol parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_period` | `uint256` | a positive integer value specifying the number of blocks defining the duration of an epoch on the network |

#### Response

No response object is returned on successful execution of the call.

The updated parameter can be retrieved from state by a call to the [`epochPeriod`](/reference/api/aut/#epochperiod) public variable.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-epoch-period [OPTIONS] EPOCH_PERIOD
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.setEpochPeriod(_period).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_setEpochPeriod", "params":[_period]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol set-epoch-period 1000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xdf3b3eb316a3070a591621d8cc450ca6d1af3a6d57a0455714b5bff72eb06b92
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.setEpochPeriod(1000).send({from: myAddress, gas: gas})
{
  blockHash: '0x97ae21f4c5622d0542501657a6d1135d71f58411021e0f6a3cb688fe522ebe2d',
  blockNumber: 6705,
  contractAddress: null,
  cumulativeGasUsed: 26108,
  effectiveGasPrice: 3000000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 26108,
  logsBloom: '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0x223f5481d30fffef094fb66e549eb6c9f14dd228cfcd187717b527fcd4cdafcd',
  transactionIndex: 0,
  type: '0x2',
  events: {}
}
{{< /tab >}}
-->
###  setMinimumBaseFee

Sets a new value for the `minBaseFee` protocol parameter. The value is denominated in `attoton`. 

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_price` | `uint256` | a positive integer value for the minimum gas price, denominated in `attoton` |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by calling the [`getMinimumBaseFee`](/reference/api/aut/#getminimumbasefee) method.

#### Event

On a successful call the function emits a `MinimumBaseFeeUpdated` event, logging: `_price`.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-minimum-base-fee [OPTIONS] base-fee
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.setMinimumBaseFee(_price).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_setMinimumBaseFee", "params":[_price]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol set-minimum-base-fee 50000000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x4d1abc6881f63d7856b3b2d6f0b9865a4a9c2b1378dd824e36e9ac194fd8da52
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.setMinimumBaseFee(50000000).send({from: myAddress, gas: gas})
{
  blockHash: '0xb72f0acd971378eb60a011527b412f5f9d5ce096a42c2674b6b670967378ce5e',
  blockNumber: 7247,
  contractAddress: null,
  cumulativeGasUsed: 30100,
  effectiveGasPrice: 2500247492,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 30100,
  logsBloom: '0x00004000000000000000000000020000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000200000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
  status: true,
  to: '0xbd770416a3345f91e4b34576cb804a576fa48eb1',
  transactionHash: '0xe102af7ad981f3e370a84c86669d8d309ab82c955a492d613904bef48a0babe0',
  transactionIndex: 0,
  type: '0x2',
  events: {
    MinimumBaseFeeUpdated: {
      address: '0xBd770416a3345F91E4B34576cb804a576fa48EB1',
      blockNumber: 7247,
      transactionHash: '0xe102af7ad981f3e370a84c86669d8d309ab82c955a492d613904bef48a0babe0',
      transactionIndex: 0,
      blockHash: '0xb72f0acd971378eb60a011527b412f5f9d5ce096a42c2674b6b670967378ce5e',
      logIndex: 0,
      removed: false,
      id: 'log_2f1e2457',
      returnValues: [Result],
      event: 'MinimumBaseFeeUpdated',
      signature: '0x1f4d2fc7529047a5bd96d3229bfea127fd18b7748f13586e097c69fccd389128',
      raw: [Object]
    }
  }
}
{{< /tab >}}
-->
###  setOperatorAccount

Sets a new governance account address as the value of the `operatorAccount` protocol parameter. 

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_account` | `address` | the ethereum formatted  address of the operator governance account |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to the [`operatorAccount`](/reference/api/aut/#operatoraccount) public variable.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-operator-account [OPTIONS] OPERATOR-ADDRESS
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.setOperatorAccount(_account).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_setOperatorAccount", "params":[_account]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol set-operator-account 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xee513f48b4ad4cd24cfc5bb0fe0c1402a5e03ae030b6c73824bae253f56efd51
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.setOperatorAccount('0x11a87b260dd85ff7189d848fd44b28cc8505fa9c').send({from: myAddress, gas: gas})
{{< /tab >}}
-->

###  setTreasuryAccount

Sets a new account address as the value of the `treasuryAccount` protocol parameter. 

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_account` | `address payable` | the ethereum formatted  address of the Autonity Treasury Account for community funds |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to the [`treasuryAccount`](/reference/api/aut/#treasuryaccount) public variable.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-treasury-account [OPTIONS] treasury-address
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.setTreasuryAccount(_account).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_setTreasuryAccount", "params":[_account]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol set-treasury-account 0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0xffe8725f6988668700896f335ecb5db75bb48c9dfb7caef90acecef85d0a2520
{{< /tab >}}

{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.setTreasuryAccount('0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4').send({from: myAddress, gas: gas})
{{< /tab >}}
-->

### setTreasuryFee

Sets a new value for the `treasuryFee` protocol parameter.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_treasuryFee ` | `uint256` | a positive integer value specifying the percentage fee levied on staking rewards before redistribution |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to the [`treasuryFee`](/reference/api/aut/#treasuryfee) public variable.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-treasury-fee [OPTIONS] TREASURY-FEE
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.setTreasuryFee(_treasuryFee).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_setTreasuryFee", "params":[_treasuryFee]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-treasury-fee 100000000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x513f36338720545a8f2c1111e0c2f4b5eebe9582e39493c6cd587ababe1e2e08
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.setTreasuryFee(100000000).send({from:myAddress,gas:gas})
{{< /tab >}}
-->

###  setUnbondingPeriod

Sets a new value for the `unbondingPeriod` protocol parameter. The unbonding period specifies the length of time that bonded stake must wait before it can be redeemed for Newton after processing a stake redeem transaction. The period of time is defined as a number of blocks.

The `unbondingPeriod` period value must be greater than the `epochPeriod` protocol parameter. When the last block of an epoch is finalised, logic checks if the unbonding period for any pending unbonding requests for unbonding has expired and if so applies the staking transitions.

#### Parameters
   
| Field | Datatype | Description |
| --| --| --| 
| `_period` | `uint256` | a positive integer value specifying the number of blocks defining the duration of an unbonding period |

#### Response

No response object is returned on successful execution of the method call.

The updated parameter can be retrieved from state by a call to read the [`unbondingPeriod`](/reference/api/aut/#unbondingperiod) public variable.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
aut protocol set-unbonding-period [OPTIONS] UNBONDING_PERIOD
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
autonity.setUnbondingPeriod(_period)).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_setUnbondingPeriod", "params":[_period]}
{{< /tab >}}
-->

#### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="aut" >}}
$ aut protocol set-unbonding-period 1000 | aut tx sign - | aut tx send -
(consider using 'KEYFILEPWD' env var).
Enter passphrase (or CTRL-d to exit): 
0x1057bf2525ee910b393ea8d54d0ec9b362355e5dbeb14235ed5eba92750a4bdd
{{< /tab >}}
{{< /tabpane >}}

<!--
{{< tab header="NodeJS Console" >}}
> autonity.setUnbondingPeriod(1000).send({from: myAddress, gas: gas})
{{< /tab >}}
-->

<!--
###  upgradeContract

The `upgradeContract` method is used as part of the Autonity Protocol Contract upgrade process. 

The method is called by the governance account (i.e. `operator`) to provide the compiled EVM bytecode and Contract ABI of the new Autonity Protocol Contract. The method appends to the contract storage buffer (i.e. fills with) the new contract bytecode and abi.

The method:

- assigns the argument data to protocol parameters `newContractBytecode` and `newContractAbi`
- sets the `contractUpgradeReady` state variable to `true`. 

The default value of `newContractBytecode` and  `newContractAbi` is `""` and `contractUpgradeReady` is `false` when the Autonity Protocol Contract is deployed. If the `bytecode` is not empty, then a contract upgrade is triggered automatically by protocol. The contract upgrade is then applied at epoch end in the last block's finalisation phase: if `contractUpgradeReady` = `true`, then a `completeContractUpgrade()` method is called by  protocol to update the bytecode of the Autonity Protocol Contract.

The new Autonity Protocol Contract version can be retrieved from state by calling the [`getVersion`](/reference/api/aut/#getversion) method.

See also the function [`getNewContract`](/reference/api/aut/#getnewcontract).
    
#### Parameters

| Field | Datatype | Description |
| --| --| --| 
| `_bytecode` | `bytes` | the EVM bytecode compiled from the new Autonity Protocol Contract's source Solidity. Assigned to protocol parameter `bytecode` |
| `_abi` | `string` | the Application Binary Interface (ABI) of the new Autonity Protocol Contract as a JSON representation. Assigned to protocol parameter `contractAbi`  |

#### Response

The method returns a boolean flag `contractUpgradeReady`, set to `true` if an Autonity Protocol Contract upgrade is available.


#### Event

None.

#### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
autonity.upgradeContract(_bytecode, _abi).send()
{{< /tab >}}
{{< tab header="RPC" >}}
{"method": "aut_upgradeContract", "params":[_bytecode, _abi, _version]}
{{< /tab >}}
{{< /tabpane >}}
-->

## Protocol only

Functions with the `onlyProtocol` access constraint can only be invoked by the Autonity protocol itself.

###  computeCommittee

Selects the consensus committee for the following epoch by selecting the validators with the highest amount of bonded stake.

The algorithm reads from the `validatorList`  state variable to select the set of registered validators that are in an `enabled` state and with bonded stake greater than `0`. 

If the number of selected validators exceeds the maximum committee size, then the selected validators are sorted by bonded stake amount in ascending order. The top `N` where `N` is the maximum committee size, are then selected to be members of the consensus committee for the next epoch.

The consensus committee variables maintained in persistent storage are deleted and recreated:

- `committee` is assigned the array of new `CommitteeMember`'s, each `CommitteeMember` struct recording the validator's account address (`_addr`) and bonded stake amount (`votingPower`)
- `committeeNodes` is assigned the array of enode URL's for the committee members
- `epochTotalBondedStake` is assigned the total amount of the stake bonded to the committee members.

Constraint checks:

- `validatorList.length > 0`. A committee cannot be selected without registered validators.
- `ValidatorState.enabled`. Validators must have a state of enabled to be included in the selection algorithm.
- `bondedStake > 0`. Validators must have a non-zero amount of bonded stake to be included in the selection algorithm.

#### Parameters

None.

#### Response

No response object is returned on successful execution of the method invocation.

The new committee can be retrieved from state by calling the [`getCommittee`](/reference/api/aut/#getcommittee) method.

The new committee enode URL's can be retrieved from state by calling the [`getCommitteeEnodes `](/reference/api/aut/#getcommitteeenodes) method.

Returns the amount of stake token bonded to the new consensus committee members and securing the network during the epoch can be retrieved from state by a call to the [`epochTotalBondedStake`](/reference/api/aut/#epochtotalbondedstake) public variable.

###  finalize

The block finalization function, invoked each block after processing every transaction within it. The function:

- tests if the `bytecode` protocol parameter is `0` length to determine if an Autonity Protocol Contract upgrade is available. If the `bytecode` length is `>0`, the `contractUpgradeReady` protocol parameter is set to `true`
- adds the `amount` parameter value to the `epochReward` protocol parameter
- checks if the block number is the last epoch block number and if so, then:
    - performs the staking rewards redistribution, redistributing the available reward amount per protocol and emitting a `Rewarded` event for each distribution
    - sets `epochReward` to `0`
    - applies any staking transitions - pending bonding and unbonding requests tracked in `Staking` darta structures in memory
    - selects the consensus committee for the following epoch, invoking the [`computeCommittee`](/reference/api/aut/op-prot/#computecommittee) function
    - assigns the `lastEpochBlock` state variable the value of the current block number.

#### Parameters

| Field | Datatype | Description |
| --| --| --| 
| `amount` | `uint256` | the amount of transaction fees collected for the block |

#### Response

| Field | Datatype | Description |
| --| --| --| 
| `contractUpgradeReady` | `bool` | Set to `true` if an Autonity Protocol Contract upgrade is available |
| `committee`| `CommitteeMember[]` array | the consensus committee that approved the block, each `CommitteeMember` struct recording the validator's account address (`_addr`) and bonded stake amount (`votingPower`)|

{{% alert title="Note" %}}If a contract upgrade is available, this is executed by the protocol at epoch finalisation. After an upgrade has been completed the new Autonity Protocol Contract version can be retrieved from state by calling the [`getVersion`](/reference/api/aut/#getversion) method.{{% /alert %}}

#### Event

On successful reward distribution the function emits a `Rewarded` event for each staking reward distribution, logging: recipient address `addr` and reward amount `amount`.
