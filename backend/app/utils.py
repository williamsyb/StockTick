from .protocol import Resp
from flask import make_response
import pandas as pd


class Utils:
    @staticmethod
    def build_resp(error_no: int, msg: str, data: dict):
        return make_response(Resp(error_no, msg, data).to_json())

    @staticmethod
    def treat_bar(data: pd.DataFrame) -> dict:
        # data = data.set_index('time').dropna(axis=0, how='all').reset_index()
        data.fillna(0, inplace=True)
        trade_volume = data.TradeVolume.tolist()
        order_volume = data.OrderVolume.tolist()
        data.drop(['TradeVolume', 'OrderVolume'], axis=1, inplace=True)
        data.time = data.time.astype(str)
        data_time = data.time.tolist()
        data = data[['open', 'close', 'low', 'high']]
        result = dict(
            trade_volume=trade_volume,
            order_volume=order_volume,
            time=data_time,
            ohlc=data.values.tolist()

        )
        return result
