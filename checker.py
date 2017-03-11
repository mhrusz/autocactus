import imaplib
import autocactus_settings as aset


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
        # process message

    imap_client.close()
    imap_client.logout()
