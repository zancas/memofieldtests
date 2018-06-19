from collections import namedtuple

FourByte = namedtuple('FourByte', ('leading',
                                   'continuation1',
                                   'continuation2',
                                   'continuation3'))


def test_hello_world():
    print("Hello world!")


def test_utf8_bounds():
    fb = FourByte(4, 191, 191, 191)
    print(fb)
    print(fb.continuation1)
    
