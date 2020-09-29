with import <nixpkgs> {};
with pkgs.coreutils;
with pkgs.glibcLocales;
with pkgs.python36Packages;

buildPythonPackage rec {
  name = "itchapterize";
  src = ".";
  propagatedBuildInputs = [ click ];
}
