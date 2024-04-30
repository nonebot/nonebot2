#! /usr/bin/env bash

# update test env
echo "Updating test env..."
(cd ./envs/test/ && poetry update --lock)

# update dev env
echo "Updating dev env..."
poetry update

# update other envs
for env in $(find ./envs/ -maxdepth 1 -mindepth 1 -type d -not -name test); do
  echo "Updating $env env..."
  (cd $env && poetry update)
done
