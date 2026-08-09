import ldap


def call_method(argument):
    l = argument.initialize("ldap://my_ldap_server.my_domain")
    l.simple_bind_s("", "")


def starting_method():
    call_method(ldap)


starting_method()
