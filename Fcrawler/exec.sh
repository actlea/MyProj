#!/bin/bash
./dbclean.sh
echo "start scrapy hupu"
scrapy crawl hupu > ./logg.txt
ls Fcrawler/data/HTML/ -print

