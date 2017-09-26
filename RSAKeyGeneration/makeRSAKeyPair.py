# Make RSA Key Pair
#   Adopted from PyOpenSSL GitHub: https://github.com/pyca/pyopenssl/tree/master/examples

import sys
from OpenSSL import crypto
from certgen import *

# Require ID argument
if len(sys.argv) < 3:
    print('Usage: python makeRSAKeyPair.py ID SIZE')
    sys.exit(1)

ID = sys.argv[1]
size = int(sys.argv[2])

privateKeyFilename = ID + '.pkey'
publicKeyFilename = ID + '.pubkey'

key = createKeyPair(crypto.TYPE_RSA, size)

print('Creating private key "' + privateKeyFilename)
with open(privateKeyFilename, 'w') as pkey:
    pkey.write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode('utf-8')
    )

print('Creating public key "' + publicKeyFilename)
with open(publicKeyFilename, 'w') as pubkey:
    pubkey.write(
        crypto.dump_publickey(crypto.FILETYPE_PEM, key).decode('utf-8')
    )
