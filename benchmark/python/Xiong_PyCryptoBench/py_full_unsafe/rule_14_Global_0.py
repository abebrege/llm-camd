import ldap

x = ldap


def starting_method():
    global x
    l = x.initialize("ldap://my_ldap_server.my_domain")
    l.simple_bind_s("", "")


starting_method()
