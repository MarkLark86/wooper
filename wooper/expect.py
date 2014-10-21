from .assertions import (
    assert_equal, assert_not_equal,
    assert_in, assert_not_in)
from .general import (
    parse_json_input, parse_json_response, apply_path, get_body)


def assert_and_print_body(response, assert_function, first, second, msg):
    body = getattr(response, 'text', None)
    if not body:
        try:
            body = response.data.decode("utf-8")
        except UnicodeDecodeError:
            body = response.data
        except Exception:
            body = '%%%_not_text_%%%'
    assert_function(
        first, second,
        """{message}.
Response body:
\"\"\"
{body}
\"\"\"
"""
        .format(body=body, message=msg))


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


def expect_json_contains(response, json_input, path=None):
    """
    checks if json response contains some json subset,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_input = parse_json_input(json_input)
    json_response = apply_path(parse_json_response(response), path)

    if isinstance(json_input, dict):
        for key in json_input.keys():
            assert_and_print_body(
                response,
                assert_equal,
                json_input[key], json_response[key],
                "JSON not matches.")
    elif isinstance(json_input, int) or isinstance(json_input, str):
        assert_in(
            json_input, json_response,
            "JSON response does not contain such value")
    else:
        raise NotImplementedError("'{}' is not implemented"
                                  .format(type(json_input)))


def expect_json_not_contains(response, json_input, path=None):
    """
    checks if json response contains some json subset,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_input = parse_json_input(json_input)
    json_response = apply_path(parse_json_response(response), path)

    if isinstance(json_input, dict):
        for key in json_input.keys():
            assert_and_print_body(
                response,
                assert_not_equal,
                json_input[key], json_response[key],
                "JSON matches.")
    elif isinstance(json_input, int) or isinstance(json_input, str):
        assert_not_in(
            json_input, json_response,
            "JSON response contains such value")
    else:
        raise NotImplementedError("'{}' is not implemented"
                                  .format(type(json_input)))


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
