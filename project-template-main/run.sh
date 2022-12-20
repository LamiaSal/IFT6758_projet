#!/bin/bash

winpty docker run -it -p 127.0.0.1:8088:8088/tcp --env DOCKER_ENV_VAR=$COMET_API_KEY ift6758/serving:1.0.0

$SHELL

