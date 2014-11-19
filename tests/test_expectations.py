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
