import urllib2, base64

def fetchfile(url, output = None, auth = None, username = None, password = None,verbose=True):
    """

    :param url: remote url to fetch
    :param output: local target name, default is same as remote one
    :param auth: None or Basic
    :param username: username if auth == Basic
    :param password: password if auth == Basic
    :param verbose: display more progress
    """
    if not output:
        output = url.split('/')[-1]

    request = urllib2.Request(url)
    if auth == "Basic":
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)

    u = urllib2.urlopen(request)
    meta = u.info()
    filesize = int(meta.getheaders("Content-Length")[0])
    if verbose:
        print "Download {0} Bytes {1}".format(output, filesize)

    file_size_dl = 0;
    block_sz = 65536
    with open(output,'wb') as f:
        while True:
            buf = u.read(block_sz)
            if not buf:
                if verbose:
                    print "Done"
                break

            file_size_dl += len(buf)
            f.write(buf)
            if verbose:
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / filesize)
                status = status + chr(8)*(len(status)+1)
                print status