
---
title: "Architecture "
description: >
  Architecture of Autonity - protocol primitives and system model layers
---

## Overview

Autonity is an EVM-based blockchain which extends the Ethereum protocol to add Autonity-specific functionality to optimise the creation and maintenance of decentralised markets. This section documents the details of these Autonity extensions. An understanding of the core Ethereum principles is assumed.

Autonity inherits from Ethereum:

- The blockchain structure comprising the distributed ledger of the system.
- Peer-to-peer networking protocols forming the communication layer of the system for message broadcast between network peer nodes.
- The EVM and smart contract technology comprising the application level of the system.

Autonity extends Ethereum at three logical layers:

- Protocol smart contracts: the Autonity protocol is deployed in part via protocol smart contracts:

	- **Autonity Protocol Contract** implementing protocol primitives for governance, tokenomics,  liquid staking, block finalisation, and rewards distribution.
	- **Liquid Newton** contracts for validator-specific liquid stake tokens.
	- **Accountability Contracts** implementing protocol primitives for accountable and omission fault detection for validators participating in the consensus committee. The consensus accountability protocol enforces validator liveness and adherence to the [Tendermint consensus](/concepts/consensus/pos/) rules, implementing slashing penalties and a [Penalty-Absorbing Stake (PAS)](/concepts/afd/#penalty-absorbing-stake-pas) model.
	- **Autonity Oracle Contract** implementing protocol primitives for the oracle protocol. It provides functionality for computing aggregated weighted average price data from external price data and managing the set of currency pairs for which Autonity's [oracle network](/concepts/oracle-network/) provides price data. It provides functionality for an oracle accountability protocol incentivising timely participation in oracle voting rounds and the submission of accurate oracle price reports by validators.
	- **Auton Stabilization Mechanism Contracts** implementing a [Stabilization Mechanism](/concepts/asm/) for the protocol's native coin [Auton](/concepts/protocol-assets/auton/) via a Collateralized Debt Position (CDP). Changes in supply and demand for Auton are absorbed by dynamically adjusting CDP incentives to increase and decrease Auton borrowing costs when Auton price moves above or below its Stabilization Target the [Autonomous Currency Unit (ACU)](/glossary/#acu).
	- **Inflation Controller Contract** implementing logic for controlling [Newton inflation](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) emissions according to the Newton inflation schedule.
	
	Autonity Protocol smart contracts are part of the client binary. _Liquid Newton_ smart contracts are deployed on validator registration.

- Consensus layer: blockchain consensus provided by the **[Proof of Stake Tendermint BFT](/concepts/consensus/pos/)** protocol. Blocks are proposed by validators and selected by the committee for inclusion in the blockchain, with finality. The consensus mechanism enables dynamic consensus committee selection using a stake-weighting algorithm, maximising the amount of stake securing the system.
- Communication layer: peer-to-peer networking is modified to enable the gossiping of transaction and consensus information among validators and participant nodes in separate consensus and transaction gossiping channels.  See [P2P networking protocols](/concepts/system-model/#p2p-networking-protocols).


## Protocol contracts

The Autonity Protocol Contracts are deployed by the node when it is initialised and run for the first time.

### Protocol contract addresses

The protocol contract account addresses are computed at contract creation according to the standard Ethereum protocol rules for contract account creation when deploying a contract: a function of the [deployer](/reference/api/aut/#deployer) address, and the count of transactions sent from that account: the account `nonce`.

These values are constant and predictable:

- the null or 'zero' account address `0x0000000000000000000000000000000000000000` is used as the [deployer](/reference/api/aut/#deployer) address.
- the account nonce increments  by `1` linear to the order of deployment, beginning at `0`.

Consequently, the Autonity Protocol Contract addresses for a network are deterministic and will always be the same.

The order of deployment and computed addresses is:

| Contract | Address |
|:--:|:--|
| Autonity Protocol Contract | `0xBd770416a3345F91E4B34576cb804a576fa48EB1` |
| Accountability Contract | `0x5a443704dd4B594B382c22a083e2BD3090A6feF3` |
| Oracle Contract | `0x47e9Fbef8C83A1714F1951F142132E6e90F5fa5D` |
| ACU Contract | `0x8Be503bcdEd90ED42Eff31f56199399B2b0154CA` |
| Supply Control Contract | `0x47c5e40890bcE4a473A49D7501808b9633F29782` |
| Stabilization Contract | `0x29b2440db4A256B0c1E6d3B4CDcaA68E2440A08f` |
| Upgrade Manager Contract | `0x3C368B86AF00565Df7a3897Cfa9195B9434A59f9` |
| Inflation Controller Contract | `0x3BB898B4Bbe24f68A4e9bE46cFE72D1787FD74F4` |
| Omission Accountability Contract | `0x117814AF22Cb83D8Ad6e8489e9477d28265bc105` |
| Auctioneer Contract | `0x6901F7206A34E441Ac5020b5fB53598A65547A23` |


### Autonity Protocol Contract
The contract implements many of the Autonity protocol extensions, including primitives for governance, staking, validators, consensus committee selection, and staking reward distribution.

The contract stores [protocol parameters](/reference/protocol/) that specify the economic, consensus, and governance settings of an Autonity network. Protocol parameters are initialised at network [genesis](/reference/genesis/) in the genesis state provided by the client's config for connecting to public Autonity networks, or a custom [genesis configuration file](/reference/genesis/#genesis-configuration-file) if running a local development network.

Many of the Autonity Protocol Contract functions can be called by all participants, such as those for bonding and unbonding stake, and for reading protocol parameters.  Some functions are restricted to the governance `operator` account, such as those related to governance of network parameters.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Autonity Contract Interface](/reference/api/aut/), governance under [Governance and Protocol Only Reference](/reference/api/aut/op-prot/).

#### Governance

Autonity system governance is executed:

- At genesis, when the blockchain is initialised with the genesis state.
- After genesis by the `operator` governance account, by calling the restricted functions of the protocol contract.

Governance operations are used to modify protocol parameterisation set in the genesis system state and enable an Autonity network to evolve dynamically over time. System protocol parameters modifiable by governance include:

- Governance and protocol contract account addresses.
- Protocol parameters to adjust the network configuration after genesis.

For all parameter definitions and the subset of modifiable parameters see the [Protocol Parameter](/reference/protocol/) reference and the Autonity Contract Interface [Governance and Protocol Only Reference](/reference/api/aut/op-prot/).

#### State finalization
The Autonity Protocol Contract manages state finalization, maintaining [system state](/glossary/#system-state). Contract logic triggers block finalization.

At epoch end finalization:

- invokes finalise on the accountability and oracle contracts:
  - [Accountability Contract](/concepts/architecture/#autonity-accountability-contract) to apply [slashing](/concepts/afd/#slashing) penalties for proven accountability faults
  - [Autonity Omission Accountability Contract](/concepts/architecture/#autonity-omission-accountability-contract) to apply [slashing](/concepts/afd/#slashing) penalties for proven omission accountability faults
  - [Oracle Contract](/concepts/architecture/#autonity-oracle-contract) to apply [slashing](/concepts/afd/#slashing) penalties for proven oracle accountability faults
- invokes the [Newton Inflation Controller Contract](/concepts/architecture/#newton-inflation-controller-contract) to compute Newton inflation emissions per the [Newton Inflation Mechanism](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation)
- invokes [distribution of ATN and NTN fees and rewards](/concepts/architecture/#reward-distribution) to Autonity protocol treasury, committee member validators, and stake delegators
- applies [staking transitions](/concepts/staking/#staking-transitions) for stake bonding and unbonding
- applies pending [validator commission rate changes](/concepts/validator/#validator-commission-rate-change)
- selects a new [consensus committee](/concepts/architecture/#committee-selection) for the following epoch
- invokes the [Oracle Contract](/concepts/architecture/#autonity-oracle-contract) to [select oracle voters for the following epoch](/concepts/architecture/#voter-selection)
- invokes the [Oracle Contract](/concepts/architecture/#autonity-oracle-contract) for the [computation of weighted average price data](/concepts/architecture/#weighted-average-price-computation) at the end of an [oracle voting round](/concepts/oracle-network/#voting-rounds).

To learn more about the finalization logic see the protocol only `finalize()` functions in the [Governance and Protocol Only Reference](/reference/api/aut/op-prot/).

#### Staking
The Autonity Protocol Contract manages liquid staking,  maintaining the ledger of _Newton_ stake token in the system and triggering the deployment of validator-specific _Liquid Newton_ contracts. The contract implements logic to:

- Maintain the ledger of _Newton_ stake token in the system, implementing the ERC20 token contract interface.
- Facilitate liquid staking by triggering the deployment of validator-specific _Liquid Newton_ ERC20 contracts as validators are registered on the system.
- Provide stakeholders standard ERC20 token operations for accessing the _Newton_ stake token ledger and metadata.
- Provide stakeholders operations to bond and unbond stake from validators, managing _Newton_ staking transitions and _Liquid Newton_ emission and redemption.
- Provide an [autobond](/glossary/#autobond) operation to automatically bond [Newton inflation emissions](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation).
- Manage staking transitions, tracking bond and unbond requests until staking transitions are applied at the end of the epoch.
- Trigger application of stake slashing penalties, calling the Autonity Accountability Contracts to apply slashing penalties at epoch end for [consensus accountability faults](/concepts/architecture/#autonity-accountability-contract), [consensus omission faults](/concepts/architecture/#autonity-omission-accountability-contract), and [oracle accountability faults](/concepts/architecture/#autonity-oracle-contract).

To learn more about the concept see [Staking](/concepts/staking/).

#### Validators
The Autonity Protocol Contract implements logic to manage validator registration and lifecycle on the system:

- Provides public contract functions to register new validators and query for existing registered validators.
- Trigger the deployment of validator-specific _Liquid Newton_ ERC20 contracts as validators are registered on the system.
- Provide lifecycle management functions, allowing validator operators to manage their validator and its lifecycle: pause and reactive validator, change commission rate.

To learn more about the concept see [Validators](/concepts/validator/).

#### Committee selection
Computing the committee is a protocol only function. As the last block of an epoch is finalized, this function is executed to determine the committee for the following epoch.

The committee is selected from the registered validators maintained in the system state by the Autonity contract. Validators are ranked by bonded stake, with those having the highest stake being selected for the available committee membership slots. This stake weighting maximises the amount of stake securing the system in each new committee. Each block header records the consensus committee members who voted to approve the block.

To learn more about the concept see [Consensus](/concepts/consensus/) and  [Committee](/concepts/consensus/committee/).

#### Reward distribution

Validators and stake delegators are incentivised by the distribution of [staking rewards](/glossary/#staking-rewards) and Newton [inflation rewards](/glossary/#inflation-rewards) for stake bonded to the active consensus committee. Staking rewards are paid in Auton. Newton inflation rewards are [automatically bonded](/glossary/#autobond).

Staking rewards accumulate from transaction fees collected by the transaction fee mechanism as blocks are finalized by the committee:

- Block _priority fees_ are distributed to block proposers at time intervals matching block generation times.
- Block _base fees_ are added to the rewards pool and distributed at the end of the epoch.

The rewards pool is held in a protocol account until reward distribution occurs as the final block of an epoch is committed to state. Consensus committee members are rewarded proportionally to their share of the bonded stake (the 'voting power') securing the committee.

When distribution occurs:

- A percentage determined by the protocol `treasuryFee` parameter is deducted and transferred to the protocol treasury account for community funds.
- Rewards are distributed to the treasury account of each committee member (validator) on a _pro rata_ basis, depending on their share of the bonded stake in the consensus committee.
- A percentage determined by the validator `commissionRate` parameter is deducted and transferred to the validator treasury account as a commission fee. The initial commission rate is set globally for all validators in the network, specified by the `delegationRate` protocol parameter in the genesis configuration file.  Individual validators can modify their commission rate after registration.
- Rewards are distributed to stake delegator accounts _pro rata_ according to their share of the stake bonded to the validator.
- Rewards accumulate until claimed by stake delegators. 

To learn more about the concept see [Staking rewards and distribution](/concepts/staking/#staking-rewards-and-distribution) and [Staking accounts](/concepts/staking/#staking-accounts).

Inflation rewards accumulate from the [Newton Inflation Mechanism](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) and are awarded for Newton stake token that has been delegated to validators in the consensus committee. The emissions are:

- Computed for stake bonded to the consensus committee members according to the Newton [inflation mechanism](/glossary/#inflation-mechanism) (note inflation rewards are _only_ earned for stake actively securing the network - stake delegations to validators that _are not_ in the current consensus committee _will not_ earn inflation rewards).
- The Newton inflation emission is minted from the [inflation reserve](/glossary/#inflation-mechanism) and [automatically bonded](/glossary/#autobond). Block _base fees_ are added to the rewards pool and distributed at the end of the epoch.

To learn more about the concept see [Total supply and Newton inflation ](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) in the [Newton](/concepts/protocol-assets/newton) concept.

### Autonity Accountability Contract
The contract implementing the Accountability Fault Detection (AFD) protocol extensions, including primitives for misbehaviour accusations, proving innocence against an accusation, proven faults, slashing, and jailing.

The contract stores [protocol configuration](/concepts/afd/#protocol-configuration) parameters used to compute slashing penalties. Contract functions are called by validators whilst participating in the AFD protocol to:

- Return a committee member's proven faults
- Determine if a new accusation can be made and is slashable
- Submit accountability events.

Function calls to compute accountability at each block and apply accountability penalties at epoch end are restricted to protocol.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Accountability Contract Interface](/reference/api/afd/), governance under [Governance and Protocol Only Reference](/reference/api/aut/op-prot/).

#### Accountability event handling
The Autonity Accountability Contract implements logic for handling accountability events submitted by committee members on-chain:

- Accusations of misbehaviour for a committee member failing to follow consensus rules correctly.
- Proofs of innocence submitted in defence against accusations. They must be presented within the constraints of an innocence window measured in blocks to be valid. An accusation successfully defended gets deleted.
- Promotion of accusations to faults when feasible after expiry of the innocence window.
- Direct submission of unforgeable faults. These lead to slashing without possibility of being defended by proof of innocence.

#### Slashing penalty computation
The Autonity Accountability Contract manages the computation of accountability penalties for proven faults at epoch end. Penalties are slashing of stake token per Autonity’s Penalty-Absorbing Stake (PAS) model and validator jailing.

A slashing model is implemented where a committee member is only slashed for the highest severity fault committed in an epoch. The contract implements logic to:

- Calculate slashing penalties based on parameters set in the [protocol configuration](/concepts/afd/#protocol-configuration) and dynamic factors specific to the epoch circumstances. See [slashing amount calculation](/concepts/afd/#slashing-amount-calculation).
- Apply slashing according to Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/afd/#penalty-absorbing-stake-pas) model: validator self-bonded stake is slashed first until exhausted, then delegated stake.
- Depending upon fault severity, a slashing penalty may also apply temporary or permanent validator jailing to bar the validator from committee selection. The severity of the jailing period is influenced by the severity of the fault committed and the validator's slashing history over time. See [Jail period calculation](/concepts/afd/#jail-period-calculation).

To learn more about the concept see [Accountability Fault Detection (AFD)](/concepts/afd/).

### Autonity Omission Accountability Contract
The contract implementing the Omission Fault Detection (OFD) protocol extensions, including primitives for detecting failure to participate in consensus voting rounds, slashing, and jailing.

The contract stores [protocol configuration](/concepts/ofd/#protocol-configuration) parameters used to compute slashing penalties.

Function calls to detect validator inactivity at each block and apply omission penalties at epoch end are restricted to protocol.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Accountability Contract Interface](/reference/api/afd/), governance under [Governance and Protocol Only Reference](/reference/api/aut/op-prot/).

#### Inactivity scoring
The Autonity Omission Accountability Protocol implements logic for measuring if a committee member is actively participating in consensus voting rounds:

- Measures validator activity by recording precommit messages as a cryptographically-verifiable BLS aggregate signature ($ActivityProof$) generated by the block proposer and included in the block headers.
- Maintains an inactivity score for committee members during the epoch, computed as a percentage of blocks in an epoch that the validator has failed to participate in consensus for.

#### Slashing penalty computation
The Autonity Omission Accountability Contract manages the computation of omission penalties for proven faults at epoch end. A slashing model is implemented with penalties increasing in severity as inactivity thresholds are passed. The contract implements logic to:

- Calculate penalties based on parameters set in the [protocol configuration](/concepts/ofd/#protocol-configuration) and dynamic factors specific to the epoch circumstances. See [slashing amount calculation](/concepts/ofd/#slashing-amount-calculation).

Depending upon the validator's inactivity score the protocol will apply penalties to:

- Withhold staking and Newton inflation rewards. See [Rewards withholding calculation](/concepts/ofd/#rewards-withholding-calculation).
- Withhold rewards and apply jailing coupled with a probation period. See [Probation period calculation](/concepts/ofd/#probation-period-calculation) and [Jail period calculation](/concepts/ofd/#jail-period-calculation).
- Apply slashing and longer jailing if repeated offences are committed while on probation. See [Slashing amount calculation](/concepts/ofd/#slashing-amount-calculation). Slashing is applied according to Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/afd/#penalty-absorbing-stake-pas) model: validator self-bonded stake is slashed first until exhausted, then delegated stake.

To learn more about the concept see [Omission Fault Detection (OFD)](/concepts/ofd/).

### Autonity Oracle Contract
The contract implementing the Oracle protocol extensions, including primitives for computing weighted average price data, managing the set of currency pairs for which Autonity provides price data, and the Autonity _Oracle Accountability Fault Detection (OAFD)_ protocol.

The contract stores:

- [Protocol parameters](/reference/protocol/) for weighted average price computation and oracle voting rounds. These specify the currency pairs for which the oracle provides weighted average price data, the interval over which an oracle round for submitting and voting on price data runs.
- [Protocol configuration](/concepts/oafd/#protocol-configuration) used to compute slashing penalties for the [Oracle Accountability Fault Detection (OFD)](/concepts/oafd/) protocol.

Per the Autonity Protocol Contract, Oracle protocol parameters are initialised at network [genesis](/reference/genesis/).

Contract functions for returning price data, currency pairs provided, and the oracle network voters can be called by all participants. Function calls to govern (i.e. manage) the set of currency pairs provided by the oracle are restricted to the governance `operator` account.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Oracle Contract Interface](/reference/api/oracle/), governance under [Governance and Protocol-Only Reference](/reference/api/aut/op-prot/).

#### Weighted average price computation
The Autonity Oracle Contract manages the computation of weighted average price data for currency pair price reports submitted by validator-operated oracle servers. The contract implements logic to:

- Aggregate price report data submitted on-chain by validator-operated oracle servers and compute weighted average prices for the currency pairs provided by the oracle network in voting rounds.
- Manage the set of currency pair symbols for which the oracle network must provide price report data.
- Provide contract operations for data consumers to determine the currency pair data provided and retrieve historical and latest computed weighted average price data.

To learn more about the concept see [Oracle network](/concepts/oracle-network/).

#### Voting rounds
The Autonity Oracle Contract implements logic to manage submission of price data reports and the calculation of weighted average price data over [voting rounds](/glossary/#voting-round). This is managed autonomously by protocol only functions to:

- Set oracle voters based on validators in the consensus committee and update the voter set as the consensus committee is re-selected at the end of an epoch.
- Manage oracle voting rounds, triggering the initiation of a new voting period at the end of a round.

#### Voter selection
Participation in the oracle protocol is a validator responsibility and validators in the consensus committee are automatically selected to vote on weighted average price computation by a protocol-only function. As the last block of an epoch is finalized, this function is executed to determine the oracle voters for the following epoch.

Consensus committee membership is computed by the Autonity Protocol Contract; see [committee selection](/concepts/architecture/#committee-selection).

#### Slashing penalty computation
The Autonity Oracle Contract manages the computation of accountability penalties for proven oracle price reporting faults at epoch end. The [Oracle Accountability Fault Detection](/concepts/oafd/) protocol implements a penalty model for reporting "outlier" prices falling outside a tolerance threshold of the median of prices reported by other oracles in the [oracle network](/concepts/oracle-network). The contract calculates penalties based on parameters set in the [protocol configuration](/concepts/oafd/#protocol-configuration) and dynamic factors specific to the epoch circumstances. See [slashing amount calculation](/concepts/ofd/#slashing-amount-calculation).

Depending upon the validator's inactivity score the protocol will apply penalties to:

- Detect outliers by a threshold mechanism setting a percentage range that a reported price can differ from the median value of prices reported by other oracles. See [Outlier detection calculation](/concepts/oafd/#outlier-detection-calculation).
- Adjust rewards and penalties for price reporting based on the confidence score an oracle places on a reported price and the oracle's price reporting performance over the epoch. See [Confidence score calculation](/concepts/oafd/#confidence-score-calculation) and [Epoch performance score calculation](/concepts/oafd/#epoch-performance-score-calculation).
- Apply slashing for reporting outliers proportionally to the confidence score provided for the outlier. See [Slashing amount calculation](/concepts/oafd/#slashing-amount-calculation). Slashing is applied according to Autonity's [Penalty-Absorbing Stake (PAS)](/concepts/afd/#penalty-absorbing-stake-pas) model: validator self-bonded stake is slashed first until exhausted, then delegated stake.

To learn more about the concept see [Oracle Accountability Fault Detection (OAFD)](/concepts/oafd/).

### ASM ACU Contract
The contract implementing the Autonomous Currency Unit (ACU) element of the Auton Stabilization Mechanism. It computes the value of the ACU, an optimal currency basket of 7 free-floating fiat currencies. Value is computed for the basket currencies using [weighted average price data](/concepts/architecture/#weighted-average-price-computation) from the Oracle Contract. The basket quantity corresponding to each symbol is set to give ACU maximum stability.

The contract provides primitives for computing the ACU value and managing the basket currency symbols and quantities (i.e. weighting). The contract stores [protocol parameters](/reference/protocol/) that specify the currency pairs for the basket, the quantities of those currencies in the basket, and the scale of precision for the ACU value. Per the Autonity Protocol Contract, ACU protocol parameters are initialised at network [genesis](/reference/genesis/).

Contract functions for returning ACU value, basket symbols, and basket quantities can be called by all participants.  Function calls to govern (i.e. manage) the basket composition and value scale are restricted to the governance `operator` account.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [ACU Contract Interface](/reference/api/asm/acu/), governance under [Governance and Protocol-Only Reference](/reference/api/aut/op-prot/).

#### ACU value computation
The Autonity ACU Contract manages the computation of the ACU value, i.e. price, for the ASM. The contract implements logic to:

- Compute the ACU value from the currency basket using the latest weighted average price data for the symbols computed by the Oracle Contract.
- Manage the ACU basket currency pair symbols, quantities, and ACU value scale precision.
- Provide contract operations for data consumers to determine the ACU value, and basket symbols and quantities.

To learn more about the concept see [Auton Stabilization Mechanism (ASM)](/concepts/asm/).


### ASM Supply Control Contract
The contract implementing the Auton supply control element of the Auton Stability Mechanism. The contract controls the supply of Auton on an Autonity network by minting and burning invoked by the ASM Stabilization Contract.

The contract provides primitives for managing the available supply of Auton in an Autonity network. The contract stores the [protocol parameter](/reference/protocol/) setting the network's available Auton supply. Per the Autonity Protocol Contract, ACU protocol parameters are initialised at network [genesis](/reference/genesis/).

The contract function for returning the available supply of Auton for minting can be called by all participants.  Function calls to mint and burn Auton are restricted to invocation by the protocol Stabilization Contract.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Supply Control Contract Interface](/reference/api/asm/supplycontrol/), mint and burn under [Governance and Protocol-Only Reference](/reference/api/aut/op-prot/).

#### Auton supply control
The Autonity Supply Control Contract manages the Auton supply. The contract implements logic to:

- Mint and burn of Auton to take Auton in and out of circulation.

To learn more about the concept see [Auton Stability Mechanism (ASM)](/concepts/asm/).

### ASM Stabilization Contract
The contract implementing the CDP-based stabilization mechanism for the Auton. Auton is borrowed against Collateral Token using a Collateralized Debt Position (CDP) mechanism. The Stabilization Contract manages CDP's throughout the lifecycle, from initial borrowing through repayment and liquidation scenarios. Collateral Token is deposited into a CDP to borrow Auton. Auton is brought in and out of circulation on an Autonity network as CDP's are opened and closed.

The contract provides primitives for stabilization configuration, CDP calculations, and CDP lifecycle management. The contract stores [protocol parameter](/reference/protocol/) setting the configuration of the stabilisation mechanism’s Collateralised Debt Position (CDP). Per the Autonity Protocol Contract, Stabilization protocol parameters are initialised at network [genesis](/reference/genesis/).

Contract functions can be called by all participants to:

- By CDP owners to take out CDP's to borrow Auton, withdraw collateral, and repay CDP's.
- By prospective CDP owners to determine borrowing limits  and collateral level requirements.
- By CDP liquidators to determine if a CDP is liquidatable or not, and to liquidate CDP's via bidding in debt auctions (see [Auctioneer Contract](/concepts/architecture/#asm-auctioneer-contract).
- To view CDP data and retrieve stabilization configuration settings from system state.

Function calls to govern (i.e. manage) the stabilization configuration are restricted to the governance `operator` account.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Stabilization Contract Interface](/reference/api/asm/stabilization/), governance under [Governance and Protocol-Only Reference](/reference/api/aut/op-prot/).

#### CDP ownership
The Autonity Stabilization Contract implements logic for a CDP owner to:

- Manage the lifecycle of a CDP through stages of initial borrowing, collateral withdrawal, and debt repayment.
- Maintain the position in a non-liquidatable state by keeping CDP debt and collateral levels within stabilisation mechanism requirements for minimum debt and collateralization values.
- Determine borrowing limits and collateral requirements for a new or existing CDP.

To learn more about the concept see [Auton Stabilization Mechanism (ASM)](/concepts/asm/).

#### CDP liquidation
The Autonity Stabilization Contract implements logic for a liquidator to:

- Determine if a CDP is liquidatable, i.e. if the CDP is under collateralized and the collateral value is less than the liquidation ratio requirement.
- Liquidate a CDP that is undercollateralized by bidding in a debt auction (see [Auctioneer Contract](/concepts/architecture/#asm-auctioneer-contract).

To learn more about the concept see [Auton Stabilization Mechanism (ASM)](/concepts/asm/).

### ASM Auctioneer Contract
The contract implementing the debt and interest auction mechanism for the ASM's Collateralized Debt Position (CDP) mechanism. The Auctioneer Contract manages debt auctions for liquidatable CDP Newton collateral and interest auctions for CDP Auton loan interest repayments.

The contract provides primitives for auction configuration, debt auctions, and interest auctions. The contract stores [protocol parameter](/reference/protocol/) setting the configuration of the auction mechanism. Per the Autonity Protocol Contract, Auctioneer protocol parameters are initialised at network [genesis](/reference/genesis/).

Contract functions can be called by all participants to:

- Bid in debt and interest auctions.
- To view auction data and retrieve auctioneer configuration settings from system state.

Function calls to govern (i.e. manage) the auctioneer configuration are restricted to the governance `operator` account.

All functions are documented in the Reference [Autonity Interfaces](/reference/api/): public API's under [Auctioneer Contract Interface](/reference/api/asm/auctioneer/), governance under [Governance and Protocol-Only Reference](/reference/api/aut/op-prot/).

#### debt auctions
The Autonity Auctioneer Contract implements logic for an auction bidder to:

- Query for open auctions and return information about a specific auction.
- Determine the Newton collateral liquidation return for a liquidatable CDP.
- Bid in the auction, triggering the liquidation of the CDP, receiving the CDP's remaining Newton collateral in return for settling the CDP's outstanding Auton debt.

To learn more about the concept see [Auton Stabilization Mechanism (ASM)](/concepts/asm/).

#### interest auction
The Autonity Auctioneer Contract implements logic for an auction bidder to:

- Query for open auctions and return information about a specific auction.
- Determine the minimum amount of Newton that is required to bid in the interest auction.
- Bid in the auction, receiving Auton interest on CDP's in return for a Newton payment.

To learn more about the concept see [Auton Stability Mechanism (ASM)](/concepts/asm/).

### Newton Inflation Controller Contract
The contract implementing the Newton emission control element of the [Newton Inflation Mechanism](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation).

The contract computes the amount of Newton to release into circulation from the [inflation reserve](/glossary/#inflation-mechanism) according to the inflation schedule.

Newton [inflation rewards](/glossary/#inflation-rewards) are [earned for delegated stake](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) on an Autonity network. The amount of Newton inflation to release from the reserve is computed by the inflation controller contract. The Newton is then minted into circulation by the Autonity Protocol Contract on finalisation of the last block of each epoch. The inflation control contract configuration is set as an Autonity network [protocol parameter](/reference/protocol/). Per the Autonity Protocol Contract, inflation controller protocol parameters are initialised at network [genesis](/reference/genesis/).

### Protocol contract upgrade
Autonity protocol contracts are upgradable by governance calling the [`upgrade()`](/reference/api/aut/op-prot/#upgrade) function on the `upgradeManagerContract` to provide new contract bytecode and abi for a designated protocol contract address.

Upgrade functions by replacing contract logic for a designated contract address. The contract address and replacement contract code is passed in as parameters to the `upgrade()` function call. The block [`finalize()`](/reference/api/aut/op-prot/#finalize) function checks if a contract upgrade is available. The protocol will then update the contract code of the autonity contract during the block finalization phase. Contract code is replaced in the EVM and existing contract state is maintained.

Upgrade functions by replacing contract logic for a designated contract address. The contract address and replacement contract code is passed in as parameters to the `upgrade()` function call. The upgrade is immediate. As soon as the `upgrade()`transaction is executed contract code is replaced in the EVM; the existing contract state is maintained.

<!--
The block [`finalize()`](/reference/api/aut/op-prot/#finalize) function checks if a contract upgrade is available. The protocol will then update the contract code of the autonity contract during the block finalization phase. Contract code is replaced in the EVM and existing contract state is maintained.
-->

## Consensus layer

The append of new blocks to the ledger with immediate finality is managed by the Proof-of-Stake based Tendermint BFT consensus mechanism. It enables dynamic committee selection and maximises stake securing the system by a stake-weighted algorithm for committee selection.

Individual blocks are proposed and agreed upon in a Tendermint consensus instance, where the process is dynamically repeated as new blocks are finalized. Consensus instances are computed by the consensus committee, a subset of validators whose bonded stake secures the network against Byzantine or malicious behaviour by committee members.

Committee selection is dynamic and stake-based, with a new committee elected for each [epoch](/glossary/#epoch-period). The physical length of an epoch is set as a number of blocks appended to the ledger, and so the temporal duration of an epoch is dependent upon the minimum block period or '[time interval](/glossary/#block-period)' at which blocks are generated by the protocol and appended to the ledger. This interval provides consistent block production to the chain and adherence to the interval is a block validity constraint. Both epoch length and block period are protocol parameters. The number of consensus instances executed in an epoch may be equal to or greater than the number of blocks in the epoch: a consensus round may timeout and fail to complete.

The consensus protocol makes use of:

- The [communication layer](/concepts/architecture/#communication-layer) for consensus round messaging and consensus state synchronisation in a [dedicated consensus channel](/concepts/system-model/#p2p-networking-protocols).
- The [Autonity Protocol Contract](/concepts/architecture/#autonity-protocol-contract) for [committee selection logic](/reference/api/aut/op-prot/#computecommittee).

To learn more about the concept, see [Consensus](/concepts/consensus/), [System model, Networking](/concepts/consensus/) and the [protocol parameters](/reference/protocol/) reference.

## Communication layer

Autonity uses a [fully connected network topology](/glossary/#mesh-network) with peer-to-peer communication based on Ethereum [devp2p](https://github.com/ethereum/devp2p) network protocols RLPx and wire protocol.

At the P2P level, Autonity separates transaction and consensus traffic on to separate channels on different TCP ports.

For transaction gossiping between nodes the Ethereum wire protocol is used for P2P propagation of block announcements and transactions. Each participant maintains a current record of peers in the network, updated as new participants join or leave the system. Participants establish an authenticated connection with one another over TCP by the RLPx transport protocol. For detail, see the Concept description [System model, Networking](/concepts/system-model/#networking). 

For consensus gossiping a separate consensus protocol runs alongside the ethwire protocol for the execution of Autonity's BFT Tendermint Consensus algorithm. This channel is used by committee members to broadcast consensus messages during Tendermint consensus rounds (propose, prevote and precommit). Validator messages sent during consensus rounds are cryptographically signed (sealed). A subset of these signatures are saved in the [block header](/concepts/system-model/#block-header) as cryptographic proof of the validator quorum that agreed on the block: the *proposer seal*, seal of the committee member proposing the block, and the *quorum certificate*, a single aggregated BLS signature of the committee members that voted and agreed on the block.

To learn more about the separation of transaction and consensus gossiping traffic, see [System model, Networking](/concepts/system-model/#networking).

For how bootnode provision works, see the How to [Run Autonity](/node-operators/run-aut/).
