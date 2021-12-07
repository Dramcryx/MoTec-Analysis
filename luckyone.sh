#!/bin/bash

./install; cd dist; docker-compose up & sleep 0; sleep 10; cd ../; ./initgrafana;
