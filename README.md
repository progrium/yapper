Yapper - A Jabber/XMPP interface to Growl
=========================================

Growl is a great utility for last mile notifications, but comes with terrible network support. It seems the most useful notifications are the ones coming from out there, not from your computer (do I really need to see the currently playing song from iTunes?). Unfortunately, Growl's network interface is based on some esoteric protocol and requires a direct connection. 

Yapper solves this problem and makes Growl instantly accessible from any system that can send Jabber/XMPP messages. Yapper runs in the background locally, like Growl, but listens on a Jabber account you specify. When messages come in, they get pushed to Growl. It's that simple.  

Requirements
------------

Yapper only runs on OS X. You'll need Growl obviously. The install script takes care of installing the Growl Python bindings necessary for Yapper, but it doesn't do such a good job with Twisted. Twisted is a major dependency, so make you sure you have that installed ("sudo port install py25-twisted"). 

In case this isn't obvious, you also need two Jabber accounts to test this with! One for Yapper and one to send it messages. You can get a friend to test it for you, but especially if you're using a GMail/GTalk account, be sure not to be signed in at the same time Yapper is running. Otherwise, your friend is most likely going to get their message routed to your signed in client instead of Yapper.

Installing
----------

After you download, drop into the directory and run:
    $ sudo python setup.py install

Make a note of the install output because it's going to install a command line tool and you may need to add the path to your PATH environment variable. It should tell you at the end of the first big chunk of lines, starting with "Installing yapper script to ..."
    
Configuring
-----------

You need to tell Yapper what Jabber account to use and make it run in the background when OS X starts. Fortunately, we have a sweet utility to manage this for you. If the install went correctly, you should now have a 'yapper' tool with a 'load' command:
    $ yapper load youraccount@example.com example.com

You need to specify your JID as well as the Jabber host right now. Redundant, sure, but I made this with a JID domain that's different from my host. Patches welcome.

Anyway, you'll be prompted for your account password. It won't tell if you failed to authenticate, so be sure to get it right. It should give you a success message quite immediately telling you that it's installed and running. It might not be, however ... best way to check is to see if the Yapper JID comes online. See Advanced section for troubleshooting tips if necessary.

If you want to kill Yapper and prevent it from starting up at system load, use the 'unload' command:
    $ yapper unload youraccount@example.com

You may have guessed you can run multiple Yapper instances with different JIDs. I don't know why you'd want to do this, but you can. 

Using Yapper
------------

Yapper will automatically add back anybody that adds its JID while it's running. Then you can send it messages. You have two options for this:

 * Plain text messages
 * JSON messages

Plain text messages don't let you specify an icon, but the default icon is going to be the avatar of the sending JID (you could have a different JID for every icon if you wanted). You have a pretty natural way to describe the title and whether it's sticky. The title is anything before a colon, like "This is the title: This is the body", and you can make a message sticky by prepending it with a bang (!), like "!This message will stick around" ... pretty simple?

JSON messages let you explicitly set each field, including the icon, using a JSON object. The fields are:

 * title, string (optional)
 * text, string
 * sticky, boolean (optional, default: false)
 * icon, string (optional, a URL!)

Yes, you can specify a URL for the icon. Standard formats please. Growl supports PNG, TIFF, JPEG, GIF, PICT, PDF, and BMP. Yapper will download whatever you give it ... if it's not one of those formats, I don't know what will happen.

Advanced
--------

Yapper uses launchd and twistd behind the scenes. If you want to manually use launchctl to start/stop/remove/check the job, you can do that. If you want to see what else is going on, you can see where launchd logs, which is usually /var/log/system.log. And lastly, the launchd job just runs twistd, so if you want to run Yapper without launchd, you can use the yapper plugin installed for twistd ("twistd -n yapper --jid JID --password PASSWORD --host HOST").

Contributing
------------

Obviously this project is open source. MIT license methinks. Feel free to fork it on GitHub.

Author
------

Jeff Lindsay <progrium@gmail.com>