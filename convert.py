import math

EarthRadius = 6378137;
MinLatitude = -85.05112878;
MaxLatitude = 85.05112878;
MinLongitude = -180;
MaxLongitude = 180;


def clip(inputVal, minVal, maxVal):
	"""
	clip the input longitude and latitude
	"""
	return min(max(inputVal,minVal),maxVal)


def LatLong2PixelXY(latitude, longitude,level):
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
	tileX=int(pixleX/256)
	tileY=int(pixelY/256)
	return tileX,tileY


def TileXYtoQuadKey(tileX, tileY, level):
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
