import ldap


def call_method():

    def starting_method():
        l = ldap.initialize("ldap://my_ldap_server.my_domain")
        l.simple_bind_s("", "")

    return starting_method


call_method()()
