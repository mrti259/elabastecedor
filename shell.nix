{ pkgs ? import<nixpkgs> {} }:

pkgs.mkShell {
    buildInputs = with pkgs; [
        poetry
	gnumake
    ];

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
}
