
---
title: "Newton "
description: >
  Newton - token for staking and securing the network
---

Newton is the native staking instrument of Autonity. Its primary function is staking the network, and it is the [stake token](/glossary/#stake-token) used in Autonity's [Proof-of-Stake](/glossary/#proof-of-stake-pos) consensus mechanism. Newton is divisible up to 18 decimal places (the smallest unit is 10^-18 or 0.000000000000000001). The symbol of _Newton_ is `NTN`.

A newton stake token can be in one of three states:

- _unbonded_, the default state in which it is transferrable by the stake holder.
- _bonded_, the bound state in which the Newton has been bonded to a validator. On bonding the Newton token is burned; the bonded stake amount of the validator is increased by the bonded amount.
- _unbonding_, the intermediate state between _bonded_ and _unbonded_. The Newton is non-transferrable. Once unbonding has completed the due amount of Newton is redeemed by minting Newton in an _unbonded_ state to the stake holder.

Newton is bonded by the owner staking the token to a [validator](/glossary/#validator) in a bonding operation. If the validator account belongs to the owner, then the newton is [self-bonded](/glossary/#self-bonded), otherwise the token is [delegated](/glossary/#delegated). The total amount of stake bonded to a validator determines its [voting power](/glossary/#voting-power). Total and self-bonded stake amounts are tracked in the validator's state on chain (see [`getValidator()`](/reference/api/aut/#getvalidator)). The bonded token may earn [staking rewards](/glossary/#staking-rewards) if the validator is in the [consensus committee](/glossary/#consensus-committee), payable in [auton](/concepts/protocol-assets/auton/) at the end of the block epoch. 

Newton is unbonded by the staker in an unbonding operation. Unbonded tokens are subject to an unbonding delay, at the end of which Newton to the owner's account.

As Newton is bonded and redeemed [Liquid Newton](/concepts/protocol-assets/liquid-newton/) is minted and burned to the staker's account for [delegated](/glossary/#delegated) stake per Autonity's [liquid staking](/concepts/staking/#liquid-staking) model.
