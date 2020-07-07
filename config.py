DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/blockchain?charset=utf8'
SECRET_KEY = '*\xff\x93\xc8w\x13\x0e@3\xd6\x82\x0f\x84\x18\xe7\xd9\\|\x04e\xb9(\xfd\xc3'

SERVER_IP = "127.0.0.1"  # 中心服务器IP地址
SERVER_PORT = 2248  # 中心服务端口号
MAX_CLIENT = 256  # 最大客户机个数
DEF_REGIST = "REGIST"  # 节点注册命令
DEF_ADDBLOCK = "ADDBLOCK"  # 节点增加命令
DEF_DELAY = 2  # 注册超时等待时间
