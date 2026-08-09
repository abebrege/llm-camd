import ldap

x = "ldap://my_ldap_server.my_domain"


def starting_method():
    global x
    l = ldap.initialize(x)
    l.simple_bind_s("", "")


starting_method()
