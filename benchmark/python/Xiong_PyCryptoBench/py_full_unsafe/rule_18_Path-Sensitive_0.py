import re
if True:
    if str(input("Accept Path?")).lower() == "yes":
        line = "Sample String To Search For"
        re.search(r'(.*) To (.*?) .*', line, re.M | re.I)
    else:
        print("Didn't accept path")
