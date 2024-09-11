{ pkgs, ... }:

{
  packages = [
    pkgs.pyright
    pkgs.quarto
  ];

  languages.python = {
    enable = true;
    version = "3.12";
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
}
