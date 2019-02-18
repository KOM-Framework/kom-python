import requests

from ..general import Log


class HTTP:

    @classmethod
    def __send_request(cls, request_type, **kwargs):
        Log.info('Sending %s request to %s url' % (request_type, kwargs['url']))
        url = kwargs.pop('url')
        method = getattr(requests, request_type)
        respond = method(url, kwargs)
        Log.info('Respond status: %s' % respond.status_code)
        Log.info('Respond text: %s' % respond.text)
        return respond

    @classmethod
    def send_get_request(cls, url, headers=None):
        return cls.__send_request('get', url=url, headers=headers)

    @classmethod
    def send_post_request(cls, url, data=None, files=None, headers=None, json=None):
        return cls.__send_request('post', url=url, data=data, files=files, headers=headers, json=json)

    @classmethod
    def send_put_request(cls, url, data=None, json=None, headers=None):
        return cls.__send_request('put', url=url, data=data, headers=headers, json=json)

    @classmethod
    def send_delete_request(cls, url, headers=None):
        return cls.__send_request('delete', url=url, headers=headers)

    @staticmethod
    def send_get_requests(api_list):
        for api in api_list:
            HTTP.send_get_request(api)
