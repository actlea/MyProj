#!/bin/bash
echo "clear log text"
find . -type f -name '*log*' -print0 | xargs -0 rm;

if [ "$1"="1" ];then
	./html_clean	
	echo "clear html file"
fi

echo "clear table html"
mysql -uroot -pzjm<<EOF
use spider;
ALTER TABLE html AUTO_INCREMENT=1;
ALTER TABLE url_item AUTO_INCREMENT=1;
delete from html;
delete from url_item;
EOF

if [ [1=1] ]; then
	echo "clear redis"
	redis-cli flushdb
fi