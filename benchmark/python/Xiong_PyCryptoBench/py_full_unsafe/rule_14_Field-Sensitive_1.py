import ldap


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


l = ldap.initialize("ldap://my_ldap_server.my_domain")
runner_object = BaseRunner(l)
runner_object.simple_bind_s("", "")
