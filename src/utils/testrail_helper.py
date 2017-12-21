from kom_framework.utils.testrail import APIClient
from kom_framework.src.general import Log
import pytest

CONST_EXTERNAL_DEFAULT_USER_EMAIL = "sergii.khomenko@x2omedia.com"
CONST_EXTERNAL_DEFAULT_PASSWORD = "X2Omedia"

CONST_TESTRAIL_URL = "https://x2o.testrail.net/"
CONST_TESTRAIL_FIELD_STEP = "custom_steps"
CONST_TESTRAIL_FIELD_TITLE = "title"
CONST_TESTRAIL_FIELD_EXPECTRESULT = "custom_expected"
CONST_TESTRAIL_FIELD_PREREQUISITE = "custom_preconds"
CONST_TESTRAIL_FIELD_PRIORITY = "priority_id"

severity = {
    0: pytest.allure.severity_level.TRIVIAL,
    1: pytest.allure.severity_level.MINOR,
    2: pytest.allure.severity_level.NORMAL,
    3: pytest.allure.severity_level.CRITICAL,
    4: pytest.allure.severity_level.BLOCKER
}

def get_case(tcid):
    client = APIClient(CONST_TESTRAIL_URL)
    client.user = CONST_EXTERNAL_DEFAULT_USER_EMAIL
    client.password = CONST_EXTERNAL_DEFAULT_PASSWORD
    return client.send_get('get_case/' + tcid[1:])

def log_testrail_info(tcid):
    case = get_case(tcid)
    title = "Test Case Title: " + case[CONST_TESTRAIL_FIELD_TITLE] + "\n"
    prerequisite = "Test Case Pre-requisite: " + case[CONST_TESTRAIL_FIELD_PREREQUISITE] + "\n"
    description = "Test Case Steps: " + case[CONST_TESTRAIL_FIELD_STEP] + "\n"
    expect_result = "Test Case Expect Result: " + case[CONST_TESTRAIL_FIELD_EXPECTRESULT] + "\n"
    priority = "Test Case Priority: " + severity.get(case[CONST_TESTRAIL_FIELD_PRIORITY]) + "\n"
    Log.info("=" * 80)
    Log.info((" " * 24).join([title, prerequisite, ("\n" + " " * 41).join(description.split("\r\n")), expect_result, priority]))
    Log.info("=" * 80)

def get_severity(tcid):
    case = get_case(tcid)
    return case[CONST_TESTRAIL_FIELD_PRIORITY]