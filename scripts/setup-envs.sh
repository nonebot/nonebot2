#! /usr/bin/env bash

# config poetry to install env in project
poetry config virtualenvs.in-project true

# setup dev environment
echo "Setting up dev environment"
poetry install --all-extras && poetry run pre-commit install && yarn install

# setup pydantic v2 test environment
for env in $(find ./envs/ -maxdepth 1 -mindepth 1 -type d -not -name test); do
  echo "Setting up $env environment"
  (cd $env && poetry install --no-root)
done
