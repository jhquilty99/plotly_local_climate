docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)

docker build -f Dockerfile.app -t climate .

docker run -d -p 5000:5000 climate