# -*- coding: utf-8 -*-

# 服务器和客户机数据传输格式
import json
class DataFormat():
    def __init__(self, dataType, param):
        self.dataType = dataType  # REGIST ADDBLOCK
        self.param = param  # OK 序列化块

    @staticmethod
    def DataFormat2dict(data):
        return {
            'dataType': data.dataType,
            'param': data.param
        }

    @staticmethod
    def dict2DataFormat(d):
        return DataFormat(d['dataType'], d['param'])


if __name__ == "__main__":
    s = DataFormat("132", "2")
    json_str = json.dumps(s, default=DataFormat.DataFormat2dict)
    print(json_str)
    d_format = json.loads(json_str, object_hook=DataFormat.dict2DataFormat)
    print(d_format.dataType)
