from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet

from yapper.core import YapperFactory

class Options(usage.Options):
    optParameters = [["jid", "j", None, "The JID to login with"],
                    ["password", "p", None, "The password to login with"],
                    ["host", "h", None, "The host to login with"]]


class YapperMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "yapper"
    description = "A Jabber/XMPP interface for Growl"
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        return internet.TCPClient(options['host'], 5222, YapperFactory(options['jid'], options['password']))

serviceMaker = YapperMaker()
