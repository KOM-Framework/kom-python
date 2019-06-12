import requests

from ..general import Log


def add_http_trace(f):

    def get_name(name):
        return name.split(' ')[1].split('_')[1].upper()

    def wrapper(*args, **kwargs):
        Log.info('Sending %s request' % get_name(str(f)))
        Log.info('Request args: %s' % str(args[1:]))
        Log.info('Request kwargs: %s' % str(kwargs))
        respond = f(*args, **kwargs)
        Log.info('Respond status: %s' % respond.status_code)
        Log.info('Respond text: %s' % respond.text)
        return respond
    return wrapper


class HTTP:

    @classmethod
    @add_http_trace
    def send_get_request(cls, url, headers=None):
        return requests.get(url, headers=headers)

    @classmethod
    @add_http_trace
    def send_post_request(cls, url, data=None, files=None, headers=None, json=None):
        return requests.post(url, data=data, json=json, headers=headers, files=files)

    @classmethod
    @add_http_trace
    def send_put_request(cls, url, data=None, json=None, headers=None):
        return requests.put(url, data=data, json=json, headers=headers)

    @classmethod
    @add_http_trace
    def send_patch_request(cls, url, data, json, headers):
        return requests.patch(url, data=data, json=json, headers=headers)

    @classmethod
    @add_http_trace
    def send_delete_request(cls, url, headers=None):
        return requests.delete(url, headers=headers)

    @staticmethod
    def send_get_requests(api_list):
        for api in api_list:
            HTTP.send_get_request(api)
