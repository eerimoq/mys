from .utils import TestCase
from mys.parser import ast
from mys.transpiler.iterators import transform


def remove_whitespace_lines(text):
    lines = []

    for line in text.splitlines():
        line = line.rstrip()

        if line:
            lines.append(line)

    return '\n'.join(lines)

class Test(TestCase):

    def assert_ok(self, iterator_code, class_code):
        tree = ast.parse(iterator_code).body[0]
        tree = transform(tree)
        self.assertEqual(
            remove_whitespace_lines(ast.unparse(ast.fix_missing_locations(tree))),
            remove_whitespace_lines(class_code))

    def test_empty(self):
        self.assert_ok(
            '@iterator\n'
            'def foo() -> i64:\n'
            '    pass\n'
            '',
            'class Foo:\n'
            '    _state: i64\n'
            '\n'
            '    def __init__(self):\n'
            '        self._state = 0\n'
            '\n'
            '    def next(self) -> i64:\n'
            '        while True:\n'
            '            match self._state:\n'
            '                case 0:\n'
            '                    pass\n'
            '                    raise RuntimeError()')

    def test_three_yield(self):
        self.assert_ok(
            '@iterator\n'
            'def foo() -> i64:\n'
            '    yield 1\n'
            '    yield 3\n'
            '    yield 5\n'
            '',
            'class Foo:\n'
            '    _state: i64\n'
            '\n'
            '    def __init__(self):\n'
            '        self._state = 0\n'
            '\n'
            '    def next(self) -> i64:\n'
            '        while True:\n'
            '            match self._state:\n'
            '                case 0:\n'
            '                    self._state = 1\n'
            '\n'
            '                    return 1\n'
            '                case 1:\n'
            '                    self._state = 2\n'
            '\n'
            '                    return 3\n'
            '                case 2:\n'
            '                    self._state = 3\n'
            '\n'
            '                    return 5\n'
            '                case 3:\n'
            '                    raise RuntimeError()')

    def test_if(self):
        self.assert_ok(
            '@iterator\n'
            'def foo() -> i64:\n'
            '    if True:\n'
            '        print(1)\n'
            '        yield 1\n'
            '    else:\n'
            '        yield 2\n'
            '        print(2)\n'
            '',
            'class Foo:\n'
            '    _state: i64\n'
            '\n'
            '    def __init__(self):\n'
            '        self._state = 0\n'
            '\n'
            '    def next(self) -> i64:\n'
            '        while True:\n'
            '            match self._state:\n'
            '                case 2:\n'
            '                    self._state = 1\n'
            '                case 3:\n'
            '                    print(2)\n'
            '                    self._state = 1\n'
            '                case 0:\n'
            '                    if True:\n'
            '                        print(1)\n'
            '                        self._state = 2\n'
            '\n'
            '                        return 1\n'
            '                    else:\n'
            '                        self._state = 3\n'
            '\n'
            '                        return 2\n'
            '                case 1:\n'
            '                    raise RuntimeError()')

    def test_while(self):
        self.assert_ok(
            '@iterator\n'
            'def foo() -> i64:\n'
            '    i = 0\n'
            '\n'
            '    while i < 10:\n'
            '        yield i\n'
            '        i += 1\n'
            '',
            'class Foo:\n'
            '    _state: i64\n'
            '\n'
            '    def __init__(self):\n'
            '        self._state = 0\n'
            '\n'
            '    def next(self) -> i64:\n'
            '        while True:\n'
            '            match self._state:\n'
            '                case 0:\n'
            '                    i = 0\n'
            '                    self._state = 2\n'
            '                case 3:\n'
            '                    i += 1\n'
            '                    self._state = 2\n'
            '                case 2:\n'
            '                    if i < 10:\n'
            '                        self._state = 3\n'
            '\n'
            '                        return i\n'
            '                    else:\n'
            '                        self._state = 1\n'
            '                case 1:\n'
            '                    raise RuntimeError()')

    def test_mixed(self):
        self.assert_ok(
            '@iterator\n'
            'def foo() -> i64:\n'
            '    i = 0\n'
            '    while i < 10:\n'
            '        if i == 5:\n'
            '            yield i\n'
            '        else:\n'
            '            yield 2 * i\n'
            '\n'
            '        i += 1\n'
            '\n'
            '    if True:\n'
            '        print(1 + 2)\n'
            '    elif False:\n'
            '        i = 1\n'
            '        while i != 1:\n'
            '            yield 5 - i\n'
            '    else:\n'
            '        print(1 - 1)\n'
            '',
            'class Foo:\n'
            '    _state: i64\n'
            '\n'
            '    def __init__(self):\n'
            '        self._state = 0\n'
            '\n'
            '    def next(self) -> i64:\n'
            '        while True:\n'
            '            match self._state:\n'
            '                case 0:\n'
            '                    i = 0\n'
            '                    self._state = 2\n'
            '                case 4:\n'
            '                    self._state = 3\n'
            '                case 5:\n'
            '                    self._state = 3\n'
            '                case 3:\n'
            '                    i += 1\n'
            '                    self._state = 2\n'
            '                case 2:\n'
            '                    if i < 10:\n'
            '                        if i == 5:\n'
            '                            self._state = 4\n'
            '\n'
            '                            return i\n'
            '                        else:\n'
            '                            self._state = 5\n'
            '\n'
            '                            return 2 * i\n'
            '                    else:\n'
            '                        self._state = 1\n'
            '                case 10:\n'
            '                    self._state = 9\n'
            '                case 9:\n'
            '                    if i != 1:\n'
            '                        self._state = 10\n'
            '\n'
            '                        return 5 - i\n'
            '                    else:\n'
            '                        self._state = 8\n'
            '                case 8:\n'
            '                    self._state = 7\n'
            '                case 7:\n'
            '                    self._state = 6\n'
            '                case 1:\n'
            '                    if True:\n'
            '                        print(1 + 2)\n'
            '                        self._state = 6\n'
            '                    elif False:\n'
            '                        i = 1\n'
            '                        self._state = 9\n'
            '                    else:\n'
            '                        print(1 - 1)\n'
            '                        self._state = 7\n'
            '                case 6:\n'
            '                    raise RuntimeError()')
