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

  scripts.lint-apidocgen.exec = ''
    ruff check _apidocgen && black --check _apidocgen && mypy _apidocgen
  '';
}
