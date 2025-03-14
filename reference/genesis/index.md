
---
title: "Genesis"

description: >
  Setting genesis configuration for an Autonity Go Client
---

Genesis configuration for public Autonity networks is built into the client's configuration. If setting up a local testnet, for example a private devnet, configuration has to be specified when initialising the node.

## Public Autonity Network configuration
Configuring the client to join a public network is done by setting the network as a [command-line option](/reference/cli/#command-line-options) when [initialising and running the Autonity Go Client](/node-operators/run-aut/). The client will then auto-detect the network genesis configuration and bootnodes, connect, and sync.

### Public network flags

|Network|Command-line option|Network settings|
|-------|-------------------|----------------|
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

#### JSON data structures

Genesis configuration file JSON objects:

- [genesis file](#genesis-file-object)
- [config](#config-object)
- [config.autonity](#config.autonity-object)
- [config.autonity.validators](#config.autonity.validators-object)
- [config.accountability](#config.accountability-object)
- [config.oracle](#config.oracle-object)
- [config.inflationController](#config.inflationcontroller-object)
- [config.asm](#config.asm-object)
- [config.asm.acu](#config.asm.acu-object)
- [config.asm.stabilization](#config.asm.stabilization-object)
- [config.asm.supplyControl](#config.asm.supplycontrol-object)
- [config.omissionAccountability](#config.omissionaccountability-object)
- [alloc](#alloc-object)
- [alloc.account object](#alloc.account-object)

#### Genesis file object

| Parameter | Description | Value |
|-----------|-------------|-------|
| `config` | Configuration variables for the Autonity Network blockchain | See [`config` object](#config-object) |
| `nonce` | Maintained by the Autonity Protocol for backward compatibility reasons in the EVM. | Set to `0` (`0x0` in hexadecimal) |
| `timestamp` | Specifies the time point when the network starts mining and the first block is mined. If set to `0` the node will start mining on deployment. If a future time point is specified, then miners will wait until `timestamp` + `blockPeriod` to begin mining. The local node consensus engine will start when its local Unix clock reaches the timestamp value. The Validator node operator must keep their local node in sync, i.e. by the [Network Time Protocol (NTP)](https://www.nwtime.org/documentationandlinks/) | Set to `0` (`0x0`) to start node mining on connection to the Autonity network |
| `baseFee` | The base gas price for computing a transaction on an Autonity network after genesis. The base fee is adjusted per the [EIP 1559](https://eips.ethereum.org/EIPS/eip-1559) fee market mechanism. See Concepts, [EIP 1559 Transaction fee mechanism (TFM)](/concepts/system-model/#eip-1559-transaction-fee-mechanism-tfm)| Set to: `15000000000` |
| `gasLimit` | The maximum amount of gas expenditure allowed for a block, placing a ceiling on transaction computations possible within a block. Denominated in [`ton`](/glossary/#ton). The gas limit determines the amount of gas allowed to compute the genesis block; for subsequent blocks the gas limit is algorithmically adjusted by protocol | Set to: `20000000` |
| `difficulty` | Derived from Ethereum where it sets the difficulty for Ethereum's Ethash Proof of Work consensus. For Autonity's implementation of Tendermint BFT Proof of Stake consensus this must be assigned `0`. | Set to `0` (`0x0`) |
| `coinbase` | Maintained for backward compatibility reasons in the EVM. Unused by the Autonity Protocol. Ethereum format address. | Set to `0x0000000000000000000000000000000000000000` |
| `number ` | A value equal to the number of ancestor blocks. At genesis there are no ancestor blocks and it is assigned the value `0` | Set to `0` (`0x0`) |
| `gasUsed` | The gas used in the computation of the block. At genesis this is assigned the value `0` | Set to `0` (`0x0`) |
| `parentHash` | A Keccak 256-bit hash of the parent block header. At genesis there is no parent block and this is assigned a zero value. | Set to `0x0000000000000000000000000000000000000000000000000000000000000000` |
| `mixHash` | Maintained by the Autonity Protocol for backward compatibility reasons in the EVM. Used for: (a) compatibility with 3rd party Ethereum tools that expect the field, (b) an internal code check by the Autonity Protocol before a block is accepted during consensus; blocks without this hash are rejected. | A 256-bit hash as a Hex encoded string, set to: `0x63746963616c2062797a616e74696e65206661756c7420746f6c6572616e6365` |
| `alloc` | An array of accounts to be assigned `Auton` on chain initialisation. Contract accounts for deployment at genesis can also be specified. | See [`alloc` object](#alloc-object) definition |


#### config object

|Parameter|Description|Value|
|---------|-----------|-----|
| `chainId` | Identifier for the Autonity blockchain network, specifying which chain the node will connect to. Introduced by [EIP 155](https://eips.ethereum.org/EIPS/eip-155) and used for transaction signature generation | 8-digit decimal integer value formed according to a naming scheme composed of 3 elements: `{A + Network Type + ID}`, where: `A` = `65`; `Network Type` = `00` (Public Mainnet) or `01` (Public General Purpose Testnet) or `10` (Public Special Purpose Testnet) or `11` (Private Internal Development Testnet); `ID` = `0000`-`9999` (unique identifier for the testnet). For example, Bakerloo Testnet has the `chainId` `65010000` |
| `autonity` | Autonity Protocol configuration parameters | See [`config.autonity` object](#configautonity-object) |
| `accountability` | Accountability Fault Detection protocol configuration parameters | See [`config.accountability` object](#configaccountability-object) |
| `oracle` | Oracle protocol and Oracle Accountability Fault Detection protocol configuration parameters | See [`config.oracle` object](#configoracle-object) |
| `inflationController` | Newton inflation mechanism configuration parameters | See [`config.inflationController` object](#config.inflationcontroller-object) |
| `asm` | Auton Stabilization Mechanism configuration parameters | See [`config.asm` object](#configasm-object) |
| `omissionAccountability ` | Omission Fault Detection protocol configuration parameters | See [`config.omissionAccountability` object](#config.omissionaccountability-object)|

#### config.autonity object

::: {.callout-note title="Note" collapse="false"}
In current state the `operator` governance account is an EOA. It could be assigned to a smart contract address. For example, in the case the blockchain is DAO-governed.
:::

|Parameter|Description|Value|
|---------|-----------|-----|
| `abi` | The abi of an upgraded Autonity Protocol Contract to be deployed at genesis. By default the Autonity Protocol Contract in the Autonity Go Client release is deployed | Only specify if overriding default contract deployment |
|`bytecode`| The EVM bytecode of an upgraded Autonity Protocol Contract to be deployed at genesis. By default the Autonity Protocol Contract in the Autonity Go Client release is deployed | Only specify if overriding default contract deployment |
| `minBaseFee` | The minimum gas price for computing a transaction on an Autonity network after genesis. A high minimum gas price setting incentivizes validators at genesis when transaction volumes are low | Set to: `500000000` |
| `epochPeriod` | The number of blocks in an epoch. The `epochPeriod` must be shorter than the `unbonding` period | Value is specific to network configuration. For a local devnet supporting rapid testing a value of `30` could be appropriate |
| `unbondingPeriod` | The number of blocks bonded stake must wait after processing a stake unbond transaction before Newton is redeemed to the stake delegator. The `unbondingPeriod` must be longer than an `epochPeriod` | Value is specific to network configuration. For a production environment a number of blocks to span a day or more could be typical to enable Byzantine behavior detection. For a local devnet supporting rapid testing a value of `120` could be appropriate |
| `blockPeriod` | The minimum time interval between two consecutive blocks, measured in seconds. Commonly known as 'block time' or 'block interval' | Value is specific to network configuration. For example, set to `1` for a 1-second block interval |
| `maxCommitteeSize` | The maximum number of validators that can be selected as members of a consensus committee | Value is specific to network configuration. For example, for a local devnet supporting rapid testing a value of `21` could be appropriate |
| `operator` | Address of the Autonity Protocol governance account. The governance account has the authority to mint Newton and change protocol parameters including specification of a new governance `operator` account address. A scenario for this would be migrating to a DAO form of governance. For functions restricted to the operator, see the See API Reference section [Autonity Protocol and Operator Only](/reference/api/aut/op-prot/) | EOA account address |
| `treasury` | The Autonity Protocol’s treasury account for receiving treasury fees used for Autonity community funds. Ethereum format address. | Value is specific to network configuration |
| `withheldRewardsPool` | The address of the Autonity Withheld Rewards account, the pool to which withheld Newton inflation rewards are sent for holding | Set to the Autonity `treasury` account at genesis |
| `treasuryFee` | The percentage fee of staking rewards that is deducted by the protocol for Autonity community funds. The fee is sent to the Autonity Treasury account at epoch end on reward distribution. Specified as an integer value representing up to 18 decimal places of precision. | Value is specific to network configuration. For example, a setting of `10000000000000000` = 1% |
| `delegationRate` | The percentage fee of staking rewards that is deducted by validators as a commission from delegated stake. The fee is sent to the validator's [`treasury`](/concepts/validator/#treasury-account) account at epoch end on reward distribution. The rate can be specified to the precision of 1 basis point. Specified as an integer value representing up to 3 decimal places of precision. | Value is specific to network configuration. For example, a setting of `1000` = 10% |
| `withholdingThreshold` | The inactivity threshold at which committee member staking and Newton inflation rewards are withheld and sent to the Withheld Rewards Pool account by the Omission Fault Detection protocol | Value is specific to network configuration. For example, a setting of `0` = 0%, no tolerance |
| `proposerRewardRate` | The percentage of epoch staking rewards allocated for proposer rewarding by the Omission Fault Detection protocol  | Value is specific to network configuration. For example, a setting of `1000` = 10% |
| `oracleRewardRate` | The percentage of epoch staking rewards deducted for oracles as a reward for correct price reporting by the Oracle Accountability Fault Detection protocol | Value is specific to network configuration. For example, a setting of `1000` = 10% |
| `initialInflationReserve` | The amount of Newton held in reserve for Newton inflation rewards| Value is set to `40` Million (40% of the total supply of 100 M Newton) |
| `validators` | Object structure for validators at genesis | See [`config.autonity.validators` object](#configautonityvalidators-object)|

#### config.autonity.validators object

|Parameter|Description|Value|
|---------|-----------|-----|
| `enode` |The [enode url](/glossary/#enode) address for the validator node on the network after genesis | The validator's enode URL |
| `treasury` | The validator’s treasury account for receiving staking rewards. Ethereum format address. | The validator's EOA account address |
| `consensusKey` | The validator's BLS key used for consensus gossiping when participating in consensus | The validator's _consensus public key_ |
| `oracleAddress` | The unique identifier for the Autonity Oracle Server providing data to the validator. Ethereum format address. | The Oracle Server's account address |
| `bondedStake` | The amount of stake bonded to the validator node at genesis. Denominated in Newton. | Positive integer for stake amount. Value is specific to validator's stake at genesis. |

#### config.accountability object

Object structure for the Accountability Fault Detection (AFD) protocol configuration at genesis.

|Parameter|Description|Value|
|---------|-----------|-----|
| `innocenceProofSubmissionWindow` | The number of blocks forming a window within which an accused offending validator has to submit a proof of innocence on-chain refuting an accusation | Set by default to `100` (100 blocks) |
| `baseSlashingRateLow` | The base slashing rate for a fault of _Low_ severity | Set by default to `400` (4%) |
| `baseSlashingRateMid` | The base slashing rate for a fault of _Mid_ severity | Set by default to `600` (6%) |
| `baseSlashingRateHigh` | The base slashing rate for a fault of _High_ severity | Set by default to `800` (8%) |
| `collusionFactor` | The percentage factor applied to the total number of slashable offences committed during an epoch when computing the slashing amount of a penalty | Set by default to `200` (2%) |
| `historyFactor` | The percentage factor applied to the proven fault count of an offending validator used as a factor when computing the slashing amount of a penalty | Set by default to `500` (5%) |
| `jailFactor` | The number of epochs used as a factor when computing the jail period of an offending validator | Set by default to `48` (48 epochs, i.e. 1 day at a 30 mins epoch) |

#### config.oracle object

Object structure for the oracle and Oracle Accountability Fault Detection (OAFD) protocol configuration at genesis.

|Parameter|Description|Value|
|---------|-----------|-----|
|`bytecode`| The EVM bytecode of an upgraded Autonity Oracle Contract to be deployed at genesis. By default the Oracle Contract in the Autonity Go Client release is deployed | Only specify if overriding default contract deployment |
| `abi` | The abi of an upgraded Autonity Oracle Contract to be deployed at genesis. By default the Autonity Oracle Contract in the Autonity Go Client release is deployed | Only specify if overriding default contract deployment |
| `symbols` | The currency pairs that the oracle component collects data points for. The first listed currency of the pair is the base currency and the second the quote currency | Comma separated list of currency pairs. Set by default to `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "ATN-USD", "NTN-USD", "NTN-ATN"]` |
| `votePeriod` | The interval at which the oracle network initiates a new oracle round for submitting and voting on oracle data, measured in blocks | Set by default to `30` (30 blocks, i.e. to initiate a new oracle voting round at 30-block intervals) |
| `outlierDetectionThreshold` | Defines the threshold for flagging outliers | Set by default to `10` (10%) |
| `outlierSlashingThreshold` | Defines the threshold for slashing penalties, controlling the sensitivity of the penalty model | Set by default to `225` (15%) |
| `baseSlashingRate` | Defines the base slashing rate for penalising outliers | Set by default to `10` (0.1%) |
	
#### config.inflationController object 

Configuration of the Inflation Controller of the Newton inflation mechanism.

|Parameter|Description|Value|
|---------|-----------|-----|
| `inflationRateInitial` | Initial inflation rate | Set by default to 7.5% AR |
| `inflationRateTransition` | Transition inflation rate | Set by default to 5.5% AR |
| `inflationReserveDecayRate` | | Constant inflation rate | Set by default to 17.3168186793% AR |
| `inflationTransitionPeriod` | Transition period | Set by default to (4+1/365) years |
| `inflationCurveConvexity` | Convexity parameter | Set by default to -1.7794797758 |
	
#### config.asm object

Configuration of the Auton Stabilization Mechanism (ASM).

|Parameter|Description|Value|
|---------|-----------|-----|
| `acu` | Object structure for the ASM's Autonomous Currency Unit (ACU) configuration at genesis | See [`config.asm.acu` object](#configasmacu-object)|
| `stabilization` | Object structure for the ASM's Stabilization mechanism CDP configuration at genesis | See [`config.asm.stabilization` object](#configasmstabilization-object)|
| `supplyControl` | Object structure for the ASM's Auton supply control configuration at genesis | See [`config.asm.supplyControl` object](#configasmsupplycontrol-object)|

#### config.asm.acu object

Configuration of the Autonomous Currency Unit (ACU), an optimal currency basket of 7 free-floating fiat currencies.

|Parameter|Description|Value|
|---------|-----------|-----|
| `symbols` | The [currency pair](/glossary/#currency-pair) symbols used to retrieve prices for the currencies in the basket | Set by default to `["AUD-USD", "CAD-USD", "EUR-USD", "GBP-USD", "JPY-USD", "SEK-USD", "USD-USD"]` |
| `quantities` | The basket quantity corresponding to each symbol. | Set by default to `[1_744_583, 1_598_986, 1_058_522, 886_091, 175_605_573, 12_318_802, 1_148_285]` |
| `scale` | The scale used to represent the basket `quantities` and ACU value. | Set by default to `7` |

#### config.asm.stabilization object

Configuration of the Stabilization mechanism's Collateralized Debt Position (CDP).

|Parameter|Description|Value|
|---------|-----------|-----|
| `borrowInterestRate` | The annual continuously-compounded interest rate for borrowing. | Set by default to 5%, `50_000_000_000_000_000` |
| `liquidationRatio` | The minimum ACU value of collateral required to maintain 1 ACU value of debt. | Set by default to 1.8, `1_800_000_000_000_000_000` |
| `minCollateralizationRatio` | The minimum ACU value of collateral required to borrow 1 ACU value of debt. | Set by default to 2, `2_000_000_000_000_000_000` |
| `minDebtRequirement` | The minimum amount of debt required to maintain a CDP. | Set by default to a [`megaton`](/concepts/protocol-assets/auton/#unit-measures-of-auton), `1_000_000 ` |
| `targetPrice` | The ACU value of 1 unit of debt. | Set by default to the Golden Ratio rounded to 5 dp `1.61804`, `1_618_034_000_000_000_000` |

#### config.asm.supplyControl object

Configuration of the Stabilization mechanism's initial Auton supply.

|Parameter|Description|Value|
|---------|-----------|-----|
| `initialAllocation` | The initial allocation of Auton to the ASM | Value is specific to network configuration |

#### config.omissionAccountability object

Object structure for the Omission Fault Detection (OFD) protocol configuration at genesis.

|Parameter|Description|Value|
|---------|-----------|-----|
| `inactivityThreshold` | Defines the threshold for flagging validator inactivity | Set by default to`1000` (10%) |
| `lookbackWindow` | The number of blocks over which the protocol will look for inactivity | Set by default to `40` (40 blocks) |
| `pastPerformanceWeight` | Determines how much weight is given to past performance of the validator in the preceding epoch in the current epoch when computing the aggregated inactivity score | Set by default to `1000` (10%) |
| `initialJailingPeriod` | The initial number of epoch(s) that a validator will be jailed for | Set by default to `10_000` (10000 blocks) |
| `initialProbationPeriod` | the initial number of epoch(s) that a validator will be set under probation for | Set by default to  `24` (24 epochs) |
| `initialSlashingRate` | the division precision used as the denominator when computing the slashing amount of a penalty | Set by default to `25` (0.25%) |
| `delta` | the number of blocks to wait before generating an activity proof | Set by default to `5` (5 blocks) |
		
#### alloc object

The `alloc` object is used to issue native coin and allows pre-deployment of smart contract accounts at network genesis.

|Parameter|Description|Value|
|---------|-----------|-----|
| `alloc` | An array of accounts objects to be created on the network at genesis. These can be EOA or contract accounts | See [`alloc.account` object](#alloc-object) definition |

#### alloc.account object

|Parameter|Description|Value|
|---------|-----------|-----|
| `alloc.ADDRESS` | The account address | Ethereum format address |
| `alloc.ADDRESS.balance` | The amount of Auton allocated to the account _ADDRESS_ | Positive integer value |
| `alloc.ADDRESS.code` | The contract bytecode to be deployed if a contract account _ADDRESS_ | EVM bytecode |
| `alloc.ADDRESS.storage` | The key-value pair for the contract bytecode storage space if a contract account _ADDRESS_ | k-v pairs for contract storage |


#### Example `genesis.json`

```javascript
{
  "config": {
    "chainId": 65110000,
    "autonity": {
      "minBaseFee": 500000000,
      "delegationRate" : 1000,
      "blockPeriod": 1,
      "maxCommitteeSize": 100,
      "unbondingPeriod": 120,
      "epochPeriod": 30,
      "operator": "0x293039dDC627B1dF9562380c0E5377848F94325A",
      "treasury": "0x7f1B212dcDc119a395Ec2B245ce86e9eE551043E",
      "withheldRewardsPool": "0x7f1B212dcDc119a395Ec2B245ce86e9eE551043E",
      "treasuryFee": 150000000,
      "withholdingThreshold": 0,
      "proposerRewardsRate": 1000,
      "initialInflationReserve": "0x2116545850052128000000",
      "oracleRewardRate": 1000,
      "validators": [
        {
          "enode": "enode://181dd52828614267b2e3fe16e55721ce4ee428a303b89a0cba3343081be540f28a667c9391024718e45ae880088bd8b6578e82d395e43af261d18cedac7f51c3@35.246.21.247:30303",
          "treasury": "0x3e08FEc6ABaf669BD8Da54abEe30b2B8B5024013",
          "consensusKey": "0x776d2652de66e7x2d294c77d0706c772x077d242076e97cx44feex03e27d59757f7c7m7905072537eccd2d6292262724",
          "oracleAddress": "0x5307a90c018513de02aa4c02B14E6F3CaaA8af3f",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://e3b8ea9ddef567225530bcbae68af5d46f59a2b39acc04113165eba2744f6759493027237681f10911d4c12eda729c367f8e64dfd4789c508b7619080bb0861b@35.189.64.207:30303",
          "treasury": "0xf1859D9feD50514F9D805BeC7a30623d061f40B7",
          "consensusKey": "0x456y2357dfk6e7x2d294c71d0k06c512x077d242076lk7cx44feex03e27d59757f7c717925692537eccd2e6292262774",
          "oracleAddress": "0xd54ba484243c99CE10f11Bc5fb24cCc728ba060D",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://00c6c1704c103e74a26ad072aa680d82f6c677106db413f0afa41a84b5c3ab3b0827ea1a54511f637350e4e31d8a87fdbab5d918e492d21bea0a399399a9a7b5@34.105.163.137:30303",
          "treasury": "0x1B441084736B80f273e498E646b0bEA86B4eC6AB",
          "consensusKey": "0xhi3d112de66e7x2d294c77d0709c772x099d272076e97cx44jyex03e27du175df7cp7hh05o71537eccd2d9282262532",
          "oracleAddress": "0xF99bC17d7db947Bf4E7171519D678882FF3Dcb8d",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://dffaa985bf36c8e961b9aa7bcdd644f1ad80e07d7977ce8238ac126d4425509d98da8c7f32a3e47e19822bd412ffa705c4488ce49d8b1769b8c81ee7bf102249@35.177.8.113:30308",
          "treasury": "0xB5C49d50470743D8dE43bB6822AC4505E64648Da",
          "consensusKey": "0x1a0j2652de66e7x2a294c7ad0406c711x077d242076e97cfc4fykx03e27d59757f7c777905072537ec9d2fhj9w26271u",
          "oracleAddress": "0x89f2CabCA5e09f92E49fACC10BBDfa5114D13113",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://1bd367bfb421eb4d21f9ace33f9c3c26cd1f6b257cc4a1af640c9af56f338d865c8e5480c7ee74d5881647ef6f71d880104690936b72fdc905886e9594e976d1@35.179.46.181:30309",
          "treasury": "0x31e1dE659A26F7638FAaFEfD94D47258FE361823",
          "consensusKey": "0xf9wd795wdew6e7x2d294c75d07c6c281xk7md282076ek7ch34fesx03e279j9d87f5c1o790i0725h7efcd2d69372mh527",
          "oracleAddress": "0x7CF62D2C8314445Df0bF3F322f84d3BF785e4aeF",
          "bondedStake": 10000000000000000000000
        },
        {
          "enode": "enode://a7465d99513715ece132504e47867f88bb5e289b8bca0fca118076b5c733d901305db68d1104ab838cf6be270b7bf71e576a44644d02f8576a4d43de8aeba1ab@3.9.98.39:30310",
          "treasury": "0xe22617BD2a4e1Fe3938F84060D8a6be7A18a2ef9",
          "consensusKey": "0x776d2602de06e7x2d294c77d0706c772x077d242076e97cx44feex00e27d09707f7c7779j0e49il2etc4kd2ar39ov3a7",
          "oracleAddress": "0xD689E4D1061a55Fd9292515AaE9bF8a3C876047d",
          "bondedStake": 10000000000000000000000
        }
      ]
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


#### Example `static-nodes.json`

```javascript
[
	"enode://bb9bb2bcd75a5cde083a6a9be2c28f31d9fd6e8de38baa594ffffab0efc5d26524b91baf002fed32f098db71acf0d7646a7c32a7d05ed89fdbbb78c74db13a1a@52.89.151.55:30303",
    "enode://e89196cae37e8041e14d7a063cc82dec3bb351f79f46ab10a059220403932c1337f144ddbf1fd830bf1221fbf539a4e986c924600b060c0a36337256aa70ee2c@52.89.151.55:40303",
    "enode://d8ec443a7a16cd0da3df70d8c96a1a4939ac3cc497097843614b0c87167c6b080f07e02f12f8609230cae5db53f677d620b6bb574155738256d6782f902b9506@52.89.151.55:50303",
    "enode://53f7ed087d55c044278279963a9d3a039d1044d2ff6ae61f11778fee42a5c14c7fdd9b529b08075de8be6f3b41ce28ab1e31b1a0a9db2fd0ec09f07cf6edabd2@512.89.151.55:60303"
]
```
