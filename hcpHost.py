'''
Created on 2013. 7. 5.

@author: muse
'''
import os
import socket
import configparser

import common




name = "www.python.org"
name = 'www.naver.com'




class HCPHosts():
    def __init__(self):
        self.hosts = 'hosts'
        self.com = common.Common()
    
    def getHosts(self):
        with open(self.hosts) as f:
            f.read()
    
    def hcpHost(self):
        cfg = configparser.RawConfigParser()
        cfg.read(os.path.join(self.com.confDir,'hcp.cfg'))
        hcpList =[]
        for hcp in sorted(set(cfg.sections())):
            hcpInfo={}
            for i in cfg.options(hcp):
                hcpInfo[i] = cfg.get(hcp,i)
            hcpList.append(hcpInfo)
        return hcpList
    
    def getIp(self,name):
        try:
            host = socket.gethostbyname(name)
            print(host)
        except socket.gaierror as err:
            print("cannot resolve hostname: ", name, err)
            
        return host
    
    def main(self):
        hcpList= self.hcpHost()
        for hcp in hcpList:
            host= hcp['hostname']
            print(host)
        

if __name__=='__main__':
    HCPHosts().main()     