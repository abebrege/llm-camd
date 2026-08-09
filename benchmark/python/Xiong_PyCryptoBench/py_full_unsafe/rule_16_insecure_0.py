from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

dump("""
---
 doe: "a deer, a female deer"
 ray: "a drop of golden sun"
""",
     stream=None,
     Dumper=Dumper)
