#!/bin/bash

docker build --tag nsp_popl_docker .

#docker run -it nsp_popl_docker /bin/bash
docker run -it --gpus 'all' nsp_popl_docker /bin/bash
