# -*- coding: utf-8 -*-
"""
@File     :future_api
@Date     :2018-03-16-10:58
@Author   : Xin Zhang
"""
from .api_utils import (rest_api, http_post, http_get,
                        build_api_sign, build_param_with_sign)


class FutureApi:
    def __init__(self, api_key=None, secret_key=None):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__api = rest_api.future

    def ticker(self, symbol, contract_type):
        """
        获取OKEx合约行情
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type: this_week:当周 next_week:下周 quarter:季度
        :return: dict, {date:int, ticker:{...}}
        """
        param = dict(symbol=symbol, contract_type=contract_type)
        return http_get(self.__api.ticker, **param)

    def depth(self, symbol, contract_type, size, merge=0):
        """
        获取OKEx合约深度信息
        :param symbol:btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type:this_week:当周 next_week:下周 quarter:季度
        :param size:value：1-200
        :param merge:value：1(合并深度)
        :return:dict, {ask:[], bid:[]}
        """
        param = dict(symbol=symbol,
                     contract_type=contract_type,
                     size=size,
                     merge=merge)
        return http_get(self.__api.depth, **param)

    def trades(self, symbol, contract_type):
        """
        获取OKEx合约交易记录信息
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type:this_week:当周 next_week:下周 quarter:季度
        :return: list, [{amount:int,..,tid:int,type:buy},{}]
        """
        param = dict(symbol=symbol, contract_type=contract_type)
        return http_get(self.__api.trades, **param)

    def index(self, symbol):
        """
        获取OKEx合约指数信息
        :param symbol:btc_usd ltc_usd eth_usd etc_usd bch_usd
        :return:dict, {future_index:int}
        """
        param = dict(symbol=symbol)
        return http_get(self.__api.index, **param)

    def exchange_rate(self):
        """
        获取美元人民币汇率
        :return: dict, {rate:float}
        """
        return http_get(self.__api.exchange_rate)

    def estimated_price(self, symbol):
        """
        获取交割预估价
        :param symbol:btc_usd ltc_usd eth_usd etc_usd bch_usd
        :return: dict, {forecast_price:float}
        """
        return http_get(self.__api.estimated_price, symbol=symbol)

    def kline(self, symbol, type, contract_type, size=0, since=0):
        """
        获取OKEx合约K线行情
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param type: 1min/3min/5min/15min/30min/1day/3day/1week/1hour/2hour/4hour/6hour/12hour
        :param contract_type:合约类型: this_week:当周 next_week:下周 quarter:季度
        :param size:指定获取数据的条数
        :param since:时间戳（eg：1417536000000）。 返回该时间戳以后的数据
        :return: list, [[float,...], []]
        """
        param = dict(symbol=symbol, type=type,
                     contract_type=contract_type,
                     size=size, since=since)
        return http_get(self.__api.kline, **param)

    def hold_amount(self, symbol, contract_type):
        """
        获取当前可用合约总持仓量
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type: this_week:当周 next_week:下周 quarter:季度
        :return: list, [{amount:int, contract_name:str}]
        """
        param = dict(symbol=symbol, contract_type=contract_type)
        return http_get(self.__api.hold_amount, **param)

    def price_limit(self, symbol, contract_type):
        """
        获取合约最高限价和最低限价
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type:this_week:当周 next_week:下周 quarter:季度
        :return: dict, {high:float, low:float}
        """
        param = dict(symbol=symbol, contract_type=contract_type)
        return http_get(self.__api.price_limit, **param)

    def userinfo(self):
        """
        获取OKEx合约账户信息(全仓)
        :return: dict, {info:{}, result:true}
        """
        self.__assert_api_secret_key()
        param = build_api_sign(self.__api_key, self.__secret_key)
        return http_post(self.__api.userinfo, param)

    def position(self, symbol, contract_type):
        """
        获取用户持仓获取OKEX合约仓位信息 （全仓）
        :return: dict, {force_liqu_price:float, holding:[], result:true}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, contract_type=contract_type,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.position, param)

    def trade(self, symbol, contract_type, price, amount, type, **params):
        """
        合约下单
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type:  this_week:当周 next_week:下周 quarter:季度
        :param price: 价格
        :param amount: 委托数量
        :param type: 1:开多 2:开空 3:平多 4:平空
        :param params:
            match_price: 是否为对手价 0:不是 1:是 ,当取值为1时,price无效
            lever_rate : 杠杆倍数, 且“开仓”若有10倍多单，就不能再下20倍多单
        :return: dict, {order_id : int, result : true}
        """
        self.__assert_api_secret_key()
        op_param = dict()
        match_price = params.get('match_price', None)
        lever_rate = params.get('lever_rate', None)
        if match_price:
            op_param['match_price'] = match_price
        if lever_rate:
            op_param['lever_rate'] = lever_rate
        param = dict(symbol=symbol, contract_type=contract_type,
                     price=price, amount=amount, type=type,
                     api_key=self.__api_key)
        param.update(op_param)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.trade, param)

    def trades_history(self, symbol, date, since):
        """
        获取OKEX合约交易历史（非个人）
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param date: 合约交割时间，格式yyyy-MM-dd
        :param since: 交易Id起始位置
        :return: list, [{amount:int, date:int, price:float, tid:int, type:buy}, ...]
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, date=date,
                     since=since, api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.trades_history, param)

    def batch_trade(self, symbol, contract_type, order_data, **params):
        """
        批量下单
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type: this_week:当周 next_week:下周 quarter:季度
        :param order_data: JSON类型的字符串
                        例：[{price:5,amount:2,type:1,match_price:1},
                            {price:2,amount:3,type:1,match_price:1}]
                            最大下单量为5
        :param params:
            lever_rate: 杠杆倍数
        :return: dict, {order_info: {}, result:true}
        """
        self.__assert_api_secret_key()
        op_param = dict()
        lever_rate = params.get('lever_rate')
        if lever_rate:
            op_param['lever_rate'] = lever_rate
        param = dict(symbol=symbol, contract_type=contract_type,
                     order_data=order_data, api_key=self.__api_key)
        param.update(op_param)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.batch_trade, param)

    def cancel(self, order_id, symbol, contract_type):
        """
        取消合约订单
        :param order_id: 订单ID(多个订单ID中间以","分隔,一次最多允许撤消3个订单)
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type: this_week:当周 next_week:下周 quarter:季度
        :return: dict, {order_id:int, result:true}
        """
        self.__assert_api_secret_key()
        param = dict(order_id=order_id, symbol=symbol,
                     contract_type=contract_type,
                     api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.cancel, param)

    def order_info(self, symbol, contract_type, status, order_id=-1, **params):
        """
        获取合约订单信息
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type:  this_week:当周 next_week:下周 quarter:季度
        :param status: 查询状态 1:未完成的订单 2:已经完成的订单
        :param order_id: 订单ID -1:查询指定状态的订单，否则查询相应订单号的订单
        :param params:
            current_page: 当前页数
            page_length: 每页获取条数，最多不超过50
        :return: dict, {orders:[{}], result:true}
        """
        self.__assert_api_secret_key()
        op_param = dict()
        current_page = params.get('current_page')
        page_length = params.get('page_length')
        if current_page:
            op_param['current_page'] = current_page
        if page_length:
            op_param['page_length'] = page_length
        param = dict(symbol=symbol, contract_type=contract_type,
                     status=status, order_id=order_id,
                     api_key=self.__api_key)
        param.update(op_param)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.order_info, param)

    def orders_info(self, symbol, contract_type, order_id):
        """
        批量获取合约订单信息
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type: this_week:当周 next_week:下周 quarter:季度
        :param order_id:订单ID(多个订单ID中间以","分隔,一次最多允许查询50个订单)
        :return: dict, {orders:[{}], result:true}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, contract_type=contract_type,
                     order_id=order_id, api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.orders_info, param)

    def userinfo_4fix(self):
        """
        获取逐仓合约账户信息
        :return: dict, {info:{btc:{},...}, result:true}
        """
        self.__assert_api_secret_key()
        param = build_api_sign(self.__api_key, self.__secret_key)
        return http_post(self.__api.userinfo_4fix, param)

    def position_4fix(self, symbol, contract_type, **params):
        """
        逐仓用户持仓查询
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type:  this_week:当周 next_week:下周 quarter:季度
        :param params:
            type: 默认返回10倍杠杆持仓 type=1 返回全部持仓数据
        :return: dict, {holding:[{},...], result:true}
        """
        self.__assert_api_secret_key()
        op_param = dict()
        if params.get('type'):
            op_param['type'] = params.get('type')
        param = dict(symbol=symbol, contract_type=contract_type,
                     api_key=self.__api_key)
        param.update(op_param)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.position_4fix, param)

    def explosive(self, symbol, contract_type, **params):
        """
        获取合约爆仓单
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param contract_type: 合约类型: this_week:当周 next_week:下周 quarter:季度
        :param params:
            status: 查询状态 1:未完成的订单 2:已经完成的订单
            current_page: 当前页数索引值
            page_number: 当前页数(使用page_number时current_page失效，current_page无需传)
            page_length: 每页获取条数，最多不超过50
        :return: list, [{data:[{}, ...]}, ...]
        """
        self.__assert_api_secret_key()
        op_param = dict()
        status = params.get('status')
        current_page = params.get('current_page')
        page_number = params.get('page_number')
        page_length = params.get('page_length')
        if status:
            op_param['status'] = status
        if current_page:
            op_param['current_page'] = current_page
        if page_number:
            op_param['page_number'] = page_number
        if page_length:
            op_param['page_length'] = page_length

        param = dict(symbol=symbol, contract_type=contract_type,
                     api_key=self.__api_key)
        param.update(op_param)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.explosive, param)

    def devolve(self, symbol, type, amount):
        """
        个人账户资金划转
        :param symbol: btc_usd ltc_usd eth_usd etc_usd bch_usd
        :param type: 划转类型。1：币币转合约 2：合约转币币
        :param amount: 划转币的数量
        :return: dict, {result:true}
        """
        self.__assert_api_secret_key()
        param = dict(symbol=symbol, type=type,
                     amount=amount, api_key=self.__api_key)
        param = build_param_with_sign(param, self.__secret_key)
        return http_post(self.__api.devolve, param)

    def __assert_api_secret_key(self):
        assert (
            self.__api_key is not None) & (
            self.__secret_key is not None), 'Api_key and secret_key is needed!'
