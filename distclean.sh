cd dist; docker-compose down; docker-compose rm -f; cd ../

sudo rm -rf ./dist/**

docker image rm pyspark
