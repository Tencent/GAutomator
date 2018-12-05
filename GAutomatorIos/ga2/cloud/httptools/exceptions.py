#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

class ConnectionException(RuntimeError):
    """

    """
    pass

class HttpException(ConnectionException):
    """
        http请求发生错误
    """
    pass
