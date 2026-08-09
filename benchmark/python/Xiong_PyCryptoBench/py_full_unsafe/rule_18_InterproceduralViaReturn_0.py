import re


def call_method(argument):

    def starting_method(second_argument, third_argument):
        argument(second_argument, third_argument)

    return starting_method


call_method(re.search)(r'(.*) To (.*?) .*', "Sample String To Search For")
