#!/bin/bash

winpty docker run -it -p 0.0.0.0:8088:8088/tcp --env-file .env ift6758/serving:1.0.0

$SHELL

