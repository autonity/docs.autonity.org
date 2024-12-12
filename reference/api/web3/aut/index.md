---
title: "`aut` Namespace"

description: >
  Autonity RPC API
---

The `aut` API gives access to Autonity-specific RPC methods to return protocol configuration and Autonity network peer information that cannot be replicated through `eth_call`.


## aut_address

Returns the address of the Autonity Contract.

### Parameters

None.

### Response

| Field | Datatype | Description |
| --| --| --|
| value | `address` | the Autonity Protocol contract account address |

### Usage

::: {.panel-tabset}
## RPC

``` {.rpc}
{"method": "aut_address", "params":[]}
```
:::

### Example

::: {.panel-tabset}
## RPC

``` {.rpc}
curl -X GET 'https://rpc1.piccadilly.autonity.org'  --header 'Content-Type: application/json' --data '{"method":"aut_address", "params":[], "jsonrpc":"2.0", "id":1}'
{"jsonrpc":"2.0","id":1,"result":"0xbd770416a3345f91e4b34576cb804a576fa48eb1"}
```
:::


## aut_config

See Autonity Contract Interface [`config()`](/reference/api/aut/#config).


## aut_acnPeers

Returns information about each consensus network peer.


### Parameters

None.

### Response

Returns a `Config` object consisting of:

| Object | Field | Datatype | Description |
| --| --| --| --|
| | `` | `` | |


//
    {
      "enode": "enode://....",
      "id": "1f7e639e880......",
      "name": "Autonity/v1.0.1-alpha.....",
      "caps": [
        "acn/1"
      ],
      "network": {
        "localAddress": "10.1....",
        "remoteAddress": "34.9......",
        "inbound": false,
        "trusted": true,
        "static": true
      },
      "protocols": {
        "acn": {
          "version": 1
        }
      }
    },
    ///
### Usage


::: {.panel-tabset}

``` {.aut}
## aut

```

## RPC

``` {.rpc}
{"method":"aut_config", "params":[]}
```
:::


### Example

::: {.panel-tabset}
## aut

``` {.aut}

```

## RPC

``` {.rpc}

```
:::



