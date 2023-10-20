import imaplib
import email
from email.header import decode_header
import re
from . import emailmodel

def call():
    mail = imaplib.IMAP4_SSL("outlook.office365.com")
    mail.login("wjunior_msn@hotmail.com", "@246824Fwrj9")
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    mail.select("inbox")
    result,data = mail.search(None, "ALL")

    ids = data[0].split()

    for id in ids:
        emailInstance = emailmodel.EmailModel()

        result, data = mail.fetch(id, "RFC822")
        email_message = email.message_from_string(data[0][1].decode("utf-8"))

        emailInstance.__build__(email=email_message)

        for part in email_message.walk():
            if (part.get_content_type() == "text/plain"):
                body = part.get_payload(decode=True)
                try:
                    obj = body.decode()
                except:
                    try:
                        obj = body.decode('ascii')
                    except:
                         break
                
                obj = obj.replace('\r\n', '')
                #obj = obj[:len(obj)-1].replace(' ', '')
                print (email_message)
                #print (str(subject).strip(), fromAddr, "---")
                print ("   ")

    mail.logout()

call()