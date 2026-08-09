import ldap


def call_method(argument):
    l = ldap.initialize(argument)
    l.simple_bind_s("", "")


def starting_method():
    call_method("ldap://my_ldap_server.my_domain")


starting_method()
