#!/bin/bash
cd "$(dirname "$0")"
exec ~/.venvs/torch/bin/python mve_train.py "$@"
