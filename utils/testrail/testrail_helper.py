import os
from datetime import datetime

from kom_framework.src.general import Log
from kom_framework.utils.testrail.api_client import APIError
from kom_framework.utils.testrail.testrail_service import TestRailService, TestCaseStatuses


class TestRailHelper:

    def __init__(self, base_url: str, user: str, password: str, project_id: str):
        self.service = TestRailService(base_url, user, password)
        self.project_id = project_id

    def get_plan_id(self):
        plan_name = f'Nightly Execution Plan for {datetime.now().strftime("%Y-%m-%d")}'
        plans = self.service.get_opened_plans(self.project_id)
        plan_names = [plan['name'] for plan in plans]
        if plan_name in plan_names:
            for plan in plans:
                if plan['name'] == plan_name:
                    return plan['id']
        else:
            created_plan = self.service.add_plan(self.project_id, plan_name, '', '', [])
            return created_plan['id']

    def get_test_rail_run_description(self):
        description_start_time = "Execution start time - '%s' \n" % datetime.now()
        description_allure_link = 'Allure results link - %sallure/' % os.environ.get(
            'BUILD_URL')
        description = description_start_time + "\n" + description_allure_link
        return description

    def update_run_description(self, run_id, description):
        run_context = self.service.get_run(run_id)
        if run_context['plan_id']:
            plan_entries = self.service.get_plan_entry_by_run_id(run_context['plan_id'], run_id)['id']
            data = {
                'description': description
            }
            if plan_entries:
                return self.service.update_plan_entry(run_context['plan_id'], plan_entries, data)
        else:
            return self.service.update_run_description(run_id, description)
        return None

    def get_run_id_by_name(self, name, data):
        for run in data['runs']:
            if run['name'] == name:
                return run['id']
        return None

    def get_test_rail_run(self):
        run_id = os.environ.get('test_rail_run_id', None)
        if not run_id:
            suite_id = os.environ.get('test_rail_suite_id', None)
            if suite_id:
                cases_list_ids = [case['id'] for case in self.service.get_cases(self.project_id, suite_id)
                                  if case['custom_execution_type'] == 2]
                suite_name = f'{self.service.get_suite(suite_id)["name"]}' \
                    f' - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                assign_to_id = self.service.get_user_by_email(email='oleh@thirdshelf.com')['id']
                plan_id = self.get_plan_id()
                plan_entry = self.service.add_plan_entry(plan_id, suite_id, suite_name,
                                                         self.get_test_rail_run_description(), assign_to_id,
                                                         False, cases_list_ids)
                run_id = str(self.get_run_id_by_name(suite_name, plan_entry))
                os.environ['test_rail_run_id'] = run_id  # For parallel execution
            else:
                return None
        self.update_run_description(run_id, self.get_test_rail_run_description())
        Log.info('TestRail run ID: "%s"' % run_id)
        return self.service.get_run(run_id)

    def get_test_ids(self, test_case):
        marker = test_case.get_closest_marker('test_id')
        if marker:
            return marker.args
        return None

    def get_result_from_string(self, str_result: str) -> TestCaseStatuses:
        if str_result == 'passed':
            return TestCaseStatuses.PASSED
        elif str_result == 'failed':
            return TestCaseStatuses.FAILED
        elif str_result == 'flaky':
            return TestCaseStatuses.FLAKY
        elif str_result == 'broken':
            return TestCaseStatuses.BROKEN
        elif str_result == 'skipped':
            return TestCaseStatuses.SKIPPED
        elif str_result == 'pending':
            return TestCaseStatuses.PENDING

    def send_logs_to_test_rail(self, run_id, call, item, outcome):
        comment = '\n'.join(Log.log_entries)
        if call.excinfo:
            comment += '\n'+str(item.repr_failure(call.excinfo))
        test_case_ids = self.get_test_ids(item)
        if test_case_ids:
            for test_id in test_case_ids:
                try:
                    actual_result = outcome.get_result().outcome
                    if hasattr(item, 'execution_count'):
                        if item.execution_count > 1 and actual_result == 'passed':
                            actual_result = 'flaky'
                    self.service.add_result_for_case(run_id, test_id,
                                                     self.get_result_from_string(actual_result), comment)
                except APIError:
                    continue

    def filter_collected_tests_by_run_id(self, run_id, items):
        test_cases_ids = [test_case['case_id']
                          for test_case in self.service.get_tests(run_id)]
        for test_case in items[:]:
            test_ids = self.get_test_ids(test_case)
            if test_ids:
                [items.remove(test_case) for test_id in self.get_test_ids(test_case)
                 if test_id not in test_cases_ids]
            else:
                items.remove(test_case)