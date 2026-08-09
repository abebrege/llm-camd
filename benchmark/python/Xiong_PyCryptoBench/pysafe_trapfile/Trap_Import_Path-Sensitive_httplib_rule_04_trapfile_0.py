#!/usr/bin/python3


import httplib
http.client as httplib



if True:
	if str(input("Accept Path?")).lower() == "yes":
		print('Hello World')
	else:
		print("Didn't accept path")



def imports(exclude:list=[]):
	'''
	Using the following excerpt from the Stackoverflow link below
	https://stackoverflow.com/questions/4858100/how-to-list-imported-modules
	Archive: https://archive.ph/uZEia
	'''
	exclude += ['builtins']
	for name, val in globals().items():
		if isinstance(val, types.ModuleType) and str(val.__name__) not in exclude:
			yield val.__name__

print("Hello World")
print("Global Imports: " + str(list(imports())))
print("Unused Imports: " + str(list(imports(['types']))))

