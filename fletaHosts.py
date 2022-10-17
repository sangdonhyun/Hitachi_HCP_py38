'''
Created on 2013. 7. 15.

@author: muse
'''
import os,sys
import socket
import io
import pycurl
import xml.etree.ElementTree as ET
import re
#--
import common
import hcpHost


com = common.Common()
hostname = 'admin.hcp.his.test.com'
addr = socket.gethostbyname(hostname)
print('The address of ', hostname, 'is', addr)

import fletaPortScan




class SysHosts():
    def __init__(self):
        self.hostsFile = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
        if not os.path.isfile(self.hostsFile):
            self.hostsFile=input('hosts file:')
            
        self.portScan = fletaPortScan.PortScan()
        
    
    def checkIP(self,ip):
        pat = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
        check= pat.match(ip)
        if check:
            return True
        else:
            return False
    def getSysHosts(self):
        with open(self.hostsFile) as f:
            tmp = f.readlines()
        
        syshostList=[]
        for i in tmp:
            
            hh= i.strip().split()
#            print hh
                        
            if hh != [] :
                if self.checkIP(hh[0]):
                    print(hh[0],hh[1],self.portScan.verbose_ping(hh[1]))
                    syshostList.append((hh[0],hh[1],self.portScan.verbose_ping(hh[1])))
#                ip,hostname = hh[0:1]
#                print 'host : ',ip,hostname.strip()
        return syshostList
    
    def sysHostsBackup(self):
        date=com.getNow('%y%m%d%H%M%S')
        backupFile = os.path.join(os.path.dirname(self.hostsFile),'hosts.%s'%date)
        print(backupFile)
        
        with open(self.hostsFile) as f:
            hosts=f.read()
        with open(backupFile ,'w') as f:
            f.write(hosts)
#    
    
    def addSysHost(self,hostList):
        self.sysHostsBackup()
        date = com.getNow()
        msg =  '#------- FLETA HCP HOSTS DATE:%s\n'%date
        for ip,host in hostList:
            
            msg=msg+ '%s    %s\n'%(ip,host)
        msg=msg+ '#------- FLETA HCP HOSTS END\n'
        with open(self.hostsFile,'a') as f:
            f.write(msg)

class hcpHost():
    def __init__(self):

        self.hcpHosts = com.hcpHost()
        self.syshost = SysHosts()
        self.sysHost = self.syshost.getSysHosts()
        self.portScan = fletaPortScan.PortScan()
    
    def getTenList(self,xmlstr):
       
        
        root = ET.fromstring(xmlstr)
        tags = root.findall('name')
        tenantsList = []
        for i in  tags:
            tenantsList.append(i.text)
        return tenantsList
    
    def getHcpSysHost(self,host):
        for ip,hostname,ping in self.sysHost:
            if host == hostname:
                return True
        return False
    
    
    def backupHosts(self):
        self.syshost.sysHostsBackup()
    
    
    
    
    def main(self):
        cmd = "https://admin.<HOSTNAME>:9090/mapi/tenants?sortType=hardQuota&sortOrder=descending&prettyprint"
        print(com.getHeadMsg('hcp hosts config'))
        print(self.hcpHosts)
        for i in self.hcpHosts:
            print(i)
            auth= i['adminauth']
            hostname= i['hostname']
            ip = i['ip']
            cmd = cmd.replace('<HOSTNAME>',hostname)
            xmldata,recode =com.curlExeCmd(auth, cmd)
            print(hostname)
#            print recode
#            print xmldata
            tenList = self.getTenList(xmldata)
            addHostList =[]
            print(tenList)
            for ten in tenList:
                hn = '%s.%s'%(ten,hostname)
                print(hn)
                if self.getHcpSysHost(hn) and self.portScan.verbose_ping(hn):
                
                    addHostList.append((ip,hn))
        self.syshost.addSysHost(addHostList)
        
        
    

if __name__=='__main__':
    hcpHost().main()
    
    
        
        