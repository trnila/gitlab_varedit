from unittest import TestCase
from gitlab_varedit.parser import parse, create, diff


class TestParser(TestCase):
    def test_empty(self):
        self.assertEqual({}, parse(""))

    def test_whitespaces(self):
        self.assertEqual({}, parse("   \n   "))

    def test_simple(self):
        self.assertEqual({"a": "b"}, parse("a=b"))

    def test_simple2(self):
        self.assertEqual({"foo": "bar"}, parse("foo=bar"))

    def test_quotes(self):
        self.assertEqual({"foo": "bar"}, parse("foo=\"bar\""))

    def test_singleQuotes(self):
        self.assertEqual({"foo": "bar"}, parse("foo='bar'"))

    def test_escaped_quotes(self):
        self.assertEqual({"foo": "b\\\"ar"}, parse("foo=\"b\\\"ar\""))

    def test_more(self):
        self.assertEqual({"foo": "bar", "baar": "baz"}, parse("foo=bar\nbaar=baz"))

    def test_lineskip(self):
        self.assertEqual({"foo": "bar", "bar": "baz"}, parse("foo=bar\n\nbar=baz"))

    def test_whitetrim(self):
        self.assertEqual({"foo": "bar"}, parse(" foo = bar "))

    def test_multiline(self):
        self.assertEqual(
            {"foo": "bar\nbaz\nfoobar"},
            parse("foo=\"bar\nbaz\nfoobar\"")
        )

    def test_equal_char(self):
        self.assertEqual({"foo": "="}, parse("foo=="))

    def test_equal_char_in_quote(self):
        self.assertEqual({"foo": "="}, parse("foo=\"=\""))

    def test_white_not_trim_in_quoted(self):
        self.assertEqual({"foo": "\nbar\n"}, parse('foo="\nbar\n"'))


class TestBuilder(TestCase):
    def test_empty(self):
        self.assertEqual("", create({}))

    def test_simple(self):
        self.assertEqual("foo=bar", create({"foo": "bar"}))

    def test_multi(self):
        self.assertEqual("foo=bar\nbaz=test", create({"foo": "bar", "baz": "test"}))

    def test_multiline(self):
        self.assertEqual("foo=\"bar\nbaz\ntest\"", create({"foo": "bar\nbaz\ntest"}))


class TestDiff(TestCase):
    def test_empty(self):
        self.assertEqual({
            'add': [],
            'delete': [],
            'update': []
        }, diff({}, {}))

    def test_add(self):
        self.assertEqual({
            'add': ['foo'],
            'delete': [],
            'update': []
        }, diff({}, {'foo': 'bar'}))

    def test_del(self):
        self.assertEqual({
            'add': [],
            'delete': ['foo'],
            'update': []
        }, diff({'foo': 'bar'}, {}))

    def test_update(self):
        self.assertEqual({
            'add': [],
            'delete': [],
            'update': ['foo']
        }, diff({'foo': 'bar'}, {'foo': 'baz'}))

    def test_no_update(self):
        self.assertEqual({
            'add': [],
            'delete': [],
            'update': []
        }, diff({'foo': 'bar'}, {'foo': 'bar'}))
