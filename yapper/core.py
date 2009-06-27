from twisted.words.protocols.jabber import client
from twisted.words.protocols.jabber.jid import JID
from twisted.words.xish import domish, xmlstream
from twisted.internet.defer import Deferred
from twisted.web.client import getPage

from Growl import GrowlNotifier, Image

import string, base64
import simplejson

avatar_cache = dict()

def sendGrowl(message, icon=None):
    g = GrowlNotifier(notifications=['yapper'])
    g.register()
    if type(message) is dict:
        g.notify('yapper', message.get('title', ''), message['text'], sticky=message.get('sticky', False), icon=icon)
    else:
        if message[0] == '!':
            sticky = True
            message = message[1:]
        else:
            sticky = False
        if message.count(':') > 0:
            title, message = string.split(message, ':', 1)
        else:
            title = ''
        g.notify('yapper', title.strip(), message.strip(), sticky=sticky, icon=icon)

def getAvatar(stream, jid):
    if jid in avatar_cache:
        return avatar_cache[jid]
    else:
        avatar_q = domish.Element(('jabber:client', 'iq'))
        avatar_q['to'] = jid
        avatar_q['type'] = 'get'
        avatar_q.addElement(('vcard-temp', 'vCard'))
        stream.send(avatar_q)
        avatar_cache[jid] = Deferred()
        return avatar_cache[jid]

def authenticated(stream):
    presence = domish.Element(('jabber:client','presence'))
    presence.addElement('status').addContent('Online')
    stream.send(presence)
    
    stream.addObserver('/message', lambda x: receivedMessage(stream, x))
    stream.addObserver('/presence', lambda x: receivedPresence(stream, x))
    stream.addObserver('/iq', lambda x: receivedResult(stream, x))
    
    roster_q = domish.Element(('jabber:client', 'iq'))
    roster_q['type'] = 'get'
    roster_q.addElement(('jabber:iq:roster', 'query'))
    stream.send(roster_q)

def receivedResult(stream, x):
    for e in x.elements(): 
        if e.name == 'vCard':
            for ee in e.elements():
                if ee.name == 'PHOTO':
                    for eee in ee.elements():
                        if eee.name == 'BINVAL':
                            image = Image.imageWithData(base64.b64decode(str(eee)))
                            if x['from'] in avatar_cache and isinstance(avatar_cache[x['from']], Deferred):
                                avatar_cache[x['from']].callback(image)
                            avatar_cache[x['from']] = image
                             

def receivedMessage(stream, x):
    for e in x.elements():
        if e.name == "body" and x.hasAttribute('type') and x['type'] == 'chat':
            message = str(e)
            avatar_result = getAvatar(stream, x['from'])
            if message.strip()[0] == '{':
                message = simplejson.loads(message)
            if type(message) is dict and 'icon' in message:
                getPage(message['icon']).addCallback(lambda x: sendGrowl(message, Image.imageWithData(x)))
            elif isinstance(avatar_result, Deferred):
                avatar_result.addCallback(lambda x: sendGrowl(message, x))
            else:
                sendGrowl(message, avatar_result)
            
def receivedPresence(stream, x):
    if x.hasAttribute('type') and x['type'] == 'subscribe':
        presence = domish.Element(('jabber:client', 'presence'))
        presence['to'] = x['from']
        presence['type'] = 'subscribed'
        stream.send(presence)

def debug(x):
    print x.toXml()

def YapperFactory(jid, password):
    f = client.XMPPClientFactory(JID(jid), password)
    f.addBootstrap('//event/stream/authd', authenticated)
    #f.addBootstrap('/*', debug)
    return f