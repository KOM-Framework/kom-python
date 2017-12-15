import requests

from ..general import Log


class HTTP:

    @staticmethod
    def send_get_request(url, headers=None):
        Log.info('Sending GET request to %s url' % url)
        respond = requests.get(url, headers=headers)
        Log.info('Respond status: %s' % respond.status_code)
        return respond

    @staticmethod
    def send_post_request(url, data=None, files=None, headers=None, json=None):
        Log.info('Sending POST request to %s url' % url)
        respond = requests.post(url, data=data, files=files, headers=headers, json=json)
        Log.info('Respond status: %s' % respond.status_code)
        return respond

    @staticmethod
    def send_put_request(url, data, headers=None):
        Log.info('Sending PUT request to %s url' % url)
        respond = requests.put(url, data=data, headers=headers)
        Log.info('Respond status: %s' % respond.status_code)
        return respond

    @staticmethod
    def send_delete_request(url, headers=None):
        Log.info('Sending DELETE request to %s url' % url)
        respond = requests.delete(url, headers=headers)
        Log.info('Respond status: %s' % respond.status_code)
        return respond

    @staticmethod
    def send_get_requests(api_list):
        for api in api_list:
            HTTP.send_get_request(api)
