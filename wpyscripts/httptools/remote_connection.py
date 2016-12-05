# -*- coding: UTF-8 -*-

# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import socket
import string
import base64

try:
    import http.client as httplib
    from urllib import request as url_request
    from urllib import parse
except ImportError:  # above is available in py3+, below is py2.7
    import httplib as httplib
    import urllib2 as url_request
    import urlparse as parse

from errorhandler import ErrorCode, ErrorHandler
import utils

LOGGER = logging.getLogger(__name__)


class Method(object):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


class Request(url_request.Request):
    """
    Extends the url_request.Request to support all HTTP request types.
    """

    def __init__(self, url, data=None, method=None):
        """
        Initialise a new HTTP request.

        :Args:
        - url - String for the URL to send the request to.
        - data - Data to send with the request.
        """
        if method is None:
            method = data is not None and 'POST' or 'GET'
        elif method != 'POST' and method != 'PUT':
            data = None
        self._method = method
        url_request.Request.__init__(self, url, data=data)

    def get_method(self):
        """
        Returns the HTTP method used by this request.
        """
        return self._method


class Response(object):
    """
    Represents an HTTP response.
    """

    def __init__(self, fp, code, headers, url):
        """
        Initialise a new Response.

        :Args:
        - fp - The response body file object.
        - code - The HTTP status code returned by the server.
        - headers - A dictionary of headers returned by the server.
        - url - URL of the retrieved resource represented by this Response.
        """
        self.fp = fp
        self.read = fp.read
        self.code = code
        self.headers = headers
        self.url = url

    def close(self):
        """
        Close the response body file object.
        """
        self.read = None
        self.fp = None

    def info(self):
        """
        Returns the response headers.
        """
        return self.headers

    def geturl(self):
        """
        Returns the URL for the resource returned in this response.
        """
        return self.url


class HttpErrorHandler(url_request.HTTPDefaultErrorHandler):
    """
    A custom HTTP error handler.

    Used to return Response objects instead of raising an HTTPError exception.
    """

    def http_error_default(self, req, fp, code, msg, headers):
        """
        Default HTTP error handler.

        :Args:
        - req - The original Request object.
        - fp - The response body file object.
        - code - The HTTP status code returned by the server.
        - msg - The HTTP status message returned by the server.
        - headers - The response headers.

        :Returns:
        A new Response object.
        """
        return Response(fp, code, headers, req.get_full_url())


class RemoteConnection(object):
    """A connection with the Remote WebDriver server.

    Communicates with the server using the WebDriver wire protocol:
    https://github.com/SeleniumHQ/selenium/wiki/JsonWireProtocol"""

    _timeout = socket._GLOBAL_DEFAULT_TIMEOUT

    @classmethod
    def get_timeout(cls):
        """
        :Returns:
        Timeout value in seconds for all http requests made to the Remote Connection
        """
        return None if cls._timeout == socket._GLOBAL_DEFAULT_TIMEOUT else cls._timeout

    @classmethod
    def set_timeout(cls, timeout):
        """
        Override the default timeout

        :Args:
        - timeout - timeout value for http requests in seconds
        """
        cls._timeout = timeout

    @classmethod
    def reset_timeout(cls):
        """
        Reset the http request timeout to socket._GLOBAL_DEFAULT_TIMEOUT
        """
        cls._timeout = socket._GLOBAL_DEFAULT_TIMEOUT

    def __init__(self, remote_server_addr, keep_alive=False):
        # Attempt to resolve the hostname and get an IP address.
        self.keep_alive = keep_alive
        self.error_handler = ErrorHandler()
        parsed_url = parse.urlparse(remote_server_addr)
        addr = ""
        if parsed_url.hostname:
            try:
                netloc = socket.gethostbyname(parsed_url.hostname)
                addr = netloc
                if parsed_url.port:
                    netloc += ':%d' % parsed_url.port
                if parsed_url.username:
                    auth = parsed_url.username
                    if parsed_url.password:
                        auth += ':%s' % parsed_url.password
                    netloc = '%s@%s' % (auth, netloc)
                remote_server_addr = parse.urlunparse(
                    (parsed_url.scheme, netloc, parsed_url.path,
                     parsed_url.params, parsed_url.query, parsed_url.fragment))
            except socket.gaierror:
                LOGGER.info('Could not get IP address for host: %s' % parsed_url.hostname)

        self._url = remote_server_addr
        if keep_alive:
            self._conn = httplib.HTTPConnection(
                str(addr), str(parsed_url.port), timeout=self._timeout)

    def _wrap_value(self, value):
        if isinstance(value, dict):
            converted = {}
            for key, val in value.items():
                converted[key] = self._wrap_value(val)
            return converted
        elif isinstance(value, list):
            return list(self._wrap_value(item) for item in value)
        else:
            return value

    def _check_response(self, response):
        if response:
            self.error_handler.check_response(response)
            response['value'] = self._unwrap_value(
                response.get('value', None))
            return response
        # If the server doesn't send a response, assume the command was
        # a success
        return {'success': 0, 'value': None, 'sessionId': self.session_id}

    def _execute(self, path, method, params=None):
        """
        Send a command to the remote server.

        Any path subtitutions required for the URL mapped to the command should be
        included in the command parameters.

        :Args:
         - command - A string specifying the command to execute.
         - params - A dictionary of named parameters to send with the command as
           its JSON payload.
        """
        assert path is not None and method is not None, 'Url Method not None'
        data = utils.dump_json(params)
        path = string.Template(path).substitute(params)
        url = '{0}/{1}'.format(self._url, path)
        return self._request(method, url, body=data)

    def get(self, path, params=None):
        """
            Get method
        :param path:
        :param params:
        :return:
        """
        reponse = self._execute(path, Method.GET, params)
        if reponse:
            self.error_handler.check_response(reponse)
            return reponse
        else:
            raise RuntimeError("get url error")

    def post(self, path, params):
        """
            Post method
        :param path:
        :param params:
        :return:
        """
        reponse = self._execute(path, Method.POST, params)
        if reponse:
            self.error_handler.check_response(reponse)
            return reponse
        return True

    def _request(self, method, url, body=None):
        """
        Send an HTTP request to the remote server.

        :Args:
         - method - A string for the HTTP method to send the request with.
         - url - A string for the URL to send the request to.
         - body - A string for request body. Ignored unless method is POST or PUT.

        :Returns:
          A dictionary with the server's parsed JSON response.
        """
        LOGGER.debug('%s %s %s' % (method, url, body))

        parsed_url = parse.urlparse(url)

        if self.keep_alive:
            headers = {"Connection": 'keep-alive', method: parsed_url.path,
                       "User-Agent": "Python http auth",
                       "Content-type": "application/json;charset=\"UTF-8\"",
                       "Accept": "application/json"}
            if parsed_url.username:
                auth = base64.standard_b64encode('%s:%s' %
                                                 (parsed_url.username, parsed_url.password)).replace('\n', '')
                headers["Authorization"] = "Basic %s" % auth
            if body and method != 'POST' and method != 'PUT':
                body = None
            try:
                self._conn.request(method, parsed_url.path, body, headers)
                resp = self._conn.getresponse()
            except (httplib.HTTPException, socket.error):
                self._conn.close()
                raise

            statuscode = resp.status
        else:
            password_manager = None
            if parsed_url.username:
                netloc = parsed_url.hostname
                if parsed_url.port:
                    netloc += ":%s" % parsed_url.port
                cleaned_url = parse.urlunparse((parsed_url.scheme,
                                                netloc,
                                                parsed_url.path,
                                                parsed_url.params,
                                                parsed_url.query,
                                                parsed_url.fragment))
                password_manager = url_request.HTTPPasswordMgrWithDefaultRealm()
                password_manager.add_password(None,
                                              "%s://%s" % (parsed_url.scheme, netloc),
                                              parsed_url.username,
                                              parsed_url.password)
                request = Request(cleaned_url, data=body.encode('utf-8'), method=method)
            else:
                request = Request(url, data=body.encode('utf-8'), method=method)

            request.add_header('Accept', 'application/json')
            request.add_header('Content-Type', 'application/json;charset=UTF-8')

            if password_manager:
                opener = url_request.build_opener(url_request.HTTPRedirectHandler(),
                                                  HttpErrorHandler(),
                                                  url_request.HTTPBasicAuthHandler(password_manager))
            else:
                opener = url_request.build_opener(url_request.HTTPRedirectHandler(),
                                                  HttpErrorHandler())
            resp = opener.open(request, timeout=self._timeout)
            statuscode = resp.code
            if not hasattr(resp, 'getheader'):
                if hasattr(resp.headers, 'getheader'):
                    resp.getheader = lambda x: resp.headers.getheader(x)
                elif hasattr(resp.headers, 'get'):
                    resp.getheader = lambda x: resp.headers.get(x)

        data = resp.read()
        try:
            if 300 <= statuscode < 304:
                return self._request('GET', resp.getheader('location'))
            body = data.decode('utf-8').replace('\x00', '').strip()
            if 399 < statuscode <= 510:
                return {'status': statuscode, 'value': body}
            content_type = []
            if resp.getheader('Content-Type') is not None:
                content_type = resp.getheader('Content-Type').split(';')
            if not any([x.startswith('image/png') for x in content_type]):
                try:
                    data = utils.load_json(body.strip())
                except ValueError:
                    if 199 < statuscode < 300:
                        status = ErrorCode.SUCCESS
                    else:
                        status = ErrorCode.UNKNOWN_ERROR
                    return {'status': status, 'value': body.strip()}

                assert type(data) is dict, (
                    'Invalid server response body: %s' % body)
                # Some of the drivers incorrectly return a response
                # with no 'value' field when they should return null.
                # if 'value' not in data:
                #     data['value'] = None
                return data
            else:
                data = {'status': 0, 'value': body.strip()}
                return data
        finally:
            LOGGER.debug("Finished Request")
            resp.close()


if __name__ == '__main__':
    remote = RemoteConnection("http://127.0.0.1:5000", keep_alive=True)
    data = remote.get("tasks")
    print(data)

    post_data = {
        'id': 3,
        'title': u'minhuaxu wukenaihesos@gmail.com',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }

    data = remote.post("tasks", post_data)
    print(data)
