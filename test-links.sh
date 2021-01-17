#!/usr/bin/env bash

set -o errexit -o noclobber -o nounset

directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

site_url=$(${directory}/siteurl.py)

linkchecker --config="${directory}/linkcheckerrc" $site_url
