import random


def call_method(argument):
    print(argument.randint(0, 25))


def starting_method():
    call_method(random)


starting_method()
