{ pkgs, ... }:

{
  packages = [
    pkgs.git
    pkgs.quarto
    pkgs.solc
  ];

  languages.python = {
    enable = true;
    version = "3.11";
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };

  scripts.apidocgen.exec = ''
    python3 -m _apidocgen $@
  '';
  scripts.apidocmon.exec = ''
    _apidocgen/apidocmon
  '';
  scripts.lint-apidocgen.exec = ''
    ruff check _apidocgen && black --check _apidocgen && mypy _apidocgen
  '';
  scripts.patch-autonity.exec = ''
    export ROOTDIR=$PWD &&
    cd autonity &&
    git apply $ROOTDIR/_apidocgen/autonity-natspec.patch 2>/dev/null &&
    echo 'Patch applied' >&2 ||
    echo 'Patch failed but it might be unnecessary' >&2
  '';
}
