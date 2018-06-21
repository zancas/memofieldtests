# https://tools.ietf.org/html/rfc3629
# https://github.com/zcash/zcash/issues/1849
# https://github.com/zcash/zips/pull/105
# NOTE: Test overlong sequences (e.g. C0 80 and D0 80 80)
# What about BOMs?
# What about 5- and 6-byte sequences? e.g. leading: 1111110x ?
# What about The Same Thing encodings (e.g. against z-board.net)?
"""From rfc3629:
   Now the "Korean mess" (ISO/IEC 10646 amendment 5) is an incompatible
   change, in principle contradicting the appropriateness of a version
   independent MIME charset label as described above.  But the
   compatibility problem can only appear with data containing Korean
   Hangul characters encoded according to Unicode 1.1 (or equivalently
   ISO/IEC 10646 before amendment 5), and there is arguably no such data
   to worry about, this being the very reason the incompatible change
   was deemed acceptable.

I wonder if there're interesting tests to write here!"""
import pytest 
from collections import namedtuple

FourByte = namedtuple('FourByte', ('leading',
                                   'continuation1',
                                   'continuation2',
                                   'continuation3'))


MAX_CONTINUATION = 191
MIN_CONTINUATION = 128
MAX_LEADING = 247
MIN_LEADING = 240

def _scan_range(minfb, maxfb):
    total_scans = 0
    scan_summary = {"decoded_fbs": [], "exception_fbs": {}}
    for l in range(minfb.leading, maxfb.leading + 1):
        for c1 in range(minfb.continuation1, maxfb.continuation1 + 1):
            for c2 in range(minfb.continuation2, maxfb.continuation2 + 1):
                for c3 in range(minfb.continuation3, maxfb.continuation3 + 1):
                    total_scans += 1
                    try:
                        current_fb = FourByte(l, c1, c2, c3)
                        decoded = bytes(current_fb).decode("utf-8")
                        scan_summary["decoded_fbs"].append(current_fb)
                    except UnicodeDecodeError as e:
                        if e.__str__() in scan_summary["exception_fbs"]:
                            scan_summary["exception_fbs"][e.__str__()]\
                                .append(current_fb)
                        else:
                            scan_summary["exception_fbs"][e.__str__()] =\
                                [current_fb]
    
    return total_scans, scan_summary


def test_scan_leading_f0_byte_range():
    minfb = FourByte(MIN_LEADING,
                     MIN_CONTINUATION,
                     MIN_CONTINUATION,
                     MIN_CONTINUATION)
    maxfb = FourByte(MIN_LEADING,
                     MAX_CONTINUATION,
                     MAX_CONTINUATION,
                     MAX_CONTINUATION)
    total_scans, scan_summary = _scan_range(minfb, maxfb)
    assert min(scan_summary["decoded_fbs"]) == FourByte(leading=240,
                                                        continuation1=144,
                                                        continuation2=128,
                                                        continuation3=128)
    assert max(scan_summary["decoded_fbs"]) == FourByte(leading=240,
                                                        continuation1=191,
                                                        continuation2=191,
                                                        continuation3=191)
    EXPECTED_EXCEPTION_MESSAGE = "'utf-8' codec can't decode byte 0xf0 in " +\
                                 "position 0: invalid continuation byte"
    EXPECTED_EXCEPTION_MESSAGES = [EXPECTED_EXCEPTION_MESSAGE]
    OBSERVED_EXCEPTION_MESSAGES =\
        [x for x in scan_summary["exception_fbs"].keys()]
    assert total_scans == 2**18
    assert EXPECTED_EXCEPTION_MESSAGES == OBSERVED_EXCEPTION_MESSAGES
    undecodedfbs = scan_summary["exception_fbs"][EXPECTED_EXCEPTION_MESSAGE]
    assert min(undecodedfbs) == FourByte(leading=240,
                                         continuation1=128,
                                         continuation2=128,
                                         continuation3=128)
    assert max(undecodedfbs) == FourByte(leading=240,
                                         continuation1=143,
                                         continuation2=191,
                                         continuation3=191)


def test_scan_leading_f1_to_f3_byte_range():
    for increment in range(1,4):
        minfb = FourByte(MIN_LEADING+increment,
                         MIN_CONTINUATION,
                         MIN_CONTINUATION,
                         MIN_CONTINUATION)
        maxfb = FourByte(MIN_LEADING+increment,
                         MAX_CONTINUATION,
                         MAX_CONTINUATION,
                         MAX_CONTINUATION)
        total_scans, scan_summary = _scan_range(minfb, maxfb)
        assert total_scans == 2**18
        assert len(scan_summary["decoded_fbs"]) == total_scans
        assert scan_summary["exception_fbs"] == {}


def test_scan_leading_f4_byte_range():
    minfb = FourByte(MIN_LEADING+4,
                     MIN_CONTINUATION,
                     MIN_CONTINUATION,
                     MIN_CONTINUATION)
    maxfb = FourByte(MIN_LEADING+4,
                     MAX_CONTINUATION,
                     MAX_CONTINUATION,
                     MAX_CONTINUATION)
    total_scans, scan_summary = _scan_range(minfb, maxfb)
    assert total_scans == 2**18
    assert min(scan_summary["decoded_fbs"]) == FourByte(leading=244,
                                                        continuation1=128,
                                                        continuation2=128,
                                                        continuation3=128)
    assert max(scan_summary["decoded_fbs"]) == FourByte(leading=244,
                                                        continuation1=143,
                                                        continuation2=191,
                                                        continuation3=191)
    OBSERVED_EXCEPTION_MESSAGES =\
        [x for x in scan_summary["exception_fbs"].keys()]
    EXPECTED_EXCEPTION_MESSAGE = "'utf-8' codec can't decode byte 0xf4 in " +\
                                 "position 0: invalid continuation byte"
    EXPECTED_EXCEPTION_MESSAGES = [EXPECTED_EXCEPTION_MESSAGE]
    assert EXPECTED_EXCEPTION_MESSAGES == OBSERVED_EXCEPTION_MESSAGES
    undecodedfbs = scan_summary["exception_fbs"][EXPECTED_EXCEPTION_MESSAGE]
    assert min(undecodedfbs) == FourByte(leading=244,
                                         continuation1=144,
                                         continuation2=128,
                                         continuation3=128)
    assert max(undecodedfbs) == FourByte(leading=244,
                                         continuation1=191,
                                         continuation2=191,
                                         continuation3=191)


def test_scan_leading_f5_to_f7_byte_range():
    for increment in range(5,8):
        minfb = FourByte(MIN_LEADING+increment,
                         MIN_CONTINUATION,
                         MIN_CONTINUATION,
                         MIN_CONTINUATION)
        maxfb = FourByte(MIN_LEADING+increment,
                         MAX_CONTINUATION,
                         MAX_CONTINUATION,
                         MAX_CONTINUATION)
        total_scans, scan_summary = _scan_range(minfb, maxfb)
        assert total_scans == 2**18
        OBSERVED_EXCEPTION_MESSAGES =\
            [x for x in scan_summary["exception_fbs"].keys()]
        EXPECTED_EXCEPTION_MESSAGE = "'utf-8' codec can't decode byte " +\
                                     f"0xf{increment} in position 0: " +\
                                     "invalid start byte"
        EXPECTED_EXCEPTION_MESSAGES = [EXPECTED_EXCEPTION_MESSAGE]
        assert EXPECTED_EXCEPTION_MESSAGES == OBSERVED_EXCEPTION_MESSAGES

        undecodedfbs =\
            scan_summary["exception_fbs"][EXPECTED_EXCEPTION_MESSAGE]
        assert min(undecodedfbs) == FourByte(leading=MIN_LEADING+increment,
                                             continuation1=128,
                                             continuation2=128,
                                             continuation3=128)
        assert max(undecodedfbs) == FourByte(leading=MIN_LEADING+increment,
                                             continuation1=191,
                                             continuation2=191,
                                             continuation3=191)
