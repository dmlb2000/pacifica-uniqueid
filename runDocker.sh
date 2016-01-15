docker rm docker-file-index-server-1

docker run -it -p 130.20.227.120:8051:8051 --rm --name docker-file-index-server-1 --link mysqlContainer1:mysql docker-file-index-server