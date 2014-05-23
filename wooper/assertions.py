import difflib
import pprint

from .general import fail


failureException = AssertionError
_diffThreshold = 2**16
_maxDiff = None
DIFF_OMITTED = ('\nDiff is %s characters long. '
                'Set self.maxDiff to None to see it.')
_MAX_LENGTH = 80
_PLACEHOLDER_LEN = 12
_MIN_BEGIN_LEN = 5
_MIN_END_LEN = 5
_MIN_COMMON_LEN = 5
_MIN_DIFF_LEN = _MAX_LENGTH - \
    (_MIN_BEGIN_LEN + _PLACEHOLDER_LEN + _MIN_COMMON_LEN +
     _PLACEHOLDER_LEN + _MIN_END_LEN)


def _shorten(s, prefixlen, suffixlen):
    skip = len(s) - prefixlen - suffixlen
    if skip > _PLACEHOLDER_LEN:
        s = '%s[%d chars]%s' % (s[:prefixlen], skip, s[len(s) - suffixlen:])
    return s


def commonprefix(m):
    "Given a list of pathnames, returns the longest common leading component"
    if not m: return ''
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1


def _common_shorten_repr(*args):
    args = tuple(map(safe_repr, args))
    maxlen = max(map(len, args))
    if maxlen <= _MAX_LENGTH:
        return args

    prefix = commonprefix(args)
    prefixlen = len(prefix)

    common_len = _MAX_LENGTH - \
                 (maxlen - prefixlen + _MIN_BEGIN_LEN + _PLACEHOLDER_LEN)
    if common_len > _MIN_COMMON_LEN:
        assert _MIN_BEGIN_LEN + _PLACEHOLDER_LEN + _MIN_COMMON_LEN + \
               (maxlen - prefixlen) < _MAX_LENGTH
        prefix = _shorten(prefix, _MIN_BEGIN_LEN, common_len)
        return tuple(prefix + s[prefixlen:] for s in args)

    prefix = _shorten(prefix, _MIN_BEGIN_LEN, _MIN_COMMON_LEN)
    return tuple(prefix + _shorten(s[prefixlen:], _MIN_DIFF_LEN, _MIN_END_LEN)
                 for s in args)

def safe_repr(obj, short=False):
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    if not short or len(result) < _MAX_LENGTH:
        return result
    return result[:_MAX_LENGTH] + ' [truncated]...'

def _truncateMessage(message, diff):
    max_diff = _maxDiff
    if max_diff is None or len(diff) <= max_diff:
        return message + diff
    return message + (DIFF_OMITTED % len(diff))


def _formatMessage(msg, std_msg):
    """Honour the longMessage attribute when generating failure messages.
    If longMessage is False this means:
    * Use only an explicit message if it is provided
    * Otherwise use the standard message for the assert

    If longMessage is True:
    * Use the standard message
    * If an explicit message is provided, plus ' : ' and the explicit message
    """
    if msg is None:
        return std_msg
    try:
        # don't switch to '{}' formatting in Python 2.X
        # it changes the way unicode input is handled
        return '%s : %s' % (std_msg, msg)
    except UnicodeDecodeError:
        return '%s : %s' % (safe_repr(std_msg), safe_repr(msg))


def _baseAssertEqual(first, second, msg=None):
    """The default assertEqual implementation, not type specific."""
    if not first == second:
        std_msg = '%s != %s' % _common_shorten_repr(first, second)
        msg = _formatMessage(msg, std_msg)
        fail(msg)


def _getAssertEqualityFunc(first, second):
    """Get a detailed comparison function for the types of the two args.

    Returns: A callable accepting (first, second, msg=None) that will
    raise a failure exception if first != second with a useful human
    readable error message for those types.
    """
    if type(first) is type(second):
        asserter = _type_equality_funcs.get(type(first))
        if asserter is not None:
            return asserter

    return _baseAssertEqual


def assert_sequence_equal(seq1, seq2, msg=None, seq_type=None):
    """An equality assertion for ordered sequences (like lists and tuples).

    For the purposes of this function, a valid ordered sequence type is one
    which can be indexed, has a length, and has an equality operator.

    Args:
        seq1: The first sequence to compare.
        seq2: The second sequence to compare.
        seq_type: The expected datatype of the sequences, or None if no
                datatype should be enforced.
        msg: Optional message to use on failure instead of a list of
                differences.
    """
    if seq_type is not None:
        seq_type_name = seq_type.__name__
        if not isinstance(seq1, seq_type):
            fail('First sequence is not a %s: %s'
                 % (seq_type_name, safe_repr(seq1)))
        if not isinstance(seq2, seq_type):
            fail('Second sequence is not a %s: %s'
                 % (seq_type_name, safe_repr(seq2)))
    else:
        seq_type_name = "sequence"

    differing = None
    try:
        len1 = len(seq1)
    except (TypeError, NotImplementedError):
        differing = 'First %s has no length.    Non-sequence?'\
                    % (seq_type_name)

    if differing is None:
        try:
            len2 = len(seq2)
        except (TypeError, NotImplementedError):
            differing = 'Second %s has no length.    Non-sequence?'\
                        % (seq_type_name)

    if differing is None:
        if seq1 == seq2:
            return

        differing = '%ss differ: %s != %s\n'\
                    % (
            (seq_type_name.capitalize(),) + _common_shorten_repr(seq1, seq2))

        for i in range(min(len1, len2)):
            try:
                item1 = seq1[i]
            except (TypeError, IndexError, NotImplementedError):
                differing += ('\nUnable to index element %d of first %s\n' %
                             (i, seq_type_name))
                break

            try:
                item2 = seq2[i]
            except (TypeError, IndexError, NotImplementedError):
                differing += ('\nUnable to index element %d of second %s\n' %
                             (i, seq_type_name))
                break

            if item1 != item2:
                differing += ('\nFirst differing element %d:\n%s\n%s\n' %
                             (i, item1, item2))
                break
        else:
            if (len1 == len2 and seq_type is None and
                type(seq1) != type(seq2)):
                # The sequences are the same, but have differing types.
                return

        if len1 > len2:
            differing += ('\nFirst %s contains %d additional '
                         'elements.\n' % (seq_type_name, len1 - len2))
            try:
                differing += ('First extra element %d:\n%s\n' %
                              (len2, seq1[len2]))
            except (TypeError, IndexError, NotImplementedError):
                differing += ('Unable to index element %d '
                              'of first %s\n' % (len2, seq_type_name))
        elif len1 < len2:
            differing += ('\nSecond %s contains %d additional '
                         'elements.\n' % (seq_type_name, len2 - len1))
            try:
                differing += ('First extra element %d:\n%s\n' %
                              (len1, seq2[len1]))
            except (TypeError, IndexError, NotImplementedError):
                differing += ('Unable to index element %d '
                              'of second %s\n' % (len1, seq_type_name))
    standardMsg = differing
    diffMsg = '\n' + '\n'.join(
        difflib.ndiff(pprint.pformat(seq1).splitlines(),
                      pprint.pformat(seq2).splitlines()))

    standardMsg = _truncateMessage(standardMsg, diffMsg)
    msg = _formatMessage(msg, standardMsg)
    fail(msg)

#######################################################################


def assert_dict_equal(d1, d2, msg=None):
    assert_is_instance(d1, dict, 'First argument is not a dictionary')
    assert_is_instance(d2, dict, 'Second argument is not a dictionary')

    if d1 != d2:
        standardMsg = '%s != %s' % _common_shorten_repr(d1, d2)
        diff = ('\n' + '\n'.join(difflib.ndiff(
                       pprint.pformat(d1).splitlines(),
                       pprint.pformat(d2).splitlines())))
        standardMsg = _truncateMessage(standardMsg, diff)
        fail(_formatMessage(msg, standardMsg))


def assert_tuple_equal(tuple1, tuple2, msg=None):
    """A tuple-specific equality assertion.
    Args:
        tuple1: The first tuple to compare.
        tuple2: The second tuple to compare.
        msg: Optional message to use on failure instead of a list of
                differences."""
    assert_sequence_equal(tuple1, tuple2, msg, seq_type=tuple)


def assert_list_equal(list1, list2, msg=None):
    """A list-specific equality assertion.
    Args:
        list1: The first list to compare.
        list2: The second list to compare.
        msg: Optional message to use on failure instead of a list of
                differences."""
    assert_sequence_equal(list1, list2, msg, seq_type=list)


def assert_is_instance(obj, cls, msg=None):
    """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
    default message."""
    if not isinstance(obj, cls):
        standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
        fail(_formatMessage(msg, standardMsg))


def assert_multiline_equal(first, second, msg=None):
    """Assert that two multi-line strings are equal."""
    assert_is_instance(first, str, 'First argument is not a string')
    assert_is_instance(second, str, 'Second argument is not a string')

    if first != second:
        # don't use difflib if the strings are too long
        if (len(first) > _diffThreshold or
            len(second) > _diffThreshold):
            _baseAssertEqual(first, second, msg)
        firstlines = first.splitlines(keepends=True)
        secondlines = second.splitlines(keepends=True)
        if len(firstlines) == 1 and first.strip('\r\n') == first:
            firstlines = [first + '\n']
            secondlines = [second + '\n']
        standardMsg = '%s != %s' % _common_shorten_repr(first, second)
        diff = '\n' + ''.join(difflib.ndiff(firstlines, secondlines))
        standardMsg = _truncateMessage(standardMsg, diff)
        fail(_formatMessage(msg, standardMsg))


def assert_in(member, container, msg=None):
    """Just like self.assertTrue(a in b), but with a nicer default message."""
    if member not in container:
        std_msg = '%s not found in %s' % (
            safe_repr(member), safe_repr(container))
        fail(_formatMessage(msg, std_msg))


def assert_not_in(self, member, container, msg=None):
    """Just like self.assertTrue(a not in b), but with a nicer default message.
    """
    if member in container:
        standardMsg = '%s unexpectedly found in %s' % (safe_repr(member),
                                                       safe_repr(container))
        fail(_formatMessage(msg, standardMsg))


_type_equality_funcs = {
    str: assert_multiline_equal,
    list: assert_list_equal,
    dict: assert_dict_equal,
    tuple: assert_tuple_equal,
}
# (set, 'assertSetEqual')
# (frozenset, 'assertSetEqual')


def assert_equal(first, second, msg=None):
    """Fail if the two objects are unequal as determined by the '=='
       operator.
    """
    assertion_func = _getAssertEqualityFunc(first, second)
    assertion_func(first, second, msg=msg)


def assert_not_equal(first, second, msg=None):
    """Fail if the two objects are equal as determined by the '!='
       operator.
    """
    if not first != second:
        msg = _formatMessage(msg, '%s == %s' % (safe_repr(first),
                                                safe_repr(second)))
        raise failureException(msg)
