#!/bin/sh
REBUILD=""
if [ $# -eq 1 ]; then
    REBUILD="--rebuild=$1"
fi     
cd ..
#echo "PYTHONPATH=. python booj/controller.py booj.db $REBUILD"
PYTHONPATH=. python booj/controller.py $REBUILD
