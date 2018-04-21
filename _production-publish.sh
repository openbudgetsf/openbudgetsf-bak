#!/bin/bash -xe

# ensure submodules are checked out
git submodule update --init

# delete the gh-pages branch and then recreate it as an orphan (untracked) branch
git branch -D gh-pages
git checkout --orphan gh-pages

# override default config files
cp config.js openbudgetoakland/_src/js
# move into the _src directory and compile source files
cd openbudgetoakland/_src
# install node dependencies
yarn install
# build a production-optimized webpack bundle
yarn run build
# exclude node dependencies from harp compilation
mv node_modules _node_modules
# compile source files to root directory
harp compile ./ ../_dist
# harp compile won't output more than one level up from source directory, so
# manually copy the files
cp -r ../_dist/* ../..
# ensure that git doesn't consider submodule dirty
rm -rf ../_dist
# restore node_modules before you forget
mv _node_modules node_modules

# move back to the root, and add and commit files
cd ../../
# GitHub Pages doesn't like submodules
rm -rf .gitmodules openbudgetoakland/
# Oakland's CNAME file conflicts with our setting
git checkout master -- CNAME
touch .nojekyll
git add -A
git commit -m "deploy"

# push changes to remote gh-pages branch using *gasp* --force!
# !!! Never push --force on any public branch besides gh-pages!
git push --set-upstream origin gh-pages --force

echo "http://openbudgetsf.org updated"
