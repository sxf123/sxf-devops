import threading

def handle_upload_file(filename,f):
    with open(filename,"wb") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()

class UploadFileThread(threading.Thread):
    def __init__(self,filename,f):
        threading.Thread.__init__(self)
        self.filename = filename
        self.f = f
    def run(self):
        handle_upload_file(self.filename,self.f)