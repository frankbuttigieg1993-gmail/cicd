#!/usr/bin/env bash
set -euo pipefail

find . -type d -name .git -prune -o -type f -print | LC_ALL=C sort
