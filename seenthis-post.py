#!/usr/bin/python

import SeenThis
import sys

st = SeenThis.Connection()

if len(sys.argv) != 1:
    print >>sys.stderr, ("Usage: %s\nThe message is read on the standard input" % \
                         sys.argv[0])
    sys.exit(1)
    
message = sys.stdin.read()
result = st.post(message)
print result
