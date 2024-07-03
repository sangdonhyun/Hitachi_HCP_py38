import hcpsdk.mapi


auth = hcpsdk.NativeAuthorization('service', 'service01')
t = hcpsdk.Target('admin.hcp1.snomis.local', auth, port=9090)
r = hcpsdk.mapi.Replication(t)
links = r.getlinklist()
# l
# ['hcp1--<-->--hcp2']
for l in links:
    d = r.getlinkdetails(l)
    print(d)
