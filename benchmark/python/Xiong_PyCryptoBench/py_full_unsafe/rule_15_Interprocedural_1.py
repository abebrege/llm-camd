import xml.sax


def call_method(argument):
    parser = argument.make_parser()


def starting_method():
    call_method(xml.sax)


starting_method()
