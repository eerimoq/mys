from mys.transpiler import TranspilerError
from .utils import build_and_test_module
from .utils import TestCase
from .utils import transpile_source


class Test(TestCase):

    def test_generics(self):
        build_and_test_module('generics')

    def test_missing_generic_type(self):
        with self.assertRaises(TranspilerError) as cm:
            transpile_source('@generic\n'
                             'def foo():\n'
                             '    pass\n')

        self.assert_exception_string(
            cm,
            '  File "", line 1\n'
            '    @generic\n'
            '     ^\n'
            "CompileError: at least one parameter required\n")

    def test_generic_given_more_than_once(self):
        with self.assertRaises(TranspilerError) as cm:
            transpile_source('@generic(T1)\n'
                             '@generic(T2)\n'
                             'def foo(a: T1, b: T2):\n'
                             '    pass\n')

        self.assert_exception_string(
            cm,
            '  File "", line 2\n'
            '    @generic(T2)\n'
            '     ^\n'
            "CompileError: @generic can only be given once\n")

    def test_generic_type_given_more_than_once(self):
        with self.assertRaises(TranspilerError) as cm:
            transpile_source('@generic(T1, T1)\n'
                             'def foo(a: T1):\n'
                             '    pass\n')

        self.assert_exception_string(
            cm,
            '  File "", line 1\n'
            '    @generic(T1, T1)\n'
            '                 ^\n'
            "CompileError: 'T1' can only be given once\n")

    def test_generic_undefined_type(self):
        with self.assertRaises(TranspilerError) as cm:
            transpile_source('@generic(T)\n'
                             'def add(a: T) -> T:\n'
                             '    return a\n'
                             'def foo():\n'
                             '    print(add[Foo](None))\n')

        # ToDo: Not perfect error message. Should also(?) show the
        # specialization.
        self.assert_exception_string(
            cm,
            '  File "", line 2\n'
            '    def add(a: T) -> T:\n'
            '               ^\n'
            "CompileError: undefined type 'Foo'\n")

    def test_generic_type_not_supported(self):
        with self.assertRaises(TranspilerError) as cm:
            transpile_source('@generic(T)\n'
                             'def add(a: T):\n'
                             '    a.bar()\n'
                             'def foo():\n'
                             '    add[u8](1)\n')

        # ToDo: Not perfect error message. Should also(?) show the
        # specialization.
        self.assert_exception_string(
            cm,
            '  File "", line 3\n'
            '        a.bar()\n'
            '        ^\n'
            "CompileError: primitive type 'u8' do not have methods\n")
