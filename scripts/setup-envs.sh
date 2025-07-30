#! /usr/bin/env bash

echo "Setting up dev environment"
uv sync --all-extras && uv run pre-commit install && yarn install
