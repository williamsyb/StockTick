from .sql import sql_dict
from ..config import Config
from flask import current_app
from ..protocol import ModuleException
import pandas as pd
import sqlite3


class Query:
    def query(self, table):
        table_sql = table + '_sql'
        if table_sql not in sql_dict:
            raise ModuleException(f"{table}不存在", f"{table}不存在")
        sql = sql_dict[table_sql]
        data = pd.read_sql(sql, con=self.conn)
        data['time'] = pd.to_datetime(data['time'])
        # print(f'sql:{sql}, data:{data}')
        current_app.logger.debug(f'sql:{sql}, data:{data}')
        return data


class DbMgr(Query):
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_NAME)

    def combine_raw(self, *args, **kwargs):
        resample_freq = kwargs.get('resample_freq', None)

        # df_list = [df.set_index('time', inplace=True) for df in args]
        for index, df in enumerate(args):
            df.set_index('time', inplace=True)
        if resample_freq is None:
            res = pd.concat(args, axis=1)
        else:
            print([df.resample(resample_freq).last() for df in args])
            res = pd.concat([df.resample(resample_freq).last() for df in args], axis=1)
        res.reset_index(inplace=True)
        return res


db_mgr = DbMgr()
