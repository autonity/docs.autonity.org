
---
title: "Development with Autonity"
linkTitle: "Development"
weight: 60
description: >
draft: true
---

<!-- TODO: following content needs editing before exposing this page. -->

## Prerequisites

You need the following software components to carry out the steps in the How to section. A Linux host is assumed.

### Necessary

The Autonity Go Client can be installed and run as a binary or Docker image.

Whether configuring and launching as binary or Docker you will need _Git_. If installing and running the Docker image, you will also need _Docker_ and _login credentials to the GitHub Container Registry (GHCR)_ to pull and run the Autonity Docker image.

To connect to your node and interact with an Autonity network, you will need to install the _aut CLI_ tool on your local machine.

#### Git

Follow the git-scm documentation to [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) onto the host machine.

#### Docker

Follow the official Docker documentation to install the Docker Engine [Server](https://docs.docker.com/engine/install/#server) onto the host Linux machine. If you are running Docker on a Windows or Mac OS, then install [Docker Desktop](https://docs.docker.com/engine/install/#desktop).

#### Login Credentials to GitHub Container Registry

Ensure that you have access to the GitHub Container Registry (GHCR). To pull the Docker image of the Autonity Go Client you will need to connect to GHCR. To log in to GHCR you need to generate a GitHub **personal access token** (PAT) with read access to packages.

To do this:

- Navigate to GitHub > Account > Settings > Developer Settings > Personal access tokens
- Click "Generate new token"
- Name the PAT. For example "CR_PAT"
- Set PAT expiry. For example, set to 7 days as this is for temporary usage only.
- Set scopes for the PAT:
    - Select `repo` and all options under `repo`
    - Select `read:packages` under `write:packages`
- Click "Generate token"
- Copy the PAT displayed to a safe location

For more information, see GitHub docs and [Authenticating to the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry).

<!--
#### NodeJS and npm

To install and run the Autonity NodeJS Console you will need to [install nodejs](https://nodejs.org/en/download/) and [install npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).
-->

#### aut CLI tool

To install and configure follow the instructions in the How to [Setup aut CLI](/account-holders/setup-autcli/). A working Python install with the `pip` tool is required to run the tool.

#### Funded accounts

You will need a funded account on the Autonity network. The accounts must be funded with sufficient Auton to pay for gas costs. The process for account creation and funding is described in the how-to's [Create an account](/account-holders/create-acct/) and [Fund an account](/account-holders/fund-acct/).


### Additional Helpers

In some of the procedures, we will perform commands that will use [`curl`](https://curl.haxx.se/download.html). You may already have `curl` installed on your system as it comes with many OS distributions.

A good helper for working with JSON response objects returned by RPC is [`jq`](https://stedolan.github.io/jq/download/) (optional).

## How to Index
