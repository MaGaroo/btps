import os
import sys

from gen_data_parser import DataVisitor, parse_data, check_test_exists
from util import load_json, run_bash_command


PROBLEM_JSON = os.environ.get('PROBLEM_JSON')
INTERNALS_DIR = os.environ.get('INTERNALS')
SINGULAR_TEST = os.environ.get('SINGULAR_TEST')
SOLE_TEST_NAME = os.environ.get('SOLE_TEST_NAME')


class InvokingVisitor(DataVisitor):
    def on_test(self, testset_name, test_name, line, line_number):
        if SINGULAR_TEST == "false" or test_name == SOLE_TEST_NAME:
            command = [
                'bash',
                os.path.join(INTERNALS_DIR, 'invoke_test.sh'),
                test_name,
            ]
            run_bash_command(command)

if __name__ == '__main__':
    task_data = load_json(PROBLEM_JSON)
    gen_data = sys.stdin.readlines()

    if SINGULAR_TEST == "true":
        check_test_exists(gen_data, task_data, SOLE_TEST_NAME)

    parse_data(gen_data, task_data, InvokingVisitor())
