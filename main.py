import hcpsdk

user=input('USER:')
passwd = input('PASSWORD:')
auth = hcpsdk.NativeAuthorization(user, passwd)

# print('AUTH :',dir(auth))
print('-'*50)
print('HCP PASSWORD MAKER')
print('your user     :',user)
print('your password :',passwd)
print('authorization :',auth.headers['Authorization'])
print('auth          :',auth.headers)
print("""example : curl -k -H "Authorization: {}"
    -H "Content-Type: application/xml" -H "Accept: application/xml"
    -d @FinanceCollisions.xml "https://admin.hcp.his.test.com:8000/cluster/nodeList.action" """.format(auth.headers['Authorization']))
print('-'*50)
