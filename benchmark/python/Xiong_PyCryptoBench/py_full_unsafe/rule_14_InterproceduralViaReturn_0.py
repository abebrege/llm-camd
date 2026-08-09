import ldap


def call_method():

    def starting_method(url):
        l = ldap.initialize(url)
        l.simple_bind_s("", "")

    return starting_method


call_method()("ldap://my_ldap_server.my_domain")
