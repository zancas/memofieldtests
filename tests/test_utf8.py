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

def search_fourbyte(four_byte):
    return (max_valid, min_invalid)
    
def _search_leading(four_byte):
    
    return (max_valid, min_invalid)

def _search_continuation(four_byte):
    return (max_valid, min_invalid)


def test_search__leading():
    temp_l = MIN_LEADING - 1
    while temp_l <= MAX_LEADING: 
        temp_l = temp_l + 1
        low_fb = FourByte(temp_l,
                          MIN_CONTINUATION,
                          MIN_CONTINUATION,
                          MIN_CONTINUATION)
        try:
            print(bytes(low_fb).decode("utf-8"))    
        except UnicodeDecodeError as e:
            print(e.__str__())
            break


def test_scan_leading_f0_byte():
    low_fb = FourByte(MIN_LEADING,
                      MIN_CONTINUATION,
                      MIN_CONTINUATION,
                      MIN_CONTINUATION)
    cant_decode_count = 0
    total_count = 0
    other_exception_count = 0
    decoded_count = 0
    undecodeables = {}
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
                    if e.__str__() == "'utf-8' codec can't decode byte 0xf0 in position 0: invalid continuation byte":
                        cant_decode_count = cant_decode_count + 1
                        try:
                            undecodeables[c1].append((c2,c3))
                        except KeyError:
                            undecodeables[c1] = [(c2,c3)]
                    else:
                        other_exception_count = other_exception_count + 1
    print("cant_decode_count: ", cant_decode_count)
    print("total_count is: ", total_count)
    print("other_exception_count is: ", other_exception_count)
    print("decoded_count is: ", decoded_count)
    from pprint import pprint as pp
    pp(len(undecodeables))
    pp(undecodeables.keys())
    assert max(undecodeables.keys()) == 143
    assert min(undecodeables.keys()) == 128


def itest_utf8_bounds():
    valid_fb = FourByte(241, 128, 128, 128)
    print(bytes(valid_fb).decode("utf-8"))
    print(VALID_FOURBYTE)
    print(type(VALID_FOURBYTE))
    print(VALID_FOURBYTE.decode())
