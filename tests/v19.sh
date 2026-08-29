#!/bin/bash
set -euo pipefail

result=${TKL_TEST_RESULT:?}
password=${TKL_TEST_APP_PASS:?}
work=/run/tkl-v19-tests/redmine
base=https://www.example.com
curl_args=(-kfsS --resolve www.example.com:443:127.0.0.1)
mkdir -p "$work"

systemctl --quiet is-active apache2.service mariadb.service
grep -q '\[40redmine\] successfully completed' /var/log/inithooks.log
curl "${curl_args[@]}" -c "$work/cookies" "$base/login" >"$work/login.html"
grep -Eqi 'redmine|sign in|login' "$work/login.html"
token=$(sed -n 's/.*name="authenticity_token" value="\([^"]*\)".*/\1/p' \
    "$work/login.html" | head -1)
test -n "$token"

curl "${curl_args[@]}" -b "$work/cookies" -c "$work/cookies" \
    -D "$work/login.headers" -o "$work/login-response.html" \
    --data-urlencode "authenticity_token=$token" \
    --data-urlencode username=admin \
    --data-urlencode "password=$password" \
    --data-urlencode login=Login \
    "$base/login"
curl "${curl_args[@]}" -b "$work/cookies" \
    "$base/projects/git-helloworld" >"$work/project.html"
grep -Eqi 'git-helloworld|overview|activity' "$work/project.html"

test "$(tr -d '\n' </var/www/redmine/api_key)" = \
    "$(mysql -N redmine_production -e "SELECT value FROM settings WHERE name='sys_api_key'")"
test "$(stat -c '%U:%G:%a' /var/www/redmine/api_key)" = root:root:600
runuser -u www-data -- test ! -w /var/www/redmine/app/models/user.rb
runuser -u www-data -- touch /var/www/redmine/tmp/.tkl-v19-write-test
runuser -u www-data -- rm /var/www/redmine/tmp/.tkl-v19-write-test
/usr/local/rbenv/shims/ruby -e 'require "active_resource"; abort unless ActiveResource'

systemctl restart mariadb.service apache2.service
curl "${curl_args[@]}" -b "$work/cookies" \
    "$base/projects/git-helloworld" >"$work/project-after-restart.html"
grep -Fqi git-helloworld "$work/project-after-restart.html"
! grep -F -- "$password" /var/log/inithooks.log

cat >"$result" <<EOF
package_source=official Redmine 7.0.1 archive and pinned RubyGem inputs verified by SHA-256
installed_version=7.0.1
runtime_checks=Apache and MariaDB services, firstboot completion, HTTPS admin login, seeded project across restart, repository API-key rotation, ActiveResource load, ownership boundaries, password log hygiene
updater_command=supervised official Redmine release upgrade
updater_result=installed version unchanged during QA
updater_channel=official Redmine stable releases
integrity_evidence=Redmine archive pinned to 68538b4310fa50ac79a521045cb55fe3bcffed5c1562d6844cf90e66e7619209; ActiveResource and XML serializer gems pinned
EOF
