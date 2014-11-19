from unittest import TestCase
from wooper import expect
from wooper.general import WooperAssertionError
from .common import response


class ExpectationsTestCase(TestCase):

    def test_expect_status_pass(self):
        response.status_code = 200
        expect.expect_status(response, 200)

    def test_expect_status_fail(self):
        response.status_code = 403
        with self.assertRaises(WooperAssertionError):
            expect.expect_status(response, 200)
