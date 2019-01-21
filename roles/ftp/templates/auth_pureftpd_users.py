#!/usr/bin/env python

"""
This is a wrapper for authenticating via api
using their API user name and password. It will return
the appropriate local filesystem path

Variables are set by Ansible. Do NOT change locally!

Test:
export AUTHD_ACCOUNT=<username>
export AUTHD_PASSWORD=<pass>
python /usr/local/bin/auth_pureftpd_users.py

Valid response for pure-ftpd:
auth_ok:1
uid:504
gid:504
dir:/home/pmdigital.ftp/1
end

"""

import os
import warnings
import logging

# From common_requirements
import requests

# Setup logging, runs as root so permissions OK
# import sys; logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(filename='/var/log/auth-pureftpd-users.log', level=logging.ERROR)


# Note that ALL users share the same uid/gid. Its legacy behaviour that is not necessarily permanent.
UID = {{ ftp_user_id }}  # pmdigital.ftp user
GID = {{ ftp_group_id }}  # 504
HOMEDIR_PREFIX = '/home/pmdigital.ftp'

# This endpoint must be publicly accessible
AUTH_ENDPOINT = '{{ ftp_public_auth_endpoint }}'  # I.e 'https://beta.canada.com/ftp_login'

STATSD_AUTH_COUNTER = 'ftp.api_credential_auth'
TIMEOUT_SECS = 5

# When verify is set getting the following errors:
# InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL
# appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to
# solve this
# SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not
# available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause
# validation failures.
VERIFY_SSL = True
# Ignoring these errors for now .. need to update python versions
warnings.filterwarnings("ignore")

# Ability to block specific users
# BLOCKED_USERS = ['test', 'admin', 'root']


def check_auth(user, password):
    """
    Checks the user name and password against the  API portal.
    Returns True if the credentials are valid,
    False if not.
    :param user: api username
    :param password: api pass
    :return: tuple(bool success, str, username)
    """

    try:
        response = requests.get(AUTH_ENDPOINT, auth=(user, password), verify=VERIFY_SSL, timeout=TIMEOUT_SECS)
    except requests.exceptions.ConnectTimeout:
        logging.exception("check_auth timeout for user".format(user))
        return False, None

    if response.status_code == 200:
        try:
            username = str(response.json()['username'])
        except (KeyError, TypeError) as e:
            # Either get a string response (not found): TypeError, or a dict without username: KeyError
            logging.exception("check_auth bad response {}".format(e))
            username = None

        return True, username

    # logging.info("User '{}', Pass '{}'".format(user, password))
    return False, None


def create_homedir(username):
    """
    Creates a user's home directory if not present
    :param username: str, username
    :return: bool, success
    """
    try:
        path = os.path.join(HOMEDIR_PREFIX, username)
        if os.path.exists(path):
            # Assuming permissions correct from previous run
            return True
        else:
            os.mkdir(path)
            os.chown(path, UID, GID)
            return True
    except AttributeError:
        # This can happen if username passed is none, due to auth error from api
        pass
    except Exception as e:
        # This should only happen if there is an FS error so shouldn't happen ever.
        logging.exception("create_homedir failed {}".format(e))

    return False


def main():
    # More on AUTHD_* env vars:
    # https://download.pureftpd.org/pub/pure-ftpd/doc/README.Authentication-Modules
    authd_account = os.getenv('AUTHD_ACCOUNT', '')

    # if authd_account and authd_account.lower in BLOCKED_USERS:
    #     auth_success = False  # Need else if we use this

    auth_success, username = check_auth(authd_account, os.getenv('AUTHD_PASSWORD'))
    home_dir_exists = create_homedir(username)  # If access not authorized, will not get username to create legacy dir
    if auth_success and username and home_dir_exists:
        # Required prints to communicate to ftpd-auth (success)
        print("auth_ok:1")
        print("uid:{}".format(UID))
        print("gid:{}".format(GID))
        print("dir:{}".format(os.path.join(HOMEDIR_PREFIX, username)))
    else:
        print("auth_ok:0")
    print("end")


if __name__ == '__main__':
    main()
