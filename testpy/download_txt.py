from wsgiref.util import FileWrapper
import os
from django.http import HttpResponse, HttpResponseRedirect

def download_txt():
    response={}
    try:
        fpath = r"C:\Users\jerryzli\PycharmProjects\Test2_py2neo\output.txt"
        if os.path.exists(fpath):
            ftype = 'text/plain'
            # Get the content of the file
            content = FileWrapper(open(fpath,'rb'))
            # print(content.__getitem__('close'))

            response['content'] = content
            # Set the correct headers
            response['Content-Length'] = os.path.getsize(fpath)
            response['Content-Type'] = ftype
            response['Content-Disposition'] = 'attachment; filename="' + fpath.split('/')[-1] + '"'
            return response
        else:
            raise ValueError('file does not exist' + fpath)
    except:
        raise ValueError

if __name__ == "__main__":
    download_txt()
