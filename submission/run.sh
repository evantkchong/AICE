#!/bin/bash

# change dir so that the script still runs from outside the submission root
LOCAL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo "Local directory >> ${LOCAL_DIR}"
cd $LOCAL_DIR

if [ "$1" == "" ]; then
    config_path="${LOCAL_DIR}/config.json"
else
    config_path=$1
fi

echo Running end-to-end Pipeline with config at ${config_path}
python3 mlp/pipeline.py -c $config_path
