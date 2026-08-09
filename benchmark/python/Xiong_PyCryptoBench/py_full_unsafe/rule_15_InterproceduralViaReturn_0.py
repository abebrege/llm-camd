import xml.sax


def call_method():

    def starting_method():
        xml.sax.make_parser()

    return starting_method


call_method()()
