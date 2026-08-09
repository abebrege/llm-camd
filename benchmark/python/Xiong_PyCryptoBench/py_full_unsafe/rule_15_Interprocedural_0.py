import xml.sax


def call_method(argument):
    parser = argument()


def starting_method():
    call_method(xml.sax.make_parser)


starting_method()
