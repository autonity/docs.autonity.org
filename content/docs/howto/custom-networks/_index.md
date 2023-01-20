---
title: "Setting up custom networks"
linkTitle: "Custom Network"
weight: 200
description: >
  Custom Autonity networks
draft: true
---

- To connect your node to an existing Autonity network other than `bakerloo` or `piccadilly`, you will need the network's:
  - bootnode file `static-nodes.json`
  - genesis file `genesis.json`

  See the [Networks](/networks/) section for file download links.

{{% alert title="Note" %}}Note that the client provides command-line flag options for connecting to the various Autonity testnets. If you specify the testnet flag, then neither genesis nor bootnode files are required: the client will use the flag to set genesis and bootstrap configuration. {{% /alert %}}

2. To connect your node to an existing Autonity network other than `bakerloo` or `piccadilly`, copy the bootnode file into the `autonity-chaindata` directory:

	```bash
	cp ./<PATH>/static-nodes.json ./autonity-chaindata/
    ```

    - `--genesis` is used to provide a genesis file, if connecting to a network other than `bakerloo` or `piccadilly`
	- `<NETWORK_ID` - is the Autonity network identifier, if connecting to a network other than `bakerloo` or `piccadilly`
