# coding:utf-8
import time, random, hashlib, json, urllib
import requests
import requests_toolbelt as rt
import os

class WeTestApi():
    def __init__(self, authparams, host):
        self.__secretid = authparams['secretid']
        self.__secretkey = authparams['secretkey']
        self.__host = host

    def _get_signature_params(self):
        t = int(time.time())
        rand = random.randint(0, 9999)
        sourcearr = [self.__secretid, self.__secretkey, str(t), str(rand)]
        sourcearr.sort()
        source_str = "".join(sourcearr)
        sign = hashlib.sha1(source_str).hexdigest()
        params = {
            'secretid': self.__secretid,
            't': t,
            'r': rand,
            'sign': sign
        }
        return params

    def _get_request_uri(self, route):
        return self.__host + route

    def _do_post_request(self, url, params):
        url = self._get_request_uri(url)
        headers = {"Conent-Type": "application/json"}
        data = json.dumps(params)
        response = requests.post(url, data=data, headers=headers)
        return response.json()

    def _do_get_request(self, url, params):
        url = self._get_request_uri(url)
        response = requests.get(url, params)
        return response.json()

    def _do_upload_request(self, url, filepath, params, fieldname="file"):
        url = self._get_request_uri(url) + "?" + urllib.urlencode(params)
        m = rt.MultipartEncoder(
            fields={
                fieldname: (filepath, open(filepath, "rb").read())
            }
        )
        headers = {
            "Content-Type": m.content_type
        }
        response = requests.post(url, data=m, headers=headers)
        return response.json()

    def add_scene_tag(self, testid, deviceid, scenename,timestamp):
        params = self._get_signature_params()
        params["testid"] = testid
        params["deviceid"] = deviceid
        params["scenename"] = scenename
        params["timestamp"] = timestamp
        return self._do_post_request("/cloud/scene_tag", params)

    def upload_video(self, testid, deviceid, videopath):
        params = self._get_signature_params()
        params["testid"] = testid
        params["deviceid"] = deviceid
        return self._do_upload_request("/cloud/test_device_video",videopath, params, "eFile")

    def upload_script_error(self, testid, deviceid, scenename, errormsg, zippath,timestamp):
        params = self._get_signature_params()
        params["testid"] = testid
        params["deviceid"] = deviceid
        params["scenename"] = scenename
        params["errormsg"] = errormsg
        params["timestamp"]= timestamp
        return self._do_upload_request("/cloud/script_error", zippath, params, "eFile")


authparams = {
    "secretid": "wetest_cloud",
    "secretkey": "ckdywKId9idmcPMJHUYsMPQ9qm",
}

if __name__ == '__main__':
    url=os.environ.get("REPORTURL")
    if url is None:
        url="http://10.12.236.230:50003"
    client = WeTestApi(authparams,url )
    # 上报场景
    resp = client.add_scene_tag(1, 2, "登陆场景",int(time.time()))
    print json.dumps(resp)

    # 上报脚本错误
    resp = client.upload_script_error(1, 2, "登陆场景", "登陆错误，遇到很二的问题","error.zip",int(time.time()))
    print resp