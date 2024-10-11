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
