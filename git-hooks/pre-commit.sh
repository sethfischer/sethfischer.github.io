#!/usr/bin/env bash

set -o errexit -o noclobber -o nounset

make test-links-internal
make lint-prose
