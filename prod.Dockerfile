~ $ make build-prod VERSION=0.0.5
~ $ docker images --filter "label=version=0.0.5"
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
docker.pkg.github.com/vtta2008/PLM   0.0.5               65e6690d9edd        5 seconds ago       86.1MB
~ $ docker run 65e6690d9edd
Hello World...