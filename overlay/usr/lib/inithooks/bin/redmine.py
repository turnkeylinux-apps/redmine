#!/usr/bin/python3
"""Set Redmine admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
import inithooks_cache
import hashlib
import random
import string

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s [options]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError as e:
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

    inithooks_cache.write('APP_EMAIL', email)

    salt = "".join(random.choice(string.ascii_letters) for line in range(16))
    pw_with_salt = salt + hashlib.sha1(password.encode('utf-8')).hexdigest()
    hashpass = hashlib.sha1(pw_with_salt.encode('utf-8')).hexdigest()
    user_id = 1

    m = MySQL()
    m.execute('UPDATE redmine_production.email_addresses SET address=\"%s\" WHERE user_id=%i;' % (email, user_id))
    m.execute('UPDATE redmine_production.users SET salt=\"%s\" WHERE login=\"admin\" AND id=%i;' % (salt, user_id))
    m.execute('UPDATE redmine_production.users SET hashed_password=\"%s\" WHERE login=\"admin\" AND id = %i;' % (hashpass, user_id))

if __name__ == "__main__":
    main()

