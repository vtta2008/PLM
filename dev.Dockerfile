~ $ make build-dev
~ $ docker images --filter "label=name=PLM"
REPOSITORY                          TAG                 IMAGE ID            CREATED             SIZE
docker.pkg.github.com/vtta2008/PLM  3492a40-dirty       acf8d09acce4        28 seconds ago      967MB
~ $ docker run acf8d09acce4
Hello World...