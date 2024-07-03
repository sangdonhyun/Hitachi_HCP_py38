import hashlib
import base64


P_USER      = "admin"
P_PASSWORD  = "password"
enc = hashlib.md5()
enc.update(P_PASSWORD.encode('utf-8'))
enc_pass = enc.hexdigest()
print(enc_pass)
enc_user=base64.encodebytes(P_USER.encode('utf-8')).strip()
print(enc_user)
if isinstance(enc_user,bytes):
    enc_user = enc_user.decode('utf-8')
"""
YWRtaW4=:ee624467b0ed4bfe902edd3890610a9b
"""

print(enc_user+enc_pass)