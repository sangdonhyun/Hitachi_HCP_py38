import configparser

import hcpsdk
import os
import sys
from lxml import etree
import datetime
import socketClient

class fleta_hcpsdk():
    def __init__(self, hcp_info, port=8000):
        """
        [HOST01]
        hostname=hcp.his.test.com
        adminuser = admin
        adminpass = passwd
        #adminauth = YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b
        ip = 121.138.181.180
        port = 9090
        :param hcp_info:
        :param port:
        """
        self.user = hcp_info['adminuser']
        self.passwd = hcp_info['adminpass']
        self.host = hcp_info['hostname']
        self.port = hcp_info['port']
        self.auth = self.get_auth()
        print('self.auth : ',self.auth)
        self.fname = os.path.join('data','hcp_{}.txt'.format(hcp_info['name']))


    def get_auth(self):
        auth = hcpsdk.NativeAuthorization(self.user, self.passwd)
        return auth

    def get_base_url(self,ten='admin', port = 9090):
        base_url = "https://{TEN}.{FQDN}:{PORT}".format(TEN=ten ,FQDN=self.host, PORT=self.port)
        return base_url

    def fwrite(self, msg, wbit='a'):
        with open(self.fname,wbit) as fw:
            fw.write(msg)
            fw.write('\n')

    def getHeadMsg(self,title='FLETA BATCH LAOD'):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = '\n'
        msg += '#'*79+'\n'
        msg += '#### '+' '*71+'###\n'
        msg += '#### '+('TITLE     : %s'%title).ljust(71)+'###\n'
        msg += '#### '+('DATA TIME : %s'%now).ljust(71)+'###\n'
        msg += '#### '+' '*71+'###\n'
        msg += '#'*79+'\n'
        return msg

    def getEndMsg(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg = '\n'
        msg += '#'*79+'\n'
        msg += '####  '+('END  -  DATA TIME : %s'%now).ljust(71)+'###\n'
        msg += '#'*79+'\n'
        return msg

    def get_tenent_list(self):
        tenant_name_list = list()
        tgt = hcpsdk.Target(self.host, self.auth, port=hcpsdk.P_MAPI)
        tenants = hcpsdk.mapi.listtenants(tgt)
        return tenants

    # def get_namespace_info(self, namespace, tenant):
    #     """
    #     import hcpsdk.namespace
    #     from pprint import pprint
    #     auth = hcpsdk.NativeAuthorization('n', 'n01')
    #     t = hcpsdk.Target('n1.m.hcp1.snomis.local', auth, port=443)
    #     n = hcpsdk.namespace.Info(t)
    #     pprint(n.nsstatistics())
    #     """
    #     t = hcpsdk.Target('{}.{}.{}'.format(namespace,tenant,self.host), self.auth, port=443)
    #     hcpsdk.namespace.Info(t)

    def tenant_detail(self,tenant_name):
        fqdn = "{}.self.host".format(tenant_name)
        target = hcpsdk.Target(fqdn, self.auth, port=hcpsdk.P_MAPI)
        c = hcpsdk.Connection(target)
        c.GET('/mapi/tenants/' + tenant_name + '/namespaces')
        c.response_status
        source = c.read()
        namespace_info = etree.fromstring(source)
        namespace_list = namespace_info.findall('name')

        for namespace in namespace_list:
            nt = hcpsdk.Target('{}.{}.{}'.format(namespace,tenant_name,self.host), self.auth, port=443)
            ns_info=hcpsdk.namespace.Info(nt)
            print(ns_info)
            print(dir(ns_info))
        return ns_info

    def get_request(self, con, url):

        r = None
        try:
            r = con.request('GET', url)
        except Exception as e:
            print('Exception: {}'.format(str(e)))
        else:
            print('\t', con.response_status, con.response_reason)
            size = int(con.getheader('x-hcp-size', 0))
            while con.read():
                pass
            print('\tService time: {} ({:5,.2f}Mb/sec)'.format(con.service_time2,
                                                               size / con.service_time2 / 1024 / 1024))
        return r


    def mapi_replication(self,mapi_user,mapi_pass,PORT=9090):
        USR = 'logmon'
        PWD = 'logmon01'
        TGT = 'admin.hcp72.archivas.com'
        PORT = hcpsdk.P_MAPI
        auth = hcpsdk.NativeAuthorization(USR, PWD)

        t = hcpsdk.Target(TGT, auth, port=PORT)
        rep = hcpsdk.mapi.Replication(t, debuglevel=0)
        link_list = rep.getlinklist()
        for link in link_list:
            d = rep.getlinkdetails(link)


    def main(self):

        head_msg = self.getHeadMsg('HCP :{}'.format(self.host))
        self.fwrite(head_msg,'w')
        self.fwrite('###***hostname***###')
        self.fwrite(self.host)
        self.fwrite('###***license***###')
        add_url = '/mapi/storage/licenses'
        url = self.get_base_url(port = hcpsdk.P_MAPI) + add_url
        ret= self.curl_request(url)
        self.fwrite(ret)

        add_url = '/mapi/nodes/statistics'
        url = self.get_base_url(hcpsdk.P_MAPI) + add_url
        ret = self.curl_request(url)
        self.fwrite('###***nodes statistics***###')
        self.fwrite(ret)
        tenants_name_list = list
        tenants = self.get_tenent_list()
        for ten in tenants:
            self.fwrite('###***tenants***###')
            ten.info()
            self.fwrite(ten.info)
            tenants_name_list.append(ten.name)
            tenant_detail = self.tenant_detail(ten.name)
            self.fwrite('###***namespaces***###')
            self.fwrite(tenant_detail)
        self.fwrite('replication')
        add_url = '/mapi/services/replication'
        url = self.get_base_url(hcpsdk.P_MAPI) + add_url
        ret = self.curl_request(url)
        self.fwrite('###***replication***###')
        self.fwrite(ret)

        for tenant_name in tenants_name_list:
            self.fwrite('###***link***###')
            tenant_info  = self.get_tenant_user(tenant_name)
            if tenant_info['user_bit'] :
                auth = hcpsdk.NativeAuthorization(tenant_info['user'], tenant_info['passwd'])
            else:
                auth = self.auth
            TGT = '{}.{}'.format(tenant_name,self.host)
            PORT = hcpsdk.P_MAPI

            t = hcpsdk.Target(TGT, auth, port=PORT)
            rep = hcpsdk.mapi.Replication(t, debuglevel=0)
            link_list = rep.getlinklist()
            for link in link_list:
                d = rep.getlinkdetails(link)
                self.fwrite(d)

        for tenant_name in tenants_name_list:
            self.fwrite('###***chargeback***###')
            self.get_chargeback(tenant_name)
        self.fwrite(self.getEndMsg())
        socketClient.SocketSender(FILENAME=self.fname, DIR='HCP.disk').main()

    def curl_request(self, url):
        curl_cmd = 'curl -k -H "Authorization: HCP {AUTH}" -H "Content-Type: application/json" -H "Accept: application/json"  "{CMD}"'.format(
            AUTH=self.auth, CMD=url)
        print(curl_cmd)
        ret = os.popen(curl_cmd).read()
        return ret

    def get_cluster_info(self):

        base_url = "http://{}.{}:{}".format('admin',self.host,self.port)
        add_url = '/cluster/users_tableData.action'
        url = base_url+add_url
        ret = self.curl_request(url)
        self.fwrite('###***users_tableData.action***###')
        self.fwrite(ret)


    def get_chargeback(self, tenant):

        fqdn = 'admin.{}'.self.host
        # auth = hcpsdk.NativeAuthorization('service', 'service01')
        tgt = hcpsdk.Target(fqdn, self.auth,
                         port=hcpsdk.P_MAPI)
        cb = hcpsdk.mapi.Chargeback(tgt)
        result = cb.request(tenant=tenant,
                         granularity=hcpsdk.mapi.Chargeback.CBG_TOTAL,
                         fmt=hcpsdk.mapi.Chargeback.CBM_JSON)
        cb.close()
        return result


    def get_tenant_user(self,tenant):
        """
            [tenant01]
            host = hcp.hitachi.local
            user = service
            passwd = service01
        """
        cfg=configparser.RawConfigParser()
        cfg_file = os.path.join('config','tenant.cfg')
        cfg.read(cfg_file)
        tenant_info = dict ()
        tenant_info['user_bit'] = False
        if tenant in cfg.sections() :
            try:
                if cfg.get(tenant, 'host') == self.host:
                    tenant_info['user_bit'] = True
                    tenant_info['user'] = self.cfg.get(tenant, 'user')
                    tenant_info['passwd'] = self.cfg.get(tenant, 'passwd')
            except Exception as e:
                print(str(e))
        return tenant_info


    def tenent(self, fqdn, port, tenant_user, tenant_pass):
        #
        base_url = "https://admin.{FQDN}:{PORT}".format(FQDN=fqdn, PORT=port)
        add_url  = "/{BASE_URL}/mapi/tenants/username={TEN_USER}&password={TEN_PASS}&forcePasswordChange=false".format(BSEE_URL=base_url,TEN_USER=tenant_user, TEN_PASS=tenant_pass)
        url = base_url + add_url
        curl_cmd = """curl -H "Content-Type: application/json" -H "Authorization: HCP {AUTH}" "{URL}"        """.format(AUTH=self.auth, URL=url)
        ret=os.popen.read(curl_cmd)
        #https://finance.hcp.example.com:9090/mapi/tenants/finance/
        "https://finance.hcp.example.com:9090...nce/namespaces"

"""
• native http(s)/REST to an authenticated Namespace:
    FQDN: namespace.tenant.hcp.dom.com
    URL: /rest/<your>/<folders>/object
• native http(s) to the default Namespace:
    FQDN: default.default.hcp.dom.com
    URL: /fcfs_data/<your>/<folders>/object
    or, if metadata access is needed:
    URL: /fcfs_metadata/<your>/<folders>/object/metafile
• HSwift http(s)/REST to an authenticated Namespace:
    FQDN: api.hcp.dom.com
    URL: /swift/v1/<tenant>/<namespace>/<your>/<folders>/object
• http(s)/REST to MAPI:
    FQDN: admin.hcp.dom.com (when using a system level user)
    -or FQDN: <tenant>.hcp.dom.com (when using a tenant level user)
    URL: /mapi/<endpoint>
"""


if __name__=='__main__':
    cfg = configparser.RawConfigParser()
    cfg_file = os.path.join('config','hcp.cfg')
    cfg.read(cfg_file)
    hcp_list = list()
    for sec in cfg.sections():
        hcp_info = dict()
        hcp_info['name'] = sec
        for opt in cfg.options(sec):
            hcp_info[opt] = cfg.get(sec,opt)
        hcp_list.append(hcp_info)
    # user = 'service'
    # passwd = 'service01'
    # hostname = 'hcp.hitachi.local'
    # port = 8000
    for hcp_info in hcp_list:
        fleta_hcpsdk(hcp_info).main()

