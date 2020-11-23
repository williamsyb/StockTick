# -*- coding:UTF-8 -*-
import traceback
import zipfile
from datetime import datetime as dt
import os

try:
    from ..config import basedir
except:
    pass
import shutil
import traceback

DATE_FORMAT_RAW = '%Y/%m/%d'
DATE_FORMAT_STD = '%Y%m%d'
FORMATNORMAL = '%Y%m%d'


# translation = os.path.join(basedir, 'translation')


class Utils(object):
    @classmethod
    def to_good_date(cls, date_str):
        """
        转换日期格式
        """
        try:
            do = dt.strptime(date_str, DATE_FORMAT_STD)
        except ValueError:
            do = dt.strptime(date_str, DATE_FORMAT_RAW)
        good_date_str = do.strftime(DATE_FORMAT_STD)
        return good_date_str

    @staticmethod
    def date2str(datelist):
        dates = map(lambda date: dt.strftime(date, FORMATNORMAL), datelist)
        return dates

    @staticmethod
    def df2dict_raw(df):
        cols = df.columns.tolist()
        result = {}
        for column in cols:
            # js_col = column.replace('(','')
            # js_col = js_col.replace(')','')
            result[column] = df[column].tolist()
        try:
            # if df.index.name == '':
            # result.
            df.index = df.index.astype(str)

            result['index'] = df.index.tolist()
        except:
            pass
        return result

    @staticmethod
    def gen_msg(status, msg, **kwargs):
        res = {'msg': msg, 'status': status}
        res.update(kwargs)
        return res

    @staticmethod
    def delete_uploaded_files(path):
        try:
            files = os.listdir(path)
            files = [os.path.join(path, file) for file in files]
            [os.remove(file) for file in files if os.path.isfile(file)]
            [shutil.rmtree(folder) for folder in files if os.path.isdir(folder)]
        except:
            traceback.print_exc()

    @staticmethod
    def make_project_env(project_name, data_path, folder_type_list):
        if not os.path.exists(data_path):
            return False, 'path:{} not exist.'.format(data_path)
        project_path = os.path.join(data_path, project_name)
        if not os.path.exists(project_path):
            os.mkdir(project_path)
        for folder_type in folder_type_list:
            folder_type_path = os.path.join(project_path, folder_type)
            if not os.path.exists(folder_type_path):
                os.mkdir(folder_type_path)
        return True

    @staticmethod
    def rm_project_env(project_name, data_path):
        if not os.path.exists(data_path):
            return False, 'path:{} not exist.'.format(data_path)
        target_path = os.path.join(data_path, project_name)
        if os.path.exists(target_path):
            Utils.delete_uploaded_files(target_path)
            os.rmdir(target_path)
        return True


def print_line(n=100):
    print('-' * n)


if __name__ == '__main__':
    path = r'F:\william\jianzhi\data\dataplat'
    Utils.delete_uploaded_files(path)
    os.rmdir(path)
