#!/bin/sh

python NSATwitter.py 1>NSAoutput.log 2>NSAerror.log &
python WHTwitter.py 1>WHoutput.log 2>WHerror.log &