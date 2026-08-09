import random

x = random.randint


def starting_method():
    global x
    print(x(0, 25))


starting_method()
