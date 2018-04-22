#!/bin/bash -xe
cp overrides/_analytics.jade openbudgetoakland/_src
cp overrides/_data.json openbudgetoakland/_src
cp overrides/_footer.jade openbudgetoakland/_src
cp overrides/_harp.json openbudgetoakland/_src
cp overrides/config.js openbudgetoakland/_src/js
cp overrides/codeforsf.png openbudgetoakland/_src/images/global

cp data/output/compare/fiscal-years-expenses/totals.json openbudgetoakland/_src/data/compare/fiscal-years-expenses
cp data/output/compare/fiscal-years-expenses/account-cats/* openbudgetoakland/_src/data/compare/fiscal-years-expenses/account-cats
cp data/output/compare/fiscal-years-expenses/depts/* openbudgetoakland/_src/data/compare/fiscal-years-expenses/depts

cp data/output/compare/fiscal-years-revenue/totals.json openbudgetoakland/_src/data/compare/fiscal-years-revenue
cp data/output/compare/fiscal-years-revenue/account-cats/* openbudgetoakland/_src/data/compare/fiscal-years-revenue/account-cats
cp data/output/compare/fiscal-years-revenue/depts/* openbudgetoakland/_src/data/compare/fiscal-years-revenue/depts

cp data/output/flow/* openbudgetoakland/_src/data/flow