
from pprint import pprint
import hcpsdk
auth = hcpsdk.NativeAuthorization('service', 'service01')
tgt = hcpsdk.Target('admin.hcp73.archivas.com', auth, port=hcpsdk.P_MAPI)
tenants = hcpsdk.mapi.listtenants(tgt)
pprint(tenants)

for tenant in tenants:
    tenant.info()

for t in tenants:
    t.close()


import hcpsdk.namespace
from pprint import pprint
auth = hcpsdk.NativeAuthorization('n', 'n01')
t = hcpsdk.Target('n1.m.hcp1.snomis.local', auth, port=443)
n = hcpsdk.namespace.Info(t)


import hcpsdk
auth = hcpsdk.NativeAuthorization('service', 'service01')
tgt = hcpsdk.Target('admin.hcp73.archivas.com', auth, port=hcpsdk.P_MAPI)
cb = hcpsdk.mapi.Chargeback(tgt)
result = cb.request(tenant='m',granularity=hcpsdk.mapi.Chargeback.CBG_TOTAL,fmt=hcpsdk.mapi.Chargeback.CBM_JSON)
print(result.read())



import hcpsdk.mapi
from pprint import pprint
auth = hcpsdk.NativeAuthorization('service', 'service01')
t = hcpsdk.Target('admin.hcp1.snomis.local', auth, port=9090)
r = hcpsdk.mapi.Replication(t)
l = r.getlinklist()
print(l)

d = r.getlinkdetails(l[0])
pprint(d)
