{ pkgs ? import <nixpkgs> { } }:

with pkgs.python38Packages;
pkgs.mkShell {
  buildInputs = [
    pkgs.hello
    pkgs.python38Full
    pandas
    jupyterlab

    # testing
    pytest

    # linting
    pyls-black

    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
