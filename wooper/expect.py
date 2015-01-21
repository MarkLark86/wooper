"""
.. module:: expect
   :synopsis: Expectations

Expectation helper functions are receiving response object as first argument.
These helpers make testing API response bodies and headers easy with minimal
time and effort.

.. moduleauthor:: Yauhen Kirylau <actionless.loveless@gmail.com>

"""


from .assertions import (
    assert_equal, assert_not_equal,
    assert_in, assert_not_in)
from .general import (
    parse_json_input, parse_json_response, apply_path, get_body,
    assert_and_print_body)


def expect_status(response, code):
    assert_and_print_body(
        response,
        assert_equal,
        code, response.status_code,
        "Status code not matches.")


def expect_status_in(response, codes):
    assert_and_print_body(
        response,
        assert_in,
        response.status_code, codes,
        "Status code not matches.")


def expect_json(response, json_input, path=None):
    """
    checks if json response equals some json,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_input = parse_json_input(json_input)
    json_response = apply_path(parse_json_response(response), path)
    assert_equal(json_input, json_response, "JSON not matches")


def expect_json_contains(response, json_input, path=None,
                         reverse_expectation=False):
    """
    checks if json response contains some json subset,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    assert_item = assert_equal
    assert_sequence = assert_in
    message = "JSON response does not contain such value"
    if reverse_expectation:
        assert_item = assert_not_equal
        assert_sequence = assert_not_in
        message = "JSON response contains such value"

    json_input = parse_json_input(json_input)
    json_response = apply_path(parse_json_response(response), path)

    if isinstance(json_input, dict) and isinstance(json_response, dict):
        for key in json_input.keys():
            assert_and_print_body(
                response,
                assert_item,
                json_input[key], json_response[key],
                message)
    else:
        assert_sequence(json_input, json_response, message)


def expect_json_not_contains(response, json_input, path=None):
    """
    checks if json response not contains some json subset,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    return expect_json_contains(response, json_input, path,
                                reverse_expectation=True)


def expect_headers_contain(response, header):
    assert_in(header,
              response.headers,
              "No such header in response.")


def expect_headers(response, headers, partly=False):
    for header, value in headers.items():
        expect_headers_contain(response, header)
        if partly:
            assert_in(value.lower(),
                      response.headers[header].lower(),
                      "Header not matches.")
        else:
            assert_equal(value.lower(),
                         response.headers[header].lower(),
                         "Header not matches.")


def expect_json_length(response, length, path=None):
    """
    checks if count of objects in json response equals provided length,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_response = apply_path(parse_json_response(response), path)
    assert_in(type(json_response), (list, dict),
              "'{}' isn't json.".format(json_response))
    assert_equal(length, len(json_response),
                 "JSON objects count not matches.")


def expect_body_contains(response, text):
    assert_in(text, get_body(response), "Body not contains '{}'.".format(text))
