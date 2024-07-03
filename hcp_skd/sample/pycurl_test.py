import pycurl
import os
from io import StringIO
import requests
import hashlib
import base64
from socket import AF_INET
from socket import SOCK_STREAM
from socket import socket
from io import BytesIO
import json
import xmltodict
from bs4 import BeautifulSoup



class conn_test():
    def __init__(self,hcp_info):
        self.user = hcp_info['USER']
        self.passwd = hcp_info['PASSWD']
        self.auth  = self.get_auth(self.user,self.passwd)
        self.target_url = hcp_info['target_url']
        self.file_name = os.path.join('data','hcp_{}.txt'.format(self.target_url))

    def get_auth(self, user,passwd):
        enc = hashlib.md5()
        enc.update(passwd.encode('utf-8'))
        enc_pass = enc.hexdigest()
        # print(enc_pass)
        enc_user = base64.encodebytes(user.encode('utf-8')).strip()
        # print(enc_user)
        if isinstance(enc_user, bytes):
            enc_user = enc_user.decode('utf-8')
        """
        YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b
        """
        admin_auth = enc_user + enc_pass
        print(admin_auth)
        return admin_auth


    def curl_test(self, url ,auth):
        b_obj = BytesIO()
        curl = pycurl.Curl()

        curl.setopt(pycurl.HTTPHEADER, ["Accept: application/xml",
                                        "Authorization: HCP %s" % auth])
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 20)
        curl.setopt(pycurl.URL, str(url))
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.WRITEFUNCTION, b_obj.write)
        curl.perform()
        recode = curl.getinfo(pycurl.RESPONSE_CODE)
        # if not curl.getinfo(pycurl.RESPONSE_CODE) == 200:
        #     print(('#' * 50 + '\n') * 5)
        #     print('CMD : ', cmd)
        #     print('ERROR', recode)
        #     print(('#' * 50 + '\n') * 5)
        print(curl.getinfo(pycurl.RESPONSE_CODE))
        # print(b_obj.getvalue())
        get_body = b_obj.getvalue()

        # Decode the bytes stored in get_body to HTML and print the result
        # print('Output of GET request:\n%s' % get_body.decode('utf8'))
        curl.close()
        return get_body

    def test_port_number(self, host, port):
        # create and configure the socket
        # print(host,port)
        with socket(AF_INET, SOCK_STREAM) as sock:
            # set a timeout of a few seconds
            sock.settimeout(3)
            # connecting may fail
            try:
                # attempt to connect
                sock.connect((host, port))
                # a successful connection was made
                return True
            except Exception as e:
                # print(str(e))
                # ignore the failure
                return False

    # scan port numbers on a host
    def ports_scan(self, host, ports):
        print(f'Scanning {host}...')
        # scan each port number
        for port in ports:
            if self.test_port_number(host, port):
                print(f'> {host}:{port} open')
            else:
                print(f'> {host}:{port} close')

    def port_scan(self, host, port):
        print(f'Scanning {host}...')
        # scan each port number
        if self.test_port_number(host, port):
            print(f'> {host}:{port} open')
        else:
            print(f'> {host}:{port} close')

    def get_tenants(self, auth):
        """
        https://admin.%s:9090/mapi/tenants?sortType=hardQuota&sortOrder=descending&prettyprint
        :return:
        """
        url = 'https://admin.{}:9090/mapi/tenants'.format(self.target_url)
        cmd = 'curl -k -H "Authorization: HCP {AUTH}" -H "Content-Type: application/xml" -H "Accept: application/xml"  "{CMD}"'.format(AUTH=auth, CMD=url)
        ret=os.popen(cmd).read(0)
        jsonString = json.dumps(xmltodict.parse(ret), indent=4)
        print(jsonString)
        json_data = json.loads(jsonString)
        return json_data

    def fwrite(self,msg,wbit='a'):
        with open(self.file_name, wbit) as fw:
            fw.write(msg)
            fw.write('\n')

    def getSerial(self):
        auth = self.auth
        cmd = 'https://admin.%s:8000/cluster/nodeList.action' % self.host
        xmldata, recode = self.curl_test(auth, cmd)
        recode = self.curl_test(self.target_url, self.auth)
        serial = ''
        for line in xmldata.splitlines():
            if 'Serial number:' in line:
                #                 print line
                serial = line.split('Serial number:')[1]
            if 'Serial Number:' in line:
                #                 print line
                serial = line.split('Serial Number:')[1]

        return serial.strip()

    def test(self):
        print('#'*50)
        port = 80
        self.port_scan(self.target_url,port)
        recode = self.curl_test(self.target_url, self.auth)
        print(self.target_url, port, recode)
        full_url = 'http://{}:{}'.format(self.target_url,port)
        adm_url='admin.{}'.format(self.target_url, self.auth)
        print(adm_url)
        port = 8000
        self.port_scan(adm_url,port)
        recode = self.curl_test(self.target_url, self.auth)
        print(adm_url,port,recode)
        port = 9090
        self.port_scan(adm_url, port)
        tenant_list = self.get_tenants()
        self.fwrite('###***nodes statistics***###')
        url = 'https://admin.{}:9090/mapi/nodes/statistics'.format(self.target_url)
        recode = self.curl_test(self.target_url, self.auth)

        for tenant in tenant_list:
            url = 'https://{}.{}:9090/mapi/tenants'.format(tenant,self.target_url)
            ten_user = 'ten'
            ten_pass = 'ten'
            ten_auth = self.get_auth(ten_user,ten_pass)

            recode = self.curl_test(self.target_url, ten_auth)

            url ='https://{}.{}:9090/mapi/tenants/{TENANT_NAME}/namespaces'.format(tenant,self.target_url,TENANT_NAME=tenant)
            recode = self.curl_test(self.target_url, ten_auth)
            recode = self.curl_test(url)



    def get_tenant_resources(self):
        """
        https://admin.hcp.example.com:9090/mapi/tenants?username=lgreen
        https://admin.{HOST}:9090/mapi/tenants/{TEN}/statistics?sortOrder=descending&prettyprint
        :return:
        """
        url_list = list()
        url_list.append('/tenants')
        url_list.append('/tenants/<tenant-name>')
        url_list.append('/tenants/<tenant-name>/availableServicePlans')
        url_list.append('/tenants/<tenant-name>/availableServicePlans/<service-plan-name>')
        url_list.append('/tenants/<tenant-name>/chargebackReport')
        url_list.append('/tenants/<tenant-name>/consoleSecurity')
        url_list.append('/tenants/<tenant-name>/contactInfo')
        url_list.append('/tenants/<tenant-name>/emailNotification')
        url_list.append('/tenants/<tenant-name>/namespaceDefaults')
        url_list.append('/tenants/<tenant-name>/permissions')
        url_list.append('/tenants/<tenant-name>/searchSecurity')
        url_list.append('/tenants/<tenant-name>/statistics')
        return url_list

    def get_namespace_resources(self):
        """
        https://finance.hcp.example.com:9090/mapi/tenants/finance/namespaces

        curl -k -i -d @AR-compliance.xml -H "Content-Type: application/xml"
    -H "Authorization: HCP bXdoaXRl:ad49ce36d0cec9634ef63b24151be0fb"
    "https://finance.hcp.example.com:9090...ce/namespaces/
         accounts-receivable/complianceSettings"

         https://finance.hcp.example.com:9090...ce/namespaces/accounts-receivable/complianceSettings"
        :return:
        """
        url_list = list()
        url_list.append('/tenants/<tenant-name>/namespaces')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/chargebackReport')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/complianceSettings')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/customMetadataIndexingSettings')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/permissions')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/protocols')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/protocols/<protocol-name>')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/replicationCollisionSettings')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/statistics')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/versioningSettings')

    def get_network_resources(self):
        url_list = list()
        url_list.append('/network')

    def retention_class_resources(self):
        """
        curl -k -H "Content-Type: application/xml"  -H "Authorization: HCP bXdoaXRl:ad49ce36d0cec9634ef63b24151be0fb"
        "https://finance.hcp.example.com:9090/mapi/tenants/finance/namespaces/accounts-receivable/retentionClasses?prettyprint"
        :return:
        """
        url_list = list()
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/retentionClasses')
        url_list.append('/tenants/<tenant-name>/namespaces/<namespace-name>/retentionClasses/<retention-class-name>')

    def content_class_resources(self):
        """
        curl -k -H "Content-Type: application/xml"  -H "Authorization: HCP bXdoaXRl:ad49ce36d0cec9634ef63b24151be0fb"
        "https://anytown-general-hospital.hcp.example.com:9090/mapi/tenants/anytown-general-hospital/contentClasses"
        :return:
        :return:
        """

    def get_replication_rsources(self):
        """
        curl -k -iT MA-CA.xml -H "Content-Type: application/xml"
    -H "Authorization: HCP YWxscm9sZXM=:04EC9F614D89FF5C7126D32ACB448382"
    "https://admin.hcp-ma.example.com:9090/mapi/services/replication/links"
        :return:
        """
        url_list = list()
        url_list.append('/services/replication')
        url_list.append('/services/replication/certificates/<certificate-id>')
        url_list.append('/services/replication/certificates/server')
        url_list.append('/services/replication/links')
        url_list.append('/services/replication/links/<link-name>')
        url_list.append('/services/replication/links/<link-name>/content')
        url_list.append('/services/replication/links/<link-name>/content/defaultNamespaceDirectories')
        url_list.append('/services/replication/links/<link-name>/content/defaultNamespaceDirectories/<directory-name>')
        url_list.append('/services/replication/links/<link-name>/content/chainedLinks')
        url_list.append('/services/replication/links/<link-name>/content/chainedLinks/<link-name>')
        url_list.append('/services/replication/links/<link-name>/content/tenants')
        url_list.append('/services/replication/links/<link-name>/content/tenants/<tenant-name>')
        url_list.append('/services/replication/links/<link-name>/localCandidates')
        url_list.append('/services/replication/links/<link-name>/localCandidates/defaultNamespaceDirectories')
        url_list.append('/services/replication/links/<link-name>/localCandidates/chainedLinks')
        url_list.append('/services/replication/links/<link-name>/localCandidates/tenants')
        url_list.append('/services/replication/links/<link-name>/remoteCandidates')
        url_list.append('/services/replication/links/<link-name>/remoteCandidates/defaultNamespaceDirectories')
        url_list.append('/services/replication/links/<link-name>/remoteCandidates/chainedLinks')
        url_list.append('/services/replication/links/<link-name>/remoteCandidates/tenants')
        url_list.append('/services/replication/links/<link-name>/schedule')

    def get_topology_resources(self):
        """
        https://admin.hcp-us.example.com:9090/mapi/services/erasureCoding/linkCandidates?verbose=true&prettyprint
        :return:
        """
        url_list = list()
        url_list.append('/services/erasureCoding/ecTopologies')
        url_list.append('/services/erasureCoding/ecTopologies/<ec-topology-name>')
        url_list.append('/services/erasureCoding/ecTopologies/<ec-topology-name>/tenantCandidates')
        url_list.append('/services/erasureCoding/ecTopologies/<ec-topology-name>/tenantConflictingCandidates')
        url_list.append('/services/erasureCoding/ecTopologies/<ec-topology-name>/tenants')
        url_list.append('/services/erasureCoding/ecTopologies/<ec-topology-name>/tenants/<tenant-name>')
        url_list.append('/services/erasureCoding/linkCandidates')

    def get_license_resources(self):
        """
        https://admin.hcp.example.com:9090/mapi/storage/licenses
        :return:
        """

    def get_node_statistics_resources(self):
        """
        https://admin.hcp.example.com:9090/mapi/nodes/statistics?prettyprint
        :return:
        """

    def get_services_statistics_rsources(self):
        """
        https://admin.hcp.example.com:9090/mapi/services/statistics?prettyprint
        :return:
        """

    def get_8000(self, target_url, tenant = None):
        """
        https://admin.%s:8000/cluster/storageVolumeGraph.action?forceCurrent=false
        :return:
        """
        url_list = list()
        url_list.append('https://admin.{}:8000/cluster/storageVolumeGraph.action?forceCurrent=false'.format(target_url))
        url_list.append('https://admin.{}:8000/cluster/tenants_input.action'.format(target_url))
        url_list.append('https://admin.{}:8000/cluster/tenants_tableData.action'.format(target_url))
        url_list.append('https://{}.{}:8000/tenant/namespace_tableData.action'.format(tenant, target_url))
        url_list.append('https://{}:8000/cluster/users_tableData.action'.format(target_url))
        url_list.append('https://{}:8000/cluster/majorEvents.action'.format(target_url))
        url_list.append('https://{}:8000/cluster/allSystemEventsLog.action?divID=stBox_1&amp;title=All+System+Events&amp;action=allSystemEventsLog'.format( target_url))
        url_list.append('https://{}:8000/cluster/securityEventsLog.action?divID=stBox_2&amp;title=Security+Events&amp;action=securityEventsLog'.format(target_url))
        url_list.append('https://{}:8000/cluster/consoleSecurity_ipListManager.action?divId=ipListManager&actionPrefixName=consoleSecurity_ipListManager&numTabs=2&selectedTabNum=0&tabTitles=Allow&tabTitles=Deny&listIds=admin.allow_list&listIds=admin.deny_list&showAllowFirsts=true&showAllowFirsts=true&allowFirstId=admin.allow_first"'.format(target_url))


    def py_curl(self,url, auth):

        # Run pip install pycurl before
        """
        curl -k -iX OPTIONS
        -H "Authorization: HCP m9sZXM=:04EC9F614D89FF5C7126D32ACB448382"
        "https://admin.hcp.example.com:9090/mapi/tenants/finance/userAccounts
        ?prettyprint
        :param url:
        :param auth:
        :return:
        import pycurl
        import os
        filehandle = open("FinanceTenant.xml", 'rb')
        curl = pycurl.Curl()
        curl.setopt(pycurl.HTTPHEADER, ["Content-Type: application/xml",
        "Authorization: HCP \
        YWxscm9sZXM=:04EC9F614D89FF5C7126D32ACB448382"])
        curl.setopt(pycurl.URL,
        "https://admin.hcp.example.com:9090/mapi/tenants?" +
        "username=lgreen&password=start123&forcePasswordChange=false")
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.setopt(pycurl.UPLOAD, 1)
        curl.setopt(pycurl.INFILESIZE, os.path.getsize("FinanceTenant.xml"))
        curl.setopt(pycurl.READFUNCTION, filehandle.read)
        curl.perform()
        print curl.getinfo(pycurl.RESPONSE_CODE)
        curl.close()
        filehandle.close()
        """
        url = "https://datadog.desk.com/api/v2/cases"

        c = pycurl.Curl()


        c.setopt(pycurl.HTTPHEADER, ["Accept: application/json",
                                     "Authorization: HCP {AUTH}".format(AUTH=auth)])
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.UPLOAD, 1)
        data = c.perform()
        c.getinfo(pycurl.RESPONSE_CODE)
        c.close()
        print(data)
        return json.loads(data)


    def main(self):
        title = '###***tenant***###'
        "https://admin.hcp.example.com:9090/mapi/tenants?username=lgreen&password=start123&forcePasswordChange=false"
        auth = self.get_auth(self.user, self.passwd)
        url_list=self.get_tenant_resources()
        print(url_list)
        base_url = 'https://admin.{}:9090/mapi/'.format(self.target_url)

        for url in url_list:
            print(base_url+url)
        ten_list = list()
        ten_url = base_url+url_list[0]
        tenants_data = self.py_curl(ten_url,self.auth)
        """
        {
        "name" : [ "Default", "Finance", "HR", "Sales", "Marketing" ]
        }
        """
        tenants = tenants_data['name']
        for tenant in tenants:
            for url in url_list[1:]:
                url = url.repracle('<tenant-name>', tenant)
                ten_url = base_url+url
                data = self.py_curl(ten_url, self.auth)

        title = '###***namespaces***##'


        curl_cmd = 'curl -k -H "Authorization: HCP {AUTH}" -H "Content-Type: application/json" -H "Accept: application/json"  "{CMD}"'.format(AUTH=self.auth, CMD=ten_url)
        os.popen(curl_cmd).read()
        ten_url = 'https://admin.{}:9090/mapi/'.format(self.target_url)


if __name__=='__main__':
    hcp_info = dict()
    hcp_info['USER'] = 'admin'
    hcp_info['PASSWD']= 'passwd9'
    hcp_info['target_url']= 'google.co.kr'

    conn_test(hcp_info).main()

