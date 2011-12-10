#!/usr/bin/python

import SeenThis

try:
    st = SeenThis.Connection()
except SeenThis.CredentialsNotFound as e:
    print 'Credentials not found at %s, using alternate login.' % e
    credentials = raw_input('Login? '), raw_input('Password? ')
    st = SeenThis.Connection(credentials)

result = st.get(n = 10000)

print result.serialize() # TODO: serialize to JSON

