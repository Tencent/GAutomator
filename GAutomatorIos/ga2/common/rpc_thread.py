# -*- coding: UTF-8 -*-
__author__ = 'minhuaxu'

import logging
import sys
import threading

from ga2.common.wetest_exceptions import *
from ga2.engine.protocol import Commands

logger = logging.getLogger(__name__)


class RPCReceiveThread(threading.Thread):
    RESET_SOCKET_FUN = '_wetest_socket_change'

    def __init__(self, socket, funcs, event):
        super(RPCReceiveThread, self).__init__()
        self._socket = socket
        self._funcs = funcs
        self._event = event
        self.running = True
        self._recv_result = None
        self.setDaemon(True)

    def close(self):
        self.running = False
        self._socket.close()

    def run(self):
        while self.running:
            try:
                logger.debug("start receive")
                self._recv_result = self._socket.recv_package()
                self._handle(self._recv_result)
            except Exception as e:
                logger.exception(e)
                self._reconnect()

    def _reconnect(self):
        self._socket.close()
        self._socket.connect()
        self._socket.send_package(Commands.PRC_SET_METHOD, RPCReceiveThread.RESET_SOCKET_FUN)

    def _send_callback_result(self, response):
        try:
            self._socket.send_package(Commands.RPC_METHOD, response)
        except Exception as e:
            logger.warning(str(e))

    def _handle(self, command):
        if command["status"] != 0:
            message = "Error code: " + str(self._recv_result['status']) + " msg: " + self._recv_result['data']
            logger.warn(message)
            return

        if command["cmd"] == Commands.PRC_SET_METHOD:
            # TODO specie Command
            logger.debug("receive set rpc method")
            self._event.set()
        elif command["cmd"] == Commands.RPC_METHOD:
            logger.debug("receive call rpc name = {0},value = {1}".format(command['data']['name'], command['data']['value']))
            result = command['data']
            if result['name'] in self._funcs:
                response = {"seq": result['seq'], "status": 0, "name": result['name']}
                try:
                    response['returnValue'] = self._funcs[result['name']](result['value'])
                except Exception as e:
                    response['returnValue'] = e.message
                    response['status'] = 1
                self._send_callback_result(response)
            else:
                logger.warn("Unknow PRC method = {0}".format(result['name']))
        else:
            logger.warn("Unknow command = {0}".format(command["cmd"]))

    def get_result(self, timeout=10):
        self._event.wait(timeout)
        if self._recv_result:
            if self._recv_result["status"] != 0:
                message = "Error code: " + str(self._recv_result['status']) + " msg: " + self._recv_result['data']
                raise WeTestSDKError(message)
            else:
                return self._recv_result['data']
        else:
            raise WeTestSDKError("Receive Message Error")
