import re

line = "A second sample string to look"
re.search(r'(.*) To (.*?) .*', line, re.M | re.I)
