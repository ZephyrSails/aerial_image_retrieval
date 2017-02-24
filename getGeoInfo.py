from sys import argv


LICENCE_KEY = 'AhHPXuVNzco40xVgSzCMz6TmC589Zlp-F2_Wj065PQW1Cr0SyOLC_EoyMEnJZ6Lx'
LICENCE_PARAM = 'key=%s' % LICENCE_KEY


def getURL(lat1, lon1, lat2, lon2):
    """
    URL encoder
    """
    return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&%s" % (encode(lat1, lon1, lat2, lon2), LICENCE_PARAM)


def downloadAerialImage(lat1, lon1, lat2, lon2):
    """
    download proper aerial image based on bounding rectangle
    """
    url = getURL(lat1, lon1, lat2, lon2)


if __name__ == '__main__':
    """
    python aerial_image.py 50.625 8.43751 53.4375 11.25
    """
    try:
        lat1, lon1, lat2, lon2 = [float(argv[i]) for i in xrange(1, 5)]
        print 'Bounding Rectangle recognized - [%f, %f; %f, %f]\nCalculating Bounding Image...' % (lat1, lon1, lat2, lon2)
    except:
        print 'Required input:\n~ python getGeoInfo.py <lat1> <lon1> <lat2> <lon2>\nE.g.\n~ stpython aerial_image.py 50.625 8.43751 53.4375 11.25'

    downloadAerialImage(lat1, lon1, lat2, lon2)



# def encode(lat1, lon1, lat2, lon2):
#     """
#     Input:
#     Rectangle defined by: lat1, lon1, lat2, lon2
#     Return:
#     18-digits location encode
#     """
