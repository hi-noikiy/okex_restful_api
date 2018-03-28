# -*- coding: utf-8 -*-
"""
@File     :http_utils
@Date     :2018-03-16-10:29
@Author   : Xin Zhang
"""
import json
import hashlib
import traceback
import time
import requests
from requests.adapters import SSLError

from urllib.parse import urlencode
from collections import OrderedDict


def build_my_sign(params: dict, secret_key):
    order_dict = OrderedDict()
    for key in sorted(params.keys()):
        order_dict[key] = params[key]
    order_dict['secret_key'] = secret_key
    data = urlencode(order_dict).encode('utf-8')
    return hashlib.md5(data).hexdigest().upper()


def build_my_sign_with_api(params: dict, api_key, secret_key):
    d = dict(params)
    d['api_key'] = api_key
    return build_my_sign(d, secret_key)


def http_get(resource, **params):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    source = urlencode(params)
    f_url = '%s?%s' % (resource, source)
    try:
        resp = requests.get(f_url, headers=headers)
        return resp.json()
    except SSLError:
        time.sleep(0.5)
        traceback.print_exc()
        return http_get(resource, **params)


def http_post(resource, params: dict):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    try:
        resp = requests.post(resource, params=params, headers=headers)
        return json.loads(resp.text)
    except BaseException:
        traceback.print_exc()
        return None


def build_api_sign(api_key, secret_key):
    prm = dict(api_key=api_key)
    sign = build_my_sign(prm, secret_key)
    return dict(api_key=api_key, sign=sign)


def build_param_with_sign(param: dict, secret_key):
    d = dict(param)
    sign = build_my_sign(d, secret_key)
    d['sign'] = sign
    return d
