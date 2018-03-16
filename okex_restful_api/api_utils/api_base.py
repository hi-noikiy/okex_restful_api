# -*- coding: utf-8 -*-
"""
@File     :api_base
@Date     :2018-03-16-10:29
@Author   : Xin Zhang
"""


def domain():
    return 'https://www.okex.com'


class ApiMeta(type):
    def __new__(cls, *args, **kwargs):
        name, bases, attr = args
        for k, v in attr.items():
            if not k.startswith('__'):
                attr[k] = '%s%s' % (domain(), str(v))
        return type.__new__(cls, name, bases, attr)


class ApiBase(metaclass=ApiMeta):
    pass


class Spot(ApiBase):
    # 行情
    # 1 - 币币行情
    ticker = '/api/v1/ticker.do'
    # 2 - 币币深度信息
    depth = '/api/v1/depth.do'
    # 3 - 币币交易记录信息
    trades = '/api/v1/trades.do'
    # 4 - 币币K线数据
    kline = '/api/v1/kline.do'
    # 交易
    # 1 - 用户信息
    userinfo = '/api/v1/userinfo.do'
    # 2 - 下单交易
    trade = '/api/v1/trade.do'
    # 3 - 批量下单
    batch_trade = '/api/v1/batch_trade.do'
    # 4 - 撤销订单
    cancel_order = '/api/v1/cancel_order.do'
    # 5 - 获取用户的订单信息
    order_info = '/api/v1/order_info.do'
    # 6 - 批量获取用户订单
    orders_info = '/api/v1/orders_info.do'
    # 7 - 获取历史订单信息，只返回最近两天的信息
    order_history = '/api/v1/order_history.do'
    # 8 - 提币BTC/LTC/ETH/ETC/BCH
    withdraw = '/api/v1/withdraw.do'
    # 9 - 取消提币BTC/LTC/ETH/ETC/BCH
    cancel_withdraw = '/api/v1/cancel_withdraw.do'
    # 10 - 查询提币BTC/LTC/ETH/ETC/BCH信息
    withdraw_info = '/api/v1/withdraw_info.do'
    # 11 - 获取用户提现/充值记录
    account_records = '/api/v1/account_records.do'


class Future(ApiBase):
    # 行情
    # 1 - 合约行情
    ticker = '/api/v1/future_ticker.do'
    # 2 - 合约深度信息
    depth = '/api/v1/future_depth.do'
    # 3 - 合约交易记录信息
    trades = '/api/v1/future_trades.do'
    # 4 - 合约指数信息
    index = '/api/v1/future_index.do'
    # 5 - 美元人民币汇率
    exchange_rate = '/api/v1/exchange_rate.do'
    # 6 - 交割预估价
    estimated_price = '/api/v1/future_estimated_price.do'
    # 7 - 合约K线
    kline = '/api/v1/future_kline.do'
    # 8 - 当前可用合约总持仓量
    hold_amount = '/api/v1/future_hold_amount.do'
    # 9 - 合约最高限价和最低限价
    price_limit = '/api/v1/future_price_limit.do'
    # 交易
    # 1 - 合约账户信息(全仓)
    userinfo = '/api/v1/future_userinfo.do'
    # 2 - 合约仓位信息(全仓)
    position = '/api/v1/future_position.do'
    # 3 - 合约下单
    trade = '/api/v1/future_trade.do'
    # 4 - 合约交易历史（非个人）
    trades_history = '/api/v1/future_trades_history.do'
    # 5 - 批量下单
    batch_trade = '/api/v1/future_batch_trade.do'
    # 6 - 取消合约订单
    cancel = '/api/v1/future_cancel.do'
    # 7 - 合约订单信息
    order_info = '/api/v1/future_order_info.do'
    # 8 - 批量获取合约订单信息
    orders_info = '/api/v1/future_orders_info.do'
    # 9 - 逐仓合约账户信息
    userinfo_4fix = '/api/v1/future_userinfo_4fix.do'
    # 10 - 逐仓用户持仓查询
    position_4fix = '/api/v1/future_position_4fix.do'
    # 11 - 获取合约爆仓单
    explosive = '/api/v1/future_explosive.do'
    # 12 - 个人账户资金划转
    devolve = '/api/v1/future_devolve.do'


class RestApi:
    spot = Spot()
    future = Future()


rest_api = RestApi()
