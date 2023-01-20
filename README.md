# docs.autonity.org

Documentation for the Autonity Go Client (AGC), the reference implementation of the Autonity blockchain protocol. 

## Build Instructions

Setup:

1. Clone this repository.
2. [Install the latest Hugo "extended version"](https://gohugo.io/getting-started/installing/)
   for your OS. If you are on an LTS Linux distro, you may need to use the Hugo
   snap package or the pre-built binaries to obtain the latest version.
3. [Install Node.js and `npm`](https://nodejs.org/en/download/package-manager/) for your OS.
4. Run `make deps` to install Docsy and its dependencies.

Usage:

* Run `make serve` (or just `make`) to serve the site in Hugo's local webserver.
* Review the [`Makefile`](Makefile) and [Github Actions workflow](.github/workflows/gh-pages.yml) for more details.

## Contributing

To contribute to this repo, please raise a pull request as per [Github Flow](https://docs.github.com/en/get-started/quickstart/github-flow).

Note that in order to maintain a legible Git history, this repo enforces _linear history_ on `master`. To ensure that your local Git commit log is linear, you should rebase your local changes on top of `origin`. You can tell Git to do this for this repository by setting the Git option `pull.rebase` in your local checkout:

```
git config --local pull.rebase true
```

Alternatively, you can apply this setting for all your repos by replacing `--local` with `--global`.

Reference: [Pro Git by Scott Chacon](https://git-scm.com/book/en/v2)
