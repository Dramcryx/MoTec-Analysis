if [ ! -d ./dist/store ]
then
    mkdir ./dist/store
    chmod -R 777 ./dist/store
fi

if [ ! -d ./dist/visualize ]
then
    mkdir ./dist/visualize
    chmod -R 777 ./dist/visualize
fi

cp dist/docker-compose.yml_template dist/docker-compose.yml

storePath=$(pwd)/dist/store
visualizePath=$(pwd)/dist/visualize

sed -i "s|STORE|$storePath|g" dist/docker-compose.yml
sed -i "s|VISUALIZE|$visualizePath|g" dist/docker-compose.yml
