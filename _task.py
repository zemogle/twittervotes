from tempfile import mkstemp
import os
import tinys3

def create_temp_file(data):
    fd, temp_path = mkstemp()
    file = open(temp_path, 'r')
    file.write(data)
    file.close()
    os.close(fd)
    return data


def push_to_s3(filepath):
    s3 = tinys3.Connection(os.environ['AWS_ACCESS_KEY_ID'],os.environ['AWS_SECRET_KEY'],tls=True)

    f = open(filepath,'rb')
    s3.upload(filepath, f ,'darkmattersheep.uk/strictly/')
    return
