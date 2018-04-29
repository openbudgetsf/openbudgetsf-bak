#!/bin/bash -xe
# Set up
git submodule update --init
cd openbudgetoakland/_src

# Install node
brew install node

# Install fswatch
brew install fswatch

# Install yarn
npm install yarn

# Install harp
yarn global add harp

# Install node dependencies
yarn install

cd ../..
