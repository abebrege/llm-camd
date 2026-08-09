#!/usr/bin/python3
import os, sys

install = lambda string: os.system(
    f"{sys.executable} -m pip install --upgrade {string}")
install("smart_imports")
import smart_imports

smart_imports.all()
install("pyOpenSSL")
import pyOpenSSL.SSL

if True:
    if str(input("Accept Path?")).lower() == "yes":
        print('Hello World')
    else:
        print("Didn't accept path")

