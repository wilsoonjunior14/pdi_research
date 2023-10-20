
from email.header import decode_header

class EmailModel:

    id = ""
    subject = ""
    fromAddr = ""
    content = ""

    def __init__(self) -> None:
        pass

    def __build__(self, email):
        self.__build_subject__(email)
        self.__build__fromAddr(email)

    def __build_subject__(self, email) -> None:
        subject = decode_header(email.get("Subject"))
        if (subject[0][1] == None):
            self.subject = subject[0][0]
        else:
            self.subject = subject[0][0].decode("utf-8")

    def __build__fromAddr(self, email) -> None:
        fromAddr = decode_header(email.get("From"))
        if (fromAddr[0][1] == None):
            self.fromAddr = fromAddr[0][0]
        else:
            self.fromAddr = fromAddr[0][0].decode("utf-8")

    def __toString(self) -> str:
        return "Email {\n id = "+self.id+" \n from = "+self.fromAddr+" \n subject = "+self.subject+" \n }"