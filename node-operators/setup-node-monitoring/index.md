---
title: "Set up node monitoring"
description: >
   How to setup node monitoring infrastructure for an Autonity Go Client node using Telegraf, InfluxDB v2.x and Grafana run in Docker containers
---

This guide outlines how to set up metrics infrastructure for an Autonity Go Client using a standard open source software stack to record, filter, and analyse performance metrics. This provides an 'observability stack' that can then be used for monitoring a single node installation or multiple nodes. For example, when operating several nodes across a number of hosting providers.

The pipeline for this metrics infrastructure is: `AGC > Telegraf > InfluxDB v2.x database > Grafana`. Telegraf is used to collect metrics from the AGC client and forward them to an InfluxDB V2 database, which is then used as a data source for Grafana dashboards. *Note that this guide uses Telegraf but it is **optional** in this pipeline as AGC can be directly configured to export to InfluxDB.*

The pipeline for this is: `AGC > Telegraf > InfluxDB v2.x database > Grafana`. Telegraf is used to collect metrics from the AGC client and forward them to an InfluxDB V2 database, which is then used as a data source for Grafana dashboards.

The steps covered are:

- Setting up Influxdb v2.x
- Setting up Telegraf.
- Starting Autonity and Telegraf to export metrics.
- Viewing the metrics on Grafana.

## Prerequisites

- An [installation](/node-operators/install-aut/) of Autonity Go Client (AGC), with the `--metrics` and `--pprof` flags enabled.
- An installation of [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) server agent, which will provide the backend service for metrics collection.
- An installation of Docker. See [Get setup, Install Docker](https://docs.autonity.org/node-operators/install-aut/#install-docker) if Docker is not already installed onto the host machine.

Familiarity with monitoring and the basics of the third-party products used in this guide is assumed:

- [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) server agent for metrics collection.
- [InfluxDB V2](https://www.influxdata.com/products/influxdb-overview/) time-series data platform.
- [Grafana](https://grafana.com/docs/grafana/latest/) observability dashboarding for monitoring and analysing metrics, log data, and application trace data.

## Install Influxdb v2 and Grafana

- Make persistent container volumes:

```bash
docker volume create grafana-storage
docker volume create influx-storage
```

This folder will be used to store the volumes for both InfluxDB and Grafana, so they will have persistent storage.

- Make a Docker network for InfluxDB and Grafana to communicate securely:

```bash
docker network create --driver bridge influxdb-grafana-net
```

### Start InfluxDB Docker container

```bash
docker run \
  -d \
  --rm \
  --name=influxdb \
  --net=influxdb-grafana-net \
  -p 8086:8086 \
  -v influx-storage:/root/.influxdb2 \
  influxdb:2.0
```

Go to the InfluxDB GUI at `localhost:8086` in a browser and setup a user and bucket, save the Token, or create a new one, as this will be needed for both Telegraf and Grafana.

To stop the InfluxDB container enter `docker stop`.


## Setup Telegraf

The metrics collection service Telegraf can be run in the Docker image or as a binary. Telegraf can be run in the same VM as Autonity or a different one. This guide assumes both AGC and the Telegraf agent are hosted on the same VM. If you set them up on different VM's, then in the template configuration below edit the `inputs.prometheus` `urls` to replace `localhost` with the IP address of the VM running Autonity.



### Get Telegraf Docker image

To pull the latest Docker image run the command:

```bash
docker pull telegraf
```

Or to download the latest Telegraf binary go to the [Telegraf download](https://www.influxdata.com/time-series-platform/telegraf/) and select the Telegraf 'platform' release for your host environment.

At time of writing this is version 1.24.2. To install on Ubuntu Linux run the command:

```bash
wget https://dl.influxdata.com/telegraf/releases/telegraf-1.24.2_linux_amd64.tar.gz
tar xf telegraf-1.24.2_linux_amd64.tar.gz
```

### Configure Telegraf

In the working directory Telegraf will be run from, create the configuration file `telegraf.conf` based on the template below, editing where:

- `<NETWORK_ID>`: Use value of `chainId` from the network's [Genesis configuration](/reference/genesis/).
- `<AGC_NODE_NAME>`: is replaced by a string with a human-readable label for the node. This is used as the name for the node in the Grafana metrics dashboard.
- Optionally edit the `[[inputs.prometheus]]` `urls` URL value to replace `localhost` with the IP address of your AGC if it is running on a different host to the Telegraf instance.
- `<OUTPUTS_INFLUXDB_URL>`: is the influxdb v2.x endpoint for example - http://localhost:8086 if installed on the same VM as the telegraf agent.
- `<BUCKET>`: is replaced by the name of the destination bucket written into.
- `<TOKEN>`: is replaced by the InfluxDB V2 token you have created in the initial steps of this tutorial.

```bash
[global_tags]
networkid = "<NETWORK_ID>"
afnc_name = "<AGC_NODE_NAME>"
user = "test"
[agent]
round_interval = true
metric_batch_size = 1000
metric_buffer_limit = 10000
collection_jitter = "0s"
flush_interval = "10s"
flush_jitter = "0s"
precision = ""
debug = false
quiet = false
logfile = ""
hostname = ""
omit_hostname = false
[[inputs.prometheus]]
urls = ["http://localhost:6060/debug/metrics/prometheus"]

[[outputs.influxdb_v2]]
urls = [ "<OUTPUTS_INFLUXDB_URL>"]
organization = "autonity"
bucket = "<BUCKET>"
token = "<TOKEN>"
```
You are now ready to run telegraf in your working directory.

## Setup Autonity to export metrics

To configure Autonity for exporting metrics set [command line options](/reference/cli/#command-line-options) when starting the node for:

- the Autonity testnet being connected to: `--piccadilly` or `--bakerloo`.
- enabling metrics collection and reporting: `--metrics`.
- enabling the pprof HTTP server: `--pprof`.

The [Piccadilly Testnet](https://docs.autonity.org/networks/testnet-piccadilly/) is connected to in the example configuration here. For a minimal command line start configuration see the how to [Run Autonity](/node-operators/run-aut/).

Autonity will serve an http feed that provides metrics at `http://localhost:6060/debug/metrics/prometheus`, which you can view in a browser. Notice this is the input specified in `telegraf.conf` above. If you are using Docker, make sure you run the container as host, as shown below:

```bash
docker run \
-d \
--volume $(pwd)/autonity-chaindata:/autonity-chaindata \
--net=host \
--name autonity \
--rm \
ghcr.io/autonity/autonity/autonity:latest \
    --datadir ./autonity-chaindata  \
    --piccadilly \
    --http  \
    --http.api aut,eth,net,txpool,web3,admin  \
    --ws  \
    --ws.addr 0.0.0.0 \
    --ws.api aut,eth,net,personal,txpool,web3,admin  \
    --nat extip:$(echo $IP_ADDRESS) \
    --metrics \
    --pprof
```


## Start Telegraf to export metrics

- Start Telegraf. Open the working directory where you created your `telegraf.conf` config file.

  To start Telegraf running in a Docker container:

  ```bash
    docker run  -d --net=host -v $PWD/telegraf.conf:/etc/telegraf/telegraf.conf telegraf
  ```

  Or if using the Telegraf binary then run with the config:

  ```bash
  telegraf --config telegraf.conf
  ```

  The Telegraf agent will initialise, report its config, and connect to the inputs url specified in `telegraf.conf`. Telegraf will now export metrics to the InfluxDB V2 database for the testnet you have installed in this tu

  To stop an Autonity Go Client or Telegraf instance enter `CTRL+C` if running a binary or `docker stop` if running a Docker container.

## Start Grafana Docker container

```bash
docker run \
  -d \
  --rm \
  --name=grafana \
  --net=influxdb-grafana-net \
  -p 3000:3000 \
  -v grafana-storage:/var/lib/grafana \
  grafana/grafana
```

To view Grafana, go to `localhost:3000` in a browser and login with username `admin`, and password `admin`, then set a new password.
Once logged in, set a new InfluxDB data source:

- Use flux query language.
- Use the url `http://influxdb:8086`.
- Disable Basic Auth.
- Use the organisation, token and default bucket from InfluxDB.

You will now be able to create a dashboard to visualise node metrics on Grafana. For help getting started with writing queries in Grafana, checkout [this](https://grafana.com/docs/grafana/latest/datasources/influxdb/influxdb-flux/) guide on the Flux query language.

To stop the Grafana Docker container enter `docker stop`.

---

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
