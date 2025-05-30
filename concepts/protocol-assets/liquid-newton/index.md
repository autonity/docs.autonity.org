
---
title: "Liquid Newton"
description: >
  Liquid Newton - liquid staking asset
---

## Liquid Newton overview

Liquid Newton is the [liquid staking](/concepts/staking/#liquid-staking) token of Autonity. Liquid Newton is minted and burned for [delegated](/glossary/#delegated) stake as stakeholders bond and redeem [Newton](/concepts/protocol-assets/newton/) stake token to validators in an Autonity system. Liquid Newton is validator-specific and represents the holder's share of the total [delegated](/glossary/#delegated) stake bonded to a [validator](/glossary/#validator). Liquid Newton has the [staking rewards](/glossary/#staking-rewards) entitlement rights due to [delegated](/glossary/#delegated) stake when the staked validator is participating in the [consensus committee](/glossary/#consensus-committee). The Liquid Newton of a validator has its own market price and is not fungible across validators. Liquid Newton is divisible up to 18 decimal places (the smallest unit is 10^-18 or 0.000000000000000001).

A Liquid Newton token can be in one of two states:

- _unlocked_, the default state in which it is unlocked and the [stake holder](/glossary/#stakeholder) can transfer ownership by sending to another [account](/glossary/#account).
- _locked_, the bound state after unbonding in which it is locked during the [unbonding period](/glossary/#unbonding-period) and cannot be transferred by the [stake holder](/glossary/#stakeholder).

The amount of Liquid Newton minted to a staker is governed autonomously by the validator's Liquid Newton contract. This contract maintains a conversion rate between Liquid Newton and Newton for bonding and unbonding operations. The rate is determined by the ratio of issued Liquid tokens over the total amount of [delegated](/glossary/#delegated) stake tokens bonded to the validator. This ensures that a validator’s Liquid Newton tokens remain fungible over time:

- On bonding, the amount of Liquid Newton minted has value matching that of the Newton being bonded.
- On unbonding, the Liquid Newton unbonded is burnt and Newton redeemed in proportion to the holder's share of the Liquid Newton pool according to the conversion rate.

A validator may or may not have had slashing penalties applied and as such the redemption value of Liquid Newton may vary across validators according to their history.

::: {.callout-note title="Note" collapse="false"}

Note that Liquid Newton is not minted for [autobonding](/glossary/#autobond) of 
[Newton inflation](/concepts/protocol-assets/newton/#total-supply-and-newton-inflation) emissions.

:::
