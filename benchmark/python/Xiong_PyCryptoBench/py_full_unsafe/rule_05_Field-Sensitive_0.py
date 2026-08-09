import random


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(0)
print(random.randint(0, runner_object.argument))
