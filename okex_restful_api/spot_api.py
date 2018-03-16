# -*- coding: utf-8 -*-
"""
@File     :spot_api
@Date     :2018-03-16-15:17
@Author   : Xin Zhang
"""
from .api_utils import (rest_api, http_post, http_get,
                        build_api_sign, build_param_with_sign)


class SpotApi:
    def __init__(self, api_key=None, secret_key=None):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__api = rest_api.spot

    def ticker(self, symbol):
        """
        获取OKEx币币行情
        :param symbol: 币对如ltc_btc
        :return: {date:int, ticker:{}}
        """
        return http_get(self.__api.ticker, symbol=symbol)

    def depth(self, symbol, size):
        """
        获取OKEx币币市场深度
        :param symbol: 币对如ltc_btc
        :param size: value: 1-200
        :return: dict, {ask:[], bid:[]}
        """
        param = dict(symbol=symbol, size=size)
        return http_get(self.__api.depth, **param)

    def trades(self, symbol, **params):
        """
        获取OKEx币币交易信息(600条)
        :param symbol: 币对如ltc_btc
        :param params:
            since: 时间戳，返回该时间戳以后的数据
        :return: [{date:int, ...}, ...]
        """
        since = params.get('since')
        param = dict(symbol=symbol)
        op_param = dict()
        if since:
            op_param['since'] = since
        param.update(op_param)
        return http_get(self.__api.trades, **param)

    def kline(self, symbol, type, **params):
        """
        获取OKEx币币K线数据(每个周期数据条数2000左右)
        :param symbol: 币对如ltc_btc
        :param type: 1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
        :param params:
            size: 指定获取数据的条数
            since: 时间戳，返回该时间戳以后的数据(例如1417536000000)
        :return: list, [[],...]
        """
        op_param = dict()
        size = params.get('size')
        since = params.get('since')
        if size:
            op_param['size'] = size
        if since:
            op_param['since'] = since
        param = dict(symbol=symbol, type=type)
        param.update(op_param)
        return http_get(self.__api.kline, **param)

    def userinfo(self):
        """
        获取用户信息
        :return: {info:{}, result:true}
        """
        self.__assert_api_secret_key()
        param = build_api_sign(self.__api_key, self.__secret_key)
        return http_post(self.__api.userinfom, param)

    def trade(self, symbol, type, **params):
        """
        下单交易,	访问频率 20次/2秒
        :param symbol: 币对如ltc_btc
        :param type: 买卖类型：限价单(buy/sell) 市价单(buy_market/sell_market)
        :param params:
            price: 下单价格 市价卖单不传price
            amount: 交易数量 市价买单不传amount
        :return: {result:true, order_id:int}
        """
        self.__assert_api_secret_key()
        op_param = dict()
        price = params.get('price')
        amount = params.get('amount')
        if price:
            op_param['price'] = price
        if amount:
            op_param['amount'] = amount
        param = dict(symbol=symbol, type=type,
                     api_key=self.__api_key)
        param.update(op_param)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.trade, param)

    def batch_trade(self, symbol, orders_data, **params):
        """
        批量下单，访问频率 20次/2秒
        :param symbol: 币对如ltc_btc
        :param orders_data: 最大下单量为5，price和amount参数参考trade接口中的说明，[{price:3,amount:5,type:'sell'},{price:3,amount:3,type:'buy'}])
        :param params:
            type: 买卖类型：限价单(buy/sell)
        :return: dict, {order_info:[{}, ...], result:true}
        """
        self.__assert_api_secret_key()
        op_param = dict()
        if params.get('type'):
            op_param['type'] = params.get('type')
        param = dict(symbol=symbol, orders_data=orders_data,
                     api_key=self.__api_key)
        param.update(op_param)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.batch_trade, param)

    def cancel_order(self, symbol, order_id):
        """
        撤销订单
        :param symbol: 币对如ltc_btc
        :param order_id: 订单ID(多个订单ID中间以","分隔,一次最多允许撤消3个订单)
        :return: dict, {success:"id1,id2", error:"id_3,id_4"}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, order_id=order_id,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.cancel_order, param)

    def order_info(self, symbol, order_id):
        """
        获取用户的订单信息, 访问频率 20次/2秒(未成交)
        :param symbol: 币对如ltc_btc
        :param order_id: 订单ID -1:未完成订单，否则查询相应订单号的订单
        :return: dict, {result:true, orders:[]}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, order_id=order_id,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.order_info, param)

    def orders_info(self, symbol, order_id, type):
        """
        批量获取用户订单,访问频率 20次/2秒
        :param symbol: 币对如ltc_btc
        :param order_id: 订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
        :param type: 查询类型 0:未完成的订单 1:已经完成的订单
        :return: {result:true, orders:[]}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, order_id=order_id,
                     type=type,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.orders_info, param)

    def order_history(self, symbol, status, current_page, page_length):
        """
        获取历史订单信息，只返回最近两天的信息
        :param symbol: 币对如ltc_btc
        :param status: 查询状态 0：未完成的订单 1：已经完成的订单(最近两天的数据)
        :param current_page: 当前页数
        :param page_length: 每页数据条数，最多不超过200
        :return: {current_page:1, orders:[], page_length:1,result:true, total:int}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, status=status,
                     current_page=current_page,
                     page_length=page_length,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.order_history, param)

    def withdraw(self, symbol, chargefee, trade_pwd, withdraw_address,
                 withdraw_amount, target):
        """
        提币BTC/LTC/ETH/ETC/BCH
        :param symbol: 币对如ltc_usd
        :param chargefee: 网络手续费>=0
                          BTC范围 [0.002，0.005]
                          LTC范围 [0.001，0.2]
                          ETH范围 [0.01]
                          ETC范围 [0.0001，0.2]
                          BCH范围 [0.0005，0.002]
                          手续费越高，网络确认越快，向OKCoin提币设置为0
        :param trade_pwd: 交易密码
        :param withdraw_address: 认证的地址、邮箱或手机号码
        :param withdraw_amount: 提币数量 BTC>=0.01 LTC>=0.1 ETH>=0.1 ETC>=0.1 BCH>=0.1
        :param target: 地址类型 okcn：国内站 okcom：国际站 okex：OKEX address：外部地址
        :return: {withdraw_id:int, result:true}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, chargefee=chargefee,
                     trade_pwd=trade_pwd, withdraw_address=withdraw_address,
                     withdraw_amount=withdraw_amount, target=target,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.withdraw, param)

    def cancel_withdraw(self, symbol, withdraw_id):
        """
        取消提币BTC/LTC/ETH/ETC/BCH
        :param symbol: 币对如ltc_usd
        :param withdraw_id: 提币申请Id
        :return: {result:true, withdraw_id:int}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, withdraw_id=withdraw_id,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.cancel_withdraw, param)

    def withdraw_info(self, symbol, withdraw_id):
        """
        查询提币BTC/LTC/ETH/ETC/BCH信息
        :param symbol: 币对如ltc_usd
        :param withdraw_id: 提币申请Id
        :return: {result:true, withdraw:[{}]}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, withdraw_id=withdraw_id,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.withdraw_info, param)

    def account_records(self, symbol, type, current_page, page_length):
        """
        获取用户提现/充值记录
        :param symbol: 币种如btc, ltc, eth, etc, bch, usdt
        :param type: 0：充值 1 ：提现
        :param current_page: 当前页数
        :param page_length:每页数据条数，最多不超过50
        :return: dict, {records:[{}], symbol:btc}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, type=type, current_page=current_page,
                     page_length=page_length, api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.account_records, param)

    def __assert_api_secret_key(self):
        assert (
            self.__api_key is not None) & (
            self.__secret_key is not None), 'Api_key and secret_key is needed!'
