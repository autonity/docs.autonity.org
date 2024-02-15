---
title: "Install Autonity in your environment"
description: >
  How to install an Autonity Go Client node on your host machine.
---

## Overview

The Autonity Go Client can be installed in several ways:

- as a pre-compiled Linux Executable File from the Release Archive
- by building the client from source code
- in a Docker container.

We assume that the Autonity Go Client will run on a _host_ machine (a VPS or other host that is always-on and persistently available), and a distinct _local_ machine will be used for creating transactions and queries which are then sent to the Autonity Go Client on the _host_ via the RPC endpoint.

::: {.callout-note title="Note" collapse="false"}
Client source code is versioned on a 3-digit `major.minor.patch` versioning scheme, and hosted and maintained in the public GitHub repo [autonity](https://github.com/autonity/autonity/).
:::

## Requirements

### Hardware

To run an Autonity Go Client node, we recommend using a host machine (physical or virtual) with the following _minimum_ specification:

| Requirement	 | At least | Recommended|
|-------------|----------|------------|
| OS | Ubuntu 20.04	LTS | Ubuntu 20.04 LTS |
| CPU | 3.10 GHz with 8 CPU's | 3.10 GHz with 16 CPU's |
| RAM | 8GB | 16GB |
| Storage | 1024GB free storage for full nodes and Validators | 1024 GB free storage for full nodes and validators |
| Network interface	| 200 Mbit/s | 200 Mbit/s |

### Network

A public-facing internet connection with static IP is required:

* If you are using a cloud provider for node hosting, then a static IP address for your cloud space should be a stated hosting requirement. Cloud vendors typically don't supply a static IP address unless it is purchased explicitly.


::: {.callout-note title="Why is a static IP Address required?" collapse="false"}
Running an Autonity node requires that you maintain a static ip address because the ip address forms part of the node's network address, the [enode URL](/glossary/#enode). The enode provides the network location of the node client for p2p networking. Changing the ip address will change the node's identity on the network, therefore. This is significant if you are operating a validator node as the enode is provided as part of the validator meta data when [registering a validator](/validators/register-vali/#step-3.-submit-the-registration-transaction).
:::

Incoming traffic must be allowed on the following:

* `TCP, UDP 30303` for node p2p (DEVp2p) communication for transaction gossiping.

You may also choose to allow traffic on the following ports:

* `TCP 8545` to make http RPC connections to the node.
* `TCP 8546` to make WebSocket RPC connections to the node (required if you are operating a validator node).
* `TCP 20203` for node p2p (DEVp2p) communication for consensus gossiping  (required if you are operating a validator node).
* `TCP 6060` to export Autonity metrics (recommended but not required)

<!-- who collects the metrics? -->

It is assumed that most administrators will want to restrict access to these ports (unless they wish to support public access to the RPC calls for anonymous clients).  However, you should ensure that you can connect to one of the RPC ports from your _local_ machine (e.g. with IP whitelisting in your firewall rules, SSH port forwarding or other technique).

The description here covers only the basic network setup. Especially in a production setting, administrators should consider further security measures based on their situation.

## Installing the pre-compiled executable {#install-binary}

::: {.callout-note title="Note" collapse="false"}
  A Linux OS running on AMD64 architecture is required to run the pre-compiled executable.
:::

1. Navigate to the Autonity [Releases](https://github.com/autonity/autonity/releases) Archive and download the latest stable release version of the client `autonity-linux-amd64-<RELEASE_VERSION>.tar.gz` from the Assets section.

2. Create a working directory for installing Autonity. For example:

    ```bash
    mkdir autonity-go-client
    cd autonity-go-client
    ```

3. Unpack the downloaded _tarball_ to your working directory:

    ```bash
    tar -xzf <PATH_TO_DOWNLOADS_DIRECTORY>/autonity-linux-amd64-<RELEASE_VERSION>.tar.gz
    ```

4. (Optional) Copy the binary to `/usr/local/bin` so it can be accessed by all users, or other location in your `PATH` :

    ```bash
    sudo cp -r autonity /usr/local/bin/autonity
    ```

{{pageinfo}}
You can now [configure and launch Autonity](/node-operators/run-aut/#run-binary).
{{/pageinfo}}


## Build from source code {#install-source}

::: {.callout-note title="Prerequisites" collapse="false"}
The following should be installed in order to build the Autonity Go Client:
- **Git** Follow the official GitHub documentation to [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). (Check if installed:  `git --version`)
- **Golang** (version 1.21 or later) - [https://golang.org/dl](https://golang.org/dl) (Check if installed:  `go --version` or `go version`)
- **C compiler** (GCC or another) (Check if GCC is installed:  `gcc --version`)
- [**GNU Make**](https://www.gnu.org/software/make/) (Check if installed:  `make --version`)
:::


1. Clone/Copy the Autonity repo:

    ```bash
    git clone git@github.com:autonity/autonity.git
    ```


2. Enter the `autonity` directory and ensure you are building from the correct release. This can be done by checking out the Release Tag in a branch:

    ```bash
    git checkout tags/v0.13.0 -b v0.13.0
    ```

3. Build autonity:

    ```bash
    make autonity
    ```

    (The `cmd` utilities, including the Clef account management tool, can be built using `make all`.)

4. (Optional) Copy the generated binary to `/usr/local/bin` so it can be accessed by all users, or other location in your `PATH` :

    ```bash
    sudo cp build/bin/autonity /usr/local/bin/autonity
    ```

### Troubleshooting

An error of the form
```bash
Caught SIGILL in blst_cgo_init, consult <blst>/bindings/go/README.md.
```
thrown on the Go [`blst`](https://github.com/supranational/blst/blob/master/bindings/go/README.md) package (Go package [docs](https://pkg.golang.ir/github.com/supranational/blst/bindings/go) when running the `make` command indicates missing environment variables for CGO Flags.

To resolve:

- Set environment variables for CGO Flags:

   ```bash
   export CGO_CFLAGS="-O -D__BLST_PORTABLE__" 
   export CGO_CFLAGS_ALLOW="-O -D__BLST_PORTABLE__"
   ```

- Run `make clean` to cleanse object and executable files from the previous `make` run  

Re-run your `make` command.


## Installing the Docker image {#install-docker}

::: {.callout-note title="Note" collapse="false"}
Follow the official Docker documentation to [install Docker](https://docs.docker.com/engine/install/) onto the host machine and [follow the post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to customise for your environment.

By default Docker needs to be run with `sudo`. To avoid using root privileges in the terminal (and error messages if you forget to use `sudo`), consider following the step to [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

Consider also [configuring Docker to start on boot](https://docs.docker.com/engine/install/linux-postinstall/#configure-docker-to-start-on-boot).
:::

::: {.callout-note title="Optional but Recommended" collapse="false"}

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
:::

1. Pull the Autonity Go Client image from the Github Container Registry:
    ```bash
    docker pull ghcr.io/autonity/autonity:latest
    ```

   (where `latest` can be replaced with another version)

   ::: {.callout-note title="Note" collapse="false"}
   For more information on using and pulling Docker images from GHCR, see GitHub docs [Working with the container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).
   :::

1. Verify the authenticity of the Autonity Docker images against the official [image digests](https://github.com/autonity/autonity/pkgs/container/autonity/versions):

    ```bash
    docker images --digests ghcr.io/autonity/autonity
    REPOSITORY                               TAG       DIGEST                                                                    IMAGE ID       CREATED        SIZE
    ghcr.io/autonity/autonity                latest    sha256:7298a5fb9834b8cc281b81df1153fcf2f955a292bf3bd5e5d3eb3f80b52f0727   3375da450343   3 weeks ago    54.4MB
    ```

{{pageinfo}}
You can now [configure and launch Autonity](/node-operators/run-aut/#run-docker).
{{/pageinfo}}


## Verify the installation {#verify}

You should now be able to execute the `autonity` command.  Verify your installation by executing `autonity version` to return the client version and executable build details:

```bash
$ ./autonity version
```
```
Autonity
Version: 0.13.0-rc
Git Commit: 8b4a17c18951088c3af01c06da707a87d7887971
Git Commit Date: 20240210
Architecture: amd64
Protocol Versions: [66]
Go Version: go1.21.6
Operating System: linux
GOPATH=
GOROOT=
```

<!-- TODO: Check this works -->

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

::: {.callout-note title="Note" collapse="false"}
The output above will vary depending on the version of the Autonity Go Client you have installed.  Confirm that the "Version" field is consistent with the version you expect.
:::

## Next steps {#next}

{{pageinfo}}
You can now [configure and launch Autonity](/node-operators/run-aut/#run-binary).
{{/pageinfo}}


------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
