#!/bin/bash
QUARTO_VERSION=${QUARTO_VERSION:-1.5.56}

# Download and install Quarto
wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb
sudo dpkg -i quarto-${QUARTO_VERSION}-linux-amd64.deb

