import re

line = "Sample String To Search For"
re.search(r'(.*) To (.*?) .*', line, re.M | re.I)
