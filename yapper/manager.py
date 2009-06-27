"""Manage Yapper instances

This command is used to create and configure launchd jobs that will run 
Yapper for a particular JID. 

Usage: yapper load|unload jid [host]

Examples:
  yapper load test@mydomain.com talk.google.com
  yapper unload test@mydomain.com
"""
import pkg_resources
import sys, getpass, tempfile, os

JOB_BASE = 'com.progrium.Yapper'

def usage():
    print __doc__

def get_job_label(jid):
    return ':'.join([JOB_BASE, jid.replace('@', '.')])

def generate_plist_file(jid, password, host = None):
    plist = pkg_resources.resource_string(__name__, 'templates/%s.plist' % JOB_BASE) \
        .replace('$label', get_job_label(jid)) \
        .replace('$jid', jid) \
        .replace('$password', password) \
        .replace('$host', host if host else '')
    f, fname = tempfile.mkstemp(suffix='.plist')
    os.write(f, plist)
    os.close(f)
    return fname

def run(args=None):
    if not args:
        args = sys.argv[1:]
    if not args:
        usage()
        sys.exit(2)
    if len(args) >= 2 and args[0] == 'load':
        jid = args[1]
        password = getpass.getpass("Enter password for %s: " % jid)
        if len(args) > 2:
            host = args[2]
        else:
            host = None
        plist_file = generate_plist_file(jid, password, host)
        os.system('launchctl load %s' % plist_file)
        os.unlink(plist_file)
        os.system('launchctl start %s' % get_job_label(jid))
        print "Installed and started."
        
    elif len(args) >= 2 and args[0] == 'unload':
        jid = args[1]
        os.system('launchctl remove %s' % get_job_label(jid))
        print "Removed."
        
    else:
        usage()
        sys.exit()

if __name__ == "__main__":
    pkg_resources.require('Yapper')
    sys.exit(run(sys.argv[1:]))
