#!/bin/sh
python twitterToFirebase.py 1>output/twitterOut.log 2>error/twitterToErr.log &
python rssToFirebase.py 1>output/twitterOut.log 2>error/twitterToErr.log &