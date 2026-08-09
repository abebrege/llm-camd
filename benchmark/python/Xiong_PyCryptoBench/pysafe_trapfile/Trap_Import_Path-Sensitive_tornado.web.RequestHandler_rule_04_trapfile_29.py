#!/usr/bin/python3
import os, sys

install = lambda string: os.system(
    f"{sys.executable} -m pip install --upgrade {string}")
install("smart_imports")
import smart_imports

smart_imports.all()
install("tornado")
import tornado.web.RequestHandler

if True:
    if str(input("Accept Path?")).lower() == "yes":
        print('Hello World')
    else:
        print("Didn't accept path")

