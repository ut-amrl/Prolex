#!/bin/bash

# Init Conda Env
conda env create -f env.yml
conda activate ns_policies_popl

# Setup Python Environment
export PYTHONPATH='/src/':$PYTHONPATH

# Setup php dir
cd /usr/
mv local/bin/php bin/php

#Move to Code source dir
cd /src
