#! /usr/bin/env bash

# update test env
echo "Updating test env..."
poetry update --lock -C ./envs/test/

# update dev env
echo "Updating dev env..."
poetry update -C .

# update other envs
for env in $(find ./envs/ -maxdepth 1 -mindepth 1 -type d -not -name test); do
  echo "Updating $env env..."
  poetry update -C $env
done
