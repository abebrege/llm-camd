import os, sys, ldap

l = ldap.initialize("ldap://my_ldap_server.my_domain")
l.simple_bind_s("", "")
