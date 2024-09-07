{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    docker
    docker-compose
  ];

  shellHook = ''
    echo "Docker development environment"
    echo "Run 'docker-compose build' to build the Docker image"
    echo "Run 'docker-compose up' to start the container"
  '';
}