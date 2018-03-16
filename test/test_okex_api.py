# -*- coding: utf-8 -*-
"""
@File     :test_okex_api
@Date     :2018-03-15-17:16
@Author   : Xin Zhang
"""

from okex_restful_api import OkexApi

api_key = ''
secret_key = ''

okex_api = OkexApi(api_key, secret_key)

# 合约行情

print('获取OKEx合约行情')
print(okex_api.future.ticker('btc_usd', 'this_week'))

print('获取OKEx合约深度信息')
print(okex_api.future.depth('btc_usd', 'this_week', size=20))

print('获取OKEx合约交易记录信息')
print(okex_api.future.trades('btc_usd', 'this_week'))

print('获取OKEx合约K线行情')
print(okex_api.future.kline('btc_usd', '15min', 'this_week', size=20))

print('获取OKEx合约指数信息')
print(okex_api.future.index('btc_usd'))

print('获取交割预估价')
print(okex_api.future.estimated_price('btc_usd'))

print('获取美元人民币汇率')
print(okex_api.future.exchange_rate())

print('获取当前可用合约总持仓量')
print(okex_api.future.hold_amount('btc_usd', 'this_week'))

print('获取合约最高限价和最低限价')
print(okex_api.future.price_limit('btc_usd', 'this_week'))


# 币币行情

print('获取OKEx币币行情')
print(okex_api.spot.ticker('ltc_btc'))

print('获取OKEx币币市场深度')
print(okex_api.spot.depth('ltc_btc', 20))

print('获取OKEx币币交易信息(600条)')
print(okex_api.spot.trades('ltc_btc'))

print('获取OKEx币币K线数据(每个周期数据条数2000左右)')
print(okex_api.spot.kline('ltc_btc', '15min', size=20))
