import imaplib
import email
from email.header import decode_header
import re

def call():
    mail = imaplib.IMAP4_SSL("outlook.office365.com")
    mail.login("wjunior_msn@hotmail.com", "@246824Fwrj9")
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    mail.select("inbox")
    result,data = mail.search(None, "ALL")
    print (result)
    print (data)

    ids = data[0].split()

    for id in ids:
        result, data = mail.fetch(id, "RFC822")

        email_data = email.message_from_bytes(data[0][1])  
        print (email_data)  

        subject = decode_header(email_data.get("Subject"))
        #print (str(email_data.get("Subject")), subject)

        # Getting the subject information.
        #print (subject)
        #if (subject[0][1] == None):
        #    print (subject[0][0])
        #else:
        #    print (subject[0][0].decode("utf-8"))

        # Getting the from address information
        fromAddr = decode_header(email_data.get("From"))
        #if (fromAddr[0][1] == None):
        #    print (fromAddr[0][0])
        #else:
        #    print (fromAddr[0][0].decode("utf-8"))
        
        body = ""
        for msg in email_data.walk():
            if(msg.get_content_maintype() == "text"):
                new_body = msg.get_payload(decode=True)[0]
                body = ""+str(body)+""+str(new_body)+"".decode()
                body = re.sub(CLEANR, '', body)

        print (body)
        print ("----")
        break

    mail.logout()

call()