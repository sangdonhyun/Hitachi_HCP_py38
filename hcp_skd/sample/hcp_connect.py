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

    def main(self):
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



if __name__=='__main__':
    hcp_info = dict()
    hcp_info['USER'] = 'admin'
    hcp_info['PASSWD']= 'passwd9'
    hcp_info['target_url']= 'google.co.kr'

    conn_test(hcp_info).main()

