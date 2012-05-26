#!/usr/bin/env python

import SeenThis
import sys
import getopt

def usage():
    # TODO: allows several message ID (which implies a way to store
    # each of the results in a file)
    print >>sys.stderr, ("Usage: %s message-ID" % sys.argv[0])
    
try:
    st = SeenThis.Connection()
except SeenThis.CredentialsNotFound as e:
    print 'Credentials not found at %s, using alternate login.' % e
    credentials = raw_input('Login? '), raw_input('Password? ')
    st = SeenThis.Connection(credentials)

try:
    optlist, args = getopt.getopt (sys.argv[1:], "h",
                               ["help"])
    for option, value in optlist:
        if option == "--help" or option == "-h":
            usage()
            sys.exit(0)
        else:
            # Should never occur, it is trapped by getopt
            print >>sys.stderr, "Unknown option %s" % option
            usage()
            sys.exit(1)
except getopt.error, reason:
    usage(reason)
    sys.exit(1)
if len(args) != 1:
    usage()
    sys.exit(1)

try:
    msg_id = args[0]
    result = st.get_message(msg_id)
    # TODO: allows to print only the summary, which is the original
    # source of the seen?
    print result.serialize()
except SeenThis.NotFound:
    print >>sys.stderr, ("Message %s does not exist, it seems" % msg_id)


