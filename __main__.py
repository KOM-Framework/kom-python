import os

import pytest
import sys

from .src.general import Log


def main():
    test_folder = "test"
    pytest_args = [test_folder]
    if os.environ.get('TEST_FOLDER'):
        test_folder += "/%s" % os.environ.get('TEST_FOLDER')
    if os.environ.get('TEST_GROUP'):
        pytest_args.append('-m')
        pytest_args.append(os.environ.get('TEST_GROUP'))
    if os.environ.get('FEATURES_TO_TEST'):
        pytest_args.append('--allure-features=%s' % os.environ.get('FEATURES_TO_TEST'))
    if os.environ.get('STORIES_TO_TEST'):
        pytest_args.append('--allure-stories=%s' % os.environ.get('STORIES_TO_TEST'))
    pytest_args.append('--alluredir=allure-results')
    Log.info('pytest args "%s"' % str(pytest_args))
    return pytest.main(pytest_args)


if __name__ == '__main__':
    sys.exit(main())
