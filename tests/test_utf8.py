import pytest 
from collections import namedtuple

FourByte = namedtuple('FourByte', ('leading',
                                   'continuation1',
                                   'continuation2',
                                   'continuation3'))


VALID_FOURBYTE = '\U0002070e'.encode("utf-8")
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


def test_scan_leading_f1_byte_range():
    minfb = FourByte(MIN_LEADING+1,
                     MIN_CONTINUATION,
                     MIN_CONTINUATION,
                     MIN_CONTINUATION)
    maxfb = FourByte(MIN_LEADING+1,
                     MAX_CONTINUATION,
                     MAX_CONTINUATION,
                     MAX_CONTINUATION)
    total_scans, scan_summary = _scan_range(minfb, maxfb)
