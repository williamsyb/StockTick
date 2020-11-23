# -*- coding:UTF-8 -*-
from flask import Blueprint, current_app, request
import pandas as pd
from app.protocol import serialize
from app.utils import Utils
from app.database.crud import db_mgr
from app.cache import redis_mgr

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route('/show_raw_data', methods=['GET'])
def show_raw_data():
    raw_key = current_app.config['CACHE_RAW_KEY']
    data = redis_mgr.load_df_from_redis(raw_key)
    if data is None:
        depth_raw = db_mgr.query('depth_raw')
        order_raw = db_mgr.query('order_raw')
        trade_raw = db_mgr.query('trade_raw')
        data = db_mgr.combine_raw(depth_raw, order_raw, trade_raw, resample_freq='1s')
        data.time = data.time.astype(str)
        data.fillna(method='ffill', inplace=True)
        data.dropna(axis=0, how='all', inplace=True)
        redis_mgr.store_df_to_redis(raw_key, data)
    data = serialize(data)
    return Utils.build_resp(0, 'success', data)


@api_v1.route('/show_bar_data/<freq>', methods=['GET'])
def show_bar_data(freq):
    """
    data的key為 trade_volume: list
                order_volume: list
                ohlc:         二維list
                time:          list
    """
    freq_key = 'CACHE_' + freq.upper()
    if freq_key not in current_app.config:
        return Utils.build_resp(-1, f'不支持{freq}', {})

    freq_key = current_app.config[freq_key]
    result: dict = redis_mgr.get_from_redis(freq_key)
    if result is None:
        ohlc_freq = db_mgr.query('ohlc_' + freq_key)
        order_freq = db_mgr.query('order_' + freq_key)
        trade_freq = db_mgr.query('trade_' + freq_key)
        data: pd.DataFrame = db_mgr.combine_raw(ohlc_freq, order_freq, trade_freq)
        # print(data.head())
        result: dict = Utils.treat_bar(data[:])
        redis_mgr.set_to_redis(freq_key, result)
    return Utils.build_resp(0, 'success', result)


@api_v1.route('/show_statistic', methods=['GET'])
def show_statistic():
    print('args:', request.args)
    print('json:', request.json)
    start_time = str(request.args.get('start_time'))
    end_time = str(request.args.get('end_time'))
    print('start_time:', start_time)
    print('end_time:', end_time)
    #  查询缓存
    statistic_key = f'start_time:{start_time}_end_time:{end_time}'
    statistic_dict = redis_mgr.get_from_redis(statistic_key)
    if statistic_dict is not None:
        return Utils.build_resp(0, 'success', statistic_dict)
    #  若没有缓存则重新构造数据
    raw_key = current_app.config['CACHE_RAW_KEY']
    data = redis_mgr.load_df_from_redis(raw_key)
    if data is None:
        depth_raw = db_mgr.query('depth_raw')
        order_raw = db_mgr.query('order_raw')
        trade_raw = db_mgr.query('trade_raw')
        data = db_mgr.combine_raw(depth_raw, order_raw, trade_raw, resample_freq='1s')
        redis_mgr.store_df_to_redis(raw_key, data)
    # res_df = data.loc['2020-11-20 09:30:03':'2020-11-20 09:30:10'].agg(
    #     {'price': ['max', 'min'], 'OrderVolume': 'sum', 'TradeVolume': 'sum'})
    data.set_index('time', inplace=True)
    res_df = data.loc[start_time:end_time].agg(
        {'price': ['max', 'min'], 'OrderVolume': 'sum', 'TradeVolume': 'sum'})
    max_price = res_df.loc['max', 'price']
    min_price = res_df.loc['min', 'price']
    total_order = res_df.loc['sum', 'OrderVolume']
    total_trade = res_df.loc['sum', 'TradeVolume']
    result = dict(
        max_price=max_price,
        min_price=min_price,
        total_order=total_order,
        total_trade=total_trade
    )
    redis_mgr.set_to_redis(statistic_key, result)
    return Utils.build_resp(0, 'success', result)
