# okex_restful_api
A simple tool for okex restful api

example code

```python
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
```
