---
title: "JSON-RPC Namespaces"

description: >
  JSON-RPC calls to Ethereum Web3 and Autonity APIs 
---

Autonity may be interacted with by sending RPC requests to JSON-RPC APIs in the Ethereum Web3 and Autonity namespaces.

Recommended usage is to make JSON-RPC calls to Autonity Contract Interfaces using `eth_call` from the Web3 [eth namespace](https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-eth) wherever possible.

Autonity provides an `aut` namespace for Autonity Protocol JSON-RPC calls that cannot be replicated through `eth_call`.

::: {.callout-note title="Configuring access to the JSON-RPC APIs" collapse="true"}
The APIs are accessed over transport protocols per upstream go-ethereum, i.e. HTTP, WebSockets, or IPC.

Public access to JSON-RPC APIs by the JSON-RPC Server is enabled when setting the Autonity Go Client (AGC) runtime configuration.

The HTTP and WebSocket Servers, and the related JSON-RPC namespaces, can be made accessible using run command flags:

- HTTP: use `--http` to enable the HTTP-RPC Server and then `--http.api` to list the namespace(s) made available in a comma-separated list.
- WebSocket: use `--ws` to enable the HTTP-RPC Server and then `--ws.api` to list the namespace(s) made available in a comma-separated list.

For example: `--http --http.api aut,eth,net,txpool,web3`

The IPC Server is enabled and can access all JSON-RPC namespaces by default. The IPC socket/pipe file `geth.ipc` is created in the default `datadir` by default. Use `--ipcpath` to set your own custom location for the socket file. To disable the IPC-RPC server set the `--ipcdisable` flag.

For all flags see `API AND CONSOLE OPTIONS` in the [Autonity Go Client (AGC) Command-line Reference](/reference/cli/agc/). For detail on the JSON-RPC Server architecture see upstream Ethereum docs [Interacting with Geth, JSON-RPC Server](https://geth.ethereum.org/docs/interacting-with-geth/rpc).
:::

## Autonity `aut`

Autonity provides an `aut` namespace for Autonity Protocol specific JSON-RPC calls:

- [aut namespace](/reference/api/web3/aut/)


## Web3

Autonity supports the following go-ethereum Web3 APIs.

::: {.callout-important title="Warning" collapse="false"}
Deprecated namespaces should not be used.
:::

Click on the links to go to the relevant Geth documentation: 

- [`admin` namespace](https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-admin)
- [`debug` namespace](https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-debug)
- [`eth` namespace](https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-eth)
- [`net` namespace](https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-net)
- [`personal` namespace](https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-personal) (deprecated)
- [`txpool` namespace](https://geth.ethereum.org/docs/interacting-with-geth/rpc/ns-txpool)

Autonity does not support the go-ethereum Web3 APIs:

- `clique` namespace
- `les` namespace
- `miner` namespace (deprecated)
- `objects` namespace
