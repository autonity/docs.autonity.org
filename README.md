# docs.autonity.org

## Getting started

### Setup

- Install Nix using [nix-installer](https://zero-to-nix.com/start/install).

- Install [devenv](https://devenv.sh/getting-started/#__tabbed_2_2) using
  `nix profile install`.

### Usage

Run `devenv shell` in the terminal to enter a Bash shell with all dependencies
installed. Alternatively, use `direnv` to manage this automatically.

once in the devenv shell the following usage can be executed.

Usage:
- Run `quarto render` to render the site to the `docs/` folder
- Run `quarto preview` to serve the site in Quarto's local webserver
- Review the [`_quarto.yml`](_quarto.yml) file and [Github Actions workflow](.github/workflows/gh-pages.yml) for more details

## Generating API reference documentation

The repository includes an API documentation generator that takes documentation
comments from Autonity protocol contracts and converts them into Markdown files.

**TL/DR:** Symlink an [autonity](https://github.com/autonity/autonity) repository
clone into the root of this repository and run [`apidocgen`](./_apidocgen/). The
configuration is in [`apidoc.toml`](./apidoc.toml).

### Setup

- Either clone the [Autonity Go Client](https://github.com/autonity/autonity) into the
  root of this repository
- Or add a symlink to an existing clone into this repository with `ln -s /path/to/autonity`

### Adding API documentation for a new Autonity release

1. If there are new contracts to document, add them to [`apidoc.toml`](./apidoc.toml).
   The configuration is documented [here](./_apidocgen/README.md#configuration).
2. Switch to the release tag in Autonity, e.g. for v0.15.0:
   ```sh
   cd autonity
   git checkout v0.15.0
   ```
3. Compile the protocol contracts:
   ```sh
   make contracts
   ```
4. Generate the API reference documentation:
   ```sh
   cd -
   apidocgen
   ```
5. Review and commit the created Markdown files.

> [!NOTE]
> Old Autonity branches (releases <= v0.14.1) do not build NatSpec data files.
> To generate API documentation for these branches, run `patch-autonity` in the
> root of this repository before step 3 to apply a patch to `autonity/Makefile`
> that modifies `solc` compiler options.

### Developing contract documentation

Autonity protocol contracts are documented via documentation comments in
Solidity source code. To help with previewing documentation, a script is
available that watches the source directory in Autonity and rebuilds the
documentation when files change.

1. Launch the monitoring script with `apidocmon`.
2. Open the preview URL from the terminal in the browser.
3. Open Solidity code from the symlinked Autonity repository clone in a
   text editor and make changes. The browser window should reload with
   the new content.

## Migrating from Hugo

For best results, clone into a new directory. However, if you are unable to do that, Delete the following directories as they will conflict and prevent Quarto from building:

``` env
 - themes/     # contains docys shortcodes
 - archetypes/ # contains docsy shortcodes
 - layouts/    # contains Markup for docsy templating
 - data/       # is empty and no longer required
 - docs/       # holds the content in a format that works for Hugo (and not Quarto).
 - content/    # holds the content in a format that works for Hugo (and not Quarto). 
```

## Development workflow

- The `master` branch will always have the live production version of the website.
- A hot-fix to the production site is published by creating a branch from `master` with the hot-fix, and creating a PR.  (Once the hot-fix has been merged, `master` should be merged to `develop` to ensure that the fix is propagated, and that conflicts are resolved in `develop`.)
- The `develop` branch will always have the WIP next version of the website being prepared.
- A new version of the production website is published by merging `develop` into `master`.

## Contributing

To contribute to this repo, please raise a pull request as per [Github Flow](https://docs.github.com/en/get-started/quickstart/github-flow).

Note that in order to maintain a legible Git history, this repo enforces _linear history_ on `master`. To ensure that your local Git commit log is linear, you should rebase your local changes on top of `origin`. You can tell Git to do this for this repository by setting the Git option `pull.rebase` in your local checkout:

```
git config --local pull.rebase true
```

Alternatively, you can apply this setting for all your repos by replacing `--local` with `--global`.

Reference: [Pro Git by Scott Chacon](https://git-scm.com/book/en/v2)
