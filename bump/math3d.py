import math

identityMatrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

def rotMatrixZ(a):
	a = math.radians(a)
	return [math.cos(a), math.sin(a), 0, 0, -math.sin(a), math.cos(a), 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

def rotMatrixY(a):
	a = math.radians(a)
	return [math.cos(a), 0, -math.sin(a), 0, 0, 1, 0, 0, math.sin(a),0,math.cos(a), 0, 0, 0, 0, 1]

def rotMatrixX(a):
	a = math.radians(a)
	return [1, 0, 0, 0, 0, math.cos(a), math.sin(a), 0, 0,-math.sin(a),math.cos(a), 0, 0, 0, 0, 1]

def transMatrix(x, y, z):
	return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, x, y, z, 1]
	
def multMatrix(a, b):
		r = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	
		for i in xrange(0, 16, 4):
			for j in xrange(0, 4, 1):
				r[i+j] = b[i]*a[j] + b[i+1]*a[j+4] + b[i+2]*a[j+8] + b[i+3]*a[j+12]
			
		return r
	
def frustumGL(l, r, b, t, n ,f):
		return [(2*n)/(r-l), 0, 0, 0,
				0, (2*n)/(t-b), 0, 0,
				(r+l)/(r-l), (t+b)/(t-b), (-1 * (f+n))/(f-n), -1.0,
				0, 0, (-2 * f * n)/(f-n), 0]
	
def perspectiveGL(fovY, aspect, zNear, zFar):
	pi = 3.1415926535897932384626433832795
	fH = math.tan( fovY / 360 * pi ) * zNear
	fW = fH * aspect
	return frustumGL( -fW, fW, -fH, fH, zNear, zFar )
	