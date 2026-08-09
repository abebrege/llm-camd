import xml.sax

x = xml.sax.make_parser


def starting_method():
    global x
    parser = x()


starting_method()
