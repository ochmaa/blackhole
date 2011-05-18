#!/usr/bin/python
# this will be filled with everything required to startup with twistd
from twisted.application import internet, service
from twisted.internet import epollreactor
epollreactor.install()
from twisted.manhole import telnet
from twisted.web.server import Site
from twisted.spread import pb
#
from blackhole.admin.resources import root
from blackhole import settings

application = service.Application("Blackhole project")

internet.TCPServer(settings.SITE_PORT, Site(root)).setServiceParent(application)

# debugging shell
telnet = telnet.ShellFactory()
telnet.username = "debug"
telnet.password = "python"
internet.TCPServer(settings.MANHOLE_PORT, telnet, interface="127.0.0.1").setServiceParent(application)
