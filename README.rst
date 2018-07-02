Redmine - Integrated SCM & Project Management
=============================================

Redmine is a Rails web application that provides integrated project
management features, issue tracking, and support for multiple version
control programs. It includes calendar and gantt charts to aid visual
representation of projects and their deadlines. It also features
multi-project support, role based access control, a per-project wiki,
and project forums.

The Redmine appliance includes all the standard features in `TurnKey
Core`_, and on top of that:

- Redmine configurations:
    - Installed from upstream source code to /var/www/redmine
    - Supports Git and Subversion.
    - Includes exemplary helloworld repositories.
    - Loaded default roles, trackers, statuses, workflows and
      enumerations.
    - Configured projects to use all available trackers (bug, feature,
      support).

- SSL support out of the box.
- Includes Phusion Passenger for Apache web server (mod_rails).
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, MySQL and Postfix.

- Repository access::

    Name        Protocol access
    ----        ---------------
    Git         http://$ipaddr/git
                https://$ipaddr/git
                ssh://vcs@$ipaddr/git
    Subversion  http://$ipaddr/svn
                svn://addr/svn
                svn+ssh://vcs@$ipaddr/srv/repos/svn

  Repositories are stored in /srv/repos.

-  Recommended configurations:
   
   -  settings->hostname and path
   -  settings->email notifications

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, Webshell, SSH, MySQL: username **root**
-  Redmine: username **admin**
-  Git, SVN: username **vcs**


.. _TurnKey Core: https://www.turnkeylinux.org/core
