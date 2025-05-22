
---
title: "Known issues "
description: >
  Known issues in the Autonity codebase
---

## Snap syncing is not supported for new networks

There is a known issue in the go-ethereum codebase where the default `snap` syncmode is not yet supported for new networks  - see [https://github.com/autonity/autonity/blob/master/eth/handler.go#L196-L200](https://github.com/autonity/autonity/blob/master/eth/handler.go#L196-L200).

To resolve, for new networks:

- genesis nodes bootstrapping the network need to run with full sync: set the flag `--syncmode "full"` when starting the node
- new nodes joining the network after genesis can run in the default "snap" syncmode.

## Autonity Protocol proposer election algorithm contains an off-by-one error

The proposer election algorithm for height `h` and round `r` actually returns the result for height `h-1` and round `r`.

The Autonity Protocol Contract Interface function [`getProposer()`](/reference/api/aut/#getproposer) takes parameters of block `height` and consensus `round`. To get the elected proposer for height = `h` and round = `r` pass the following parameters to it:
- height = `h - 1`.
- round = `r`.

## Light client syncing is not supported

Autonity does not currently support light clients and the LES Protocol. The blockchain sync mode "light" should not be set: `--syncmode light` is not supported.

