import xml.sax
if True:
    if str(input("Accept Path?")).lower() == "yes":
        parser = xml.sax.make_parser()
    else:
        print("Didn't accept path")
