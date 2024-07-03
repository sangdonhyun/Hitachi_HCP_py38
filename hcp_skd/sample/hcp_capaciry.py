import hcpsdk
import hcpsdk.namespace
import lxml
from lxml import etree
from pprint import pprint
import datetime
import re

'''This 'python 3' script is built to collect the capacity information from all namespaces in all the tenants on a specific HCP that is
being referenced to. The hcp name along with the domain name has to be mentioned against the very first variable called "url". This way
you will tell the script which HCP does it have to talk to to fetch the information. The next important step is to have the right 
credentials updated against the very first "auth" variable(in this case at line 33). The credentials being provided must have monitor 
access to all the tenants. You need not have access to the namespaces underneath. Still we will be able to fetch the capacity information
of the namespaces. All content written with <> must be replaced with actual values. We will collect the following information in this
script: `TenantName`, `NamespaceName`, `TotalCapacity or the hard quota set for the namespace`, `Current Used Capacity of the namespace`,
`total current Object count in that namespace`, `todays Date`. All of this information is dropped into a mysql database. 
Any analysis can be done from the data in the database at a future point '''


url = '<hcpname>.hcp.<domain>.com'
tenantshortnamelist = []
tenantfullnamelist = []
namespacenamelist = []
nscapacityinfolist = []
nsquotainfolist = []

adminportal = 'admin.'+url

today = datetime.date.today()
datestr = str(today.year)+"/"+str(today.month)+"/"+str(today.day)

auth = hcpsdk.NativeAuthorization('<monitoring user>', '<password>')
tgt = hcpsdk.Target( adminportal, auth, port=hcpsdk.P_MAPI)
alltenants = hcpsdk.mapi.listtenants(tgt)

for atenant in alltenants:
    tenantshortnamelist.append(atenant.name)

for btenant in alltenants:
    tgttnts = hcpsdk.Target(btenant.name+'.'+url, auth, port=443)
    tenantfullnamelist.append(tgttnts._Target__fqdn)


for tenantfullname in tenantfullnamelist:
    tgttnt = hcpsdk.Target(tenantfullname, auth, port=hcpsdk.P_MAPI)
    c = hcpsdk.Connection(tgttnt)

for tenantsn in tenantshortnamelist:
    c.GET('/mapi/tenants/'+tenantsn+'/namespaces')
    c.response_status
    source = c.read()

    if source == "b''":
        pass
    else:
        try:
            namespacelistpertenant = etree.fromstring(source)
            namespaceinfopertenant = namespacelistpertenant.findall('name')
            for q, value in enumerate(namespaceinfopertenant):
                namespacename = str(value.text)
                cona = hcpsdk.Connection(tgt)
                conb = hcpsdk.Connection(tgt)
                cona.GET('/mapi/tenants/'+tenantsn+'/namespaces/'+value.text)
                conb.GET('/mapi/tenants/'+tenantsn+'/namespaces/'+value.text+'/statistics')
                quotasource = cona.read()
                capacitysource = conb.read()
                print(quotasource)
                print(capacitysource)
        except Exception as e:
            print(str(e))
