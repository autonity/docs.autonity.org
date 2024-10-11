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

## Development workflow

For changes to *content* relating to the *current version* of Autonity, raise a PR against the `master` branch. If the changes relate to the *next version* of Autonity, raise a PR against the `develop` branch.

The `develop` branch is regularly rebased on `master` to pick up the latest changes. When a new version of Autonity is released, the `develop` branch is merged to `master`.

For changes to site *styling* and/or *configuration*, raise a PR against the `master` branch. If these changes need to be gated, _use feature flags to keep them hidden or disabled_ in `master` until the time they need to go live. Activate feature flags by means of a PR against `master` or as a commit in the `develop` branch.

In summary:

| change type | autonity version | git branch |
|-|-|-|
| new/updated content | current version | `master` |
| new/updated content | next version | `develop` |
| styling/configuration | - | `master` |

## Migrating from Docsy/Hugo

For best results, clone this repo into a new directory. If you are working with a clone of this repo that used Docsy and Hugo, delete the following directories as they will conflict and prevent Quarto from building:

``` env
 - themes/     # contains docsy shortcodes
 - archetypes/ # contains docsy shortcodes
 - layouts/    # contains Markup for docsy templating
 - data/       # is empty and no longer required
 - docs/       # holds the content in a format that works for Hugo (and not Quarto).
 - content/    # holds the content in a format that works for Hugo (and not Quarto). 
```

## Contributing

To contribute to this repo, please raise a pull request as per [Github Flow](https://docs.github.com/en/get-started/quickstart/github-flow).

Note that in order to maintain a legible Git history, this repo enforces _linear history_ on `master`. To ensure that your local Git commit log is linear, you should rebase your local changes on top of `origin`. You can tell Git to do this for this repository by setting the Git option `pull.rebase` in your local checkout:

```
git config --local pull.rebase true
```

Alternatively, you can apply this setting for all your repos by replacing `--local` with `--global`.

Reference: [Pro Git by Scott Chacon](https://git-scm.com/book/en/v2)
