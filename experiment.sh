#!/usr/bin/env bash

for url in $(cat 1fe55eae-cb62-4f81-8db7-c5b7eee21996.csv); do
  bin/vshot --url ${url} --save-html --fullpage --above-the-fold --no-js
done