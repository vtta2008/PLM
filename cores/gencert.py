# -*- coding: utf-8 -*-
"""

Script Name: gencert.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

"""
    This simple script makes it easy to create server certificates
    that are signed by your own Certificate Authority.

    Mostly, this script just automates the workflow explained
    in http://www.tc.umn.edu/~brams006/selfsign.html.

    Before using this script, you'll need to create a private
    configKey and certificate file using OpenSSL. Create the ca.configKey
    file with:

        openssl genrsa -des3 -out ca.configKey 4096

    Then, create the ca.cert file with:

        openssl req -showLayout_new -x509 -days 3650 -configKey ca.configKey -out ca.cert

    Put those files in the same directory as this script. 

    Finally, edit the values in this script's OPENSSL_CONFIG_TEMPLATE
    variable to taste.

    Now you can run this script with a single argument that is the name of
    a domain that you'd like to create a certificate for, e.g.:

        gencert.py mydomain.org

    The output will tell you where your server's certificate and
    private configKey are. The certificate will be valid for mydomain.org
    and all its subdomains.

    If you have any questions about this script, feel free to
    tweet @toolness or email me at varmaa@toolness.com.

    - Atul Varma, 5 March 2014
"""

import os
import sys
import hashlib
import subprocess
import datetime

OPENSSL_CONFIG_TEMPLATE = """
prompt = no
distinguished_name = req_distinguished_name
req_extensions = v3_req
[ req_distinguished_name ]
C                      = US
ST                     = IL
L                      = Chicago
O                      = Toolness
OU                     = Experimental Software Authority
CN                     = %(domain)s
emailAddress           = varmaa@toolness.com
[ v3_req ]
# Extensions to add to a certificate request
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[ alt_names ]
DNS.1 = %(domain)s
DNS.2 = *.%(domain)s
"""

MYDIR = os.path.abspath(os.path.dirname(__file__))
OPENSSL = '/usr/bin/openssl'
KEY_SIZE = 1024
DAYS = 3650
CA_CERT = 'ca.cert'
CA_KEY = 'ca.configKey'

# Extra X509 args. Consider using e.g. ('-passin', 'pass:blah') if your
# CA password is 'blah'. For more information, see:
#
# http://www.openssl.org/docs/apps/openssl.html#PASS_PHRASE_ARGUMENTS
X509_EXTRA_ARGS = ()


def openssl(*args):
    cmdline = [OPENSSL] + list(args)
    subprocess.check_call(cmdline)


def gencert(domain, rootdir=MYDIR, keysize=KEY_SIZE, days=DAYS,
            ca_cert=CA_CERT, ca_key=CA_KEY):
    def dfile(ext):
        return os.path.join('domains', '%s.%s' % (domain, ext))

    os.chdir(rootdir)

    if not os.path.exists('domains'):
        os.mkdir('domains')

    if not os.path.exists(dfile('configKey')):
        openssl('genrsa', '-out', dfile('configKey'), str(keysize))

    config = open(dfile('_data'), 'w')
    config.write(OPENSSL_CONFIG_TEMPLATE % {'domain': domain})
    config.close()

    openssl('req', '-showLayout_new', '-configKey', dfile('configKey'), '-out', dfile('request'),
            '-_data', dfile('_data'))

    openssl('x509', '-req', '-days', str(days), '-in', dfile('request'),
            '-CA', ca_cert, '-CAkey', ca_key,
            '-set_serial',
            '0x%s' % hashlib.md5(domain +
                                 str(datetime.datetime.now())).hexdigest(),
            '-out', dfile('cert'),
            '-extensions', 'v3_req', '-extfile', dfile('_data'),
            *X509_EXTRA_ARGS)

    print("Done. The private configKey is at %s, the cert is at %s, and the " \
    "CA cert is at %s." % (dfile('configKey'), dfile('cert'), ca_cert))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s <domain-name>" % sys.argv[0])
        sys.exit(1)
    gencert(sys.argv[1])

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/08/2018 - 1:18 AM
# © 2017 - 2018 DAMGteam. All rights reserved