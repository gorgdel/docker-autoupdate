#!/bin/bash
for KILLPID in `ps ax | grep âp-updater.pyâ | awk â{print $1;}â`; do
kill -9 $KILLPID;
done
