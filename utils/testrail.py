#
# TestRail API binding for Python 3.x (API v2, available since 
# TestRail 3.0)
#
# Learn more:
#
# http://docs.gurock.com/testrail-api2/start
# http://docs.gurock.com/testrail-api2/accessing
#
# Copyright Gurock Software GmbH. See license.md for details.
#

import base64
import json
import urllib.error
import urllib.request


class APIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    #
    # Send Get
    #
    # Issues a GET request (read) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. get_case/1)
    #
    def send_get(self, uri):
        return self.__send_request('GET', uri, None)

    #
    # Send POST
    #
    # Issues a POST request (write) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. add_case/1)
    # data                The data to submit as part of the request (as
    #                     Python dict, strings must be UTF-8 encoded)
    #
    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        request = urllib.request.Request(url)
        if (method == 'POST'):
            request.data = bytes(json.dumps(data), 'utf-8')
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        request.add_header('Authorization', 'Basic %s' % auth)
        request.add_header('Content-Type', 'application/json')

        e = None
        try:
            response = urllib.request.urlopen(request).read()
        except urllib.error.HTTPError as ex:
            response = ex.read()
            e = ex

        if response:
            result = json.loads(response.decode())
        else:
            result = {}

        if e != None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received'
            raise APIError('TestRail API returned HTTP %s (%s)' %
                           (e.code, error))

        return result


class APIError(Exception):
    pass


class TestRail:
    def __init__(self, url, user, password):
        self.client = APIClient(url)
        self.client.user = user
        self.client.password = password

    STATUSES = {
        "passed": 1,
        "failed": 5,
        "broken": 4,
        "skipped": 2,
        "pending": 2
    }

    def add_run(self, project_id, suite_id, name, description="", milestone_id="", assignedto_id=1, include_all=True,
                case_ids=[]):
        data = {
            "suite_id": suite_id,
            "name": name,
            "assignedto_id": assignedto_id,
            "include_all": include_all,
            "case_ids": case_ids,
            "description": description,
            "milestone_id": milestone_id
        }
        respond = self.client.send_post('add_run/%s' % project_id, data=data)
        return respond['id']

    def add_result_for_case(self, run_id, case_id, status, comment="", elapsed="", defects="", version=""):
        status = self.STATUSES[status]
        data = {
            "status_id": status,
            "comment": comment,
            "elapsed": elapsed,
            "defects": defects,
            "version": version
        }
        self.client.send_post('add_result_for_case/%s/%s' % (run_id, case_id), data=data)

    def get_case(self, case_id):
        return self.client.send_get("get_case/%s" % case_id)

    def updated_case(self, case_id, data):
        return self.client.send_post('update_case/%s' % case_id, data=data)

    def delete_run(self, run_id):
        return self.client.send_post("delete_run/%s" % run_id, data={})

    def get_user_by_email(self, email):
        response = self.client.send_get("get_user_by_email&email=%s" % email)
        return response['id']

    def get_tests(self, run_id):
        response = self.client.send_get("get_tests/%s" % run_id)
        return response

    def get_run(self, run_id):
        response = self.client.send_get("get_run/%s" % run_id)
        return response

    def get_configs(self, run_id):
        run_response = self.get_run(run_id)
        config_response = self.client.send_get("get_configs/%s" % run_response['project_id'])
        out = dict()
        for config_id in run_response['config_ids']:
            for config in config_response[0]['configs']:
                if config['id'] == config_id:
                    out[config_response[0]['name']] = config['name']
        return out

    def get_latest_milestone(self, project_id):
        response = self.client.send_get("get_milestones/%s" % project_id)[-1]
        return response

    def get_suite(self, suite_id):
        response = self.client.send_get("get_suite/%s" % suite_id)
        return response

    def get_cases(self, project_id, suite_id):
        response = self.client.send_get("get_cases/%s&suite_id=%s" % (project_id, suite_id))
        return response
