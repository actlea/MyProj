#!/usr/bin/env python
# coding:utf-8
# manning  2015-05-16
import time

class UrlNode(object):
	def __init__(self, dest_url, src_url, html_length, time, html_title, depth, priority=0):
		self.dest_url = dest_url
		self.src_url = src_url
		self.depth = int(depth) + 1
		self.html_length = int(html_length)
		self.priority = int(priority)
		self.time = time
		self.html_title=html_title

class HtmlNode(object):
	'''
	Args:
		url: url link to html
		html: content of html page
		time: fetch time of html page
		depth: depth of url
	'''
	def __init__(self, url, html, time, depth):
		self.url = url		
		self.html = html
		self.time = time
		self.depth = depth

