Yapper - A Jabber/XMPP interface to Growl
=========================================

Growl is a great utility for last mile notifications, but comes with terrible network support. It seems the most useful notifications are the ones coming from out there, not on your computer (do I really need to see the currently playing song in iTunes?). Unfortunately, Growl's network interface is based on some esoteric protocol and requires a direct connection. 

Yapper solves this problem and makes Growl instantly accessible for integrating with any system that can send Jabber/XMPP messages. Yapper runs in the background, like Growl, but listening on a Jabber account you specify. When messages come in, they get pushed to Growl. It's that simple.  

Requirements
------------

Yapper only runs on OS X. You'll need Growl obviously. The install script takes care of installing the Growl Python bindings necessary for Yapper, but it doesn't do such a good job at installing Twisted. Twisted is a major dependency, so make you sure you have that installed. 

Installing
----------

After you download, drop into the directory and run:
    $ sudo python setup.py install
    
Configuring
-----------

You need to tell Yapper what Jabber account to use and install it to run in the background when OS X starts. We have a sweet utility to manage this for you. If the install went correctly, you should now have a 'yapper' tool with a 'load' command:
    $ yapper load youraccount@example.com example.com

You need to specify your JID as well as the Jabber host right now. Redundant, sure, but I made this with a JID domain that's different from my host. Patches welcome.

Anyway, you'll be prompted for your account password. It won't tell if you failed to authenticate, so be sure to get it right. It should give you a success message quite immediately telling you that it's installed and running!

If you want to kill Yapper and prevent it from starting up at system load, use the 'unload' command:
    $ yapper unload youraccount@example.com

You may have guessed you can run multiple Yapper instances with difference JIDs. I don't know why you'd want to do this, but you can. 

Using Yapper
------------

Yapper will automatically add back anybody that adds its JID while it's running. Then you can send it messages. You have two options for this:
* Plain text messages
* JSON messages

Plain text messages don't let you specify an icon, but the default is going to be the avatar of the sending JID (you could have a different JID for every type of message to have a different icon). But you have a pretty natural way to describe the title and whether it's sticky. The title is anything before a colon, like "This is the title: This is the body"

You can make a message sticky by prepending it with a bang (!), like "!This message will stick around" ... pretty simple?

JSON messages let you explicitly set each field, including the icon, with the values of a single JSON object. The keys are:
* title, string (optional)
* text, string
* sticky, boolean (optional, default: false)
* icon, string (optional, a URL!)

Yes, you can specify a URL for the image. Standard formats please. Growl supports PNG, TIFF, JPEG, GIF, PICT, PDF, BMP, and .icns and Yapper will download whatever you give it ... if it's not one of those, I don't know what will happen.

Contributing
------------
Obviously this project is open source. MIT license methinks. Feel free to fork it on GitHub.

Author
------
Jeff Lindsay <progrium@gmail.com>