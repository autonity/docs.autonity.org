---
title: "Install Autonity in your environment"
linkTitle: "Install Autonity"
weight: 10
description: >
  How to install an Autonity Go Client node on your host machine.
---

## Overview

The Autonity Go Client can be installed in several ways:

- as a pre-compiled Linux Executable File from the Release Archive
- in a Docker container,
- by building the client from source code.

We assume that the Autonity Go Client will run on a _host_ machine (a VPS or other host that is always-on and persistently available), and a distinct _local_ machine will be used for creating transactions and queries which are then sent to the Autonity Go Client on the _host_ via the RPC endpoint.

{{< alert title="Note" >}}
Client source code is versioned on a 3-digit `major.minor.patch` versioning scheme, and hosted and maintained in the public GitHub repo [autonity](https://github.com/autonity/autonity/).
{{< /alert >}}

## Requirements

### Hardware

To run an Autonity Go Client node, we recommend using a host machine (physical or virtual) with the following _minimum_ specification:

| Requirement	 | At least | Recommended|
|-------------|----------|------------|
| OS | Ubuntu 20.04	LTS | Ubuntu 20.04 LTS |
| CPU | 3.10 GHz with 8 CPU's | 3.10 GHz with 16 CPU's |
| RAM | 8GB | 8GB |
| Storage | 1024GB free storage for full nodes and Validators | 1024 GB free storage for full nodes and validators |
| Network interface	| 200 Mbit/s | 200 Mbit/s |

### Network

A public-facing internet connection with static IP is required.  Incoming traffic must be allowed on the following:
* `TCP, UDP 30303` for node p2p (DEVp2p) communication.

You may also choose to allow traffic on the following ports:
* `TCP 8545` to make http RPC connections to the node.
* `TCP 8546` to make WebSocket RPC connections to the node.
* `TCP 6060` to export Autonity metrics (recommended but not required)

<!-- who collects the metrics? -->

It is assumed that most administrators will want to restrict access to these ports (unless they wish to support public access to the RPC calls for anonymous clients).  However, you should ensure that you can connect to one of the RPC ports from your _local_ machine (e.g. with IP whitelisting in your firewall rules, SSH port forwarding or other technique).

The description here covers only the basic network setup. Especially in a production setting, administrators should consider further security measures based on their situation.

## Installing the pre-compiled executable {#install-binary}

{{< alert title="Note" >}}
  A Linux OS running on AMD64 architecture is required to run the pre-compiled executable.
{{< /alert >}}

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

{{% pageinfo %}}
You can now [configure and launch Autonity](/node-operators/run-aut/#run-binary).
{{% /pageinfo %}}

## Installing the Docker image {#install-docker}

{{< alert title="Note" >}}
Follow the official Docker documentation to [install Docker](https://docs.docker.com/engine/install/) onto the host machine and [follow the post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to customise for your environment.

By default Docker needs to be run with `sudo`. To avoid using root privileges in the terminal (and error messages if you forget to use `sudo`), consider following the step to [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

Consider also [configuring Docker to start on boot](https://docs.docker.com/engine/install/linux-postinstall/#configure-docker-to-start-on-boot).
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

1. Verify the authenticity of the Autonity Docker images against the official [image digests](https://github.com/autonity/autonity/pkgs/container/autonity%2Fautonity):

    ```bash
    docker images --digests ghcr.io/autonity/autonity/autonity
    REPOSITORY                               TAG       DIGEST                                                                    IMAGE ID       CREATED        SIZE
    ghcr.io/autonity/autonity/autonity   latest    sha256:f374ac6575051037b03992854f1fb794b8b81eec3e7934849970ed192b08848c   a91c690c2bd0   5 months ago   51.6MB
    ```

    <!-- Required once the repo is public?? -->

1. Create a GitHub personal access token to pull the Autonity Go Client Docker image from GitHub Container Registry. See [Login Credentials to GitHub Container Registry](/developer/#login-credentials-to-github-container-registry)

1. Login to the Container Registry service, where:

    - `<PAT_TOKEN>` is your GitHub PAT token
    - `<GH_USERNAME>` is your GitHub username
    - `password.txt` is your Docker login password

	```bash
	export GHCR_PAT="<PAT_TOKEN>"
	export GH_USER="<GITHUB_USERNAME>"
	echo $GHCR_PAT | docker login https://ghcr.io --username $GH_USER --password-stdin
	```

1. Pull the Autonity Docker image:

    ```bash
    docker pull ghcr.io/autonity/autonity/autonity:latest
    ```

   (where `latest` can be replaced with another version)

   {{< alert title="Note" >}}
   For more information on using and pulling Docker images from GHCR, see GitHub docs [Working with the container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).
   {{< /alert >}}

{{% pageinfo %}}
You can now [configure and launch Autonity](/node-operators/run-aut/#run-docker).
{{% /pageinfo %}}

## Build from source code {#install-source}

{{< alert title="Prerequisites" >}}
The following should be installed in order to build the Autonity Go Client.:
- **Git** Follow the official GitHub documentation to [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). (Check if installed:  `git --version`)
- **Golang** (version 1.15 or later) - [https://golang.org/dl](https://golang.org/dl) (Check if installed:  `go --version` or `go version`)
- **C compiler** (GCC or another) (Check if GCC is installed:  `gcc --version`)
- [**GNU Make**](https://www.gnu.org/software/make/) (Check if installed:  `make --version`)
{{< /alert >}}


1. Clone/Copy the Autonity repo:

    ```bash
    git clone git@github.com:autonity/autonity.git
    ```

1. Enter the `autonity` directory and build autonity:

    ```bash
    cd autonity
    make autonity
    ```

    (The `cmd` utilities, including the Clef account management tool, can be built using `make all`.)

1. (Optional) Copy the generated binary to `/usr/local/bin` so it can be accessed by all users, or other location in your `PATH` :

    ```bash
    sudo cp build/bin/autonity /usr/local/bin/autonity
    ```

1. (Optional) Copy the Autonity Go Client binary to `/usr/local/bin`, so it can be accessed system-wide without specifying the path to the install directory:

## Verify the installation {#verify}

You should now be able to execute the `autonity` command.  Verify your installation by executing `autonity version` to return the client version and executable build details:

```bash
$ ./autonity version
```
```bash
Autonity
Version: 0.10.1
Architecture: amd64
Protocol Versions: [66]
Go Version: go1.18.2
Operating System: linux
GOPATH=
GOROOT=/usr/local/go
```

<!-- TODO: Check this works -->

If using Docker, the setup of the image can be verified with:

```bash
$ docker run --rm ghcr.io/autonity/autonity/autonity:latest version
```
```bash
Autonity
Version: 0.10.0
Git Commit: 1183a1130f192c70cab78831c76aed16f5715eca
Git Commit Date: 20230118
Architecture: amd64
Protocol Versions: [66]
Go Version: go1.18.1
Operating System: linux
GOPATH=
GOROOT=go
```

{{< alert title="Note" >}}
The output above will vary depending on the version of the Autonity Go Client you have installed.  Confirm that the "Version" field is consistent with the version you expect.
{{< /alert >}}

## Next steps {#next}

{{% pageinfo %}}
You can now [configure and launch Autonity](/node-operators/run-aut/#run-binary).
{{% /pageinfo %}}


------------------------------------------------

If you need help, you can chat to us on Autonity [Discord Server](https://discord.gg/autonity)!
