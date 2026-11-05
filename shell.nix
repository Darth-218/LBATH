{
  pkgs ? import <nixpkgs> { },
}:

let
  pythonEnv = pkgs.python3.withPackages (
    ps: with ps; [
      pyyaml
    ]
  );
in
pkgs.mkShell {
  packages = [
    pythonEnv
    # pkgs.libyaml
  ];

  shellHook = ''
    echo "LBATH env ready."
  '';
}
