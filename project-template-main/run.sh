#!/bin/bash

docker run -it --expose 127.0.0.1:8088:8088/tcp --env DOCKER_ENV_VAR=$COMET_API_KEY ift6758/serving:0.0.1 