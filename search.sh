#!/bin/bash

query="$1"
mindate=2015
output=`echo "$1" | sed 's/ /_/g'`
output_file="raw/${output}_${mindate}.xml"

echo "query:\"$query\",mindate:$mindate,output_file:$output_file" >> "raw/query.log"
esearch -db pubmed -query "$query" -datetype PDAT -mindate "$mindate" | efetch -format xml > "$output_file"
