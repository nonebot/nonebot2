#! /usr/bin/env bash

# cd to the root of the tests
cd "$(dirname "$0")/../tests"

# Run the tests
pytest -n auto --cov-append --cov-report xml --junitxml=./junit.xml $@
