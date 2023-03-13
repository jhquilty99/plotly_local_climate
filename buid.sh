docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)

docker build -f Dockerfile -t climate .

docker run -d -p 80:5000 climate