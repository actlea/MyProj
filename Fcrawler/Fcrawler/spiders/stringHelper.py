# -*- coding: utf-8 -*-
'''
Created on May 27, 2015

@author: root
'''

import time
from hashlib import sha256
import re


def timestamp():
    return str(time.strftime("%y-%m-%d %H:%M:%S", time.localtime()))


#ll is list
ext = lambda x:x[0] if x else None

def clean_link(link_text):
    """
        Remove leading and trailing whitespace and punctuation
    """

    return link_text.strip("\t\r\n '\"")

def delete_punc(words):
    re.sub("[！，。？：、]+".decode("utf-8"),"".decode("utf-8"),words)
    
#去除多余的空格
def blank_delete(text):
    try:
        return ''.join(text.split())
    except Exception:
        return text


def text_format(text, PUC_DELETE=True):
    if text:
        if PUC_DELETE:
            return delete_punc(clean_link(blank_delete (ext(text))))
        else:
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


class Logger:                                                                      
        HEADER = '\033[95m'                                                        
        OKBLUE = '\033[94m'                                                        
        OKGREEN = '\033[92m'                                                       
        WARNING = '\033[93m'                                                       
        FAIL = '\033[91m'                                                          
        ENDC = '\033[0m'                                                           
                                                                                   
        @staticmethod                                                              
        def log_normal(info):                                                      
                print Logger.OKBLUE + info + Logger.ENDC                           
                                                                                   
        @staticmethod                                                              
        def log_high(info):                                                        
                print Logger.OKGREEN + info + Logger.ENDC                          
                                                                                   
        @staticmethod                                                              
        def log_fail(info):                                                        
                print Logger.FAIL + info + Logger.ENDC 



if __name__=='__main__':
    Logger.log_normal("This is a normal message!")
    Logger.log_fail("This is a fail message!")
    Logger.log_high("This is a high-light message!")
    
    
    
    
    
    
    
