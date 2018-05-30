from kom_framework.utils.testrail import APIClient, TestRail
from kom_framework.src.general import Log
import pytest
import re

CONST_EXTERNAL_DEFAULT_USER_EMAIL = "sergii.khomenko@x2omedia.com"
CONST_EXTERNAL_DEFAULT_PASSWORD = "X2Omedia"
CONST_TESTRAIL_URL = "https://x2o.testrail.net/"
CONST_TESTRAIL_FIELD_STEP = "custom_steps"
CONST_TESTRAIL_FIELD_TITLE = "title"
CONST_TESTRAIL_FIELD_EXPECTRESULT = "custom_expected"
CONST_TESTRAIL_FIELD_PREREQUISITE = "custom_preconds"
CONST_TESTRAIL_FIELD_PRIORITY = "priority_id"

TESTRAIL_PREFIX = 'testrail'

severity = {
    0: pytest.allure.severity_level.TRIVIAL,
    1: pytest.allure.severity_level.MINOR,
    2: pytest.allure.severity_level.NORMAL,
    3: pytest.allure.severity_level.CRITICAL,
    4: pytest.allure.severity_level.BLOCKER
}


def clean_test_ids(test_id):
    return [re.search('(?P<test_id>[0-9]+$)', test_id).groupdict().get('test_id') for test_id in test_id][0]

def get_testrail_key(item):
    if item.get_marker("testrail"):
        return clean_test_ids(item.get_marker("testrail").kwargs.get('ids'))
    return None


def get_testrail_keys(items):
    """Return TestRail ids from pytests markers"""
    testcaseids = []
    for item in items:
        if item.get_marker(TESTRAIL_PREFIX):
            testcaseids.extend(
                clean_test_ids(
                    item.get_marker(TESTRAIL_PREFIX).kwargs.get('ids')
                )
            )
    return testcaseids


class pytestrail(object):
    @staticmethod
    def case(*ids):
        return pytest.mark.testrail(ids=ids)


def get_cases_from_run(rid):
    test_run_json_response = TestRail(CONST_TESTRAIL_URL, CONST_EXTERNAL_DEFAULT_USER_EMAIL, CONST_EXTERNAL_DEFAULT_PASSWORD).get_tests(rid)
    return {test["case_id"]:test for test in test_run_json_response}

def log_testrail_info(tcid):
    case = TestRail(CONST_TESTRAIL_URL, CONST_EXTERNAL_DEFAULT_USER_EMAIL, CONST_EXTERNAL_DEFAULT_PASSWORD).get_case(tcid)
    id = "Test Case ID: " + tcid + "\n"
    title = "Test Case Title: " + case[CONST_TESTRAIL_FIELD_TITLE] + "\n"
    prerequisite = "Test Case Pre-requisite: " + (case[CONST_TESTRAIL_FIELD_PREREQUISITE] if case[CONST_TESTRAIL_FIELD_PREREQUISITE] else "None") + "\n"
    description = "Test Case Steps: " + (case[CONST_TESTRAIL_FIELD_STEP] if case[CONST_TESTRAIL_FIELD_STEP] else "None") + "\n"
    expect_result = "Test Case Expect Result: " + (case[CONST_TESTRAIL_FIELD_EXPECTRESULT] if case[CONST_TESTRAIL_FIELD_EXPECTRESULT] else "None") + "\n"
    priority = "Test Case Priority: " + severity.get(case[CONST_TESTRAIL_FIELD_PRIORITY]) + "\n"
    Log.info((" " * 24).join([id, title, prerequisite, ("\n" + " " * 41).join(description.split("\r\n")), expect_result, priority]))
    Log.info("=" * 80)


def get_severity(tcid):
    case = TestRail(CONST_TESTRAIL_URL, CONST_EXTERNAL_DEFAULT_USER_EMAIL, CONST_EXTERNAL_DEFAULT_PASSWORD).get_case(tcid)
    return case[CONST_TESTRAIL_FIELD_PRIORITY]
