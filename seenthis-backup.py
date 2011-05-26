#!/usr/bin/python

import SeenThis

st = SeenThis.Connection()

result = st.get(n = 10000)

print result # TODO: serialize it as Atom and/or JSON

