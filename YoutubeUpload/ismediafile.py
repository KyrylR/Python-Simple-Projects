import mimetypes

mimetypes.init()


def isMediaFile(fileName):
    mimestart = mimetypes.guess_type(fileName)[0]

    if mimestart != None:
        mimestart = mimestart.split('/')[0]

        if mimestart in ['video']:
            return True

    return False
