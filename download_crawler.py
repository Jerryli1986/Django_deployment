from __future__ import ( division, absolute_import, print_function, unicode_literals )

import sys, os, tempfile, logging

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

def download_file1(url, dest=None):
    """
    Download and save a file specified by url to dest directory,
    """
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    return filename

def download_file(url, dest=None):
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if dest:
        filename = os.path.join(dest, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename

def write_to_log(log_file, log_string):
    with open(log_file, 'a+') as writer:
        writer.writelines(log_string + "\n")

def get_last_log(log_file):

    if not os.path.isfile(log_file):
       line = "0"
    else:
        with open(log_file) as reader:
            lines = reader.read().splitlines()
            line = lines[-1]
            if line == "":
                line = lines[-2]
    return line


def main(url_dir, destination_dir, log_dir, name):
    log_file = os.path.join(log_dir, "download_log.txt")
    last_download = get_last_log(log_file)
    curr_iteration = int(last_download.replace(".zip", "")) + 1
    # Run over all zips
    if name == "Dave":
        start_zip = 0
        end_zip = 249
    elif name == "Thu":
        start_zip = 250
        end_zip = 499
    elif name == "Jerry":
        start_zip = 500
        end_zip = 749
    elif name == "Harriet":
        start_zip = 750
        end_zip = 999
    start = max(start_zip, curr_iteration)
    for i in range(start, end_zip, 1):
        # Build output file
        filename = "{:0>3}".format(i) + '.zip'
        outfilepath = os.path.join(destination_dir, filename)
        # Check if file already exists?
        if not os.path.isfile(outfilepath):
            print('Downloading file ' + outfilepath)
            filename = download_file(url_dir + filename, destination_dir)
            #filename = "{:0>3}".format(i) + ".zip"
            #print(filename)
            write_to_log(log_file, filename)
    return filename

if __name__ == "__main__":  # Only run if this file is called directly
    #print("Testing with 10MB download")
    url = r"http://downloads.digitalcorpora.org/corpora/files/govdocs1/zipfiles/"
    dest_dir = "P:/NON-CLIENT/DUST/Fileshare Dataset/GovDocs1/RAW/"
    name = "Jerry" #Fill in name HERE
    log_dir = "P:/NON-CLIENT/DUST/Fileshare Dataset/GovDocs1/" + name
    #filename = download_file(url, "C:/Users/daeldridge/Documents/DUST/FileDownloads")
    #print(filename)
    filename = main(url, dest_dir, log_dir, name)
    print(filename + ' Downloaded')
