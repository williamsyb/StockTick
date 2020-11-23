from flask import jsonify


class Resp:
    __slots__ = 'error_no', 'msg', 'data'

    def __init__(self, error_no, msg, data):
        self.error_no = error_no
        self.msg = msg
        self.data = data

    def to_json(self):
        return jsonify({'error_no': self.error_no, 'msg': self.msg, 'data': self.data})


# TODO DATAFRAME转dict
def serialize(data):
    data = data.to_dict(orient='list')
    return data


class ModuleException(Exception):
    def __init__(self, trace_error, msg):
        self.trace_error = trace_error
        self.msg = msg
