---
title: "`aut` Namespace"

description: >
  Autonity RPC API
---

The `aut` API gives access to Autonity-specific RPC methods to return protocol configuration and Autonity network peer information that cannot be replicated through `eth_call`.

Given an `RPC_URL` from <https://chainlist.org/?testnets=true&search=autonity>.

## aut_address

Returns the address of the Autonity Protocol Contract.

See Autonity Contract Interface [`address()`](/reference/api/aut/#address).

## aut_config

Returns the Autonity Network configuration at the block height the call was submitted.

See Autonity Contract Interface [`config()`](/reference/api/aut/#config).


## aut_acnPeers

Returns information about each consensus network peer connected to the queried validator node.


### Parameters

None.

### Response

Returns an array of objects providing information about each peer node the queried node is connected to in the Autonity consensus network. Each acn peer information object consists of:

| Field | Datatype | Description |
|:------|:---------|:------------|
| `enode ` | `string` | the enode url of the node |
| `id ` | `string` | the node ID, the public key of the node’s [`autonitykeys`](/concepts/validator/#p2p-node-keys-autonitykeys), a hex string |
| `name` | `string` | the name of the node, including client type, version, OS, custom data |
| `caps` | `string` | an array of the protocol capabilities advertised by this peer. Returns `acn/1` |
| network `localAddress` | `string` | the local endpoint of the tcp data connection on the network |
| network `remoteAddress` | `string` | the remote endpoint of the tcp data connection on the network |
| network `inbound` | `boolean` | false, if there is not an inbound connection |
| network `trusted` | `boolean` | true, if the node is a trusted peer of the node queried (trusted peers are a type of peer connection which can be accepted above the peer connection limit set by the client's [`--maxpeers`](/reference/cli/agc/) NETWORKING OPTION) |
| network `static` | `boolean` | true, if the node is configured as a static peer of the node queried (static peers connections are always maintained and retried if there are any failures) |
| protocols `acn`  `version` | `string` | the acn protocol version. Returns `1`. (Note: this doesn't duplicate the `acn/1` returned under `caps`. `caps` returns a list of all capabilities. |


### Usage

::: {.panel-tabset}

## RPC

``` {.rpc}
{"method":"aut_acnPeers", "params":[]}
```
:::


### Example

::: {.callout-caution title="Known issue" collapse="false"}
The RPC call needs to be made using the deprecated RPC call `admin_acnPeers`.

This is a known issue and a PR with the fix is pending. See [Known issue, RPC `aut_acnPeers` returns empty result](http://localhost:3000/issues/#rpc-aut_acnpeers-returns-empty-result).
:::

::: {.panel-tabset}
## RPC

``` {.rpc}
curl -X GET $RPC_URL --header 'Content-Type: application/json' --data '{"method":"admin_acnPeers", "params":[], "jsonrpc":"2.0", "id":1}' | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1109  100  1044  100    65   2691    167 --:--:-- --:--:-- --:--:--  2865
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "enode": "enode://0c1414b8291e8df39a1fb513f0fe8655e07d32a14cf87a32aa17f66919cd8b531c5900f278145a07dfbc693befe00ccb02bf073bcb42debe5b2f2f1de1c3cf75@34.92.69.160:20203?discport=0",
      "id": "1f7e639e880e54f1180348d6a49bd18570b0dde971dfe5f4b1b0d73737c21136",
      "name": "Autonity/v1.0.1-alpha-00d69978-20241202/linux-amd64/go1.22.0",
      "caps": [
        "acn/1"
      ],
      "network": {
        "localAddress": "11.154.11.203:34430",
        "remoteAddress": "31.91.69.160:20203",
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
    {
      "enode": "enode://debfb4bb49136767a685dcadcf95880d5539168f1ab042a545fd1890664f5afe9fe41259dfae2d5824f4cf8cb6ad9c080866349bb1b3064027e46c24a52512b3@35.244.41.229:20203?discport=0",
      "id": "d5a9df5fdcf74b350251818a38077b7bbba04267eb86d2106dd804c1351d7239",
      "name": "Autonity/v1.0.1-alpha-00d69978-20241202/linux-amd64/go1.22.0",
      "caps": [
        "acn/1"
      ],
      "network": {
        "localAddress": "11.114.15.203:59500",
        "remoteAddress": "15.214.41.229:20203",
        "inbound": false,
        "trusted": true,
        "static": true
      },
      "protocols": {
        "acn": {
          "version": 1
        }
      }
    }
  ]
}
```
:::



