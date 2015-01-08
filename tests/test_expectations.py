from unittest import TestCase
from wooper import expect
from wooper.general import WooperAssertionError
from .common import response


class ExpectStatusTestCase(TestCase):

    def test_pass(self):
        response.status_code = 200
        expect.expect_status(response, 200)

    def test_fail(self):
        response.status_code = 403
        with self.assertRaises(WooperAssertionError):
            expect.expect_status(response, 200)


class ExpectStatusInTestCase(TestCase):

    def test_pass(self):
        response.status_code = 200
        expect.expect_status_in(response, {200, 201})

    def test_fail(self):
        response.status_code = 400
        with self.assertRaises(WooperAssertionError):
            expect.expect_status_in(response, {200, 401, 500})


class ExpectJsonTestCase(TestCase):

    def setUp(self):
        response.text = """{
            "foo": "bar",
            "list": [ {"baz": "spam"}, "1", "qwe" ]
        }"""

    def test_pass(self):
        expect.expect_json(
            response,
            """{
                "foo": "bar",
                "list": [ {"baz": "spam"}, "1", "qwe" ]
            }"""
        )

    def test_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json(
                response,
                """{
                    "foo": "bar",
                    "list": [ {"baz": "spa"}, "1", "qwe" ]
                }"""
            )

    def test_path_pass(self):
        expect.expect_json(
            response,
            "spam",
            path="list/[0]/baz"
        )

    def test_path_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json(
                response,
                "spa",
                path="list/[0]/baz"
            )


class ExpectJsonContainsTestCase(TestCase):

    def setUp(self):
        response.text = """{
            "foo": "bar",
            "list": [
                {
                    "baz": "spam",
                    "second": "item"
                },
                1,
                "qwe",
                ["a", "b"]
            ]
        }"""

    def test_fulljson_pass(self):
        expect.expect_json_contains(
            response,
            """{
                "foo": "bar",
                "list": [
                    {"baz": "spam", "second": "item"},
                    1,
                    "qwe",
                    ["a", "b"]
                ]
            }"""
        )

    def test_fulljson_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json_contains(
                response,
                """{
                    "foo": "bar",
                    "list": [
                        {"baz": "spam", "other": "item"},
                        1,
                        "qwe",
                        ["a", "b"]
                    ]
                }"""
            )

    def test_object_in_object_pass(self):
        expect.expect_json_contains(
            response,
            {
                "list":
                [{"baz": "spam", "second": "item"}, 1, "qwe", ["a", "b"]]
            }
        )

    def test_object_in_object_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json_contains(
                response,
                {
                    "list":
                    [{"baz": "spa", "second": "item"}, 1, "qwe", ["a", "b"]]
                }
            )

    def test_object_in_array_pass(self):
        expect.expect_json_contains(
            response,
            {"baz": "spam", "second": "item"},
            path="list"
        )

    def test_object_in_array_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json_contains(
                response,
                {"baz": "spa", "second": "item"},
                path="list"
            )

    def test_array_in_array_pass(self):
        expect.expect_json_contains(
            response,
            ['a', 'b'],
            path="list"
        )

    def test_array_in_array_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json_contains(
                response,
                ['a', 'b', 'c'],
                path="list"
            )

    def test_item_in_array_pass(self):
        expect.expect_json_contains(
            response,
            1,
            path="list"
        )

    def test_item_in_array_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json_contains(
                response,
                2,
                path="list"
            )

    def test_item_pass(self):
        expect.expect_json_contains(
            response,
            "spam",
            path="list/[0]/baz"
        )

    def test_partitem_pass(self):
        expect.expect_json_contains(
            response,
            "spa",
            path="list/[0]/baz"
        )

    def test_item_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json_contains(
                response,
                "span",
                path="list/[0]/baz"
            )


class ExpectJsonNotContainsTestCase(TestCase):

    def setUp(self):
        response.text = """{
            "foo": "bar",
            "list": [
                {
                    "baz": "spam",
                    "second": "item"
                },
                1,
                "qwe",
                ["a", "b"]
            ]
        }"""

    def test_object_in_object_pass(self):
        expect.expect_json_not_contains(
            response,
            {
                "list":
                [{"baz": "spam", "second": "item"}, 1, "qwe", ["a", "c"]]
            }
        )

    def test_object_in_object_fail(self):
        with self.assertRaises(WooperAssertionError):
            expect.expect_json_not_contains(
                response,
                {
                    "list":
                    [{"baz": "spam", "second": "item"}, 1, "qwe", ["a", "b"]]
                }
            )
