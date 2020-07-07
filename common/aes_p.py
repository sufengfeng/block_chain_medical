#!/usr/bin/python
# -*- coding:utf-8-*-
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class aes():  # 自己实现了一个aes类，用于aes的加密和解密
    def __init__(self, key, mode):  # key为aes秘钥,mode为加密模式
        self.key = key
        self.mode = mode

    def encrypt(self, text, count):  # text的为要加密的文本或者二进制流,count为加密数据的长度
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        length = 16
        if count < length:
            add = (length - count)
            # \0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.cipherText = cryptor.encrypt(text)
        return b2a_hex(self.cipherText)  # 将内存中的数据已16进制字符串打印出来

    def decrypt(self, cipherText):  # cipherText类型为16进制字符串如:"fa0345da",一般为32个字节长度
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plainText = cryptor.decrypt(a2b_hex(cipherText))  # 将秘钥转换为二进制流
        return plainText  # 返回值为二进制流，因为有很多不可打印字符


if __name__ == "__main__":
    key = '1234567890123456'  # 秘钥的长度必须为16
    cryptor = aes(key, AES.MODE_ECB)  # 这里选用的是ECB模式
    msg = 'helloworld'  # 加密字符串
    cipher = cryptor.encrypt(msg, len(msg))  # 返回值是内存中的16进制字符串
    print(cipher)
    plainText = cryptor.decrypt(cipher)  # 解密函数,秘钥在aes初始化的时候设置好了,aes是对称加密的,加密的秘钥和解密的秘钥是一样的
    print(plainText)
