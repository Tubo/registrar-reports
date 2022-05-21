let
  nixos-21 = import (builtins.fetchTarball {
    # Descriptive name to make the store path easier to identify
    name = "nixos-21.11-2012-01-03";
    # Commit hash for nixos-unstable as of 2018-09-12
    url =
      "https://github.com/nixos/nixpkgs/archive/9e27e2e6bbc1e72f73fff75f669b7be53d0bba62.tar.gz";
    # Hash obtained using `nix-prefetch-url --unpack <url>`
    sha256 = "sha256:0c6qnrwch1xhh38bbwcxcypc6vprypl1mvxhs8dfwcb7iy61gikk";
  });

  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix";
    ref = "refs/tags/3.4.0";
  }) {
    pkgs = nixos-21 { };
    python = "python39";
  };

  pyEnv = mach-nix.mkPython rec {
    requirements = ''
      python-dotenv
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
