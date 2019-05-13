# Testing that a single Tracer can handle many mixed uses
import pysnooper

snoop = pysnooper.snoop()


def foo(x):
    if x == 0:
        bar1(x)
        qux()
        return

    with snoop:
        # There should be line entries for these three lines,
        # no line entries for anything else in this function,
        # but calls to all bar functions should be traced
        foo(x - 1)
        bar2(x)
        qux()
    int(4)
    bar3(9)
    return x


@snoop
def bar1(_x):
    qux()


@snoop
def bar2(_x):
    qux()


@snoop
def bar3(_x):
    qux()


def qux():
    return 9  # not traced, mustn't show up


def main():
    foo(2)


expected_output = """
New var:....... x = 2
12:34:56.789012 line        17         foo(x - 1)
New var:....... x = 1
12:34:56.789012 line        17         foo(x - 1)
Starting var:.. _x = 0
12:34:56.789012 call        26 def bar1(_x):
12:34:56.789012 line        27     qux()
12:34:56.789012 return      27     qux()
Return value:.. None
12:34:56.789012 line        18         bar2(x)
Starting var:.. _x = 1
12:34:56.789012 call        31 def bar2(_x):
12:34:56.789012 line        32     qux()
12:34:56.789012 return      32     qux()
Return value:.. None
12:34:56.789012 line        19         qux()
Starting var:.. _x = 9
12:34:56.789012 call        36 def bar3(_x):
12:34:56.789012 line        37     qux()
12:34:56.789012 return      37     qux()
Return value:.. None
12:34:56.789012 line        18         bar2(x)
Starting var:.. _x = 2
12:34:56.789012 call        31 def bar2(_x):
12:34:56.789012 line        32     qux()
12:34:56.789012 return      32     qux()
Return value:.. None
12:34:56.789012 line        19         qux()
Starting var:.. _x = 9
12:34:56.789012 call        36 def bar3(_x):
12:34:56.789012 line        37     qux()
12:34:56.789012 return      37     qux()
Return value:.. None
"""