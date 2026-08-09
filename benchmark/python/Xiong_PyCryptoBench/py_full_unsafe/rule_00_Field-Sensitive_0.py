import random


class BaseRunner(object):

    def __init__(self):
        self.argument = random.randint


runner_object = BaseRunner()
print(runner_object.argument(0, 25))
