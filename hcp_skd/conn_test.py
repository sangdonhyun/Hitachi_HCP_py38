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


target_url = 'hcp.co.kr'
user = 'admin'
passwd = 'passwd9'

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

url = 'https://admin.{}:8000/cluster/nodeList.action'.format(target_url)
curl_cmd = 'curl -k -H "Authorization: HCP {AUTH}" -H "Content-Type: application/xml" -H "Accept: application/xml"  "{CMD}"'.format(
            AUTH=admin_auth, CMD=url)
ret=os.poepen.read(curl_cmd)





