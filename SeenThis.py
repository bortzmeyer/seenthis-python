"""
Documentation of the SeenThis API:

http://seenthis.net/fran%C3%A7ais/mentions/article/api
http://seenthis.net/messages/14646
"""

import os
import sys
import urllib2
import locale
import base64

from FeedParserPlus import FeedParserPlus

try:
    from simpletal import simpleTAL, simpleTALES, simpleTALUtils
except ImportError:
    print >>sys.stderr, "I need the module simpleTAL, see <http://www.owlfish.com/software/simpleTAL/>"

__VERSION__ = '0.0'

authfile = "%s/.seenthis/auth" % os.environ['HOME']
create_endpoint = 'https://seenthis.net/api/messages'
retrieve_endpoint_tmpl = 'https://seenthis.net/api/people/%s/messages'
mytemplate = """
<entry xmlns='http://www.w3.org/2005/Atom'
       xmlns:thr='http://purl.org/syndication/thread/1.0'
       xmlns:docs='http://schemas.google.com/docs/2007'>
    <summary tal:content="message"/>
</entry>
"""
myencoding = locale.getpreferredencoding()
if myencoding is None:
    myencoding='UTF-8'
    
class InternalError(Exception):
    pass

class CredentialsNotFound(InternalError):
    pass

class Connection:

    def __init__(self, credentials=None):
        if credentials:
            self.username, self.password = credentials
        else:
            if not os.path.exists(authfile):
                raise CredentialsNotFound(authfile)
            auth = open(authfile)
            self.username = auth.readline()[:-1]
            self.password = auth.readline()[:-1]
        self.retrieve_endpoint = retrieve_endpoint_tmpl % self.username
        self.template = simpleTAL.compileXMLTemplate(mytemplate)
        
    def _add_headers(self, r, post=False):
        credentials = base64.b64encode('%s:%s' % (self.username, self.password))
        r.add_header('User-agent', 'SeenThis-package/%s Python/%s' % \
                     (__VERSION__, sys.version.split()[0]))
        r.add_header('Authorization', 'Basic %s' % credentials)
        if post:
            r.add_header('Content-Type', 'application/atom+xml;type=entry')

    # TODO: how to retrieve one message? An ID parameter?
    def get(self, n=None):
        """
        n is the number of messages to retrieve. When None, we just retrieve what
        SeenThis gives us (today, the last 25 messages). Otherwise, we
        loop to retrieve n messages. Warning: because there may be
        less messages on SeenThis, there is no guarantee to have n
        entries in the result.

        To get all the messages, just set n to a very high number.

        The result is a FeedParserPlus object (which inherits from
        traditional FeedparserDict).
        """
        total = 0
        over = False
        result = None
        step = 0
        while not over:
            # TODO: we could use feedparser to retrieve the feed, not
            # only to parse it...
            if step == 0:
                endpoint = self.retrieve_endpoint
            else:
                endpoint = "%s/%i" % (self.retrieve_endpoint, total)
            request = urllib2.Request(url=endpoint)
            self._add_headers(request)
            server = urllib2.urlopen(request)
            data = server.read()
            atom_feed = FeedParserPlus.parse(data) # TODO handle errors
            got = len(atom_feed['entries'])
            if got == 0:
                over = True
            else:
                total += got
                step += 1
                print >>sys.stderr, "Got %i entries..." % total
                if result is None:
                    result = atom_feed
                else:
                    result['entries'].append(atom_feed['entries'])
                if n is not None and total >= n:
                    over = True
        return result

    def post(self, message):
        context = simpleTALES.Context(allowPythonPath=False)
        context.addGlobal ("message", unicode(message, encoding=myencoding))
        result = simpleTALUtils.FastStringOutput()
        self.template.expand (context, result)
        request = urllib2.Request(url=create_endpoint,
                                  data=result.getvalue())
        self._add_headers(request, post=True)
        server = urllib2.urlopen(request)
        return server.read()
