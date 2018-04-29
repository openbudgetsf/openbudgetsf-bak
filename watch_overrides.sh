#!/bin/bash
fswatch --event Created --event Updated --event Removed --event Renamed \
		--event MovedFrom --event MovedTo --event Link overrides/ -r -o | xargs -n1 -I{} ./deploy_overrides.sh &

cd openbudgetoakland/_src
yarn run watch &
harp server &

cd ../..
wait