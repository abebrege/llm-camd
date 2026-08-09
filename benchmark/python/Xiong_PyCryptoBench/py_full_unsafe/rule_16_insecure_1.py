from yaml import load, dump_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

dump_all("""
---
 sample: "sample here"
""",
         stream=None,
         Dumper=Dumper,
         default_style=None,
         default_flow_style=False,
         canonical=None,
         indent=None,
         width=None,
         allow_unicode=None,
         line_break=None,
         encoding=None,
         explicit_start=None,
         explicit_end=None,
         version=None,
         tags=None,
         sort_keys=True)
