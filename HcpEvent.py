'''
Created on 2013. 7. 8.

@author: muse
'''
import pycurl
import os
import sys
import io
import xml.etree.ElementTree as ET
import urllib.request, urllib.error, urllib.parse
import configparser

import common

class HcpEvent():
    def __init__(self):
        self.com = common.Common()
        self.loger = self.com.logger
        self.fname = ''
    
    def getHostList(self):
        cfg = configparser.RawConfigParser()
        cfg.read(os.path.join(self.com.confDir,'hcphost.cfg'))
        hostList = []
        for host in cfg.sections():
            hostInfo={}
            hostInfo['name'] = host
            for item in cfg.items(host):
                hostInfo[item[0]] = item[1]
            hostList.append(hostInfo)
        return hostList
    def getSerial(self,auth):
        
        cmd = 'https://admin.hcp.his.test.com:8000/cluster/nodeList.action'
        xmldata,recode= self.curlExeCmd(auth, cmd)
        serial = ''
        for line in xmldata.splitlines():
            if 'Serial number:' in line:
                print(line)
                serial = line.split('Serial number:')[1]
        
        return serial.strip()
    def curlExeCmd(self,auth,cmd):
        print(cmd)
        
        bu = io.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.HTTPHEADER, ["Accept: application/xml"])
        curl.setopt(pycurl.HTTPHEADER, ["Authorization: HCP %s"%auth])
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 20)
        curl.setopt(pycurl.URL, str(cmd))
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.WRITEFUNCTION, bu.write)
        
        curl.perform()
        
        recode = curl.getinfo(pycurl.RESPONSE_CODE)
        print('return code :',curl.getinfo(pycurl.RESPONSE_CODE))
        if not curl.getinfo(pycurl.RESPONSE_CODE) == 200:
            print(('#'*50+'\n')*5)
            print('ERROR',recode)
            print(('#'*50+'\n')*5)
             
        curl.close()
        return bu.getvalue(),recode

    
    def getCmdList(self):
        """
        (1) Overview -> Major Events
        curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://121.138.181.180:8000/cluster/majorEvents.action"
        (2) Monitoring -> System Events -> All Events
        curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://121.138.181.180:8000/cluster/allSystemEventsLog.action?divID=stBox_1&amp;title=All+System+Events&amp;action=allSystemEventsLog" > all.txt
        (3) Monitoring -> System Events -> Security Events
        curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://121.138.181.180:8000/cluster/securityEventsLog.action?divID=stBox_2&amp;title=Security+Events&amp;action=securityEventsLog" > sec.txt
        9. Services status
        curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://admin.hcp.his.test.com:8000/cluster/currentPolicyStatus.action"
        """
        cfg = configparser.RawConfigParser()
        cfg.read(os.path.join(self.com.confDir,'eventcmd.cfg'))
        cmdList =[]
        for cmdInfo in sorted(set(cfg.sections())):
            cmd = cfg.get(cmdInfo,'cmd')
            title = cfg.get(cmdInfo,'title')
            cmdList.append((title,cmd))
        
        return cmdList
            
        
    def fwrite(self,msg,wbit='a'):
        with open(self.fname,wbit) as f:
            f.write(msg+'\n')
    
    def run(self):
        
        for hostInfo in self.getHostList():
            print(hostInfo['name'])
            hostname= hostInfo['hostname']
            admin_user = hostInfo['admin_user']
            port= hostInfo['port']
            auth= hostInfo['admin_auth']
            self.fname = os.path.join(self.com.dataDir,'hcp_event_%s.tmp'%hostname)
            self.fwrite(self.com.getHeadMsg('FLETA HCP EVENT(%s)'%hostname), 'w')
            #STEP 0 HCP INFO
            self.fwrite('###***SERIAL.START***###')
            self.fwrite(self.getSerial(auth))
            self.fwrite('---SERIAL.END---')
            self.fwrite('###***HOSTNAME.START***###')
            self.fwrite(hostname)
            self.fwrite('---HOSTNAME.END---')
            
            
            for title,cmd in self.getCmdList():
                self.fwrite(title)
                self.fwrite('COMMAND: %s'%cmd)
                cmd = cmd.replace('<HOSTNAME>',hostname)
                cmd = cmd.replace('<ADMIN_USER>',admin_user)
                print(cmd)
                xmlData,recode = self.curlExeCmd(auth, cmd)
                self.fwrite(xmlData.strip())
        endmsg = self.com.getEndMsg()
        print(endmsg)
        self.fwrite(endmsg)
    
    
    
    def curlTest(self):
        auth='YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b'
        cmd = "https://121.138.181.180:8000/cluster/majorEvents.action"
        cmd = "https://admin.hcp.his.test.com:8000/cluster/majorEvents.action"
        
        data = self.curlExeCmd(auth, cmd)
        print(data)
        
    
if __name__=='__main__':
    HcpEvent().run()