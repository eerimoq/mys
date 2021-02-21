import shutil
import subprocess
from unittest.mock import patch

import mys.cli

from .utils import Path
from .utils import TestCase
from .utils import remove_build_directory


class Test(TestCase):

    def run_test_assert(self, name, expected):
        proc = subprocess.run(['./build/default/test', name],
                              capture_output=True,
                              text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assert_in(expected, proc.stderr)

    def test_traceback(self):
        name = 'test_traceback'
        remove_build_directory(name)

        shutil.copytree('tests/files/traceback', f'tests/build/{name}')

        with Path(f'tests/build/{name}'):
            try:
                with patch('sys.argv', ['mys', 'test', '-v']):
                    mys.cli.main()
            except SystemExit:
                pass

            self.run_test_assert(
                'test_panic',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 3 in test_panic\n'
                '    print(""[1])\n'
                '\n'
                'Panic(message="String index 1 is out of range.")\n')

            self.run_test_assert(
                'test_panic_2',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 11 in test_panic_2\n'
                '    panic_2()\n'
                '  File: "./src/lib.mys", line 7 in panic_2\n'
                '    print(""[i])\n'
                '\n'
                'Panic(message="String index 10 is out of range.")\n')

            self.run_test_assert(
                'test_panic_in_except',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 21 in test_panic_in_except\n'
                '    print(b""[11])\n'
                '\n'
                'Panic(message="Bytes index 11 is out of range.")\n')

            self.run_test_assert(
                'test_panic_in_if',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 26 in test_panic_in_if\n'
                '    print(b""[5])\n'
                '\n'
                'Panic(message="Bytes index 5 is out of range.")\n')

            self.run_test_assert(
                'test_panic_in_else',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 33 in test_panic_in_else\n'
                '    print(b""[6])\n'
                '\n'
                'Panic(message="Bytes index 6 is out of range.")\n')

            self.run_test_assert(
                'test_panic_in_for',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 38 in test_panic_in_for\n'
                '    print(b"123"[i])\n'
                '\n'
                'Panic(message="Bytes index 3 is out of range.")\n')

            self.run_test_assert(
                'test_panic_in_while',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 43 in test_panic_in_while\n'
                '    print(b""[10])\n'
                '\n'
                'Panic(message="Bytes index 10 is out of range.")\n')

            self.run_test_assert(
                'test_panic_in_match',
                'Traceback (most recent call last):\n'
                '  File: "./src/lib.mys", line 49 in test_panic_in_match\n'
                '    print(b""[-1])\n'
                '\n'
                'Panic(message="Bytes index -1 is out of range.")\n')