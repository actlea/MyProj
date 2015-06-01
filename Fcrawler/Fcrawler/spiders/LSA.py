#coding=utf-8
import jieba
import numpy  as np
import re
import os

if os.path.exists("../data/dict.txt"):
    jieba.load_userdict("../data/dict.txt")
titles = ["奇才塞拉芬漂移跳投得2分，由沃尔助攻",
 "老鹰霍福德失误：丢球，被波特断球",
 "奇才沃尔第二罚命中，得1分",
 "奇才塞申斯换下比尔",
 "奇才沃尔第一罚命中，得1分",
 "老鹰巴泽莫尔防守沃尔投篮时犯规",
 "奇才古登得到防守篮板球",
 "老鹰施劳德跳投不中",
 "老鹰巴泽莫尔得到防守篮板球"
]

title="卡罗尔第一罚命中，得1分"
stopwords=[u'奇才',u'塞拉芬',u'沃尔',u'老鹰',u'霍福德',u'波特',u'塞申斯',u'巴泽莫尔',u'古登',u'施劳德',u'由',
           u'被',u'得',u'得到',u'比尔',u'时']

class LSA(object):
    def __init__(self,stopwords):
        self.stopwords=stopwords
        self.widct={}
        self.dcount=0
    def parse(self,doc):
        doc=doc.decode("utf-8")
        doc=re.sub("[！，。？：、]+".decode("utf-8"),"".decode("utf-8"),doc)
        seg_list=jieba.cut(doc)
        words=[]
        for i in seg_list:
            words.append(i)
        for w in words:
            if w in self.stopwords:
                continue
            elif w in self.widct:
                self.widct[w].append(self.dcount)
            else:
                self.widct[w]=[self.dcount]
        self.dcount+=1
    
    def build(self):     
        self.keys=[k for k in self.widct.keys() if len(self.widct[k])>0]
        self.keys.sort()
       #matrix len(keys) * len(dcount)
        self.A=np.zeros([len(self.keys),self.dcount])
        for i,k in enumerate(self.keys):           
            for d in self.widct[k]:
                self.A[i,d]+=1
    
    def printA(self):
        print self.A
        
    def calc(self):
        self.U,self.S,self.V=np.linalg.svd(self.A)# calc SVD matrix
        
    def calct(self):      
        self.u=self.U[0:,0:3]
        self.s=np.diag((self.S[0],self.S[1],self.S[2]))
        self.v=self.V[0:3].T         
        self.e=np.dot(self.v,self.s)
       
    def calsim(self,doc):
        test_list=jieba.cut(doc)
        testwords=[]
        for i in test_list:
            testwords.append(i)
        self.x=np.zeros(len(self.widct))
        self.keys=[k for k in self.widct.keys() if len(self.widct[k])>0]
        self.keys.sort()       
        for i,k in enumerate(self.keys):
            if k in testwords:
                self.x[i]=1
           
        self.d=np.dot(np.dot(self.x.T,self.u),np.linalg.inv(self.s))
        
        
        self.sim=np.zeros(self.dcount)
        for i in range(self.dcount):
            a=self.e[i]
            d=self.d
            La=np.sqrt(a.dot(a))
            Ld=np.sqrt(d.dot(d))
            m=a.dot(d)
            if La*Ld==0:
                cos=0
            else:
                cos=m/(La*Ld)         
            self.sim[i]=cos           
        print self.sim
    def getnum(self):
        for i in range(len(self.sim)):
            if self.sim[i]==max(self.sim):
                num=i
                print num

# mylsa=LSA(stopwords)
# for t in titles:
#     mylsa.parse(t)
# mylsa.build()
# mylsa.calc()
# mylsa.calct()
# mylsa.calsim(title)   
# mylsa.getnum()