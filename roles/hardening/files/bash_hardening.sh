#!/bin/bash

# Set soft code dump size to zero
ulimit -S -c 0 > /dev/null 2>&1

# Disable stored bash history
unset HISTFILE

