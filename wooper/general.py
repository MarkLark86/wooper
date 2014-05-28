import json
from pprint import pformat


failureException = AssertionError


def fail(msg=None):
    """Fail immediately, with the given message."""
    raise failureException(msg)


def fail_and_print_body(context, msg):
    fail(
        """{msg}
Response body:
\"\"\"
{body}
\"\"\"
"""
        .format(body=context.response.text, msg=msg))


def apply_path(json_dict, path):
    if not path:
        return json_dict
    path_elements = path.split('/')
    for element in path_elements:
        if element.startswith('['):
            try:
                element = int(element.lstrip('[').rstrip(']'))
            except ValueError as e:
                fail("Path can't be applied: {exception}."
                     .format(exception=e.args))
        try:
            json_dict = json_dict[element]
        except (IndexError, TypeError, KeyError):
            fail(
                """Path can't be applied:
no such index '{index}' in \"\"\"{dict}\"\"\"."""
                .format(index=element, dict=pformat(json_dict)))
    return json_dict


def parse_json_input(json_dict):
    if isinstance(json_dict, str) \
       and ('{' in json_dict or '[' in json_dict):
        try:
            return json.loads(json_dict)
        except ValueError:
            fail('You have provided not a valid JSON.')
    else:
        return json_dict


def parse_json_response(context):
    try:
        return json.loads(context.response.text)
    except ValueError:
        fail_and_print_body(context, 'Response in not a valid JSON.')
