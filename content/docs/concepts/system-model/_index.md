
---
title: "System model "
linkTitle: "System model"
weight: 2
description: >
  Autonity system model - participant nodes, blockchain primitives, transactions and fees 
---

An Autonity network is a distributed blockchain system comprised of peer nodes running client software executing the Autonity Protocol. It is a permissionless network: nodes can leave and join the network on demand. On connecting to an Autonity network a node becomes a **participant** of the distributed system and one of the processes comprising the system's distributed virtual machine. Each participant maintains a local copy of the system's distributed ledger, maintains synchrony with network time, and runs the Autonity Go Client software. Autonity is an _eventually synchronous_ distributed system utilising Tendermint BFT consensus protocol, the Ethereum EVM, and reliable networking protocols to synchronise time and replicate state across the system.

## Participants
A participant is a network node connected to an Autonity distributed system and forming part of the system's distributed virtual machine. Participants run the Autonity Go Client software, communicate with one another over networking protocols in Autonity's communication layer, execute state transitions in the Ethereum runtime environment, and have read and write access to the system ledger. Each participant maintains an up-to-date copy of system state in a ledger object.
 
Participants are secured and uniquely identified by public key cryptography. Each participant has a public and private keypair ([node key](/concepts/validator/#p2p-node-key)) for signing the messages it broadcasts at the communication layer. This message signature allows cryptographic verification of message sender identity by recipient participants. 

Each participant node has:

- A keypair - the [node key](/concepts/validator/#p2p-node-key). The private key is used to sign messages in the communication layer. The public key is used to uniquely identify the participant:
	- Public keys are accessible to other participants and a participant can identify other participants by their public key.
	- It is used to derive participant identifier and network address.
- A unique network address (the [enode URL](/concepts/validator/#validator-enode-url)).
- If a participant is registered as a validator, then an address derived determinstically from the node key public key is used as the [validator identifier](/concepts/validator/#validator-identifier) address.

Participants can register as validators and have stake bonded to them as described in the [Validator](/concepts/validator/) section. Consequently the set of participants can be subdivided into divisions or subclassed as:

- The set of possible validator participants, and, for those validators selected to the consensus committee.
- The set of committee members.

The committee is dynamically maintained and selection is a deterministic function of the protocol - see [Committee member selection](/concepts/consensus/committee/#committee-member-selection).

A committee member participates in Tendermint Consensus instances, voting for and deciding on proposed blocks. Blocks endorsed by two-thirds or more of the committee's voting power are appended to the blockchain. The validator votes for a block are recorded in the [block header](/concepts/system-model/#the-blockchain-object) `committedSeals` field.

[System participants](/overview/#system-participants) submit calls and state affecting transactions to the system by RPC to [Autonity Interfaces](/reference/api/) provided by Autonity Go Client nodes. 

## Networking

An Autonity system has a full [mesh network](/glossary/#mesh-network) topology. Each participant is connected to every other participant by a direct TCP/IP connection. This gives a reliable and _eventually synchronous_ channel for message broadcast between peers.

P2P networking protocols are Ethereum [devp2p](https://github.com/ethereum/devp2p), RLPx as transport to an ethereum wire protocol (eth65) modified to add messages for Tendermint BFT consensus rounds.
 
_Eventual synchrony_ is a model described by a Global Stabilisation Time (GST) and a _Delta_ time. If a message is sent by a participant at time _t, then the message is received by time _max{t,GST} + Delta_, _Delta > 0_ and unknown by all the participants. Client logic verifies if a received message has been sent to a participant before forwarding, preventing duplicate message sends. The Tendermint algorithm assumes that at _GST + Delta_, all the consensus messages sent at GST should have been received by committee members.

The principal message primitives of the networking communication layer are:

- Transaction: valid transaction messages submitted to clients from the external environment, broadcast for processing.
- Block announcement: notification of a new block sent by consensus committee members.
- Consensus, Tendermint consensus messages sent by and forwarded between committee members during consensus rounds.

{{% alert title="Note" %}}Transaction calls execute against local state and are not broadcast to the network, per standard Ethereum.{{% /alert %}}

## System state

Autonity inherits Ethereum's state model, ledger trie structures, and transaction state machine. Per Ethereum the state of the system incrementally evolves from genesis state as blocks are decided and appended to the ledger, each individual transaction forming a valid arc between state transitions to an account. The world (or global) state of the system comprises the mapping between accounts and their states, recorded in the distributed ledger maintained by participants. Per Ethereum, a participant can compute the current world state of each account on the system at any time by using the ledger and EVM, and applying in order the sequence of transactions from genesis block to current block height.

At network genesis the ledger state comprises the Autonity Protocol Contract and the genesis block state as set in the [genesis configuration file](/reference/genesis/). The genesis block contains the initial set of participant validators and smart contracts, both with their states. The initial smart contracts are: Autonity Protocol Contract, validator _liquid newton_ contracts, and optionally additional contracts deployed using the `alloc` structure in the genesis file. Initial smart contract state is Autonity Protocol Contract parameterisation and validator _liquid newton_ contract bonded stake.


### The Ledger Object

Each participant maintains a local copy of the system state in a local ledger object, the participant's state database. Per Ethereum, the blockchain state is persisted as a _directed rooted tree_ using a modified Merkle Patricia tree (trie) structure in RLP serialisation, each tree node linked by a cryptographic hash. (See [Ethereum Yellow Paper](https://github.com/ethereum/yellowpaper) Appendix B Recurisve Length Prefix, Appendix D Modified Merkle Patricia Tree). 

The ledger is an _[append-only](https://en.wikipedia.org/wiki/Append-only)_ immutable data structure with the property that new data can be appended and existing data is immutable. Blocks are appended to the chain over time at the interval set by the protocol (block period), each block pointing back toward the root, the genesis block. A block once committed is an _[immutable object](https://en.wikipedia.org/wiki/Immutable_object)_ whose state cannot be changed. It cannot be altered - _cf. [finality](/glossary/#finality)_. Immutability is assured by the cryptographically verifiable tree structure of the ledger object; it allows any previous state to be retrieved and recomputed.

Ledger integrity is assured cryptographically by the hash tree, by block validity constraints according to the Autonity Protocol, and by deterministic consensus computation before block commit - i.e. append - to the ledger.

### The Blockchain Object

Autonity modifies the inherited Ethereum blockchain structure, extending the block header data structure to add fields for managing block production by the committee-based Tendermint BFT Consensus mechanism.

#### Block Header

Fields inherited from Ethereum:

- `coinbase`, unused
- `difficulty`, a scalar value corresponding to the difficulty level of this block. Can be calculated from the previous block's difficulty level and the timestamp
- `extraData`, an arbitrary byte array containing data relevant to this block. This must be 32 bytes or fewer
- `gasLimit`, a scalar value equal to the current limit of gas expenditure per block
- `gasUsed`, a scalar value equal to the total gas used in transactions in this block
- `baseFeePerGas`, minimum price per unit of gas for your transaction to be included in the block.
- `hash`, the Keccak 256-bit hash of the current block's header.
- `logsBloom`, the Bloom filter composed from indexable information (logger address and log topics) contained in each log entry from the receipt of each transaction in the transactions list
- `miner`, the address of the block proposer
- `mixHash`, a 256-bit hash which, combined with the nonce, proves that a sufficient amount of computation has been carried out on this block
- `nonce`, a 64-bit value which, combined with the mixHash, proves that a sufficient amount of computation has been carried out on this block
- `number`, a scalar value equal to the number of ancestor blocks. The genesis block has a number of zero.
- `ommersHash`, unused.
- `parentHash`, the Keccak 256-bit hash of the parent block’s header.
- `receiptsRoot`, the Keccak 256-bit hash of the root node of the trie structure populated with the receipts of each transaction in the transactions list portion of the block
- `sha3Uncles`, the SHA3 hash of the uncle parents of the block. This always has the value '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347'
- `size`, a scalar value corresponding to the current block byte size
- `stateRoot`, the Keccak 256-bit hash of the root node of the state trie after transactions execution and finalization.
- `timestamp`, a scalar value equal to the reasonable output of [Unix's `time()`](/glossary/#unix-time) at this block's inception.
- `totalDifficulty`, a scalar value corresponding to the difficulty of computing blocks in the chain to the current block
- `transactionsRoot`, the Keccak 256-bit hash of the root node of the trie structure populated with each transaction in the transactions list portion of the block


New Autonity Fields:

- `committedSeals`, array of signed committee member precommit votes for the block
- `committee`, array of the consensus committee members for the **following block**. Each item in the array is recorded as an RLP-encoded pair of committee member properties (`account`, `voting_power`).
- `proposerSeal`, the block proposer's signed block proposal
- `round`, a scalar value corresponding to the number of consensus rounds initiated for the block. Initial value of `0`.

{{% alert title="Note" %}}If you want to determine how many validators voted for a block with regard to the total committee membership, check if there is a delta between the count of seals in this block and the committee members in the preceding block.{{% /alert %}}


#### Block content

The block content structure is unmodified per standard Ethereum:

- transactions: a list of the transactions comprising the block. Recorded as an array of Keccak 256-bit hashes of the signed transaction.
- uncles: unused


#### Example block

```javascript
> web3.eth.getBlock(await web3.eth.getBlockNumber())
{
  baseFeePerGas: 5000,
  committedSeals: [
    '0x53f8f109e5a3391437a5511bd85e9ea9da60abd1031b52a73ba6d133b132a5bb40121f0c2836ed4ce2199ab9c95f9f76ed3a24d80467863bea44fce37378e30401',
    '0x99988475e5a1d77777d903cc6680b24f7cfd0fd5259ea59708fbd35646da6d4a7758a0bc4639fc6398d4f667f3210695191c90949116d2a89af6705ad84648ab00',
    '0xeeba261aca27203c5410fec6cef70d33794afae69379e704e46f582002b29eb91cc9354fd2825e59d6dc617746d24242216b664b6ed1d705bd39a3cf7ea4a06d01',
    '0x64ddbe2cf7f31c0e04c46a06e2edf10de34a4acc429c9faf86dbc5a17e456de00fab2b3e7edc83643645b0aac3d5f6e11570bacff801b6491a85699d212ae91c01'
  ],
  committee: [
    {
      address: '0x055a7c97b73db9649ff03ac50db0552c959cca91',
      votingPower: '0x2710'
    },
    {
      address: '0x0be4ee22d794c640366352ef6ce666e52229886d',
      votingPower: '0x2710'
    },
    {
      address: '0x21bb01ae8eb831fff68ebe1d87b11c85a766c94c',
      votingPower: '0x2710'
    },
    {
      address: '0x35379a60fc0f108583d6692cc6d2fa0317cc9724',
      votingPower: '0x2710'
    },
    {
      address: '0x8cc985ded2546e9675546db6bcf34f87f4a16c56',
      votingPower: '0x2710'
    },
    {
      address: '0x94c1eee283fac8102ddb08ac0661a268d4977b2d',
      votingPower: '0x2710'
    }
  ],
  difficulty: '1',
  extraData: '0x',
  gasLimit: 8000000,
  gasUsed: 35358,
  hash: '0x550eb0801af4421e70c97a001314fd79a110d70f3921fbadce144c1480427126',
  logsBloom: '0x00004000000000000000000000020400000000010000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000004000000002000000000000000000000000000000000000000000000002000000000000000000000000000000000000000080000000000000000000000000000000',
  miner: '0x0be4Ee22d794c640366352Ef6CE666E52229886d',
  mixHash: '0x63746963616c2062797a616e74696e65206661756c7420746f6c6572616e6365',
  nonce: '0x0000000000000000',
  number: 1206023,
  parentHash: '0x8f7f604767283c9c20ba8db627e4a9ecd663de059f663c367ec83fb6bc575c5e',
  proposerSeal: '0x83b4c1d76dd0879cc38d2a8d0af587869163de3ee5fcaedb332e6659eb04d4af04725fe5f3a80371372183cf3ff2ca7601d9a1ecd6839e47a6b93e125815970e01',
  receiptsRoot: '0x51b9007d1c90e4c49520a136e26146d08d5120071ac93f280e0eaed97feb273f',
  round: '0x0',
  sha3Uncles: '0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347',
  size: 1195,
  stateRoot: '0xd59bc7f93e7bbc21ef51da834c12319fd3d9f97f272df5a5b689a1bef7cdf1f9',
  timestamp: 1649686303,
  totalDifficulty: '1206023',
  transactions: [
    '0x155e061b49a5c0340c982cce856fb8ec3e6c1d2914f72a8e0429452e3a790fd2'
  ],
  transactionsRoot: '0x2f8dc505d5d06ba6023a20ffcfa2683a8febfeee9ade2ac2edd9b9386027b2a4',
  uncles: []
}
```

### Transactions

Transactions are standard Ethereum transaction structures. Autonity supports both legacy (type 0) and EIP 1559 (type 2) transaction types. Use of the EIP 1559 type 2 transaction to take advantage of the economic benefits provided by the EIP 1559 fee market mechanism is recommended.

{{% alert title="Note" %}}For an explanation of how specifying gas in transactions differs between legacy and EIP 1559 transaction types, see the Ethereum developer docs explanation of Gas and Fees - https://ethereum.org/en/developer/docs/gas/.{{% /alert %}}

Generated and signed by accounts on the network, transactions are submitted to the system via participant node client API's. The client performs standard Ethereum pre-flight checks to the transaction before broadcasting it to the network.

Transactions are used to transfer value between individual account state, invoke calls on smart contracts, and to add new smart contracts to an Autonity network. 

#### Requests, transactions and calls

Transactions are submitted as [requests](/concepts/system-model/#request) over the JSON-RPC remote procedure call (RPC) protocol to read and write to system state. Requests to protocol contract functions are made as Ethereum [transactions and calls](/concepts/system-model/#transactions-and-calls) executed in the Ethereum runtime. The on-chain operation executed by smart contract logic may be a [transaction](/concepts/system-model/#transaction-1) that is a write operation resulting in a change to system state or a read-only [call](/concepts/system-model/#call-1) that queries system state. Execution of a contract function may result in one contract invoking another contract, resulting in a [message call](/concepts/system-model/#message-call) between contracts. For example, a bonding request submitted to the Autonity Protocol contract results in a state change to the validator's liquid newton contract ledger when staking transitions are applied at epoch end.

#### Request

User interactions with contracts originate in the external environment and are always initiated by an external user - i.e. an EOA. They are received at the Autonity System boundary as an RPC to an Autonity Go Client. Requests adhere to the REST constraints for Web service design and are stateless and self-contained, the JSON-RPC request object containing all necessary parameters. Requests use the [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) protocol. On-chain contract interactions between smart contracts are by contract logic invoking [message calls](/concepts/system-model/#message-call).

#### Transactions and calls

The on-chain operation resulting from a [request](/concepts/system-model/#request) message may be a [transaction](/concepts/system-model/#transaction-1) or a [call](/concepts/system-model/#call-1):

- a write operation executed by a *transaction* passing in parameters. This executes and records transaction outcome in state. It is made by a Web3  'sendTransaction' to a contract function that results in a change to contract state. As such, a *transaction* represents a valid arc between two states (See Ethereum Yellow Paper, [2. The Blockchain Paradigm](https://ethereum.github.io/yellowpaper/paper.pdf)). A processed transaction is recorded in a block in the distributed ledger
- a read-only operation executed by a *call* passing in parameters. This simulates an outcome without recording it in state and may be by a Web3 'call' to a contract function that returns a result according to parameters passed in, or by a call to a read-only contract function

While both are signed by the EOA and execute contract functions there are important distinctions:

##### Call

| Computation cost | Execution scope | State-affecting | Synchronicity | Execution guarantee |
|------------------|-----------------|-----------------|---------------|---------------------|
| No gas cost | Executed against local node ledger object| No: if state-inspecting it reads local node state only; simulates execution - no state transition recorded | Synchronous: the result is returned immediately | Result returned immediately |

##### Transaction
| Computation cost | Execution scope | State-affecting | Synchronicity | Execution guarantee |
|------------------|-----------------|-----------------|---------------|---------------------|
| Gas spent per transaction. Legacy type 0 transactions use the `gasPrice` parameter - see [Transactions](/concepts/system-model/#transactions). EIP1559 type 2 transactions use the base fee model - see [Autonity EIP 1559 configuration](/concepts/system-model/#autonity-eip-1559-configuration). See also Ethereum Yellow Paper, [4.2. The Transaction; 5. Gas and Payment](https://ethereum.github.io/yellowpaper/paper.pdf)) | Propagated and executed across all nodes in the peer-to-peer network | Yes: causes global state transition | Asynchronous: state transition applied on commit to block and dependent upon factors such as `gasPrice` / base fee, the time for which it remains in the pending pool, Autonity System's block mining interval | State transition applied subject to transaction validity being verified by consensus computation. The transaction hash is returned. A subsequent call is required to return the transaction data or, if emitted by the state-affecting function, event data |

For the Ethereum Web3 modules supported by Autonity, see Reference [Autonity Interfaces](/reference/api/web3/). For official Web3 docs, see [https://readthedocs.org/projects/web3js/](https://readthedocs.org/projects/web3js/).

#### Transaction

Transactions result in a change to a contract's state and:

- have a type (see [EIP 2718](https://eips.ethereum.org/EIPS/eip-2718)) and are legacy (type '0') or EIP 1559 (type '2')
- are signed by the message sender
- identify the recipient
- pass in parameters for the requested function, which may include an `amount` if the transaction is executing a transfer of value, e.g. a 'mint', 'burn' or 'transfer'
- have a data structure that varies according to their type and have a legacy transaction structure or a type 2 transaction payload ( see [EIP 1559](https://eips.ethereum.org/EIPS/eip-1559#specification) 
- provide information about the fees the sender is willing to pay for each step in transaction computation and influencing the priority with which the transaction is processed by the participant nodes computing in the Autonity System's decentralised virtual machine
- return a transaction receipt hash asynchronously on verification of the transaction by consensus computation.

#### Call

Calls are non state-affecting and simulate an outcome without recording it in state. Calls are made to `pure` or `view` contract functions that execute according to parameters passed in, but are distinct in that whereas a `pure` function does not read state, a `view` function reads local state only. I.e. of the node to which the call was submitted.

Calls to a contract:

- are signed by the message sender
- pass in parameters for the requested function, which will return requested state or a simulation of execution outcome according to the passed in parameters
- return a value synchronously.

#### Message call

A contract may interact with another contract by a call, sending a message, resulting in the recipient contract executing code. 

A message call is executed in the EVM at runtime and will:

- implicitly identify the original sender
- identify the target contract account
- may contain a value if the call is executing a transfer of value
- may contain data taken as input by the receiving contract


{{% alert title="Note" %}}Although often referred to as an 'internal transaction', a _message call_  is not strictly a transaction. A transaction is always signed. A _message call_ is not because it is initiated by a contract account and not an account held by an external system user, i.e. externally owned account (EOA).{{% /alert %}}


### Transaction fees

Fees for processing transactions on an Autonity network are paid in the protocol coin `auton`, the native balance of an Autonity account.

Autonity uses Ethereum's [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) transaction fee mechanism for pricing gas in transaction fee markets


#### EIP 1559 Transaction fee mechanism (TFM)
EIP 1559 fee markets accommodate demand volatility by a variable block size and dynamic adjustment of the minimum price for each unit of gas used to compute a transaction on the network. The TFM functions by targeting usage of an average percentage of available block capacity over time. Mean-reverting to this target is achieved by adjusting gas price each block according to the delta between actual gas used versus targeted gas usage in the preceding block.

The minimum gas price is set as a _base fee_, which may remain static, increase, or decrease according to actual consumption. Change in the base fee is a function of the _actual_ gas used in computing the preceding block and the expected _target_ gas consumption of the parent block. A _base fee change denominator_ bounds the amount the fee is allowed to change between blocks. This smooths volatility in price movements away from and back to the target usage over block time. The _target_ is derived by dividing the parent _block gas limit_ by an _elasticity multiplier_ to project a desired block usage as a percentage of the block capacity. The surpus block capacity gives elasticity, a buffer zone, that can accommodate volatility in transaction demand. Surplus block capacity absorbs the increased throughput and adjustment of base fee every block responds to market demand for the blockchain's computational and storage resources by adjusting base fee per gas unit cost accordingly:

- increasing when blocks are above the gas target
- decreasing when blocks are below the gas target.

To incentivise inclusion of a transaction in a block, EIP 1559 allows a transaction to include an optional _priority fee_ or 'tip' as a reward incentive to the block proposer for including the transaction in a block.

 
#### Autonity EIP 1559 configuration

Autonity maintains the Ethereum protocol settings for EIP 1559:

- _block gas target_ = `15M`, the pre EIP 1559 block gas limit
- _block gas limit_ = `30M`, double the preceding block gas limit accommodating 50% elasticity
- _base fee change denominator_ = `8`, limiting possible change in base fee to 12.5% each block.
- _elasticity multiplier_ = `2`, setting targeted block usage at 50% of the block limit.


Autonity modifies EIP 1559 by:

- specifying a _minimum base fee_. Setting a minimum base fee imposes a floor to the minimum gas price cost per unit of gas used to process a transaction on the network. This floor ensures base fee cannot revert to `0` in a period of network inactivity, maintaining the inherent security properties of gas economics. The value is set at genesis. See [`minBaseFee`](/reference/genesis/#configautonitycontract-object) parameter in the [Protocol](/reference/protocol/) section
- the _base fee_ is _not burned_ as in EIP 1559. The base fees collected for each block are added to the rewards pool for distribution as staking rewards at epoch end.
- the _priority fee_ rewards are given to the block proposer per EIP 1559. In current state, the priority fee is paid to the proposing validator entity's account every block.


### Accounts - EOA and contract

An _account_ is the unique identifier for referring to an external system user, a participant node, or a smart contract deployed on the system:

- External users require an Ethereum account based on public-key cryptography to access and call functionality of the Autonity Protocol contracts and other decentralised application contracts deployed on the system.
- Participant and validator nodes and their operators have unique accounts as described in [Participants](/concepts/system-model/#participants) and [Validator identity, accounts and keypairs](/concepts/validator/#validator-identity-accounts-and-keypairs)
- Smart contracts deployed on the system ledger are uniquely identified by their contract account addresses and have a state. Smart contracts native to Autonity and forming part of an Autonity system are described in [Autonity Protocol Contract](/concepts/#autonity-protocol-contract). 


As an Ethereum-based blockchain system, Autonity account addresses are in Ethereum format - a 42 character hexadecimal string derived from last 20 bytes of the account's public key and prepended by `0x`. Keccak-256 and the Elliptic Curve Digital Signature Algorithm (ECDSA) are used for generating (and verifying) cryptographic signatures over the `secp256k1` Elliptic Curve (EC). The use of public-key cryptography based on elliptic curves allows the system to efficiently secure user's data via asymmetric encryption and provides pseudonymity to the user's identity via the public key. The private key gives the owner control over transfer and ownership of the Autonity system's native protocol coins (_Auton_, _Newton_, _Liquid Newton_) to another account. In the wider Ethereum ecosystem this private key may be referred to as a user's 'Ethereum private key'. The private key is used to sign all [transactions and calls](/concepts/system-model/#transactions-and-calls) submitted to an Autonity system by users from the external environment via an EOA.

The key elements of an Ethereum account are:

- **Private-public key pair:** A private-public key pair is generated by the key generation algorithm of the digital signature scheme used (i.e. ECDSA over secp256k1). The key pair allows the account holder to carry out signing operations with the private key (also referred to as "secret key"). Furthermore, the associated public key allows verification of the various digital signatures generated by account holders, and thus allows to keep the system secure.
- **Address:** The address is the unique identifier for a user's account on the ledger. It is derived from the account's public key.
- **Ethereum keystore file:** The Ethereum keystore is the file format for storing and working with encrypted private keys. For a definition of the keystore file format see the Ethereum wiki page [Web3 Secret Storage Definition](https://ethereum.org/en/developers/docs/data-structures-and-encoding/web3-secret-storage/).

The steps for creating an account are described in the How To [Create an account](/account-holders/create-acct/).

There are two types of Account object maintained in the Autonity system state, _Externally Owned Accounts (EOA)_ and _Contract Accounts_.

#### Externally Owned Account (EOA)

EOA's: represent accounts belonging to external users with a private key, are funded with gas to pay for transaction costs, and do not have smart contract code. All [transactions and calls](/concepts/system-model/#transactions-and-calls) submitted _from the external environment_ to smart contracts in an Autonity system are submitted by externally owned accounts and signed using the submitting user's private key.

#### Contract Account

Contract Account's: deployed smart contracts are also account objects. However, while these accounts have a balance, they are initialised with code and do not have an associated private key. As opposed to EOA's, interactions with a contract account are governed by its EVM code. Such code is either triggered by transactions from EOA's or message calls from other contract accounts. A contract account can call other contracts by [message calls](/concepts/system-model/#message-call), but such message calls are not signed by a private key.

Contract accounts native to an Autonity system are described in [Autonity Protocol Contract](/concepts/#autonity-protocol-contract).

  
#### References

- Ethereum uses the Keccak-256 cryptographic hash function developed by the [Keccak Team](https://keccak.team/keccak.html) - see "[The Keccak SHA-3 Submission](https://keccak.team/files/Keccak-submission-3.pdf)". This differs slightly to the NIST standardised Sha-3 hash function published as [FIPS 202](https://keccak.team/specifications.html#FIPS_202).
- Elliptic Curve Digital Signature Algorithm (ECDSA) for generating (and verifying) cryptographic signatures over the `secp256k1` Elliptic Curve (EC). See [SEC 2: Recommended Elliptic Curve Domain Parameters](http://www.secg.org/sec2-v2.pdf).
- For more information on transaction signing with ECDSA, see the Ethereum Yellow Paper, [Appendix F. Signing Transactions](https://ethereum.github.io/yellowpaper/paper.pdf).
- For an overview of EOA vs. Contract account, see Clearmatics "Zeth Protocol Specification, [Section 1.2.1](https://raw.githubusercontent.com/clearmatics/zeth-specifications/master/zeth-protocol-specification.pdf).

