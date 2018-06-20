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
    return (exceptions, except_count, decoded_count)

def test_scan_leading_f0_byte():
    low_fb = FourByte(MIN_LEADING,
                      MIN_CONTINUATION,
                      MIN_CONTINUATION,
                      MIN_CONTINUATION)
    invalid_continuation_byte = 0
    total_count = 0
    other_exception_count = 0
    decoded_count = 0
    inval_cont_bytes = {}
    for c1 in range(MIN_CONTINUATION, MAX_CONTINUATION+1):
        for c2 in range(MIN_CONTINUATION, MAX_CONTINUATION+1):
            for c3 in range(MIN_CONTINUATION, MAX_CONTINUATION+1):
                total_count = total_count + 1
                try:
                    temp_fb = FourByte(MIN_LEADING,
                                       c1, c2, c3)
                    decoded = bytes(temp_fb).decode("utf-8")
                    decoded_count = decoded_count + 1
                except UnicodeDecodeError as e:
                    if e.__str__() == ("'utf-8' codec can't decode byte 0xf0 "
                                       "in position 0: invalid continuation "
                                       "byte"):
                        invalid_continuation_byte += 1
                        try:
                            inval_cont_bytes[c1].append((c2,c3))
                        except KeyError:
                            inval_cont_bytes[c1] = [(c2,c3)]
                    else:
                        other_exception_count = other_exception_count + 1
    assert total_count == 2**18
    assert invalid_continuation_byte + \
           other_exception_count + \
           decoded_count == total_count
    assert max(inval_cont_bytes.keys()) == 143
    assert min(inval_cont_bytes.keys()) == 128

MIN_VALID_FOURBYTE = FourByte(MIN_LEADING, 144, 128, 128)
MAX_INVALID_FOURBYTE = FourByte(MIN_LEADING, 143, 191, 191)


def test_min_valid_fb():
    with pytest.raises(UnicodeDecodeError):
        bytes(MAX_INVALID_FOURBYTE).decode()
    bytes(MIN_VALID_FOURBYTE).decode()
