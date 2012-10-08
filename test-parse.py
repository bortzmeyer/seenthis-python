#!/usr/bin/env python

from FeedParserPlus import FeedParserPlus
import sys

for atom in sys.argv[1:]:
    atom_feed = FeedParserPlus.parse(open(atom).read())
    #print atom_feed.serialize()
    

