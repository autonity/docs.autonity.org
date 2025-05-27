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

  # API doc generator commands
  scripts.apidocgen.exec = ''
    python3 -m _apidocgen $@
  '';
  scripts.apidocmon.exec = ''
    _apidocgen/apidocmon
  '';
  scripts.lint-apidocgen.exec = ''
    ruff check _apidocgen && black --check _apidocgen && mypy _apidocgen
  '';

  # Quarto commands
  scripts.site-render.exec = ''
    if [ -d autonity ]; then
      apidocgen
    fi &&
    quarto render
  '';
  scripts.site-preview.exec = ''
    if [ -d autonity ]; then
      apidocmon
    else
      quarto preview
    fi
  '';
}
