# -*- coding: utf-8 -*-
"""
@File     :__init__
@Date     :2018-03-16-15:23
@Author   : Xin Zhang
"""

from .future_api import FutureApi
from .spot_api import SpotApi


class OkexApi:
    __slots__ = ['future', 'spot']

    def __init__(self, api_key, secret_key):
        self.future = FutureApi(api_key, secret_key)
        self.spot = SpotApi(api_key, secret_key)
