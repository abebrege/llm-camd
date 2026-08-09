import random


def call_method():

    def starting_method():
        print(random.randint(0, 25))

    return starting_method


call_method()()
