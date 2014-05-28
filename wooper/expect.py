from .assertions import (
    assert_equal, assert_not_equal,
    assert_in, assert_not_in)
from .general import (
    parse_json_input, parse_json_response, apply_path)


def assert_and_print_body(context, assert_function, first, second, msg):
    if not getattr(context.response, 'text', None):
        try:
            context.response.text = context.response.data.decode("utf-8")
        except Exception:
            setattr(context.response, 'text', '%%%_not_text_%%%')
    assert_function(
        first, second,
        """{message}.
Response body:
\"\"\"
{body}
\"\"\"
"""
        .format(body=context.response.text, message=msg))


def expect_status(context, code):
    assert_and_print_body(
        context,
        assert_equal,
        code, context.response.status_code,
        "Status code not matches.")


def expect_status_in(context, codes):
    assert_and_print_body(
        context,
        assert_in,
        context.response.status_code, codes,
        "Status code not matches.")


def expect_json(context, json_input, path=None):
    """
    checks if json response equals some json,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_input = parse_json_input(json_input)
    json_response = apply_path(parse_json_response(context), path)
    assert_equal(json_input, json_response, "JSON not matches")


def expect_json_contains(context, json_input, path=None):
    """
    checks if json response contains some json subset,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_input = parse_json_input(json_input)
    json_response = apply_path(parse_json_response(context), path)

    if isinstance(json_input, dict):
        for key in json_input.keys():
            assert_and_print_body(
                context,
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


def expect_json_not_contains(context, json_input, path=None):
    """
    checks if json response contains some json subset,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_input = parse_json_input(json_input)
    json_response = apply_path(parse_json_response(context), path)

    if isinstance(json_input, dict):
        for key in json_input.keys():
            assert_and_print_body(
                context,
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


def expect_header(context, header, value, partly=False):
    assert_in(header,
              context.response.headers,
              "No such header in response.")
    if partly:
        assert_in(value.lower(),
                  context.response.headers[header].lower(),
                  "Header not matches.")
    else:
        assert_in(value.lower(),
                  context.response.headers[header].lower(),
                  "Header not matches.")


def expect_header_contains(context, header, value):
    expect_header(context, header, value, partly=True)


def expect_json_length(context, length, path=None):
    """
    checks if count of objects in json response equals provided length,
    path separated by slashes, ie 'foo/bar/spam', 'foo/[0]/bar'
    """
    json_response = apply_path(parse_json_response(context), path)
    assert_equal(
        length, len(json_response), "JSON objects count not matches.")


def expect_body_contains(context, body):
    if not getattr(context.response, 'text', None):
        context.response.text = context.response.data.decode("utf-8")
    assert_in(body, context.response.text, "Body not matches.")
