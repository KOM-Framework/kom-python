from kom_framework.utils.testrail.api_client import APIClient


class TestCaseStatuses:
    PASSED = 1
    BLOCKED = 2
    SKIPPED = 2
    PENDING = 2
    UNTESTED = 3
    RETEST = 4
    BROKEN = 4
    FAILED = 5
    FLAKY = 6
    NOT_APPLICABLE = 7

    @classmethod
    def all(cls):
        return [cls.PASSED, cls.BLOCKED, cls.UNTESTED, cls.RETEST,
                cls.FAILED, cls.FLAKY, cls.NOT_APPLICABLE]

    @classmethod
    def get_result_status(cls, result: str):
        string_mapping = {
            "passed": cls.PASSED,
            "failed": cls.FAILED,
            "broken": cls.BLOCKED,
            "skipped": cls.SKIPPED,
            "pending": cls.PENDING,
            'flaky': cls.FLAKY
        }
        return string_mapping[result]


class TestRailService(APIClient):
    def __init__(self, base_url, user, password):
        super().__init__(base_url)
        self.user = user
        self.password = password

    def add_attachment_to_result(self, result_id, path):
        response = self.send_post(f'add_attachment_to_result/{result_id}', path)
        return response

    def add_plan(self, project_id: str, name: str, description: str, milestone_id: str, entries: list):
        data = {
            'name': name,
            'description': description,
            'milestone_id': milestone_id,
            'entries': entries
        }
        response = self.send_post(f'add_plan/{project_id}', data=data)
        return response

    def add_plan_entry(self, plan_id: str, suite_id: str, name: str, description: str = '', assigned_to_id: int = 1,
                       include_all: bool = True, case_ids: list = (), config_ids: list = (), runs: list = ()):
        data = {
            'suite_id': suite_id,
            'name': name,
            'description': description,
            'assignedto_id': assigned_to_id,
            'include_all': include_all,
            'case_ids': case_ids,
            'config_ids': config_ids,
            'runs': runs
        }
        response = self.send_post(f'add_plan_entry/{plan_id}', data=data)
        return response

    def add_result_for_case(self, run_id: str, case_id: str, status: TestCaseStatuses,
                            comment: str = '', elapsed: str = '', defects='', version=''):
        data = {
            'status_id': status,
            'comment': comment,
            'elapsed': elapsed,
            'defects': defects,
            'version': version
        }
        response = self.send_post('add_result_for_case/%s/%s' % (run_id, case_id), data=data)
        return response

    def add_run(self, project_id: str, suite_id: str, name: str, description: str = '', milestone_id: str = '',
                assigned_to_id: int = 1, include_all: bool = True, case_ids: list = ()):
        data = {
            'suite_id': suite_id,
            'name': name,
            'assignedto_id': assigned_to_id,
            'include_all': include_all,
            'case_ids': case_ids,
            'description': description,
            'milestone_id': milestone_id
        }
        response = self.send_post(f'add_run/{project_id}', data=data)
        return response

    def close_run(self, run_id: str):
        response = self.send_post(f'close_run/{run_id}', data={})
        return response

    def delete_attachment(self, attachment_id):
        response = self.send_post(f'delete_attachment/{attachment_id}', None)
        return response

    def delete_run(self, run_id):
        return self.send_post(f"delete_run/{run_id}", data={})

    def get_attachments_for_test(self, test_id):
        response = self.send_get(f'get_attachments_for_test/{test_id}')
        return response

    def get_case(self, case_id: str):
        return self.send_get(f'get_case/{case_id}')

    def get_cases(self, project_id: str, suite_id: str):
        all_cases = []
        response = True
        step = 250
        i = 0
        while response:
            response = self.send_get(f'get_cases/{project_id}&suite_id={suite_id}&limit={step}&offset={step*i}')
            all_cases.extend(response)
            i += 1
        return all_cases

    def get_configs_names(self, run: dict):
        config_response = self.send_get(f'get_configs/{run["project_id"]}')
        out = dict()
        for config_run_id in run['config_ids']:
            for config_group in config_response:
                for config in config_group['configs']:
                    if config['id'] == config_run_id:
                        out[config_group['name']] = config['name']
                        break
        return out

    def get_configs(self, project_id: str):
        return self.send_get(f'get_configs/{project_id}')

    def get_milestones(self, project_id: str):
        response = self.send_get(f'get_milestones/{project_id}')
        return response

    def get_opened_plans(self, project_id: str):
        response = self.send_get(f'get_plans/{project_id}&is_completed=0')
        return response

    def get_plan(self, plan_id):
        response = self.send_get(f'/get_plan/{plan_id}')
        return response

    def get_plans(self, project_id: str, filters: str = None):
        url = f'/get_plans/{project_id}'
        if filters:
            url += f'&{filters}'
        response = self.send_get(url)
        return response

    def get_plan_entry_by_run_id(self, plan_id: str, run_id: str):
        plan_context = self.get_plan(plan_id)
        for entry in plan_context['entries']:
            for run in entry['runs']:
                if run['id'] == int(run_id):
                    return entry
        return None

    def get_results_for_case(self, run_id: str, case_id: str):
        response = self.send_get(f'get_results_for_case/{run_id}/{case_id}')
        return response

    def get_run(self, run_id: str):
        response = self.send_get(f'get_run/{run_id}')
        return response

    def get_runs(self, project_id: str, filters: str):
        url = f'get_runs/{project_id}'
        if filters:
            url += f'&{filters}'
        response = self.send_get(url)
        return response

    def get_suite(self, suite_id: str):
        response = self.send_get(f'get_suite/{suite_id}')
        return response

    def get_suites(self, project_id: str):
        response = self.send_get(f'get_suites/{project_id}')
        return response

    def get_tests(self, run_id: str):
        response = self.send_get(f'get_tests/{run_id}')
        return response

    def get_user_by_email(self, email: str):
        response = self.send_get(f'get_user_by_email&email={email}')
        return response

    def update_case(self, case_id: str, data: dict):
        return self.send_post(f'update_case/{case_id}', data=data)

    def update_plan_entry(self, plan_id: str, entry_id: str, data: dict = ()):
        response = self.send_post(f'/update_plan_entry/{plan_id}/{entry_id}', data)
        return response

    def update_run_description(self, run_id: str, description: str):
        data = {
            'description': description
        }
        response = self.send_post(f'/update_run/{run_id}', data=data)
        return response

    def close_plan(self, plan_id: str):
        response = self.send_post(f'/close_plan/{plan_id}', data={})
        return response
