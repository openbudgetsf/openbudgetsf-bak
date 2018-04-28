#!/bin/bash
echo -n "Deploying... "
rsync -a overrides/ openbudgetoakland/_src/
echo "done"