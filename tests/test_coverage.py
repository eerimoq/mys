from unittest.mock import patch

import mys.cli

from .utils import Path
from .utils import TestCase
from .utils import build_and_test_module


class Test(TestCase):

    def test_coverage(self):
        build_and_test_module('coverage', ['--coverage'])

        with open('tests/build/test_coverage/.mys-coverage.txt', 'r') as fin:
            mys_coverage = fin.read()

        self.assert_in(
            'File: ./src/coverage.mys\n'
            '1 0\n'
            '2 0\n'
            '4 3\n'
            '5 3\n'
            '7 3\n'
            '8 1\n'
            '9 2\n'
            '11 0\n'
            '15 2\n'
            '17 3\n'
            '18 0\n'
            '20 3\n'
            '21 6\n'
            '22 3\n'
            '23 3\n'
            '24 0\n'
            '26 3\n'
            '28 2\n'
            '29 2\n'
            '30 1\n'
            '31 1\n'
            '32 0\n'
            '33 0\n'
            '34 1\n'
            '35 1\n'
            '43 1\n'
            '44 1\n'
            '49 1\n'
            '50 1\n'
            '52 0\n'
            '53 0\n',
            mys_coverage)

        self.assert_file_exists('tests/build/test_coverage/covhtml/index.html')
        self.assert_file_exists('tests/build/test_coverage/.coverage')
        self.assert_file_exists('tests/build/test_coverage/.mys-coverage.txt')

        with Path('tests/build/test_coverage'):
            with patch('sys.argv', ['mys', 'clean']):
                mys.cli.main()

        self.assert_file_not_exists('tests/build/test_coverage/covhtml')
        self.assert_file_not_exists('tests/build/test_coverage/.coverage')
        self.assert_file_not_exists('tests/build/test_coverage/.mys-coverage.txt')
