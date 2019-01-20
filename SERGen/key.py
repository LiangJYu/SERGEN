import gpg
import getpass
import dropbox

def DropboxAccess:
    def setup():
        print("initializing dropbox access\n")

        # get key
        _db_key = ''
        while _db_key == '':
            db_key0 = getpass.getpass(promt='Enter dropbox key: ')
            db_key1 = getpass.getpass(promt='Renter dropbox key: ')
            if db_key0 == db_key1:
                _db_key = db_auth0
            else:
                print("dropbox keys do not match. please re-enter\n")

        # get oauth
        _db_oauth = ''
        while _db_oauth == '':
            db_oauth0 = getpass.getpass(promt='Enter dropbox oauth2: ')
            db_oauth1 = getpass.getpass(promt='Renter dropbox oauth2: ')
            if db_oauth0 == db_oauth1:
                _db_oauth = db_auth0
            else:
                print("dropbox oauth2 do not match. please re-enter\n")

        # encrypt
        c = gpg.core.Context(armor=True)
        rkey = list(c.keylist(pattern=a_key, secret=False))
        ciphertext, result, sign_result = c.encrypt(text, recipients=rkey,
                                                    always_trust=True,
                                                    add_encrypt_to=True)
        with open("key.asc", "wb") as f:
            f.write(ciphertext)


    def connect():
        print("connecting to dropbox\n")
        with open("key.asc", "rb") as f:
            plaintext, result, verify_result = gpg.Context().decrypt(f)
        dbx = dropbox.Dropbox(plaintext)

