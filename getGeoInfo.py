from sys import argv
import urllib
from PIL import Image
from convert import *
import io

LICENCE_KEY = 'AhHPXuVNzco40xVgSzCMz6TmC589Zlp-F2_Wj065PQW1Cr0SyOLC_EoyMEnJZ6Lx'
LICENCE_PARAM = 'key=%s' % LICENCE_KEY

RESOLUTION_UPBOUND = 23 # resolution level upper bound, defined by Bing Maps REST Services

TILE_SIZE = 2 ** 8  # Tile size deside how small should we compress tile image,
# The origial tile image is 256 * 256, so if TILE_SIZE is too small, even it will
# provide more detail, it would be meaningless since we can not render it properly
# (it will be squeezed)

# TILE_UP_BOUND = 2 ** 8    # We decide not to use this
IMG_SIZE = 2 ** 14  # If you do not want to wait so long, use smaller IMG_SIZE


def buildImage(lat1, lon1, lat2, lon2, fileName='test.jpeg'):
    """
    Main logic to generate the image, this could take about 10 mins or more,
    Given the default setting
    """

    print 'looking for common detailed level'
    currLv = calcCommonLevel(lat1, lon1, lat2, lon2)

    image = Image.new('RGB', (IMG_SIZE, IMG_SIZE))

    print 'current detailed level: %d, trying to detailing' % currLv
    x0, y0 = map(min, (zip(LatLong2TileXY(lat1, lon1, currLv), LatLong2TileXY(lat2, lon2, currLv))))
    currTileSize = IMG_SIZE / 2
    # print currTileSize

    # while currTileSize == TILE_SIZE or currTileAmount(lat1, lon1, lat2, lon2, currLv) <= TILE_UP_BOUND or currLv == RESOLUTION_UPBOUND:
    while currTileSize >= TILE_SIZE and currLv <= RESOLUTION_UPBOUND:
        print "current detail level: %d, current tile size: %dpx" % (currLv, currTileSize)
        print "\tcurrent tile amount: %d" % currTileAmount(lat1, lon1, lat2, lon2, currLv)
        x1, y1 = LatLong2TileXY(lat1, lon1, currLv)
        x2, y2 = LatLong2TileXY(lat2, lon2, currLv)

        # swap the index, if the index is not proper
        if x1 > x2: x1, x2 = x2, x1
        if y1 > y2: y1, y2 = y2, y1

        for X in xrange(x1, x2 + 1):
            for Y in xrange(y1, y2 + 1):
                try:    # sometime there might be connection problem
                    subImg = downloadImageByTileXY(X, Y, currLv).resize((currTileSize, currTileSize))
                except:
                    continue
                if isExist(subImg):
                    pX, pY = (X-x0) * currTileSize, (Y-y0) * currTileSize
                    # Paste the downloaded image to proper place
                    image.paste(subImg, (pX, pY, pX + currTileSize, pY + currTileSize))

        x0, y0 = x0 * 2, y0 * 2
        currLv += 1
        currTileSize /= 2

    # at last, we will crop the imgage to a proper place
    x0, y0 = x0 / 2, y0 / 2
    currTileSize *= 2

    p1X, p1Y = (x1-x0) * currTileSize, (y1-y0) * currTileSize
    p2X, p2Y = (x2-x0+1) * currTileSize, (y2-y0+1) * currTileSize
    print 'cropping by pixel: ' + str((p1X, p1Y, p2X, p2Y))
    image = image.crop((p1X, p1Y, p2X, p2Y))
    image.show()
    print 'image saved as %s, Cheers' % fileName
    image.save(fileName)


def isExist(subImg):
    """
    We realized, we do not actually need this, if the image is not found
    It will return a empty image, and this won't influence the result
    """
    return True


def downloadImageByTileXY(x, y, level):
    """
    Given the tile index
    return download the image
    """
    url = getURL(TileXYtoQuadKey(x, y, level))
    socket = urllib.urlopen(url)
    return Image.open(io.BytesIO(socket.read()))


def currTileAmount(lat1, lon1, lat2, lon2, currLv):
    """
    calculate how many tile are gonna be there, given current detail level
    """
    x1, y1 = LatLong2TileXY(lat1, lon1, currLv)
    x2, y2 = LatLong2TileXY(lat2, lon2, currLv)
    # print (x2 - x1 + 1) * (y2 - y1 + 1)
    # print (x2 - x1 + 1), (y2 - y1 + 1)
    return (x2 - x1 + 1) * (y1 - y2 + 1)


def calcCommonLevel(lat1, lon1, lat2, lon2):
    """
    calculate the most common level shared by rectangle,
    we will start our work from here.
    """
    for level in xrange(RESOLUTION_UPBOUND, -1, -1):
        x1, y1 = LatLong2TileXY(lat1, lon1, level)
        x2, y2 = LatLong2TileXY(lat2, lon2, level)
        # print level, x1, y1, x2, y2
        if abs(y2 - y1) <= 1 and abs(x1 - x2) <= 1:
            return level


def encode(lat1, lon1, lat2, lon2):
    """
    encode the lat, lon infor to qKey
    """
    return LatLong2QuadKey(lat1, lon1, 1)


def getURL(qKey):
    """
    URL encoder, given qKey, return the URL
    """
    return "http://h0.ortho.tiles.virtualearth.net/tiles/h%s.jpeg?g=131&%s" % (qKey, LICENCE_PARAM)


def downloadAerialImage(lat1, lon1, lat2, lon2):
    """
    download proper aerial image based on bounding rectangle
    """
    url = getURL(encode(lat1, lon1, lat2, lon2))
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
    You can try following command, or somewhere yourself.
    # Germen
    ~ python getGeoInfo.py 50.625 8.43751 53.4375 11.25
    # White house
    ~ python getGeoInfo.py 38.900386 -77.041809 38.893573 -77.027433
    # Somewhere East of New York
    ~ python getGeoInfo.py 38.857979 -75.570881 36.959861 -72.533161
    """
    try:
        lat1, lon1, lat2, lon2 = [float(argv[i]) for i in xrange(1, 5)]
        # if lat1 > lat2: lat1, lat2 = lat2, lat1
        # if lon1 > lon2: lon1, lon2 = lon2, lon1
        print 'Bounding Rectangle recognized - [%f, %f; %f, %f]\nCalculating Bounding Image...' % (lat1, lon1, lat2, lon2)
    except:
        print 'Required input:\n~ python getGeoInfo.py <lat1> <lon1> <lat2> <lon2>\nE.g.\n~ stpython aerial_image.py 50.625 8.43751 53.4375 11.25'

    # downloadAerialImage(lat1, lon1, lat2, lon2)
    buildImage(lat1, lon1, lat2, lon2)
