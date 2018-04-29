#!/bin/bash
echo -n "Deploying overrides... "
rsync -a overrides/ openbudgetoakland/_src/
echo "done"