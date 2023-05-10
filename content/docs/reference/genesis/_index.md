
---
title: "Genesis"
linkTitle: "Genesis"

description: >
  Setting genesis configuration for an Autonity Go Client
---

Genesis configuration for public Autonity networks is built into the client's configuration. If setting up a local testnet, for example a private devnet, configuration has to be specified when initialising the node.

## Public Autonity Network configuration
Configuring the client to join a public network is done by setting the network as a [command-line option](/reference/cli/#command-line-options) when initialising the Autonity Go Client. The client will then auto-detect the network genesis configuration and bootnodes, connect, and sync.

### Public network flags

|Network|Command-line option|Network settings|
|-------|-------------------|----------------|
|Bakerloo Testnet| [`--bakerloo` command-line option](/reference/cli/#command-line-options)| [Genesis configuration](/networks/testnet-bakerloo/#genesis-configuration) |
|Piccadilly Testnet| [`--piccadilly` command-line option](/reference/cli/#command-line-options) | [Genesis configuration](/networks/testnet-piccadilly/#genesis-configuration) |


For details of individual public network purpose and use see the [Networks](/networks/) section.

## Local Autonity Network configuration
For launching a local Autonity network, genesis configuration and bootnodes need to be specified when running the client:

- Genesis configuration file. To set genesis state of your local Autonity network you will need to provide your own custom `genesis.json` configuration file, a JSON formatted file containing the initialisation configuration for the network. This file defines:
  - the genesis block and that block's header
  - protocol parameters configuring protocol rules of the network
  - validators from which the genesis consensus committee will be selected
  - oracle network configuration
  - accounts to be created at network genesis: initial allocation of Auton to EOA accounts; contract accounts.
- Bootnodes. Bootnodes can be provided statically as a file or as a command-line option when running the client.  To provide statically, specify a `static-nodes.json` file, or as a comma-separated list in the `--bootnodes` command-line option.


### Genesis configuration file

| Parameter | Description | Value |
|-----------|-------------|-------|
| `config` | Configuration variables for the Autonity Network blockchain | See [`config` object](#config-object) |
| `nonce` | Maintained by the Autonity Protocol for backward compatibility reasons in the EVM. | Set to `0` (`0x0` in hexadecimal) |
| `timestamp` | Specifies the time point when the network starts mining and the first block is mined. If set to `0` the node will start mining on deployment. If a future time point is specified, then miners will wait until `timestamp` + `blockPeriod` to begin mining. The local node consensus engine will start when its local Unix clock reaches the timestamp value. The Validator node operator must keep their local node in sync, i.e. by the [Network Time Protocol (NTP) <i class='fas fa-external-link-alt'></i>](https://www.nwtime.org/documentationandlinks/) | Set to `0` (`0x0`) to start node mining on connection to the Autonity network |
| `baseFee` | The base gas price for computing a transaction on an Autonity network after genesis. The base fee is adjusted per the [EIP 1559 <i class='fas fa-external-link-alt'></i>](https://eips.ethereum.org/EIPS/eip-1559) fee market mechanism. See Concepts, [EIP 1559 Transaction fee mechanism (TFM)](/concepts/system-model/#eip-1559-transaction-fee-mechanism-tfm)| Set to: `15000000000` |
| `gasLimit` | The maximum amount of gas expenditure allowed for a block, placing a ceiling on transaction computations possible within a block. Denominated in `attoton`. The gas limit determines the amount of gas allowed to compute the genesis block; for subsequent blocks the gas limit is algorithmically adjusted by protocol | Set to: `30000000` |
| `difficulty` | Derived from Ethereum where it sets the difficulty for Ethereum's Ethash Proof of Work consensus. For Autonity's implementation of Tendermint BFT Proof of Stake consensus this must be assigned `0`. | Set to `0` (`0x0`) |
| `coinbase` | Maintained for backward compatibility reasons in the EVM. Unused by the Autonity Protocol. Ethereum format address. | Set to `0x0000000000000000000000000000000000000000` |
| `number ` | A value equal to the number of ancestor blocks. At genesis there are no ancestor blocks and it is assigned the value `0` | Set to `0` (`0x0`) |
| `gasUsed` | The gas used in the computation of the block. At genesis this is assigned the value `0` | Set to `0` (`0x0`) |
| `parentHash` | A Keccak 256-bit hash of the parent block header. At genesis there is no parent block and this is assigned a zero value. | Set to `0x0000000000000000000000000000000000000000000000000000000000000000` |
| `mixHash` | Maintained by the Autonity Protocol for backward compatibility reasons in the EVM. Used for: (a) compatibility with 3rd party Ethereum tools that expect the field, (b) an internal code check by the Autonity Protocol before a block is accepted during consensus; blocks without this hash are rejected. | A 256-bit hash as a Hex encoded string, set to: `0x63746963616c2062797a616e74696e65206661756c7420746f6c6572616e6365` |
| `alloc` | An array of accounts to be assigned `Auton` on chain initialisation. Contract accounts for deployment at genesis can also be specified. | See [`alloc` object](#alloc-object) definition |

### JSON data structures
Genesis configuration file JSON objects:

- [config](#config-object)
- [config.autonity](#configautonity-object)
- [config.autonity.validators object](#configautonityvalidators-object)
- [config.autonity.oracle object](#configautonityoracle-object)
- [alloc object](#alloc-object)
- [alloc.account object](#allocaccount-object)

#### config object

|Parameter|Description|Value|
|---------|-----------|-----|
| `chainId` | Identifier for the Autonity blockchain network, specifying which chain the node will connect to. Introduced by [EIP 155 <i class='fas fa-external-link-alt'></i>](https://eips.ethereum.org/EIPS/eip-155) and used for transaction signature generation | 8-digit decimal integer value formed according to a naming scheme composed of 3 elements: `{A + Network Type + ID}`, where: `A` = `65`; `Network Type` = `00` (Public Mainnet) or `01` (Public General Purpose Testnet) or `10` (Public Special Purpose Testnet) or `11` (Private Internal Development Testnet); `ID` = `0000`-`9999` (unique identifier for the testnet). For example, Bakerloo Testnet has the `chainId` `65010000` |
| `autonity` | Autonity Protocol configuration parameters | See [`config.autonity` object](#configautonity-object) |


#### config.autonity object

{{% alert title="Note" %}}In current state the `operator` governance account is an EOA. It could be assigned to a smart contract address. For example, in the case the blockchain is DAO-governed.{{% /alert %}}

|Parameter|Description|Value|
|---------|-----------|-----|
| `abi` | The abi of an upgraded Autonity Protocol Contract to be deployed at genesis. By default the Autonity Protocol Contract in the Autonity Go Client release is deployed | Leave empty for default contract deployment |
|`bytecode`| The EVM bytecode of an upgraded Autonity Protocol Contract to be deployed at genesis. By default the Autonity Protocol Contract in the Autonity Go Client release is deployed | Leave empty for default contract deployment |
| `minBaseFee` | The minimum gas price for computing a transaction on an Autonity network after genesis. A high minimum gas price setting incentivises validators at genesis when transaction volumes are low | Set to: `500000000` |
| `blockPeriod` | The minimum time interval between two consecutive blocks, measured in seconds. Commonly known as 'block time' or 'block interval' | Value is specific to network configuration. For example, set to `1` for a 1-second block interval |
| `unbondingPeriod` | The number of blocks bonded stake must wait before Liquid Newton can be redeemed for Newton after processing a stake redeem transaction. The `unbondingPeriod` must be longer than an `epochPeriod` | Value is specific to network configuration. For a production environment a number of blocks to span 1 week to 1 month would be typical to enable Byzantine behaviour detection. For a local devnet supporting rapid testing a value of `120` could be appropriate|
| `epochPeriod` | The number of blocks in an epoch. The `epochPeriod` must be shorter than the `unbonding` period | Value is specific to network configuration. For a local devnet supporting rapid testing a value of `30` could be appropriate |
| `treasury` | The Autonity Protocol’s treasury account for receiving treasury fees used for Autonity community funds. Ethereum format address. | Value is specific to network configuration |
| `treasuryFee` | The percentage fee of staking rewards that is deducted by the protocol for Autonity community funds. The fee is sent to the Autonity Treasury account at epoch end on reward distribution. Specified as an integer value representing up to 18 decimal places of precision. | Value is specific to network configuration. For example, a setting of `10000000000000000` = 1% |
| `delegationRate` | The percentage fee of staking rewards that is deducted by validators as a commission from delegated stake. The fee is sent to the validator entity's account at epoch end on reward distribution. The rate can be specified to the precision of 1 basis point. Specified as an integer value representing up to 3 decimal places of precision. | Value is specific to network configuration. For example, a setting of `1000` = 10% |
| `maxCommitteeSize` | The maximum number of validators that can be selected as members of a consensus committee | Value is specific to network configuration. For example, for a local devnet supporting rapid testing a value of `21` could be appropriate |
| `operator` | Address of the Autonity Protocol governance account. The governance account has the authority to mint Newton and change protocol parameters including specification of a new governance `operator` account address. A scenario for this would be migrating to a DAO form of governance. For functions restricted to the operator, see the See API Reference section [Autonity Protocol and Operator Only](/reference/api/aut/op-prot/) | EOA account address |
| `validators` | Object structure for validators at genesis | See [`config.autonity.validators` object](#configautonityvalidators-object)|
| `oracle` | Object structure for a validator's oracle server at genesis | See [`config.autonity.validators` object](#configautonityvalidators-object)|

##### config.autonity.validators object

|Parameter|Description|Value|
|---------|-----------|-----|
| `enode` |The [enode url](/glossary/#enode) address for the validator node on the network after genesis | The validator node enode URL |
| `treasury` | The validator’s treasury account for receiving staking rewards. Ethereum format address. | The validator's EOA account address |
| `oracleAddress` | The unique identifier for the Autonity Oracle Server providing data to the validator. Ethereum format address. | The Oracle Server's account address |
| `bondedStake` | The amount of stake bonded to the validator node at genesis. Denominated in Newton. Positive integer for stake amount | Value is specific to validator's stake at genesis |

##### config.autonity.oracle object

|Parameter|Description|Value|
|---------|-----------|-----|
|`bytecode`| The EVM bytecode of an upgraded Autonity Oracle Contract to be deployed at genesis. By default the Oracle Contract in the Autonity Go Client release is deployed | Leave empty for default contract deployment |
| `abi` | The abi of an upgraded Autonity Oracle Contract to be deployed at genesis. By default the Autonity Oracle Contract in the Autonity Go Client release is deployed | Leave empty for default contract deployment |
| `symbols` | The currency pairs that the oracle component collects data points for. The first listed currency of the pair is the base currency and the second the quote currency | Comma separated list of currency pairs. For example, `"NTNUSD","NTNJPY",..` |
| `votePeriod` | The interval at which the oracle network initiates a new oracle round for submitting and voting on oracle data, measured in blocks | Value is specific to network configuration. For example, set to `60` for initiating a new oracle voting round at 60-block intervals |

#### alloc object

The `alloc` object is used to issue native coin and allows pre-deployment of smart contract accounts at network genesis.

|Parameter|Description|Value|
|---------|-----------|-----|
| `alloc` | An array of accounts objects to be created on the network at genesis. These can be EOA or contract accounts | See [`alloc.account` object](#alloc-object) definition |

##### alloc.account object

|Parameter|Description|Value|
|---------|-----------|-----|
| `alloc.ADDRESS` | The account address | Ethereum format address |
| `alloc.ADDRESS.balance` | The amount of Auton allocated to the account _ADDRESS_ | Positive integer value |
| `alloc.ADDRESS.code` | The contract bytecode to be deployed if a contract account _ADDRESS_ | EVM bytecode |
| `alloc.ADDRESS.storage` | The key-value pair for the contract bytecode storage space if a contract account _ADDRESS_ | k-v pairs for contract storage |


### Example `genesis.json`

```javascript
{
  "config": {
    "chainId": 65110000,
    "autonity": {
      "bytecode": "",
      "abi": "",
      "minBaseFee": 500000000,
      "delegationRate" : 1000,
      "blockPeriod": 1,
      "maxCommitteeSize": 10,
      "unbondingPeriod": 120,
      "epochPeriod": 30,
      "operator": "0x293039dDC627B1dF9562380c0E5377848F94325A",
      "treasury": "0x7f1B212dcDc119a395Ec2B245ce86e9eE551043E",
      "treasuryFee": 150000000,
      "validators": [
        {
          "enode": "enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303",
          "treasury": "0x3e08FEc6ABaf669BD8Da54abEe30b2B8B5024013",
          "oracleAddress": "0x5307a90c018513de02aa4c02B14E6F3CaaA8af3f",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303",
          "treasury": "0xf1859D9feD50514F9D805BeC7a30623d061f40B7",
          "oracleAddress": "0xd54ba484243c99CE10f11Bc5fb24cCc728ba060D",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303",
          "treasury": "0x1B441084736B80f273e498E646b0bEA86B4eC6AB",
          "oracleAddress": "0xF99bC17d7db947Bf4E7171519D678882FF3Dcb8d",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308",
          "treasury": "0xB5C49d50470743D8dE43bB6822AC4505E64648Da",
          "oracleAddress": "0x89f2CabCA5e09f92E49fACC10BBDfa5114D13113",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309",
          "treasury": "0x31e1dE659A26F7638FAaFEfD94D47258FE361823",
          "oracleAddress": "0x7CF62D2C8314445Df0bF3F322f84d3BF785e4aeF",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310",
          "treasury": "0xe22617BD2a4e1Fe3938F84060D8a6be7A18a2ef9",
          "oracleAddress": "0xD689E4D1061a55Fd9292515AaE9bF8a3C876047d",
          "bondedStake": 10000000000000000000000
        }
      ]
    },
    "oracle": {
      "bytecode": "",
      "abi": "",
      "symbols": [
       "BTCUSD",
       "BTCUSDC",
       "BTCUSDT",
       "BTCUSD4"
      ],
      "votePeriod": 60
    }
  },
  "nonce": "0x0",
  "timestamp": "0x0",
  "baseFee": "15000000000",
  "gasLimit": "10000000000",
  "difficulty": "0x0",
  "coinbase": "0x0000000000000000000000000000000000000000",
  "number": "0x0",
  "gasUsed": "0x0",
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "mixHash": "0x63746963616c2062797a616e74696e65206661756c7420746f6c6572616e6365",
  "alloc": {
    "0xe22617BD2a4e1Fe3938F84060D8a6be7A18a2ef9": {
      "balance": "10000000000000000000000"
    },
    "0x31e1dE659A26F7638FAaFEfD94D47258FE361823": {
      "balance": "10000000000000000000000"
    },
    "0x293039dDC627B1dF9562380c0E5377848F94325A": {
      "balance": "1000000000000000000000000000000000000000000000000000000000000000"
    },
    "0xB5C49d50470743D8dE43bB6822AC4505E64648Da": {
      "balance": "10000000000000000000000"
    },
    "0xf1859D9feD50514F9D805BeC7a30623d061f40B7": {
      "balance": "10000000000000000000000"
    },
    "0x3e08FEc6ABaf669BD8Da54abEe30b2B8B5024013": {
      "balance": "10000000000000000000000"
    },
    "0x1B441084736B80f273e498E646b0bEA86B4eC6AB": {
      "balance": "10000000000000000000000"
    },
    "0x5307a90c018513de02aa4c02B14E6F3CaaA8af3f": {
      "balance": "10000000000000000000000"
    },
    "0xd54ba484243c99CE10f11Bc5fb24cCc728ba060D": {
      "balance": "10000000000000000000000"
    },
    "0xF99bC17d7db947Bf4E7171519D678882FF3Dcb8d": {
      "balance": "10000000000000000000000"
    },
    "0x89f2CabCA5e09f92E49fACC10BBDfa5114D13113": {
      "balance": "10000000000000000000000"
    },
    "0x7CF62D2C8314445Df0bF3F322f84d3BF785e4aeF": {
      "balance": "10000000000000000000000"
    },
    "0xD689E4D1061a55Fd9292515AaE9bF8a3C876047d": {
      "balance": "10000000000000000000000"
    }
  }
}
```

### Static nodes file

| Parameter | Description | Value |
|-----------|-------------|-------|
| `enode` | An array of [enode url](/glossary/#enode) addresses for the network bootnodes | The node's enode URL |


### Example `static-nodes.json`

```javascript
[
	"enode://bb9bb2bcd75a5cde083a6a9be2c28f31d9fd6e8de38baa594ffffab0efc5d26524b91baf002fed32f098db71acf0d7646a7c32a7d05ed89fdbbb78c74db13a1a@52.89.151.55:30303",
    "enode://e89196cae37e8041e14d7a063cc82dec3bb351f79f46ab10a059220403932c1337f144ddbf1fd830bf1221fbf539a4e986c924600b060c0a36337256aa70ee2c@52.89.151.55:40303",
    "enode://d8ec443a7a16cd0da3df70d8c96a1a4939ac3cc497097843614b0c87167c6b080f07e02f12f8609230cae5db53f677d620b6bb574155738256d6782f902b9506@52.89.151.55:50303",
    "enode://53f7ed087d55c044278279963a9d3a039d1044d2ff6ae61f11778fee42a5c14c7fdd9b529b08075de8be6f3b41ce28ab1e31b1a0a9db2fd0ec09f07cf6edabd2@512.89.151.55:60303"
]
