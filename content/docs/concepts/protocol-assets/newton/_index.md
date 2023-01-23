
---
title: "Newton "
linkTitle: "Newton"
weight: 2
description: >
  Newton - token for staking and securing the network
---

Newton is the native staking instrument of Autonity. Its primary function is staking the network, and it is the stake token used in Autonity's Proof-of-Stake consensus mechanism. Newton is divisible up to 18 decimal places (the smallest unit is 10^-18 or 0.000000000000000001). The symbol of _Newton_ is `NTN`.

A newton stake token can be in one of three states:

- _unbonded_, the default state in which it is unlocked and transferrable by the stake holder.
- _bonded_, the bound state in which it is locked and cannot be transferred by the stake holder.
- _unbonding_, the intermediate state between _bonded_ and _unbonded_ in which the token is locked and untransferrable until unbonding has completed and the token reverts to an _unbonded_ state.

Newton is bonded by the owner staking the token to a [validator](/glossary/#validator) in a bonding operation. If the validator account belongs to the owner, then the newton is [self-bonded](/glossary/#self-bonded), otherwise the token is [delegated](/glossary/#delegate). The total amount of stake bonded to a validator determine its [voting power](/glossary/#voting-power). Total and self-bonded stake amounts are tracked in the validator's state on chain (see [`getValidator()`](/reference/api/aut/#getvalidator)). The bonded token may earn [staking rewards](/glossary/#staking-rewards) if the validator is in the [consensus committee](/glossary/#consensus-committee), payable in [auton](/architecture/protocol-assets/auton/) at the end of the block epoch. 

Newton is unbonded by the staker in an unbonding operation. Unbonded tokens are subject to an unbonding delay, at the end of which it is redeemed and the staked Newton tokens are transferred back to the owner's account.

As Newton is bonded and redeemed a corresponding equivalent amount of [Liquid Newton](/architecture/protocol-assets/liquid-newton/) is minted and burned to the staker's account per Autonity's [liquid staking](/architecture/staking/#liquid-staking) model.
