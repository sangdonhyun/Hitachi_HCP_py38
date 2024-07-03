import json
import ast
import unicodedata

import requests
import os
import requests

def _remove_accents(data):
    """
    Changes accented letters to non-accented approximation, like Nestle

    """
    return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
    ##
def _asciify_list(data):
    """ Ascii-fies list values """
    ret = []
    for item in data:
        if isinstance(item, unicode):
            item = _remove_accents(item)
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _asciify_list(item)
        elif isinstance(item, dict):
            item = _asciify_dict(item)
        ret.append(item)
    return ret
    #
def _asciify_dict(data):
    """ Ascii-fies dict keys and values """
    ret = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = _remove_accents(key)
            key = key.encode('utf-8')
        ## note new if
        if isinstance(value, unicode):
            value = _remove_accents(value)
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _asciify_list(value)
        elif isinstance(value, dict):
            value = _asciify_dict(value)
        ret[key] = value
    return ret


# cmd = """curl -H "Content-Type: application/json; charset=UTF-8" --user root:ibrm222!@ -k -i "https://121.170.193.213:215/api/network/v1/interfaces" """
# req = os.popen(cmd).read()
# print('-'*50)
# print(req)
#
# print(type(req))
#
# json_data = json.loads(req)
#
# print(json_data)

s_url="https://121.170.193.213:215/api/network/v1/interfaces"
with requests.Session() as o_session:

    o_response = o_session.get(s_url, auth=("root", "ibrm222!@"), verify=False)

    if o_response.status_code == 200:
        a_response = json.loads(o_response.text)
    else:
        a_response = {}



print(a_response)
print(type(a_response))
jd=json.dumps(a_response, ensure_ascii=False)
print(jd)
print(type(jd))




