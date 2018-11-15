#!/bin/sh

mkdir output
mkdir error

python twitterToFirebase.py 1>output/twitterOut.log 2>error/twitterToErr.log &