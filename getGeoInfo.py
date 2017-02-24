from sys import argv
import urllib
from PIL import Image
from convert import *
import io


LICENCE_KEY = 'AhHPXuVNzco40xVgSzCMz6TmC589Zlp-F2_Wj065PQW1Cr0SyOLC_EoyMEnJZ6Lx'
LICENCE_PARAM = 'key=%s' % LICENCE_KEY
RESOLUTION_UPBOUND = 23

TILE_SIZE = 64
TILE_UP_BOUND = 64
IMG_SIZE = TILE_SIZE * TILE_UP_BOUND


def buildImage(lat1, lon1, lat2, lon2):
    currLv = calcCommonLevel(lat1, lon1, lat2, lon2)

    image = Image.new('RGB', (IMG_SIZE, IMG_SIZE))

    x0, y0 = LatLong2PixelXY(lat1, lon1, currLv)
    currTileSize = IMG_SIZE / 2

    while currTileAmount(lat1, lon1, lat2, lon2, currLv) >= TILE_SIZE ** 2:
        x1, y1 = LatLong2PixelXY(lat1, lon1, currLv)
        x2, y2 = LatLong2PixelXY(lat2, lon2, currLv)

        for X in xrange(x1, x2 + 1):
            for Y in xrange(y1, y2 + 1):
                subImg = downloadImageByTileXY(X, Y)
                if isExist(subImg):

                    image.paste(subImg, ((x1-x0) * currTileSize), (y1-y0) * currTileSize)


        x0, y0 = x0 * 2, y0 * 2
        currLv += 1
        currTileSize /= 2


def downloadImageByTileXY(x, y):
    url = getURL(TileXYtoQuadKey(X, Y, level))
    socket = urllib.urlopen(url)
    tinker = socket.read()
    return Image.open(io.BytesIO(tinker))



def currTileAmount(lat1, lon1, lat2, lon2, currLv):
    x1, y1 = LatLong2PixelXY(lat1, lon1, level)
    x2, y2 = LatLong2PixelXY(lat2, lon2, level)
    return (x2 - x1 + 1) * (y2 - y1 + 1)


def calcCommonLevel(lat1, lon1, lat2, lon2):
    for level in xrange(RESOLUTION_UPBOUND, -1, -1):
        x1, y1 = LatLong2PixelXY(lat1, lon1, level)
        x2, y2 = LatLong2PixelXY(lat2, lon2, level)
        if abs(y2 - y1) <= 1 and abs(x1 - x2) <= 1:
            return level


def encode(lat1, lon1, lat2, lon2):
    return LatLong2QuadKey(lat1, lon1, 12)


def getURL(qKey):
    """
    URL encoder
    """
    return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&%s" % (qKey, LICENCE_PARAM)


def downloadAerialImage(lat1, lon1, lat2, lon2):
    """
    download proper aerial image based on bounding rectangle
    """
    url = getURL(lat1, lon1, lat2, lon2)
    socket = urllib.urlopen(url)
    # print socket.read()
    tinker = socket.read()
    # print tinker
    img = Image.open(io.BytesIO(tinker))
    # img.save('%f_%f.jpeg' % (lat1, lon1))
    img.save('test.jpeg')
    img.show()


if __name__ == '__main__':
    """
    ~ python getGeoInfo.py 50.625 8.43751 53.4375 11.25
    """
    try:
        lat1, lon1, lat2, lon2 = [float(argv[i]) for i in xrange(1, 5)]
        if lat1 > lat2: lat1, lat2 = lat2, lat1
        if lon1 > lon2: lon1, lon2 = lon2, lon1
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
