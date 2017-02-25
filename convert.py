import math

#define the Radius of Earth
EarthRadius = 6378137;
#in Bing Maps Tile System, the maximum latitude shown is 85.05112878 degrees
MinLatitude = -85.05112878;
MaxLatitude = 85.05112878;
#define the range of longitude
MinLongitude = -180;
MaxLongitude = 180;

def clip(inputVal, minVal, maxVal):
	"""
	if the input exceeds the min/max value, clip it into min/max value
	"""
	return min(max(inputVal,minVal),maxVal)


def LatLong2PixelXY(latitude, longitude,level):
	"""
	Converts a point from latitude/longitude WGS-84 coordinates (in degrees)
	into pixel XY coordinates at a specified level of detail.
	"""
	latitude=float(latitude)
	longitude=float(longitude)
	latitude=clip(latitude,MinLatitude,MaxLatitude)
	longitude=clip(longitude,MinLongitude,MaxLongitude)

	x=(longitude+180)/360
	sinLatitude=math.sin(latitude*math.pi/180)
	y=0.5-math.log((1+sinLatitude)/(1-sinLatitude))/(4*math.pi)

	# print level
	mapSize=256*(2**level)
	pixelX=int(clip(x*mapSize+0.5,0,mapSize-1))
	pixelY=int(clip(y*mapSize+0.5,0,mapSize-1))

	return pixelX,pixelY


def PixelXY2TileXY(pixleX,pixelY):
	"""
	Converts pixel XY coordinates into
	tile XY coordinates of the tile containing the specified pixel.
	"""
	tileX=int(pixleX/256)
	tileY=int(pixelY/256)
	return tileX,tileY


def TileXYtoQuadKey(tileX, tileY, level):
	"""
	Converts tile XY coordinates into
	a QuadKey at a specified level of detail.
	"""
	quad=""
	for i in xrange(level,0,-1):
		digit='0'
		mask=(1<<(i-1))&0xffffffff
		if (tileX&mask)!=0:
			digit=chr(ord(digit) + 1)
		if (tileY&mask)!=0:
			digit = chr(ord(digit) + 1)
			digit = chr(ord(digit) + 1)
		quad+=digit
	return quad


def LatLong2TileXY(lat, lon, level):
	"""
	Convert latitude/longitude into tileXY coordinates of tile
	containing the specified point
	"""
	pixelX,pixelY=LatLong2PixelXY(lat,lon,level)
	return PixelXY2TileXY(pixelX,pixelY)


def LatLong2QuadKey(lat,lon,level):
	"""
	input:
	latitude, longitude,level
	return:
	quadkey
	"""
	lat=clip(lat,MinLatitude,MaxLatitude)
	lon=clip(lon,MinLongitude,MaxLongitude)
	# pixelX,pixelY=LatLong2PixelXY(lat,lon,level)
	#
	# tileX,tileY=PixelXY2TileXY(pixelX,pixelY)
	tileX,tileY = LatLong2TileXY(lat,lon,level)
	quad=TileXYtoQuadKey(tileX,tileY,level)
	return quad


if __name__ == '__main__':
	print LatLong2QuadKey(2000,0.0,3)
