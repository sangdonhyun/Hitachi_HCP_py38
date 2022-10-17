'''
Created on 2013. 7. 5.

@author: muse
'''
import os
import socket
import configparser

import common
import base64
import pycurl
import io
import sys



name = "www.python.org"
name = 'www.naver.com'

import hashlib


class HCPHosts():
    def __init__(self):
        self.com = common.Common()
    
    def getPasswd(self,pw):
        m=hashlib.md5()
        m.update(pw)
        return m.hexdigest().strip() 
    
    def curlExeCmd(self,auth):
#         print cmd
        user=auth['user']
        passwd=auth['passwd']
        url = auth['url']
        bu = io.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.HTTPHEADER, ["Accept: application/xml"])
#         curl.setopt(pycurl.HTTPHEADER, ["Authorization: HCP %s"%auth])
#         curl.setopt(pycurl.HTTPHEADER, ["Host: finance.europe.hcp.example.com"])
        curl.setopt(pycurl.COOKIE, "hcp-api-auth=%s:%s"%(user,passwd))
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 20)
        curl.setopt(pycurl.URL, str(url))
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.WRITEFUNCTION, bu.write)
        
        try:
            print('*'*40)
            print(url)
            
            curl.perform()
        except:
            sys.stdout.write('CRUN ERROR')
            pass
        
        recode = curl.getinfo(pycurl.RESPONSE_CODE)
        print('return code :',curl.getinfo(pycurl.RESPONSE_CODE))
        print('*'*40)
        if not curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            print(('#'*50+'\n')*5)
            print('url : ',url)
            print('ERROR',recode)
            print(('#'*50+'\n')*5)
        
        
        curl.close()
        print(bu.getvalue(),recode) 
        return bu.getvalue(),recode 
    
    def curlExeCmd2(self,auth):
#         print cmd
        user=auth['user']
        passwd=auth['passwd']
        url = auth['url']
        bu = io.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.HTTPHEADER, ["Accept: application/xml"])
        curl.setopt(pycurl.HTTPHEADER, ["Authorization: HCP %s:%s"%(user,passwd)])
#         curl.setopt(pycurl.HTTPHEADER, ["Host: finance.europe.hcp.example.com"])
#         curl.setopt(pycurl.COOKIE, "hcp-api-auth=%s:%s"%(user,passwd))
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 20)
        curl.setopt(pycurl.URL, str(url))
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.WRITEFUNCTION, bu.write)
        
        try:
            print('*'*40)
            print(url)
            
            curl.perform()
        except:
            sys.stdout.write('CRUN ERROR')
            pass
        
        recode = curl.getinfo(pycurl.RESPONSE_CODE)
        print('return code :',curl.getinfo(pycurl.RESPONSE_CODE))
        print('*'*40)
        if not curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            print(('#'*50+'\n')*5)
            print('CMD : ',cmd)
            print('ERROR',recode)
            print(('#'*50+'\n')*5)
        
        
        curl.close()
        print(bu.getvalue(),recode) 
        return bu.getvalue(),recode 
    def example(self):
        
        filehandle = open("wind.jpg", 'rb')
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, "https://192.168.125.125/rest/images/wind.jpg")
        curl.setopt(pycurl.COOKIE, "hcp-ns-auth=bXl1c2Vy:3f3c6784e97531774380db177774ac8d")
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.HTTPHEADER, ["Host: finance.europe.hcp.example.com"])
        curl.setopt(pycurl.PUT, 1)
        curl.setopt(pycurl.INFILESIZE, os.path.getsize("wind.jpg"))
        curl.setopt(pycurl.READFUNCTION, filehandle.read)
        curl.perform()
        print(curl.getinfo(pycurl.RESPONSE_CODE))
        curl.close()
        filehandle.close()
    
    def main(self):
        
        user   = input('USER  :')
        passwd = input('PASSWD:')
        url    = input('URl   :')
        port   = input('PORT  :')
#         user='admin'
#         passwd='vmffpxk1!@'
#         url='http://121.170.193.200'
        epasswd = self.getPasswd(passwd).strip()
        euser=base64.encodestring(user).strip()
        print('USER  :',user,'-->%s<--'%euser)
        print('PASSWD:',passwd,'-->%s<--'%epasswd)
        print('URL   :',url)
        if 'http' not in url:
            hurl = 'https://%s'%url
        else:
            hurl=url
        hurl='%s:%s'%(url,port)
        auth={}
        auth['user']=euser
        auth['passwd']=epasswd
        auth['url'] = hurl
        print('TEST1')
        self.curlExeCmd(auth)
        print('TEST2')
        self.curlExeCmd(auth)
        
        
        cpath=input('CRUL PATH:')
        env=os.environ
        print(dir(env))
        path=env['PATH']
        env['PATH']='%s;%s'%(cpath,path)
        cmd='curl -k -i -H "Accept: application/xml" -H "Authorization: HCP %s:%s" "https://admin.%s:9090/mapi/tenants" '%(euser,epasswd,url)
        print(cmd)
        print(os.popen(cmd).read())
        
        print('TEST4')
        cmd='curl -i -H "Accept: application/xml" -b hcp-api-auth=%s:%s "https://admin.%s:9090/static/mapi-4_1_1.xsd" -k'%(euser,epasswd,url)
        print(cmd)
        print(os.popen(cmd).read())
                
         

if __name__=='__main__':
    HCPHosts().main()     