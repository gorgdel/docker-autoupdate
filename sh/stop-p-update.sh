#!/bin/bash
for KILLPID in `ps ax | grep ‘p-updater.py’ | awk ‘{print $1;}’`; do
kill -9 $KILLPID;
done
