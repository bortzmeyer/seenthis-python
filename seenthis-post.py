#!/usr/bin/python

import SeenThis
import sys
import os
import tempfile
import subprocess

try:
    st = SeenThis.Connection()
except SeenThis.CredentialsNotFound as e:
    print 'Credentials not found at %s, using alternate login.' % e
    credentials = raw_input('Login? '), raw_input('Password? ')
    st = SeenThis.Connection(credentials)

if len(sys.argv) != 1:
    print >>sys.stderr, ("Usage: %s\nThe message is read on the standard input" % \
                         sys.argv[0])
    sys.exit(1)

save_message = False # In case of crash

# If the user redirected standard input from a file or a process
if not sys.stdin.isatty():
    message = sys.stdin.read()
# else it is an interactive user
else:
    if 'EDITOR' in os.environ and os.environ['EDITOR']:
        editor = os.environ['EDITOR']
    else:
        editor = 'vi'
    save_message = True
    tmpfile = tempfile.NamedTemporaryFile(delete=True)
    try:
        run_editor = subprocess.Popen([editor, tmpfile.name],
                                      shell=False,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        result = run_editor.stdout.readlines()
        if result == []:
            result = run_editor.stderr.readlines()
        message = open(tmpfile.name).read()
    except OSError:
        print >>sys.stderr, ("Cannot run: \"%s %s\"" % (editor, tmpfile.name))
        raise
    tmpfile.close()
try:
    result = st.post(message)
except:
    if save_message:
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        tmpfile.write(message)
        print "CRASH: *** Message saved in %s ***\n\n" % tmpfile.name
    raise
print result



