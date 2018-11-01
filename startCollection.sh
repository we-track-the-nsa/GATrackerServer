#!/bin/sh

mkdir output
mkdir error

python NSATwitter.py 1>output/NSAoutput.log 2>error/NSAerror.log &
python WHTwitter.py 1>output/WHoutput.log 2>error/WHerror.log &