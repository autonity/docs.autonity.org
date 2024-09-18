{ pkgs, ... }:

{
  packages = [
    pkgs.git
    pkgs.quarto
  ];

  languages.python = {
    enable = true;
    version = "3.11";
    venv.enable = true;
    venv.requirements = ./requirements.txt;
  };
}
