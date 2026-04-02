#!/bin/sh
set -e

# Sync dependencies
uv sync

exec uv run "$@" --host 0.0.0.0
