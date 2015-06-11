# -*- coding: utf-8 -*-
# actlea  2015-05-21
'''
Created on Jun 9, 2015

@author: root
'''


import MySQLdb
import pickle
import sys
from url import Url
from stringHelper import Logger


reload(sys) 
sys.setdefaultencoding('utf-8')  # @UndefinedVariable


def getMysql():
    return MySQLdb.connect(host='localhost',\
            user='root',passwd='zjm',db="spider",port=3306,charset="utf8")

class BaseDb:  
    db = None   
    def connectdb(self):        
        try:
            self.db = getMysql()
            print 'connect to the dbserver !'
        except:
            print ":failed connected to db!"
        return self.db

    def execsql(self,sql):
        """execute the sql"""
        cursor=self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            info=sys.exc_info()
            print info[0],":---",info[1]
            self.connectdb()
            return False
    
        cursor.close()
        return True

    def __del__(self):
        self.db.close()

    def escapeString(self, s):
        if s is None:
            return 'NULL'
        elif isinstance(s, basestring):
            return '"%s"' % (s.replace('\\','\\\\').replace('"','\\"'))
        else:
            return str(s)

    def sql_insert(self, table, d):
        #construct INSERT SQL
        ks = ",".join(d.keys())
        vs = ",".join([self.escapeString(v) for v in d.values()])
        sql = 'insert into %s (%s) values (%s)' % (table,ks,vs)
        return sql

    def sql_update(self, table, d, key_name='url', renew=2):
        # construct UPDATE SQL
        key_value = d.pop(key_name)
        tmp = ''
        for k,v in d.items():
            tmp += ' `%s`=%s,' % (k, self.escapeString(v))
        sql = 'update %s set %s renew=%d where `%s`="%s"' % (table,tmp,renew,key_name,key_value)
        return sql

    def exception(self, url, type):
        #type: 0-fail to get the page
        #  1-No matching rules
        #  2-infomation extraction failure
        #  3-insert into db failure
        #  4-update db failure
        #  5-json infomation extraction failure
        #  6-failed to write file
        #  7-Error pages
        #  8-Error code of http response(http's 403、404)
        sql = "insert into spider_exception (url,time,type) values ('%s', now(), %s)" % (url, type)
        print "[exception]type=%s,url=%s" % (type,url)
        self.execsql(sql)

    def query(self, sql):
        cur = self.db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        numrows = int(cur.rowcount)
        for i in range(numrows):
            fields = cur.fetchone()
            yield fields

    


class HTML_URL_DB():
    def __init__(self):
        self.db = BaseDb()
        self.db.connectdb()
    
    def create_table(self):
        sql = """
        create table if not exists html(
         row_id INTEGER PRIMARY KEY auto_increment,         
         original_url        varchar(100),                
         priority            float(3,2),
         main_text           text,
         hash                char(60),
         encode              char(10),
         time                TIMESTAMP
         
         )ENGINE=MyISAM DEFAULT CHARSET=utf8         
        """
        self.db.execsql(sql)
        
        sql = """
        create table if not exists url_item(
        row_id INTEGER PRIMARY KEY auto_increment,
        url     varchar(100),
        purl    varchar(100),
        depth   Integer,
        priority Integer,
        anchor  varchar(200),
        time    TIMESTAMP
        )ENGINE=MyISAM DEFAULT CHARSET=utf8
        """
        self.db.execsql(sql)
        
    
    def html_insert(self, html_item_tuple, table_name='html'):
        if html_item_tuple is not None:           
            item = html_item_tuple[0]
            flag = html_item_tuple[1]
            
            sql = self.db.sql_insert(table_name, item)  
            
            if flag and self.db.execsql(sql):
                return True
            else:
                url = item['original_url']
                self.db.exception(url, 3)
                return False
    
    
    def url_item_insert(self, html, purl, table_name='url_item'):
        for item in Url.url_todo(html, purl):
            sql = self.db.sql_insert(table_name, item)
            self.db.execsql(sql)
            Logger.info(purl+' url_item_insert')  
        
        
    
    def select(self):
        import lxml.html as html
        
        sql = 'select main_text from html'       
        for i in self.db.query(sql):
            text = i['main_text']
            if text is not None:
                text = text.encode('utf-8')
                print type(text)
                hxs=html.fromstring(text)
                title = hxs.xpath('.//title/text()')
                if title is not None:
                    print title[0] 


    
    
if __name__=='__main__':
    PH = HTML_URL_DB()
    PH.create_table()














