# apidocgen

Markdown API reference documentation generator for
[docs.autonity.org](https://github.com/autonity/docs.autonity.org).

## Purpose

Generates API reference documentation for Autonity protocol contracts in
Markdown format. These documents are then used as the inputs for rendering the
documentation site via [Quarto](https://quarto.org/).

## Usage

The tool can be executed simply with `apidocgen` inside the devenv shell.

A (symlink to a) clone of the [Autonity repository](https://github.com/autonity/autonity)
is assumed to be in the working directory, or its path can be specified with the
`--autonity` command line option.

The configuration is read from a TOML file. This defaults to `config.toml` in the
working directory, or its path can be specified with the `--config` command line
option.

The `--watch` command line option launches an observer that detects contract code being
modified and automatically recompiles the contracts and regenerates the Markdown
documentation. Used together with `quarto preview`, it is possible to automatically
rebuild the docsite when any of the contracts is modified.

The `apidocmon` shell script runs `apidocgen --watch` and `quarto preview` together
in the same terminal window.

## Configuration

The configuration format is the following:

```toml
[autonity]
# The directory of contract artefacts
# relative to the Autonity repository root
build_dir = "params/generated"
# The root directory of contract source code
# relative to the Autonity repository root
src_dir = "autonity/solidity/contracts"
# Autonity repository home page on GitHub
github_url = "https://github.com/autonity/autonity"

[contracts]
# The directory in this repository where
# the generated API documentation is saved
output_dir = "contracts"

[contracts.Liquid]
# Optional contract name to use as the title of the generated document
# if it is different from the one in the section header
display_name = "Liquid Newton"
# Optional array of contract function & event names that should be excluded
# from the generated document
excludes = ["lock", "unlock"]
```

Alongside the `excludes` configuration parameter, another way to exclude
functions & events from the documentation is to add the `@custom:exclude`
custom NatSpec tag to documentation comments in the contracts' source code.

## Development

Dependencies are specified in [../requirements.in](../requirements.in). They
should be compiled with `pip-compile` and installed automatically by devenv.

Linters can be executed with the `lint-apidocgen` command inside the devenv shell.

To show full stack traces of errors, set the `DEBUG` environment variable to `1`.

## Testing

No automated tests are provided; after any change, run `DEBUG=1 apidocgen`
and inspect whether there are unwanted changes in the generated documents.
