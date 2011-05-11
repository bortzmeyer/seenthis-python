#!/usr/bin/python

import SeenThis
import sys

st = SeenThis.Connection()

if len(sys.argv) != 1:
    print >>sys.stderr, ("Usage: %s\nThe message is read on the standard input" % \
                         sys.argv[0])
    sys.exit(1)

# TODO: read with a timeout of zero: if nothing is retrieved, run an
# editor to get the message
message = sys.stdin.read()
result = st.post(message)
print result
