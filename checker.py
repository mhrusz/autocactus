import imaplib
import email
import pymongo
from urllib.parse import quote_plus
import autocactus_settings as aset


def save_to_db(msg):
    """
    Saving to MongoDB
    """
    mongo_uri = "mongodb://{0}:{1}@{2}".format(quote_plus(aset.MONGODB_USER),
                                               quote_plus(aset.MONGODB_PASSWORD),
                                               aset.MONGODB_SERVER)
    client = pymongo.MongoClient(mongo_uri)
    db = client.test_database


def check():
    """
    Checker main function.
    """
    imap_client = imaplib.IMAP4(aset.INBOX_MAILSERVER)
    imap_client.login(aset.INBOX_NAME, aset.INBOX_PASSWORD)
    # select INBOX - default
    imap_client.select()
    typ, data = imap_client.search(None, 'ALL')
    for num in data[0].split():
        typ, data = imap_client.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        # check as seen
        typ, data = imap_client.store(num, '-FLAGS', '\\Seen')
        # process message
        print(msg)

    imap_client.close()
    imap_client.logout()
