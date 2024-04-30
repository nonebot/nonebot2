#! /usr/bin/env bash

# cd to the root of the project
cd "$(dirname "$0")/.."

poetry run nb-autodoc nonebot \
  -s nonebot.plugins \
  -u nonebot.internal \
  -u nonebot.internal.*
cp -r ./build/nonebot/* ./website/docs/api/
yarn prettier
