---
title: "Accountability"
---

## Events

### [InnocenceProven(address,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/interfaces/IAccountability.sol#L39)

Event emitted after receiving a proof-of-innocence cancelling an accusation.

#### Parameters

| Name | Type |
| --- | --- |
| _offender | address |
| _id | uint256 |

### [NewAccusation(address,uint256,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/interfaces/IAccountability.sol#L34)

Event emitted after receiving an accusation, the reported validator has a certain amount of time to submit a proof-of-innocence, otherwise, he gets slashed.

#### Parameters

| Name | Type |
| --- | --- |
| _offender | address |
| _severity | uint256 |
| _id | uint256 |

### [NewFaultProof(address,uint256,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/interfaces/IAccountability.sol#L28)

Event emitted when a fault proof has been submitted. The reported validator will be silencied and slashed at the end of the current epoch.

#### Parameters

| Name | Type |
| --- | --- |
| _offender | address |
| _severity | uint256 |
| _id | uint256 |

### [SlashingEvent(address,uint256,uint256,bool,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/interfaces/IAccountability.sol#L44)

Event emitted after a successful slashing.

#### Parameters

| Name | Type |
| --- | --- |
| validator | address |
| amount | uint256 |
| releaseBlock | uint256 |
| isJailbound | bool |
| eventId | uint256 |

## Functions

### [beneficiaries(address)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L75)

#### Parameters

| Type |
| --- |
| address |

#### Returns

| Type |
| --- |
| address |

### [canAccuse(address,uint8,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L180)

#### Parameters

| Name | Type |
| --- | --- |
| _offender | address |
| _rule | uint8 |
| _block | uint256 |

#### Returns

| Name | Type |
| --- | --- |
| _result | bool |
| _deadline | uint256 |

### [canSlash(address,uint8,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L172)

#### Parameters

| Name | Type |
| --- | --- |
| _offender | address |
| _rule | uint8 |
| _block | uint256 |

#### Returns

| Type |
| --- |
| bool |

### [config()](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L72)

#### Returns

| Name | Type |
| --- | --- |
| innocenceProofSubmissionWindow | uint256 |
| baseSlashingRateLow | uint256 |
| baseSlashingRateMid | uint256 |
| collusionFactor | uint256 |
| historyFactor | uint256 |
| jailFactor | uint256 |
| slashingRatePrecision | uint256 |

### [distributeRewards(address,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L120)

called by the Autonity Contract at block finalization, to reward the reporter of a valid proof.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| _validator | address | validator account which got slashed. |
| _ntnReward | uint256 | total amount of ntn to be transferred to the repoter. MUST BE AVAILABLE in the accountability contract balance. |

### [epochPeriod()](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L21)

#### Returns

| Type |
| --- |
| uint256 |

### [events(uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L71)

#### Parameters

| Type |
| --- |
| uint256 |

#### Returns

| Name | Type |
| --- | --- |
| chunks | uint8 |
| chunkId | uint8 |
| eventType | uint8 |
| rule | uint8 |
| reporter | address |
| offender | address |
| rawProof | bytes |
| id | uint256 |
| block | uint256 |
| epoch | uint256 |
| reportingBlock | uint256 |
| messageHash | uint256 |

### [finalize(bool)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L105)

called by the Autonity Contract at block finalization, before processing reward redistribution.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| _epochEnd | bool | whether or not the current block is the last one from the epoch. |

### [getValidatorAccusation(address)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L197)

#### Parameters

| Name | Type |
| --- | --- |
| _val | address |

#### Returns

| Type |
| --- |
| tuple |

### [getValidatorFaults(address)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L202)

#### Parameters

| Name | Type |
| --- | --- |
| _val | address |

#### Returns

| Type |
| --- |
| tuple[] |

### [handleEvent(tuple)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L143)

#### Parameters

| Name | Type |
| --- | --- |
| _event | tuple |

### [setEpochPeriod(uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L523)

called by the Autonity Contract when the epoch period is updated.

#### Parameters

| Name | Type | Description |
| --- | --- | --- |
| _newPeriod | uint256 | the new epoch period. |

### [slashingHistory(address,uint256)](https://github.com/autonity/autonity/tree/v0.14.1/autonity/solidity/contracts/Accountability.sol#L86)

#### Parameters

| Type |
| --- |
| address |
| uint256 |

#### Returns

| Type |
| --- |
| uint256 |

::: {.footer-navigation prev-url="previous-page.qmd" prev-contract="Previous Contract Name"}
:::
