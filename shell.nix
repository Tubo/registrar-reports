let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix";
    ref = "refs/tags/3.4.0";
  }) {
    pkgs = import <nixpkgs> { };
    python = "python39";
  };

  pyEnv = mach-nix.mkPython rec {
    requirements = ''
      playwright
    '';
  };
in mach-nix.nixpkgs.mkShell {
  buildInputs = with mach-nix.nixpkgs; [
    pyEnv
    black
    python39Packages.pyyaml
    python39Packages.pyparsing
    python39Packages.pandas
    python39Packages.jupyterlab
    python39Packages.pytest
    python39Packages.requests
    python39Packages.python-dotenv
  ];
  shellHook = "";
}
