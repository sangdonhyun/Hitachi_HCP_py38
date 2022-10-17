'''
Created on 2013. 7. 3.

@author: muse
'''
import pycurl
import os
import sys
import io
import xml.etree.ElementTree as ET
import urllib.request, urllib.error, urllib.parse
import configparser
from bs4 import BeautifulSoup
# import BeautifulSoup
import common
import socketClient
from python_hosts import Hosts, HostsEntry
import re

class FletaCurl():
    def __init__(self,hcpInfo):
        self.name = hcpInfo['name']
        self.adminauth= hcpInfo['adminauth']
        self.host = hcpInfo['hostname']
        self.ip = hcpInfo['ip']
        self.com = common.Common()
        
        self.fname = os.path.join(self.com.dataDir,'hcp_%s.txt'%self.name)
        self.namespacesCmdList=[]
        self.namespacesCmdDetilList=[]
        self.set_hosts()

    def set_hosts(self):

        if os.path.isfile(self.name):
            os.remove(self.name)
        hosts = Hosts(path=self.name)
        new_entry = HostsEntry(entry_type='ipv4', address=self.ip, names=[self.host, 'hcp'])
        hosts.add([new_entry])
        hosts.write()

    def hcpInfo(self):

        request = urllib.request.Request('http://default.default.%s'%self.host)
        request.get_method = lambda : 'HEAD'
        response = urllib.request.urlopen(request)
        return str(response.info())
    
    
    
    
    """
    """
    def getTenants(self):
        tenantsList = []
        tenants={}
        tenants['name'] = 'admin'
        tenants['user'] = 'admin'
        tenants['auth'] = self.adminauth
        tenantsList.append(tenants)
        tenants['name'] = 'Default'
        tenants['user'] = 'admin'
        tenants['auth'] = self.adminauth
        tenantsList.append(tenants)
        tenants={}
        tenants['name'] = 'fleta'
        tenants['user'] = 'fleta'
#        tenants['auth'] = 'ZmxldGE=:aaac12f039770302dac101baa30ab12c'
        tenants['auth'] = self.adminauth
        tenantsList.append(tenants)
        return tenantsList

    def getTenantInfo(self,tenname):
#         print tenname
        tenants=self.getTenants()
        deften = None
        for ten in tenants:
            if ten['user'] == 'admin':
                deften = ten
        for i in self.getTenants():
            if i['user'] == tenname:
                deften =i
        return deften
            
    
    def commandExec(self,cmd):
        try:
#             print cmd
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            output = stdout.read().strip()
#             print output
        except:
            sys.stdout.write('EXCEPT: %s'%cmd)
            sys.exit(-1)
        return output
    

    def curlExeCmd(self,auth,cmd):
#         print cmd
        
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
        
        try:
            print('*'*40)
            print(cmd)

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
        return bu.getvalue(),recode

    def getAuth(self,user):
        tenList= self.getTenants()
        auth = self.adminauth
        for ten in tenList:
            
            if ten['name'] == user:
                auth = ten['auth'] 
        return auth
    def getUserName(self,user):
        tenList= self.getTenants()
        uname ='admin'
        for ten in tenList:
            
            if ten['name'] == user:
                uname = ten['user'] 
        return uname
    
        
        
    def getTenList(self,xmlstr):
        try:
            root = ET.fromstring(xmlstr)
            tags = root.findall('name')
            tenantsList = []
            for i in  tags:
                tenantsList.append(i.text)
            return tenantsList
        except:
            return []
    
    def AppendnameSpaceList(self,tenname):
        
        
        cmd = 'https://%s.%s:9090/mapi/tenants/%s/namespaces?sortOrder=descending&prettyprint'%(tenname,self.host,tenname)
        
        xmldata,recode = self.curlExeCmd(self.adminauth, cmd)
        
        if not recode ==200:
            return [tenname,'ERROR',None], [tenname,'ERROR',None]
        
#         print xmldata
        ten=self.getTenantInfo(tenname)
        name = ten['name']
        auth = ten['auth']
        user = ten['user']
        
        
        
        root = ET.fromstring(xmldata)
        tags = root.findall('name')
        
        nlist = []
        ndlist = []
        
        
        for i in  tags:
            ns = i.text
            
            """
            https://fleta.hcp.his.test.com:9090/mapi/tenants/fleta/namespaces/ns/statistics?sortOrder=descending&prettyprint
            """
            cmd ="https://%s.%s:9090/mapi/tenants/%s/namespaces/%s?sortOrder=descending&prettyprint"%(tenname,self.host,tenname,ns)
            cmd1="https://%s.%s:9090/mapi/tenants/%s/namespaces/%s/statistics?sortOrder=descending&prettyprint"%(tenname,self.host,tenname,ns)
            
#             print '$'*50
#             print '$'*50
#             print '$'*50
#             print 'tenname : ',tenname
#             print 'ns      : ',ns
#             print 'cmd     : ',cmd
#             print tenname,ns,cmd
#             print '$'*50
#             print '$'*50
#             print '$'*50
            nlist.append([tenname,ns,cmd])
            ndlist.append([tenname,ns,cmd1])
            self.namespacesCmdList.append([tenname,ns,cmd])
            self.namespacesCmdDetilList.append([tenname,ns,cmd1])
        
#         print self.namespacesCmdList
#         print self.namespacesCmdDetilList
        return nlist,ndlist
#        return self.namespaceCmdList,self.namespacesCmdDetilList
    
    def fwrite(self,msg,wbit='a'):
        with open(self.fname,wbit) as f:
            f.write(msg+'\n')

    def getNodeUsage(self,xmldata):
        s = BeautifulSoup(xmldata,'html.parser')
        
        #print s
        serial = ''
        for line in xmldata.splitlines():
            if 'Serial number:' in line or 'Serial Number:' in line:
                serial = line.split(':')[1]
        
        self.fwrite('serial : '+serial)
        
        nodeIdList = []
        for item in s.findAll('a'):
            linka= item['href']
            if 'nodeNumber=' in  linka:
                nodeIdList.append(linka.split('nodeNumber=')[1])
        
        
        i=0
        for node in s.findAll('td', {'class' :"usage last"}):
            self.fwrite ('Node ID : '+nodeIdList[i] +', Volume Usage :'+node.text)
            i = i+1       
        
        return nodeIdList
    def getSerial(self):
        auth = self.adminauth
        cmd = 'https://admin.%s:8000/cluster/nodeList.action'%self.host
        xmldata,recode= self.curlExeCmd(auth, cmd)
       
        serial = ''
        for line in xmldata.splitlines():
            if 'Serial number:' in line:
#                 print line
                serial = line.split('Serial number:')[1]
            if 'Serial Number:' in line:
                #                 print line
                serial = line.split('Serial Number:')[1]

        return serial.strip()
    
    
    def  run(self):
        """
        step 1 ) tenants list (admin)          "https://admin.hcp.his.test.com:9090/mapi/tenants?sortType=hardQuota&sortOrder=descending&prettyprint"
        step 2 ) fleta detail (admin)          "https://admin.hcp.his.test.com:9090/mapi/tenants/fleta?sortOrder=descending&prettyprint"
        step 3 ) fleta statistcs (fleta)       "https://fleta.hcp.his.test.com:9090/mapi/tenants/fleta/statistics?sortOrder=descending&prettyprint"
        step 4 ) felta namespace list (fleta)  "https://fleta.hcp.his.test.com:9090/mapi/tenants/fleta/namespaces?sortOrder=descending&prettyprint"
        step 5 ) felta namespace detail (fleta)"https://fleta.hcp.his.test.com:9090/mapi/tenants/fleta/namespaces/ns/statistics?sortOrder=descending&prettyprint"
        """
        self.fwrite(self.com.getHeadMsg('FLETA HCP MODULE(%s)'%self.host), 'w')
        #STEP 0 HCP INFO
        self.fwrite('###***SERIAL.START***###')
        self.fwrite(self.getSerial())
        self.fwrite('---SERIAL.END---')
        self.fwrite('###***HOSTNAME.START***###')
        self.fwrite(self.host)
        self.fwrite('---HOSTNAME.END---')
        ten=self.getTenantInfo('admin')
        name = ten['name']
        auth = ten['auth']
        user = ten['user']
        
        self.fwrite('###***OVERVIEW.START***###')
        cmd = "https://admin.%s:8000/cluster/storageVolumeGraph.action?forceCurrent=false"%self.host
        print('-'*40)
        print(auth)
        print('-'*40)
        xmldata,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xmldata)
        self.fwrite('---OVERVIEW.END---')
        
        
#        self.fwrite('###***HCPINFO.START***###')
#        self.fwrite(self.hcpInfo())
#        self.fwrite('---HCPINFO.END---')
#        
        
        
        # STEP 1
        
        cmd = "https://admin.%s:9090/mapi/tenants?sortType=hardQuota&sortOrder=descending&prettyprint"%self.host
        self.fwrite('###***TENANTS.LIST.START***###')
        
        tenxml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(tenxml)
        tenList = self.getTenList(tenxml)
        
        
        
        
        
        self.fwrite('---TENANTS.LIST.END---\n\n')
        self.fwrite('###***TENANTS.SUB.START***###')
        cmd = "https://admin.%s:8000/cluster/tenants_tableData.action"%self.host
        xml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xml)
        
        self.fwrite('---TENANTS.SUB.END---')

        
        
        
        #STEP3 
        
        for ten in tenList:
            self.fwrite('###***TANENTS.NS.START.TENANTS %s***###'%ten)
            
            cmd ='https://%s.%s:8000/tenant/namespace_tableData.action'%(ten,self.host)
            
            tenxml,recode =self.curlExeCmd(auth, cmd)
            self.fwrite(tenxml)
#            self.fwrite('#'*50)
            self.fwrite('---TANENTS.NS.END.TENANTS %s---'%ten)
        
       
        """
        7. user data
curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://121.138.181.180:8000/cluster/users_tableData.action"
8. system event
(1) Overview -> Major Events
curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://121.138.181.180:8000/cluster/majorEvents.action"
(2) Monitoring -> System Events -> All Events
curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://121.138.181.180:8000/cluster/allSystemEventsLog.action?divID=stBox_1&amp;title=All+System+Events&amp;action=allSystemEventsLog" > all.txt
(3) Monitoring -> System Events -> Security Events
curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://121.138.181.180:8000/cluster/securityEventsLog.action?divID=stBox_2&amp;title=Security+Events&amp;action=securityEventsLog" > sec.txt
9. Services status
curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://admin.hcp.his.test.com:8000/cluster/currentPolicyStatus.action"
        """
        # user data
        self.fwrite('###***USERDATA.START***###')
        cmd = "https://%s:8000/cluster/users_tableData.action"%self.ip
        xml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xml)
        self.fwrite('---USERDATA.END---')
        
        self.fwrite('###***EVENTS.MAJOR.START***###')
        cmd = "https://%s:8000/cluster/majorEvents.action"%self.ip
        xml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xml)
        self.fwrite('---EVENTS.MAJOR.END---')
        
        self.fwrite('###***EVENTS.ALL.START***###')
        cmd = "https://%s:8000/cluster/allSystemEventsLog.action?divID=stBox_1&amp;title=All+System+Events&amp;action=allSystemEventsLog"%self.ip
        xml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xml)
        self.fwrite('---EVENTS.ALL.END---')
        
        self.fwrite('###***EVENTS.ALL.START***###')
        cmd = "https://%s:8000/cluster/securityEventsLog.action?divID=stBox_2&amp;title=Security+Events&amp;action=securityEventsLog"%self.ip
        xml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xml)
        self.fwrite('---EVENTS.SECURITY.END---')

        self.fwrite('###***SERVICES.STATUS.START***###')
        cmd = "https://admin.%s:8000/cluster/currentPolicyStatus.action"%self.host
        xml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xml)
        self.fwrite('---SERVICES.STATUS.END---')
        
        self.fwrite('###***ALLOWEDIP.START***###')
        cmd = "https://admin.%s:8000/cluster/consoleSecurity_ipListManager.action?divId=ipListManager&actionPrefixName=consoleSecurity_ipListManager&numTabs=2&selectedTabNum=0&tabTitles=Allow&tabTitles=Deny&listIds=admin.allow_list&listIds=admin.deny_list&showAllowFirsts=true&showAllowFirsts=true&allowFirstId=admin.allow_first"%self.host
        xml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(xml)
        self.fwrite('---ALLOWEDIP.END---')
        
        self.fwrite('###***NODE.START***###')
        cmd = "https://admin.%s:8000/cluster/nodeList.action"%self.host
        
        
        
        #admin/hcpadmin1
        xmldata,recode =self.curlExeCmd(auth, cmd)
        
        nodeIdList = self.getNodeUsage(xmldata)
        
        self.fwrite('---NODE.END---')
        self.fwrite('###***NODE.DETAIL.START***###')
        for nodeId in nodeIdList:
            self.fwrite('NODE ID : %s'%nodeId)
            cmd = "https://admin.%s:8000/cluster/nodeDetails.action?nodeNumber=%s"%(self.host,nodeId)
            xmldata,recode =self.curlExeCmd(auth, cmd)
            
            self.fwrite(xmldata)
            self.fwrite('#'*50)
        
        self.fwrite('---NODE.DETAIL.END---')
        self.fwrite('###***TENENTS.URL.START***###')
        cmd ='https://admin.%s:8000/cluster/tenants_tableData.action'%self.host
        xmldata,recode =self.curlExeCmd(auth, cmd)
        try:
            self.getTenantInfoUrl(xmldata)
        except:
            pass
        
        
        self.fwrite('---TENENTS.URL.END---')
        
        
        
        
        
        #curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://admin.hcp.his.test.com:8000/cluster/consoleSecurity_ipListManager.action?divId=ipListManager&actionPrefixName=consoleSecurity_ipListManager&numTabs=2&selectedTabNum=0&tabTitles=Allow&tabTitles=Deny&listIds=admin.allow_list&listIds=admin.deny_list&showAllowFirsts=true&showAllowFirsts=true&allowFirstId=admin.allow_first"
        #curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://admin.hcp.his.test.com:8000/cluster/nodeList.action"
        #curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://admin.hcp.his.test.com:8000/cluster/getAdminView.action"
        endMsg=self.com.getEndMsg()
        print(endMsg)
        self.fwrite(endMsg)
        with open(self.fname) as f:
            content = f.read()
        if not re.search('Change Password',content):
            self.fileTran()
        
    
        
    def fileTran(self):
        try:
            cfg = configparser.RawConfigParser()
            cfg_file = os.path.join('config','config.cfg')
            cfg.read(cfg_file)
            tarn= cfg.get('server','tran',fallback='SOCKET')
            targetDir = cfg.get('server','targetDir',fallback='HCP.disk')
        except Exception as e:
            print(str(e))
            tarn = 'SOCKET'
            targetDir='HCP.disk'
        if tarn.upper()=='SOCKET':
            socketClient.SocketSender(FILENAME=self.fname,DIR=targetDir).main()
        else:
            self.com.fletaPutFtp(self.fname, targetDir)
        
    def getTenUrl(self,urlList,uid):
        for turl in urlList:
            if uid in turl:
                return turl
#        
    
    def getTenantInfoUrl(self,xmldata):
        
#        print 'cmdUrl : ',cmd
#        xmlData,recode=self.curlExeCmd(cmd,auth)
        soup = BeautifulSoup(xmldata,'html.parser')
        print(soup)
        url = soup.findAll('div',{'class':'infoContent'})
        urlList = []
        
        for i in url:
            suri = str(i['rdiv'])
            url = 'https://admin.%s:8000'%self.host+suri
            urlList.append(url)
        
        for ten in soup.findAll('tr',{'class':'titleRow'}):
            
            uid =  str(ten['id'])
            if 'titleRow_' in uid:
                uid = uid.split('titleRow_')[1]
            turl=self.getTenUrl(urlList,uid)        
            s2 = BeautifulSoup(str(ten),'html.parser')
            tenInfo=[]
            for td in  s2.findAll('td'):
                tenInfo.append(td.text)
            tenDic ={}
            tenDic['UID']          = uid
            tenDic['URL']          = turl
            tenDic['Name']         = tenInfo[0] 
            tenDic['Mgmt Network'] = tenInfo[1]
            tenDic['Data Network'] = tenInfo[2]
            tenDic['Alerts']       = tenInfo[3]
            tenDic['Storage Used'] = tenInfo[4]
            tenDic['Quota']        = tenInfo[5]
            
            self.fwrite('#### USERNAME : %s'%tenDic['Name'])
            for i in list(tenDic.keys()):
                msg = '%s : %s'%(i,tenDic[i])
                self.fwrite(msg)
            
        
            # detail info
            detailInfoList=self.tenantDetail(turl)
            for i in detailInfoList:
                for key in list(i.keys()):
                    self.fwrite('%s : %s'%(key,i[key]))
            self.fwrite('#'*50)
            
    
    def tenantDetail(self,cmdUrl):
        xmlData,recode = self.curlExeCmd(self.adminauth,cmdUrl) 
    
        soup= BeautifulSoup(xmlData,'html.parser')
        devList=[]
        for i in soup.findAll('div',{'class':'pkShadowWrap'}):
            devInfo={}
            print(('#'*50+'\n')*5)
            title = i.find('h3').text
            s1= BeautifulSoup(str(i),'html.parser')
            for art in  s1.findAll('div',{'class':"sp-row"}):
                cont= art.text
                if ':' in cont:
                    contS = cont.split(':')
                    devInfo['%s_%s'%(title,contS[0])] = contS[1]
            devList.append(devInfo)  
#         print devList
        return devList
    
    def getTenantsInfo(self):
        """
        curl -k -i -H "Accept: application/xml" -H "Authorization: HCP YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b" "https://admin.hcp.his.test.com:8000/cluster/tenant_input.action?uuId=00000000-0000-0000-0000-000000000000&rowIndex=0"
        """
        uidList = self.uidList()
        cmdList  =[]
        for uid in uidList:
            cmd='https://admin.%s:8000/cluster/tenant_input.action?uuId=%s&rowIndex=0'%(self.host,uid)
            cmdList.append(cmd)
        return cmdList
    
    
    def moTest(self):
        auth = 'YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b'
        cmd='https://minsoo2.hcp.his.test.com:9090/mapi/tenants/minsoo2/namespaces?sortOrder=descending&prettyprint'
        tenxml,recode =self.curlExeCmd(auth, cmd)
        print(tenxml)
        
        
        
    def test(self):
#        cmd ='https://admin.hcp.his.test.com:8000/cluster/tenants_tableData.action'
#        auth = 'YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b'
#        xmldata,recode=self.curlExeCmd(auth, cmd)
#        self.test1(xmldata)
#        print self.uidList()
        auth = 'YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b'
        
        cmd = "https://admin.%s:9090/mapi/tenants?sortType=hardQuota&sortOrder=descending&prettyprint"%self.host
        self.fwrite('###***TENANTS.LIST.START***###')
        
        tenxml,recode =self.curlExeCmd(auth, cmd)
        self.fwrite(tenxml)
        print(tenxml)
        tenList = self.getTenList(tenxml)
        print(tenList)
        
        
        
        for i in tenList:
            cmd = "https://%s.%s:9090/mapi/tenants/%s/namespaces?sortOrder=descending&prettyprint"%(i,self.host,i)
            
            print(cmd)
            tenxml,recode =self.curlExeCmd(auth, cmd)
            
            print(self.AppendnameSpaceList(i,tenxml))
            
    
    
    def dev(self):
        cmd ="https://admin.%s:8000/cluster/tenants_tableData.action"%self.host
        auth = 'YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b'
        xmldata,recode=self.curlExeCmd(auth, cmd)
        print(xmldata)
        
    def dev11(self):
        cmd ="https://admin.%s:8000/cluster/tenant_input.action?uuId=9d8d71b5-9504-4546-9bd2-be9790d33939&rowIndex=0"%self.host
        self.dev(cmd)
        
        
        

class FletaCurnRun():
    def __init__(self):
        self.com  = common.Common()
        cfg = configparser.RawConfigParser()
        cfg.read(os.path.join(self.com.confDir,'config.cfg'))
#         self.hostlist = []
#         print cfg.options('HOSTS')
#         for host in  sorted(set(cfg.options('HOSTS'))):
#             print cfg.get('HOSTS','host01')
#             self.hostlist.append(cfg.get('HOSTS','host01'))
    
        self.hcplist = self.hcpHosts()
    
    def hcpHosts(self):
        cfg = configparser.RawConfigParser()
        cfg.read(os.path.join(self.com.confDir,'hcp.cfg'))
        hcpList = []
        for hcp in sorted(set(cfg.sections())):
            hcpInfo = dict()
            hcpInfo['name'] = hcp
            for arg in cfg.options(hcp):
                hcpInfo[arg] = cfg.get(hcp,arg)
            hcpList.append(hcpInfo)
        return hcpList
            
    
    def main(self):
        
        
        for hcpInfo in self.hcplist:
#            FletaCurl(host).test()
#            FletaCurl(host).moTest()
            FletaCurl(hcpInfo).run()            

        
        
if __name__=='__main__':
    FletaCurnRun().main()
    
    

    