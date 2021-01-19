#!/usr/bin/env bash

echo "📺 Xvfb Listening on :$DISPLAY"
Xvfb -ac -listen tcp $arg :$DISPLAY &

export DISPLAY=:$DISPLAY

for url in $(cat /src/1fe55eae-cb62-4f81-8db7-c5b7eee21996.csv); do
  bin/vshot --url ${url} \
    --save-s3 s3://public-assets.mle.va.sx.ggops.com/screenshots-2020-01-19 \
    --save-html \
    --fullpage \
    --above-the-fold \
    --no-js
done