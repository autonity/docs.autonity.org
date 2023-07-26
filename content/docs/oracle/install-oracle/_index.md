---
title: "Install Autonity Oracle Server in your environment"
linkTitle: "Install Autonity Oracle Server"
weight: 10
description: >
  How to install an Autonity Oracle Server on your host machine.
---

## Overview

The Autonity Oracle Server can be installed in several ways:

- as a pre-compiled Linux Executable File from the Release Archive
<!-- - in a Docker container -->
- by building the client from source code.

We assume that the Autonity Oracle Server will run on a _host_ machine (a VPS or other host that is always-on and persistently available), and a distinct _host_ machine will be used for Autonity Go Client the oracle serves via the WSS endpoint.

{{< alert title="Note" >}}
Autonity Oracle Server source code is versioned on a 3-digit `major.minor.patch` versioning scheme, and hosted and maintained in the public GitHub repo [autonity-oracle <i class='fas fa-external-link-alt'></i>] (https://github.com/autonity/autonity-oracle).
{{< /alert >}}

## Requirements

### Hardware

To run an Autonity Oracle Server, we recommend using a host machine (physical or virtual) with the following _minimum_ specification:

| Requirement	 | At least | Recommended|
|-------------|----------|------------|
| OS | Ubuntu 20.04 LTS | Ubuntu 20.04 LTS |
| CPU |1.9GHz with 4CPU's |  1.9GHz with 4CPU's |
| RAM |2GB |  4GB |
| Storage |32GB |  64GB |
| Network interface	| 64Mbit/s |  128Mbit/s |

### Network

A public-facing internet connection with static IP is required.  Incoming traffic must be allowed on the following:

* `TCP 8546` to make WebSocket RPC connections to the node.

{{< alert title="Note" >}}

Your validator node's [installation](/node-operators/install-aut/#network) must also allow traffic on your validator node's port `TCP 8546` to allow the Oracle Server's WebSocket RPC connection to the node.
{{< /alert >}}

The description here covers only the basic network setup. Especially in a production setting, administrators should consider further security measures based on their situation.

## Installing the pre-compiled executable {#install-binary}

{{< alert title="Note" >}}
  A Linux OS running on AMD64 architecture is required to run the pre-compiled executable.
{{< /alert >}}

1. Navigate to the Autonity Oracle Server [Releases <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/releases) Archive and download the latest stable release version of the Autonity Oracle Server `autoracle-linux-amd64-<RELEASE_VERSION>.tar.gz` from the Assets section.

2. Create a working directory for installing Oracle Server. For example:

    ```bash
    mkdir autonity-oracle
    cd autonity-oracle
    ```

3. Unpack the downloaded _tarball_ to your working directory:

    ```bash
    tar -xf <PATH_TO_DOWNLOADS_DIRECTORY>/autoracle-linux-amd64-<RELEASE_VERSION>.tar.gz
    ```
    This will unpack the pre-compiled executable and create a `/plugins` subdirectory containing data source plugins packaged in the release.

4. (Optional) Add data source plugins. Navigate to the `plugins` sub-directory of your working directory and add sub-directories for additional plugins you are installing.

5. (Optional) Copy the binary to `/usr/local/bin` so it can be accessed by all users, or other location in your `PATH` :

    ```bash
    sudo cp -r autoracle /usr/local/bin/autoracle
    ```

{{% pageinfo %}}
You can now [configure and launch Autonity Oracle Server](/oracle/run-oracle/#run-binary).
{{% /pageinfo %}}

<!--
## Installing the Docker image {#install-docker}

{{< alert title="Note" >}}
Follow the official Docker documentation to [install Docker <i class='fas fa-external-link-alt'></i>](https://docs.docker.com/engine/install/) onto the host machine and [follow the post-installation steps <i class='fas fa-external-link-alt'></i>](https://docs.docker.com/engine/install/linux-postinstall/) to customise for your environment.

By default Docker needs to be run with `sudo`. To avoid using root privileges in the terminal (and error messages if you forget to use `sudo`), consider following the step to [Manage Docker as a non-root user <i class='fas fa-external-link-alt'></i>](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

Consider also [configuring Docker to start on boot <i class='fas fa-external-link-alt'></i>](https://docs.docker.com/engine/install/linux-postinstall/#configure-docker-to-start-on-boot).
{{< /alert >}}

{{< alert title="Optional but recommended" >}}

To limit the size of the log files, add the following to the file `/etc/docker/daemon.json` (create it if it does not exist):

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "500m",
    "max-file": "20"
  }
}
```

Restart the Docker service to ensure the change is reflected:

``` bash
sudo systemctl restart docker
```
{{< /alert >}}

1. Pull the Autonity Go Client image from the Github Container Registry:
    ```bash
    docker pull ghcr.io/autonity/autonity:latest
    ```

   (where `latest` can be replaced with another version)

   {{< alert title="Note" >}}
   For more information on using and pulling Docker images from GHCR, see GitHub docs [Working with the container registry <i class='fas fa-external-link-alt'></i>](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).
   {{< /alert >}}

1. Verify the authenticity of the Autonity Docker images against the official [image digests <i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity/pkgs/container/autonity/versions):

    ```bash
    docker images --digests ghcr.io/autonity/autonity
    REPOSITORY                               TAG       DIGEST                                                                    IMAGE ID       CREATED        SIZE
    ghcr.io/autonity/autonity                latest    sha256:0eb561ce19ed3617038b022db89586f40abb9580cb0c4cd5f28a7ce74728a3d4   3375da450343   3 weeks ago    51.7MB
    ```
-->
<!-- TODO: Check this works

If using Docker, the setup of the image can be verified with:

```bash
$ docker run --rm ghcr.io/autonity/autonity:latest version
```
```
Autonity
Version: 0.10.1
Architecture: amd64
Protocol Versions: [66]
Go Version: go1.17.10
Operating System: linux
GOPATH=
GOROOT=/usr/local/go
```
-->
<!--
{{% pageinfo %}}
You can now [configure and launch oracle server](/oracle/run-oracle/#run-docker).
{{% /pageinfo %}}
-->
## Build from source code {#install-source}

{{< alert title="Prerequisites" >}}
The following should be installed in order to build the Autonity Oracle Server:
- **Git** Follow the official GitHub documentation to [install git <i class='fas fa-external-link-alt'></i>](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). (Check if installed:  `git --version`)
- **Golang** (version 1.19.3 or later) - [https://golang.org/dl <i class='fas fa-external-link-alt'></i>](https://golang.org/dl) (Check if installed:  `go --version` or `go version`)
- **C compiler** (GCC or another) (Check if GCC is installed:  `gcc --version`)
- [**GNU Make** <i class='fas fa-external-link-alt'></i>](https://www.gnu.org/software/make/) (Check if installed:  `make --version`)
{{< /alert >}}


1. Clone/Copy the Autonity Oracle Server repo:

    ```bash
    git clone git@github.com:autonity/autonity-oracle.git
    ```

2. Enter the `autonity-oracle` directory and build autonity:

    ```bash
    cd autonity-oracle
    make
    ```
    
    This will build the executable (`./build/bin/autoracle`) and create a subdirectory containing data source plugins packaged in the release (`./build/bin/plugins/`).

4. (Optional) Add data source plugins. Navigate to the `plugins` sub-directory of your working directory and add sub-directories for additional plugins you are installing.

5. (Optional) Copy the generated binary to `/usr/local/bin` so it can be accessed by all users, or other location in your `PATH`:

    ```bash
    sudo cp build/bin/autoracle /usr/local/bin/autoracle
    ```

## Verify the installation {#verify}

You should now be able to execute the `autoracle` command.  Verify your installation by executing `autoracle version` to return the oracle version and configuration:

```bash
$ ./autoracle version
```
```
v0.0.2
```

{{< alert title="Note" >}}
The output above will vary depending on the version of the Autonity Oracle Server you have installed.  Confirm that the "Version" field is consistent with the version you expect.
{{< /alert >}}


## Installing data source plugins {#install-plugin}

Oracle server will need to provide price data for FX and ATN/NTN currency pairs utilised in the Autonity Stability Mechanism.

A basic set of data adaptor plugins for sourcing this data is provided out the box with oracle server for testnet pre-Mainnet:

- Forex plugins: for connecting to public FX data sources. See the `forex_` prefixed adaptors in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins). Four forex plugins are currently provided.
- Simulator plugin: for simulated ATN/NTN data. See the `simulator_plugin` adaptor in [`/plugins`<i class='fas fa-external-link-alt'></i>](https://github.com/autonity/autonity-oracle/tree/master/plugins). 

To install:

1. To build the Simulator data source simulator run `make simulator`.

This will build the `simulator_plugin` in the `/plugins` directory.

The FX plugins in the `/plugins` directory are built when running `make autoracle`.

{{% alert title="Note"%}}
If you have developed your own plugins for external data sources using the oracle server's plugin template architecture, then you will need to build them and add to the `/plugins` directory.

For how to do this, see [Developing data plugins](/concepts/oracle-network/#developing-data-plugins).
{{% /alert %}}

## Next steps {#next}

{{% pageinfo %}}
You can now [configure and launch the oracle server](/oracle/run-oracle/#run-binary).
{{% /pageinfo %}}


------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!