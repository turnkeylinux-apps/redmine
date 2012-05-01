#!/usr/bin/python
"""Set Redmine admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
import hashlib
import random
import string

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Redmine Password",
            "Enter new password for the Redmine 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "Redmine Email",
            "Enter email address for the Redmine 'admin' account.",
            "admin@example.com")
    
    salt = "".join(random.choice(string.letters) for line in range(16))
    hashpass = hashlib.sha1(salt + hashlib.sha1(password).hexdigest()).hexdigest()

    m = MySQL()
    m.execute('UPDATE railsapp_production.users SET mail=\"%s\" WHERE login=\"admin\";' % email)
    m.execute('UPDATE railsapp_production.users SET salt=\"%s\" WHERE login=\"admin\";' % salt)
    m.execute('UPDATE railsapp_production.users SET hashed_password=\"%s\" WHERE login=\"admin\";' % hashpass)

if __name__ == "__main__":
    main()

