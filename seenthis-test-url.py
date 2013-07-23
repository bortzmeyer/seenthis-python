#!/usr/bin/env python

import SeenThis
import sys
import getopt

BASE_URL = "http://seenthis.net/messages"

# Default values
display_missing = False
display_messages = False

def usage():
    print >>sys.stderr, ("Usage: %s [-n] [-m] url ..." % sys.argv[0])
    
try:
    st = SeenThis.Connection()
except SeenThis.CredentialsNotFound as e:
    print 'Credentials not found at %s, using alternate login.' % e
    credentials = raw_input('Login? '), raw_input('Password? ')
    st = SeenThis.Connection(credentials)

try:
    optlist, args = getopt.getopt (sys.argv[1:], "nmh",
                               ["not-found", "messages", "help"])
    for option, value in optlist:
        if option == "--help" or option == "-h":
            usage()
            sys.exit(0)
        elif option == "--not-found" or option == "-n":
            display_missing = True
        elif option == "--messages" or option == "-m":
            display_messages = True
        else:
            # Should never occur, it is trapped by getopt
            print >>sys.stderr, "Unknown option %s" % option
            usage()
            sys.exit(1)
except getopt.error, reason:
    usage(reason)
    sys.exit(1)
if len(args) <= 0:
    usage()
    sys.exit(1)

for url in args:
    result = st.url_exists(url)
    if display_missing:
        if not result["found"]:
            print url
    else:
        if result["found"]:
            if display_messages:
                the_messages = ": %s" % map(lambda num: "%s/%s" % (BASE_URL, num),
                                       result["messages"])
            else:
                the_messages = ""
            print "%s (%i)%s" % (url, len(result["messages"]), the_messages)
