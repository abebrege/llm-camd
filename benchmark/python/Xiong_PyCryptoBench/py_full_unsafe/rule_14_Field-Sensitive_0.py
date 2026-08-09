import ldap


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("ldap://my_ldap_server.my_domain")
l = ldap.initialize(runner_object.argument)
l.simple_bind_s("", "")
