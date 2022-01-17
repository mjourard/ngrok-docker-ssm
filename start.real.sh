#!/bin/sh -e

CMD="ngrok start --all"
set -x
exec $CMD

