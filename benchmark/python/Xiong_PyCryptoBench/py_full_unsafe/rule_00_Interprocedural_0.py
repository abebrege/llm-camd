import random


def call_method(argument):
    print(argument(0, 25))


def starting_method():
    call_method(random.randint)


starting_method()
