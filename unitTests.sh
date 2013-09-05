#!/bin/sh
#run some unit tests on the application

cd test/database
./testdatabase.sh
cd ../player
./testplayer.sh
