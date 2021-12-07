#!/bin/bash

./install && cd dist && (docker-compose up & sleep 0) && sleep 25 && cd ../ && ./initgrafana && cd dist && docker-compose down && cd ../ && echo "DONE!"
