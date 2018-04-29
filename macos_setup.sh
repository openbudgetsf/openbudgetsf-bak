#!/bin/bash -xe
git submodule update --init
cd openbudgetoakland/_src

brew install node
brew install fswatch
brew install python

npm install yarn

yarn global add harp
yarn install

cd ../..
