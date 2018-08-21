from devops.settings import DEFAULT_FROM_MAIL
from django.core.mail import EmailMultiAlternatives
import threading

def sendmail(subject,content,to_addr):
    from_email = DEFAULT_FROM_MAIL
    msg = EmailMultiAlternatives(subject,content,from_email,to_addr)
    msg.content_subtype = "html"
    msg.send()

class EmailThread(threading.Thread):
    def __init__(self,subject,content,to_addr):
        threading.Thread.__init__(self)
        self.subject = subject
        self.content = content
        self.to_addr = to_addr
    def run(self):
        sendmail(self.subject,self.content,self.to_addr)
