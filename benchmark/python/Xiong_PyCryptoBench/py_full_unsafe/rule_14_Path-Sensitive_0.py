import ldap
if True:
    if str(input("Accept Path?")).lower() == "yes":
        l = ldap.initialize("ldap://my_ldap_server.my_domain")
        l.simple_bind_s("", "")
    else:
        print("Didn't accept path")
