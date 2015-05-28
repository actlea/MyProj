# -*- coding: utf-8 -*-
'''
Created on May 27, 2015

@author: root
'''

import time
from hashlib import sha256


def timestamp():
    return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


#ll is list
ext = lambda x:x[0] if x else None

def clean_link(link_text):
    """
        Remove leading and trailing whitespace and punctuation
    """

    return link_text.strip("\t\r\n '\"")
#去除多余的空格
def blank_delete(text):
    try:
        return ''.join(text.split())
    except Exception:
        return text


def text_format(text):
    if text:
        return clean_link(blank_delete (ext(text)))
    else:
        return text    
    
def url_hashcode(url):
    code=None
    if type(url)==unicode:
        code = sha256(url.encode('utf-8')).hexdigest()
    else:
        code = sha256(url.__str__()).hexdigest()
    int_code = int(code, 16)
    return int_code
