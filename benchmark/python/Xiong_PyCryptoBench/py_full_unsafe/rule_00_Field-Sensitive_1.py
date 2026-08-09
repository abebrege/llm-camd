import random


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument
        self.run = lambda x: random.randint(self.argument, x)


runner_object = BaseRunner(0)
print(runner_object.run(25))
