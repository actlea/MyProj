#!/bin/bash

echo "clear log text"
find . -type f -name '*log*' -print0 | xargs -0 rm;

./html_clean
./url_clean

echo "clear table html"
mysql -uroot -pzjm<<EOF
use spider;
delete from html;
EOF

if [ [1=1] ]; then
	echo "clear redis"
	redis-cli flushdb
fi
echo "start scrapy hupu"
scrapy crawl hupu > ./logg.txt
ls Fcrawler/data/HTML/ -print

