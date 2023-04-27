#!/bin/sh

src="C:\Users\usingh\OneDrive - WatchGuard Technologies Inc\Documents\bank-rest-api"

schemacrawler \
  --server=sqlite \
  --database="$src\backend\instance\data.db" \
  --info-level=standard \
  --command=schema \
  --output-format=png \
  --portable-names \
  --output-file="$src\doc\models.png" \
