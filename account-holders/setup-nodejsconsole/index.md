---
title: "Setup the NodeJS Console"
description: How to install and launch the NodeJS Console.
draft: true
---

<!-- This is a collection of all content cut-and-pasted from other
sections, so it is unlikely to be coherant or well-ordered. -->

### Autonity NodeJS Console
#### Prerequisites
- AMD64 instruction set Linux OS
- To install and run the Autonity NodeJS Console  you need current versions of [nodejs](https://nodejs.org/en/download/) and [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

#### Install
The Autonity NodeJS Console is distributed as part of the Autonity Go Client Release in the `nodejsconsole` sub directory. For users who only require a console, it is also available as a separate download from the Autonity [Releases](https://github.com/autonity/autonity/releases) Archive - `nodejsconsole-<RELEASE_VERSION>.tar.gz`.

To install, get the _tarball_ and unpack. The tarball contains a folder with 2 artefacts, so you don't need to create a home directory for it. Simply unpack the tarball file from your Downloads folder to your working directory as described for the client in steps 1-3 above.

To run the Console and connect to a node, specify WebSockets as the transport and the IP address and port `8546` of the Autonity client node you will connect to.  Use WS for a local node and WSS for secure connection to a public node on an Autonity network. For example, to connect to a node running on local host:

```bash
./console ws://127.0.0.1:8546
```

On initial running, the console will install web3 and node modules, then initialise the console and display:

```javascript
Welcome to the Autonity node console
modules: eth net rpc autonity
Type "module".<Tab> to get started
>
```

### Install the Autonity NodeJS Console

The Autonity NodeJS Console can be used to connect to the WebSocket endpoint on an Autonity Go Client node, and execute commands to interact with the Autonity client and Autonity Protocol smart contracts. Set up the NodeJS Console on your local machine using one of two methods:

- If you have already cloned Autonity, create a directory and copy the console from the Autonity repo:

    ```bash
    mkdir nodejsconsole
    cd nodejsconsole
    cp <PATH TO AUTONITY>/autonity/nodejsconsole/console
    cp <PATH TO AUTONITY>/autonity/nodejsconsole/script.js
    ```

- For users who only require a console, download the separate NodeJS Console release from the Autonity [Releases](https://github.com/autonity/autonity/releases) Archive - `nodejsconsole-<RELEASE_VERSION>.tar.gz`.

- Unpack the _tarball_ file from your Downloads folder to your install directory:

    ```bash
    tar -xzf nodejsconsole-amd64-<RELEASE_VERSION>.tar.gz  --directory /<PATH_TO_WORKING_DIREoCTORY>
    ```

### Run the Autonity NodeJS Console

Run the console, specifying the IP address of the Autonity client node you will connect to using WebSocket.

If the node you are connecting to has an encrypted WebSocket endpoint, then you need to connect to it via `wss` ("web socket secure"). For example, to connect to the Piccadilly Testnet public endpoint `rpc1.piccadilly.autonity.org`:

``` bash
./console wss://rpc1.piccadilly.autonity.org:8546
```

Here are some examples:

#### Get the block number:

 ```javascript
 web3.eth.getBlockNumber()
 ```

#### Get maximum consensus committee size:

 ```javascript
 autonity.getMaxCommitteeSize().call()
 ```

#### Get all nodes in the consensus committee:

 ```javascript
 autonity.getCommittee().call()
 ```

#### Get the genesis config:

To return the protocol parameterisation set at network genesis for:

- operatorAccount
- treasuryAccount
- treasuryFee
- minBaseFee
- delegationRate
- epochPeriod
- unbondingPeriod
- committeeSize
- contractVersion
- blockPeriod

 ```javascript
 autonity.config().call()
 ```


#### Check the auton balance of an account:

 ```javascript
 eth.getBalance('<_addr>')
 ```

#### Check the newton balance of an account:

 ```javascript
 autonity.balanceOf('<_addr>').call()
 ```

### Syntax when making calls

- For functions that read information by calling Autonity protocol smart contract methods such as above, add `.call()`.

- For functions that retrieve information from the node client itself, like many of the `web3.eth` functions, you do not need `.call()`.

- Web3 commands can be accessed by typing `web3.` then pressing `<TAB>` twice to list available functions.

- The 'eth' command namespace can be found by typing `web3.eth.` then pressing `<TAB>` twice.

- Autonity specific commands can be found by typing `autonity.` then pressing `<TAB>` twice. (e.g., as above, ` autonity.getCommittee().call()`).

- You can leave the console by typing `.exit`.

## JavaScript CLI: NodeJS Console

The Autonity NodeJS console is a command-line interface for invoking an interactive JavaScript runtime environment to connect to an  Autonity node. It gives access to `web3` and `autonity` interfaces, and access to Autonity Protocol method calls for which public JSON-RPC calls are not defined.

The Autonity NodeJS console can be used in interactive or script mode as the Geth console can be.

### Installation

The Autonity NodeJS Console is provided as part of the Autonity Go Client binary and as a separate download package.

To install, see the How to _Install Autonity_ and:

- [Build from source code](/node-operators/install-aut/#build-from-source-code) to build and install from binary, and,
- [Autonity Node JS Console](/node-operators/install-aut/#autonity-nodejs-console) to install from the download package.

CD to the Node JS Console directory. This will be `./nodejsconsole` if you have built from source, or if you are using the separate download then the directory location where you unzipped the _tar_ file to.

To connect to a node on an Autonity network in an interactive session run the Autonity console, specifying the IP address of the node you will connect to. The connection is made over WebSockets to port 8546 by default:

```bash
./console ws://<IP-ADDRESS>:8546
```

For example, to connect to a local node run:

```bash
./console ws://127.0.0.1:8546
```

The console installs, initialises with web3 and Autonity Go Client interface modules, then displays:

```javascript
Welcome to the Autonity node console
modules: eth net rpc tendermint autonity
Type "module".<Tab> to get started
>
```

An interactive session is now open with the connected node.

Note that the NodeJS Console:

- Provides `aut` (Autonity), `eth`, `net`, `rpc`, `tendermint` modules by default. Web3 method calls can be prefixed by `web3.`but this is not required. Additional Web3 modules may be available if the node you are connecting to has provided them in its `--ws.api` flag when starting Autonity (See How to [Run Autonity](/node-operators/run-aut/)).
- Will not timeout if idle. The console implements an automatic reconnect mechanism and will reconnect if left idle after 1000 ms.

::: {.callout-important title="Warning" collapse="false"}
Public access to the `tendermint` namespace module is deprecated and will be removed in a future release. See [Known Issues](/issues/), [Tendermint Namespace Interface is accessible but not meant for use by external clients](/issues/#tendermint-namespace-interface-is-accessible-but-not-meant-for-use-by-external-clients).
:::

### Usage

The Autonity console is invoked as an interactive shell. Refer to the [Autonity Interfaces](/reference/api) Reference section 'console' entries for guidance on how to call the API from the console.

::: {.callout-note title="Note" collapse="false"} Some functions provided by the NodeJS console are asynchronous and they return promises (https://www.w3schools.com/Js/js_promise.asp). For conveniency reasons promises are automatically resolved by the NodeJS console CLI when calling asynchronous functions; however this is not true when performing assigments or nested function calls, in this case the `await` keyword needs to be specified to resolve the promise. Examples: `wallet = await web3.personal.listWallets()`, `web3.eth.getBlock(await web3.eth.getBlockNumber())`:::

#### `.call()` and `.send()`

API interactions made using the console may have `.call()` or `.send()` appended depending on the method and module called.

Use `.call()` for `Autonity` calls to read ledger state and retrieve [calldata](/glossary/), appending `.call()` to the method name:

```bash
> autonity.totalSupply().call()
'80000'
```

Use `.send()` for `Autonity `and `web3` calls to submit state affecting transactions, appending `. send()` to the method name:

```bash
> autonity.transfer('<_recipient>', <_amount>).send({from: myAddress, gas: gas})
```

Console configuration for use of `.send()` is described in the How to Submit a transaction from Autonity NodeJS Console.

#### JavaScript Object Prototype functions

`Node.JS` automatically attaches the following prototype functions to a JavaScript object at runtime. These functions are displayed for both `web3` and `autonity` namespaces in the Autonity NodeJS Console but are **unused**. For the function definitions see the linked Mozilla Developer Network Reference documentation.


| Field | MDN Web Docs Reference |
|-------|-------------|
|`.__defineGetter__`|[`Object.prototype.__defineGetter__()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/__defineGetter__)|
|`.__defineSetter__`|[`Object.prototype.__defineSetter__()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/__defineSetter__)|
|`.__lookupGetter__`|[`Object.prototype.__lookupGetter__()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/__lookupGetter__)|
|`.__lookupSetter__`|[`Object.prototype.__lookupSetter__()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/__lookupSetter__)|
|`.__proto__`|[`Object.prototype.__proto__`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/proto)|
|`.hasOwnProperty`|[`Object.prototype.hasOwnProperty()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty)|
|`.isPrototypeOf`|[`Object.prototype.isPrototypeOf()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isPrototypeOf)|
|`.propertyIsEnumerable`|[`Object.prototype.propertyIsEnumerable()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/propertyIsEnumerable)|
|`.toLocaleString`|[`Object.prototype.toLocaleString()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/toLocaleString)|
|`.toString`|[`Object.prototype.toString()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/toString)|
|`.valueOf`|[`Object.prototype.valueOf()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/valueOf)|
|`.constructor`|[`Object.prototype.constructor`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/constructor)|

#### Exiting the console

To exit the console press `^C` twice or type `.exit`.


### RPC Calls
#### Calling the Ethereum `web3` API

Enter `web3.<tab>` to see a list of available function calls:

```bash
> web3.
web3.__defineGetter__      web3.__defineSetter__      web3.__lookupGetter__
web3.__lookupSetter__      web3.__proto__             web3.hasOwnProperty
web3.isPrototypeOf         web3.propertyIsEnumerable  web3.toLocaleString
web3.toString              web3.valueOf

web3.constructor

web3.BatchRequest          web3._provider             web3._requestManager
web3.admin                 web3.bzz                   web3.currentProvider
web3.eth                   web3.extend                web3.givenProvider
web3.net                   web3.personal              web3.providers
web3.rpc                   web3.setProvider           web3.setRequestManager
web3.shh                   web3.tendermint            web3.txpool
web3.utils                 web3.version
```

##### Console functions

###### JavaScript Object Prototype functions

As noted [above](/reference/cli#javascript-object-prototype-functions), these prototype functions added by  `Node.JS` are **unused**.

###### Web3 method calls

For the function definitions see the linked `web3.js` and upstream Geth JSON-RPC API Reference in the [Autonity Interfaces](/reference/api/) documentation.

| Field | Reference - web3.js| Reference - JSON-RPC API |
|-------|-----------|-----------------|
| `web3.BatchRequest` | [`BatchRequest`](https://web3js.readthedocs.io/en/v1.2.11/web3.html?highlight=web3.BatchRequest#batchrequest) |
| `web3._provider` | | |
| `web3._requestManager` | | |
| `web3.admin` | | Geth [`admin`](https://geth.ethereum.org/docs/rpc/ns-admin) |
| `web3.bzz` | [`bzz`](https://web3js.readthedocs.io/en/v1.2.11/web3-bzz.html) |
| `web3.currentProvider` | [`currentProvider`](https://web3js.readthedocs.io/en/v1.2.11/web3.html#currentprovider) |
| `web3.eth` | [`eth`](https://web3js.readthedocs.io/en/v1.2.11/web3-eth.html) |  Geth [`eth`](https://geth.ethereum.org/docs/rpc/ns-eth) |
| `web3.extend` | [`extend`](https://web3js.readthedocs.io/en/v1.2.11/web3.html#extend) |
| `web3.givenProvider` | [`givenProvider`](https://web3js.readthedocs.io/en/v1.2.11/web3.html#givenprovider) |
| `web3.net` | [`*.net`](https://web3js.readthedocs.io/en/v1.2.11/web3-net.html?highlight=web3.net#) |
| `web3.personal` | [`eth.personal`](https://web3js.readthedocs.io/en/v1.2.11/web3-eth-personal.html#eth-personal) | Geth [`personal`](https://geth.ethereum.org/docs/rpc/ns-personal) |
| `web3.providers` | [`providers`](https://web3js.readthedocs.io/en/v1.2.11/web3.html#providers) |
| `web3.rpc` | | Geth [`JSON-RPC Server`](https://geth.ethereum.org/docs/rpc/server) |
| `web3.setProvider` | [`setProvider`](https://web3js.readthedocs.io/en/v1.2.11/include_package-core.html?highlight=.setProvider) |
| `web3.setRequestManager` | |
| `web3.shh` | [`shh`](https://web3js.readthedocs.io/en/v1.2.11/web3-shh.html) |
| `web3.tendermint` | | |
| `web3.txpool` | | Geth [`txpool`](https://geth.ethereum.org/docs/rpc/ns-txpool) |
| `web3.utils` | [`utils`](https://web3js.readthedocs.io/en/v1.2.11/web3-utils.html) |
| `web3.version` | [`version`](https://web3js.readthedocs.io/en/v1.2.11/web3.html#version) |

#### Calling the `autonity` Protocol Contract Interface

Enter `autonity.<tab>` to see a list of available function calls.

```bash
> autonity.
autonity.__defineGetter__       autonity.__defineSetter__
autonity.__lookupGetter__       autonity.__lookupSetter__
autonity.__proto__              autonity.constructor
autonity.hasOwnProperty         autonity.isPrototypeOf
autonity.propertyIsEnumerable   autonity.toLocaleString
autonity.toString               autonity.valueOf

autonity.allowance              autonity.approve
autonity.balanceOf              autonity.bond
autonity.burn                   autonity.computeCommittee
autonity.config                 autonity.deployer
autonity.epochID                autonity.epochReward
autonity.epochTotalBondedStake  autonity.finalize
autonity.getBondingReq          autonity.getCommittee
autonity.getCommitteeEnodes     autonity.getMaxCommitteeSize
autonity.getMinimumBaseFee      autonity.getNewContract
autonity.getOperator            autonity.getProposer
autonity.getUnbondingReq        autonity.getValidator
autonity.getValidators          autonity.getVersion
autonity.headBondingID          autonity.headUnbondingID
autonity.lastEpochBlock         autonity.mint
autonity.name                   autonity.registerValidator
autonity.setCommitteeSize       autonity.setEpochPeriod
autonity.setMinimumBaseFee      autonity.setOperatorAccount
autonity.setTreasuryAccount     autonity.setTreasuryFee
autonity.setUnbondingPeriod     autonity.symbol
autonity.tailBondingID          autonity.tailUnbondingID
autonity.totalRedistributed     autonity.totalSupply
autonity.transfer               autonity.transferFrom
autonity.unbond                 autonity.upgradeContract

```

##### Console functions

###### JavaScript Object Prototype functions

As noted [above](/reference/cli#javascript-object-prototype-functions), these prototype functions added by  `Node.JS` are **unused**.

###### Autonity method calls

For the function definitions see the linked [Autonity Interfaces](/reference/api/) Reference documentation for the Autonity Protocol Contract functions. If accessing the method is constrained to the protocol or governance account is shown.

| Field | Reference | Access constraint? |
|-------|-----------|-----------------|
| `autonity.allowance` | [`allowance`](/reference/api/aut/#allowance) |
| `autonity.approve` | [`approve`](/reference/api/aut/#approve) |
| `autonity.balanceOf` | [`balanceOf`](/reference/api/aut/#balanceof) |
| `autonity.bond` | [`bond`](/reference/api/aut/#bond) |
| `autonity.burn` | [`burn`](/reference/api/aut/op-prot/#burn) | onlyOperator |
| `autonity.computeCommittee` | [`computeCommittee`](/reference/api/aut/op-prot/#computecommittee) | onlyProtocol |
| `autonity.config` | [`config`](/reference/api/aut/#config) |
| `autonity.deployer` | [`deployer`](/reference/api/aut/#deployer) |
| `autonity.epochID` | [`epochID`](/reference/api/aut/#epochid) |
| `autonity.epochReward` | [`epochReward`](/reference/api/aut/#epochreward) |
| `autonity.epochTotalBondedStake` | [`epochTotalBondedStake`](/reference/api/aut/#epochtotalbondedstake) |
| `autonity.finalize` | [`finalize`](/reference/api/aut/op-prot/#finalize) | onlyProtocol
| `autonity.getBondingReq` | [`getBondingReq`](/reference/api/aut/#getbondingreq) |
| `autonity.getCommittee` | [`getCommittee`](/reference/api/aut/#getcommittee) |
| `autonity.getCommitteeEnodes` | [`getCommitteeEnodes`](/reference/api/aut/#getcommitteeenodes) |
| `autonity.getMaxCommitteeSize` | [`getMaxCommitteeSize`](/reference/api/aut/#getmaxcommitteesize) |
| `autonity.getMinimumBaseFee` | [`getMinimumBaseFee`](/reference/api/aut/#getminimumbasefee) |
| `autonity.getNewContract` | [`getNewContract`](/reference/api/aut/#getnewcontract) |
| `autonity.getOperator` | [`getOperator`](/reference/api/aut/#getoperator) |
| `autonity.getProposer` | [`getProposer`](/reference/api/aut/#getproposer) |
| `autonity.getUnbondingReq` | [`getUnbondingReq`](/reference/api/aut/#getunbondingreq) |
| `autonity.getValidator` | [`getValidator`](/reference/api/aut/#getvalidator) |
| `autonity.getValidators` | [`getValidators`](/reference/api/aut/#getvalidators) |
| `autonity.getVersion` | [`getVersion`](/reference/api/aut/#getversion) |
| `autonity.headBondingID` |  [`headBondingID`](/reference/api/aut/#headbondingid) |
| `autonity.headUnbondingID` | [`headUnbondingID`](/reference/api/aut/#headunbondingid) |
| `autonity.lastEpochBlock` | [`lastEpochBlock`](/reference/api/aut/#lastepochblock) |
| `autonity.mint` |[`mint`](/reference/api/aut/op-prot/#mint) | onlyOperator |
| `autonity.name`| [`name`](/reference/api/aut/#name) |
| `autonity.registerValidator` | [`registerValidator`](/reference/api/aut/#registervalidator) |
| `autonity.setCommitteeSize` |[`setCommitteeSize`](/reference/api/aut/op-prot/#setcommitteesize) | onlyOperator |
| `autonity.setEpochPeriod` |[`setEpochPeriod`](/reference/api/aut/op-prot/#setepochperiod) | onlyOperator |
| `autonity.setMinimumBaseFee` |[`setMinimumBaseFee`](/reference/api/aut/op-prot/#setminimumbasefee) | onlyOperator |
| `autonity.setOperatorAccount` |[`setOperatorAccount`](/reference/api/aut/op-prot/#setoperatoraccount) | onlyOperator |
| `autonity.setTreasuryAccount` |[`setTreasuryAccount`](/reference/api/aut/op-prot/#settreasuryaccount) | onlyOperator |
| `autonity.setTreasuryFee` |[`setTreasuryFee`](/reference/api/aut/op-prot/#settreasuryfee) | onlyOperator |
| `autonity.setUnbondingPeriod` |[`setUnbondingPeriod`](/reference/api/aut/op-prot/#setunbondingperiod) | onlyOperator |
| `autonity.symbol` | [`symbol`](/reference/api/aut/#symbol) |
| `autonity.tailBondingID` | [`tailBondingID`](/reference/api/aut/#tailbondingid) |
| `autonity.tailUnbondingID` | [`tailUnbondingID`](/reference/api/aut/#tailunbondingid) |
| `autonity.totalRedistributed`| [`totalRedistributed`](/reference/api/aut/#totalredistributed) |
| `autonity.totalSupply` | [`totalSupply`](/reference/api/aut/#totalsupply) |
| `autonity.transfer` | [`transfer`](/reference/api/aut/#transfer) |
| `autonity.transferFrom` | [`transferFrom`](/reference/api/aut/#transferfrom) |
| `autonity.unbond` | [`unbond`](/reference/api/aut/#unbond) |
| `autonity.upgradeContract` | [`upgradeContract`](/reference/api/aut/op-prot/#upgradecontract) | onlyOperator |


#### Calling the `Liquid Newton Contract` interface `Staking Wallet` functions

The Node JS Console provides `Staking Wallet` functions for a stake delegator to:

 - View information about registered validators on the network
 - view stake delegations: the delegator's own Liquid Newton holding and claimable reward balances
 - Claim rewards
 - Send Liquid Newton to another account.

The functions are accessible from the default context: a module namespace prefix is not required when calling.

For the function definitions see the linked [Autonity Interfaces](/reference/api/liquid-newton) Reference documentation for the Autonity Liquid Newton Contract functions available from the NodeJS Console.

| Function| Reference |
|-------|-----------|
| `vals()` Print validator information | [`vals`](/reference/api/liquid-newton/#vals-_print-validator-information_) |
| `wal()` Print Staking Wallet | [`wal`](/reference/api/liquid-newton/#wal-_print-staking-wallet_) |
| `rclm()` Claim staking rewards for single stake delegation | [`rclm`](/reference/api/liquid-newton/#rclm-_claim-staking-rewards_) |
| `rclm_a()` Claim staking rewards for all stake delegations | [`rclm_a`](/reference/api/liquid-newton/#rclm_a-_claim-all-staking-rewards_) |
| `lsend()` Send Liquid Newton| [`lsend`](/reference/api/liquid-newton/#lsend-_send-liquid-newton_) |


## Geth Javascript Console

The Geth JavaScript Console provides a JavaScript runtime environment for executing RPC calls encoded as JSON objects.

The console is deprecated in favour of the [Autonity NodeJS Console](/reference/utility-tools/#javascript-cli-nodejs-console) as an interactive JavaScript environment for Autonity.


::: {.callout-important title="Warning" collapse="false"}
The console remains in the codebase but is not officially supported. It may be used with this caveat.
:::

### Usage

For how to invoke and use the CLI see the Geth docs [JavaScript Console](https://geth.ethereum.org/docs/interface/javascript-console).

# Built in functions

TODO: old Node JS Console built-in functions content

Interface for interacting with Autonity Liquid Newton Contract using wrapper functions implemented by the NodeJS Console. Function calls do not require the `.call()` or `.send()` suffix.

Datatypes are [Solidity v0.8.3 Types](https://docs.soliditylang.org/en/v0.8.3/types.html#).

{{pageinfo}}
Examples use the setup described in the How to's:

- [Submit a transaction from Autonity NodeJS Console](/account-holders/submit-trans-nodejsconsole/)
- [Claim Staking Rewards](/delegators/claim-rewards/)
- [Transfer Liquid Newton](/delegators/transfer-lntn/).
{{/pageinfo}}

{{pageinfo}}
- `unclaimedRewards()`: returns the total amount of rewards available and pending retrieval
- `claimRewards()`: claims the sender's pending rewards.
{{/pageinfo}}

## `vals` _Print validator information_

Displays the list of current registered validators.

### Parameters

None.

### Response

Displays a formatted list of `Validator` object data for each registered validator, sorted by registration index in ascending order. I.E. the last processed registration request has the highest index identifier value and is always the last result returned.


`Validator` object information returned consists of:

| Field | Datatype | Description |
| --| --| --|
| `treasury` | `address payable` | the address that will receive staking rewards the validator earns |
| `addr` | `address` | the validator identifier account address |
| `enode` | `string` | the enode url of the validator node |
| `delegationRate` | `uint256` | the percentage commission that the validator will charge on staking rewards from delegated stake |
| `bondedStake` | `uint256` | the total amount of delegated and self-bonded stake that has been bonded to the validator |
| `totalSlashed` | `uint256` | a counter of the number of times that a validator has been penalised for accountability and omission faults since registration |
| `liquidContract` | `Liquid` | the address of the validator's Liquid Newton contract |
| `liquidSupply` | `uint256` | the total amount of the validator's Liquid Newton in circulation |
| `registrationBlock` | `uint256` | the block number in which the registration of the validator was committed to state|
| `state` | `ValidatorState` | the state of the validator. `ValidatorState` is an enumerated type with enumerations: `active`, `paused` |


### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
vals()
{{< /tab >}}
{{< /tabpane >}}


### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
> vals()

__________________________Validator 0__________________________
treasury:            0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C
addr:                0x07d872935972Aa0848d0cec9c67b270E5291D7e8
enode:               enode://bb9bb2bcd75a5cde083a6a9be2c28f31d9fd6e8de38baa594ffffab0efc5d26524b91baf002fed32f098db71acf0d7646a7c32a7d05ed89fdbbb78c74db13a1a@51.89.151.55:30303
commissionRate:      1000
bondedStake:         10000
totalSlashed:        0
liquidContract:      0xf4D9599aFd90B5038b18e3B551Bc21a97ed21c37
liquidSupply:        10000
registrationBlock:   0
state:               0

__________________________Validator 1__________________________
treasury:            0xd4EdDdE5D1D0d7129a7f9C35Ec55254f43b8E6d4
addr:                0x45998C7d6341CD32256E9eeEdd9865450d4aCB18
enode:               enode://e89196cae37e8041e14d7a063cc82dec3bb351f79f46ab10a059220403932c1337f144ddbf1fd830bf1221fbf539a4e986c924600b060c0a36337256aa70ee2c@51.89.151.55:40303
commissionRate:      1000
bondedStake:         11360
totalSlashed:        0
liquidContract:      0x109F93893aF4C4b0afC7A9e97B59991260F98313
liquidSupply:        11360
registrationBlock:   0
state:               0

__________________________Validator 2__________________________
...
{{< /tab >}}
{{< /tabpane >}}



## `wal` _Print Staking Wallet_
Display holding in LNTN and claimable rewards for the specified account.


### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | account address of the stake delegator  |

### Response

Displays an index-sorted list of all the stake delegations from the specified (i.e. _Staking Wallet_) account, showing:

- `Account`: the _staking Wallet_ account address

Then, a table showing stake delegations sorted by validator index:

- `(index)`: the validator index, i.e. if the 1st or nth validator registered in the network.
- `validator`: the unique [validator identifier](/concepts/validator/#validator-identifier).
- `lntn`: the amount of Liquid Newton the staker owns for that validator.
- `claimableRewards`: the amount of rewards the staker can claim from the stake delegation, denominated in [ton](/glossary/#ton), auton's wei equivalent.


### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
wal('account')
{{< /tab >}}
{{< /tabpane >}}


### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
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
{{< /tab >}}
{{< /tabpane >}}

## `rclm` _Claim staking rewards_
Claims staking rewards for a specified staking delegation.

Calls the `claimRewards()` function for the specified validator. The sender's account must be unlocked to call.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | the account address of the sender. This is the sender's _Staking Wallet_ account: the staker address that owns the liquid newton being sent |
| `validator` | `address` | the unique [validator identifier](/concepts/validator/#validator-identifier) of the validator stake delegation from which liquid newton is being sent |


### Response

Displays the validator and staker addresses, the amount of claimable rewards from that validator, and the transaction receipt.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
rclm('account','validator')
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
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
{{< /tab >}}
{{< /tabpane >}}

## `rclm_a` _Claim all staking rewards_
Claims staking rewards for all of the sender's stake delegations.

Calls the `claimRewards()` function for every validator stake delegation with a non 0 `unclaimedRewards()` balance. The sender's account must be unlocked to call.


### Parameters

| Field | Datatype | Description |
| --| --| --|
| `account` | `address` | the account address of the sender. This is the sender's _Staking Wallet_ account: the staker address that owns the liquid newton being sent |

### Response

Displays a listing of each validator you have delegated to, your claimable reward for each validator stake delegation, and the total amount of rewards claimed.


### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
rclm_a('account')
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
> rclm_a('0x11A87b260Dd85ff7189d848Fd44b28Cc8505fa9C')
    validator:          0x07d872935972Aa0848d0cec9c67b270E5291D7e8
    claimable reward:   213928433236770

    validator:          0x45998C7d6341CD32256E9eeEdd9865450d4aCB18
    claimable reward:   29094266920200


    total claimed:        243022700156970
{{< /tab >}}
{{< /tabpane >}}



## `lsend` _Send Liquid Newton_
Transfers an amount of Liquid Newton from a stake delegation to another account.

Calls the `transfer()` function for the specified validator. The sender's account must be unlocked to call.

### Parameters

| Field | Datatype | Description |
| --| --| --|
| `val` | `address` | the unique [validator identifier](/concepts/validator/#validator-identifier) of the validator stake delegation from which liquid newton is being sent |
| `from` | `address` | the account address of the sender. This is the sender's _Staking Wallet_ account: the staker address that owns the liquid newton being sent |
| `to` | `address` | the account address of the recipient. |
| `value` | `uint256 ` | the amount of liquid newton being sent |

### Response

None.

### Event

On a successful call the function emits a Transfer event, logging: `msg.sender`, `to`, `amount`.

### Usage

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
lsend({'from','to','val',value})
{{< /tab >}}
{{< /tabpane >}}

### Example

{{< tabpane langEqualsHeader=true >}}
{{< tab header="NodeJS Console" >}}
> lsend({from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c', to: '0xd4eddde5d1d0d7129a7f9c35ec55254f43b8e6d4', val: '0x45998C7d6341CD32256E9eeEdd9865450d4aCB18', value: 100})
Sending 100 LNTN - Validator 0x45998C7d6341CD32256E9eeEdd9865450d4aCB18
{
  blockHash: '0xa883dc4beffebc5a903ecc3d0f1fbc7dad97d7ccaeea0bd580ac124ea8b7ddf4',
  blockNumber: 36016,
  contractAddress: null,
  cumulativeGasUsed: 63512,
  effectiveGasPrice: 12500000000,
  from: '0x11a87b260dd85ff7189d848fd44b28cc8505fa9c',
  gasUsed: 63512,
  logsBloom: '0x00000000000000000000000000000400000000010000000000000000000000000000000000000000000000000000000004000000000000000000000001000000000000000000000000040008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000002000000000000000000000000000000000000000000000002000000000000000000000000000000000000000080000000000000000000001000000000',
  status: true,
  to: '0x109f93893af4c4b0afc7a9e97b59991260f98313',
  transactionHash: '0x844b8bf3c165a20a93b15586acdfe263a55445519f3b01d98324bea2300ab32d',
  transactionIndex: 0,
  type: '0x2',
  events: {
    Transfer: {
      address: '0x109F93893aF4C4b0afC7A9e97B59991260F98313',
      blockNumber: 36016,
      transactionHash: '0x844b8bf3c165a20a93b15586acdfe263a55445519f3b01d98324bea2300ab32d',
      transactionIndex: 0,
      blockHash: '0xa883dc4beffebc5a903ecc3d0f1fbc7dad97d7ccaeea0bd580ac124ea8b7ddf4',
      logIndex: 0,
      removed: false,
      id: 'log_67107f69',
      returnValues: [Result],
      event: 'Transfer',
      signature: '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
      raw: [Object]
    }
  }
}
{{< /tab >}}
{{< /tabpane >}}
