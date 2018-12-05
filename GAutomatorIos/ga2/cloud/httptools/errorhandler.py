#-*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

from .exceptions import *

class ErrorCode(object):
    """
    Error codes defined in the WebDriver wire protocol.
    """
    # Keep in sync with org.openqa.selenium.remote.ErrorCodes and errorcodes.h
    SUCCESS = 0
    UNKNOWN_ERROR = [-1, 'server method error']
    METHOD_NOT_ALLOWED = [500, 'server error']



class ErrorHandler(object):
    """
    Handles errors returned by the WebDriver server.
    """
    def check_response(self, response):
        """
        Checks that a JSON response from the WebDriver does not have an error.

        :Args:
         - response - The JSON response from the WebDriver server as a dictionary
           object.

        :Raises: If the response contains an error message.
        """
        status = response.get('status', None)
        if status is None or status == ErrorCode.SUCCESS:
            return


        message=''
        if isinstance(status, int):
            message = response.get('value', None)

        if 399<status<=510:
            error_info="Error code : {0} ,message {1}".format(status,message)
            raise HttpException(error_info)
