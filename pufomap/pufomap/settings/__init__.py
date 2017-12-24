import sys

try:
    from .local import *
    print("Using local settings...", file=sys.stderr)
except ImportError:
    from .common import *
    print("Using common settings...", file=sys.stderr)

