# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2014-2016 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os.path
import socket
import hashlib
import base64

def port_check(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(ip, int(port()))
    status = False
    if result == 0:
        print("Port is open")
        status = True
    else:
        print("Port is not open")
    sock.close()
    return status

def get_passwd(pw):
    m=hashlib.md5()
    m.update(pw)
    return m.hexdigest().strip()


sys.path.insert(0, os.path.abspath('..'))
import hcpsdk

# primary HCP
P_HCP       = 'hcp73.archivas.com'
P_ADMIN     = 'admin.' + P_HCP
P_TENANT    = 'm.' + P_HCP
P_NS_GOOD   = 'n1.' + P_TENANT
P_NS_BAD    = "this_wont_work.at-all"
P_PORT      = 80
P_SSLPORT   = 443
P_ADMINPORT = 8000
P_MAPIPORT  = 9090
P_DNSCACHE  = True

P_USER      = "admin"
P_PASSWORD  = "password"
epasswd = get_passwd(P_PASSWORD)
euser = base64.encodestring(P_USER).strip()

P_AUTH      = hcpsdk.NativeAuthorization(P_USER, P_PASSWORD)

print(P_AUTH_hash)
print(P_AUTH)


P_ADMUSER   = "service"
P_ADMPWD    = "service01"
P_ADMAUTH      = hcpsdk.NativeAuthorization(P_ADMUSER, P_ADMPWD)


# replica HCP
R_HCP       = 'hcp2.snomis.local'
R_ADMIN     = 'admin' + R_HCP
R_TENANT    = 'm.' + R_HCP
R_NS_GOOD   = 'n1.' + R_TENANT
R_NS_BAD    = "this_wont_work.at-all"
R_PORT      = P_PORT
R_ADMINPORT = P_ADMINPORT
R_MAPIPORT  = P_MAPIPORT
R_DNSCACHE  = P_DNSCACHE

R_USER      = P_USER
R_PASSWORD  = P_PASSWORD
R_AUTH      = hcpsdk.NativeAuthorization(R_USER, R_PASSWORD)

R_ADMUSER   = "service"
R_ADMPWD    = "service01"
R_ADMAUTH      = hcpsdk.NativeAuthorization(R_ADMUSER, R_ADMPWD)


# primary HCP for mapi.Logs() tests
L_HCP       = 'hcp72.archivas.com'
L_ADMIN     = 'admin.' + L_HCP
L_TENANT    = 'm.' + L_HCP
L_NS_GOOD   = 'n1.' + L_TENANT
L_NS_BAD    = "this_wont_work.at-all"
L_PORT      = 80
L_SSLPORT   = 443
L_ADMINPORT = 8000
L_MAPIPORT  = 9090
L_DNSCACHE  = True

L_USER      = "n"
L_PASSWORD  = "n01"
L_AUTH      = hcpsdk.NativeAuthorization(L_USER, L_PASSWORD)

L_ADMUSER   = "service"
L_ADMPWD    = "service01"
L_ADMAUTH      = hcpsdk.NativeAuthorization(L_ADMUSER, L_ADMPWD)


