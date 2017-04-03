import imaplib
import email
import pymongo
from urllib.parse import quote_plus
import autocactus_settings as aset


def save_to_db(msg):
    """
    Saving to MongoDB
    """
    mongo_uri = "mongodb://{0}:{1}@{2}/{3}".format(quote_plus(aset.MONGODB_USER),
                                               quote_plus(aset.MONGODB_PASSWORD),
                                               aset.MONGODB_SERVER,
                                               aset.MONGODB_DBNAME)
    client = pymongo.MongoClient(mongo_uri)
    db = client[aset.MONGODB_DBNAME]
    entry = {
      'status': 'new',
      'title': msg['Subject'],
      'author': msg['From'],
      'send_date': msg['Date'],
      'body': msg.get_payload()
    }
    result = db[aset.MONGODB_DBNAME].insert_one(entry)
    print( result.inserted_id)

def check():
    """
    Checker main function.
    """
    imap_client = imaplib.IMAP4(aset.INBOX_MAILSERVER)
    imap_client.login(aset.INBOX_NAME, aset.INBOX_PASSWORD)
    # select INBOX - default
    imap_client.select()
    typ, data = imap_client.search(None, '(UNSEEN)')
    for num in data[0].split():
        typ, data = imap_client.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        print(msg)
        # check as seen
        typ, data = imap_client.store(num, '+FLAGS', '\\Seen')
        # process message from email.message
        save_to_db(msg)

    imap_client.close()
    imap_client.logout()

check()
