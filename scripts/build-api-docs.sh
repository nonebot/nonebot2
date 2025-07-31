#!/usr/bin/env bash

set -e

# cd to the root of the project
cd "$(dirname "$0")/.."

nb-autodoc nonebot \
  -s nonebot.plugins \
  -u nonebot.internal \
  -u nonebot.internal.*
cp -r ./build/nonebot/* ./website/docs/api/
yarn prettier
