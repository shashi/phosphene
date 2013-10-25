import numpy
import random
import time

from cubelib import mywireframe
from cubelib import emulator

# TODO:
# shiftPlane(axis, plane, delta)
#   moves the plane along the axis by delta steps, if it exceeds dimensions, just clear it out, don't rotate.
# swapPlanes(axis1, plane1, axis2, plane2)
# rain should set random LEDs on the first plane (not a lot of them)
#   and shift the plane along that axis by one step---Fixed
#   and shift the plane along that axis by one step
#
# THINK:
#   The python code keeps sending a 125 byte string to redraw the
#   cube as often as it can, this contains 1000 bit values that the MSP
#   handles. Now, in our code we have been using time.sleep() a lot.
#   We probably can have a counter that each of these functions uses to
#   advance its steps, and then increment / decrement that
#   counter according to music

def wireframeCubeCenter(cube,size):
    if size % 2 == 1:
            size = size+1

    half = size/2
    start = cube.dimension/2 - half
    end = cube.dimension/2 + half - 1

    for x in range(0,cube.dimension):
        for y in range(0,cube.dimension):
            for z in range(0,cube.dimension):
                cube.set_led(x,y,z,0)

    for x in (start,end):
        for y in (start,end):
            for z in range(start,end+1):
                cube.set_led(x,y,z)
                cube.set_led(x,z,y)
                cube.set_led(z,x,y)

def wireframeCube(cube,START,END):
    x0,y0,z0 = START
    x1,y1,z1 = END
    for x in range(0,cube.dimension):
        for y in range(0,cube.dimension):
                for z in range(0,cube.dimension):
                        cube.set_led(x,y,z,0)
    for x in (x0,x1):
        for y in (y0,y1):
            if z0<z1:
                for z in range(z0,z1+1):
                    cube.set_led(x,y,z)
            else:
                for z in range(z1,z0+1):
                    cube.set_led(x,y,z)    
    for x in (x0,x1):
        for z in (z0,z1):
            if y0<y1:
                for y in range(y0,y1+1):
                        cube.set_led(x,y,z)
            else:
                for y in range(y1,y0+1):
                    cube.set_led(x,y,z)

    for y in (y0,y1):
        for z in (z0,z1):
            if x0<x1:
                for x in range(x0,x1+1):
                    cube.set_led(x,y,z)
                else:
                    for x in range(x1,x0+1):
                        cube.set_led(x,y,z)

def solidCubeCenter(cube,size):
    if size % 2 == 1:
        size = size+1

    half = size/2 
    start = cube.dimension/2 - half
    end = cube.dimension/2 + half

    for x in range(0,cube.dimension):
        for y in range(0,cube.dimension):
            for z in range(0,cube.dimension):
                cube.set_led(x,y,z,0)

    for i in range(start,end):
        for j in range(start,end):
            for k in range(start,end):
                cube.set_led(i,j,k)

def solidCube(cube,START,END):
    x0,y0,z0 = START
    x1,y1,z1 = END

    for x in range(0,cube.dimension):
        for y in range(0,cube.dimension):
            for z in range(0,cube.dimension):
                cube.set_led(x,y,z,0)

    for i in range(x0,x1+1):
        for j in range(y0,y1+1):
            for k in range(z0,z1+1):
                cube.set_led(i,j,k)

def setPlane(cube,axis,x,level = 1):
    plane = level
    if isinstance(level, int):
        plane = numpy.array([[level]*10]*10, dtype=bool)

    if axis == 1:
        for i in range(0,cube.dimension):
            for j in range(0,cube.dimension):
                cube.set_led(x,i,j,plane[i][j])
    elif axis == 2:
        for i in range(0,cube.dimension):
            for j in range(0,cube.dimension):
                cube.set_led(i,x,j,plane[i][j])
    else:
        for i in range(0,cube.dimension):
            for j in range(0,cube.dimension):
                cube.set_led(i,j,x,plane[i][j])

def shiftPlane(cube,axis,plane,delta):
    if axis == 1:
        for i in range(0,cube.dimension):
	        for j in range(0,cube.dimension):
			try:
			    cube.set_led(plane+delta,i,j,cube.get_led(plane,i,j))
                            cube.set_led(plane,i,j,0)
			except:
			    cube.set_led(plane,i,j,0)
    elif axis == 2:
        for i in range(0,cube.dimension):
	    for j in range(0,cube.dimension):
		try:
		    cube.set_led(i,plane+delta,j,cube.get_led(i,plane,j))
                    cube.set_led(i,plane,j,0)
		except: 
		    cube.set_led(i,plane,j,0)
    else:
        for i in range(0,cube.dimension):
            for j in range(0,cube.dimension):
		try:
	            cube.set_led(i,j,plane+delta,cube.get_led(i,j,plane))
                    cube.set_led(i,j,plane,0)
                except:
		    cube.set_led(i,j,plane,0)
#def swapPlane(cube,axis,plane1,plane2):

def randPlane(cube,minimum,maximum):
    array = numpy.array([[0]*cube.dimension]*cube.dimension,dtype = 'bool')
    for i in range(minimum,maximum):
        x = random.choice([i for i in range(0,cube.dimension)]) 
        y = random.choice([i for i in range(0,cube.dimension)])   
        array[x][y] = 1
    return array
def wireframeExpandContract(cube,start=(0,0,0)):
    (x0, y0, z0) = start

    for i in range(0,cube.dimension):
        j = cube.dimension - i - 1
        if(x0 == 0):
            if(y0 == 0 and z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0+i,z0+i))
            elif(y0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0+i,z0-i))
            elif(z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0-i,z0+i))
            else:
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0-i,z0-i))
        else:
            if(y0 == 0 and z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0+i,z0+i))
            elif(y0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0+i,z0-i))
            elif(z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0-i,z0+i))
            else:
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0-i,z0-i))
        time.sleep(0.1)
	cube.redraw()    

    max_coord = cube.dimension - 1
    corners = [0,max_coord]
    x0 = random.choice(corners)
    y0 = random.choice(corners)
    z0 = random.choice(corners)
    for j in range(0,cube.dimension):
        i = cube.dimension - j - 1
        if(x0 == 0):
            if(y0 == 0 and z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0+i,z0+i))
            elif(y0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0+i,z0-i))
            elif(z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0-i,z0+i))
            else:
                wireframeCube(cube,(x0,y0,z0),(x0+i,y0-i,z0-i))
        else:
            if(y0 == 0 and z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0+i,z0+i))
            elif(y0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0+i,z0-i))
            elif(z0 == 0):
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0-i,z0+i))
            else:
                wireframeCube(cube,(x0,y0,z0),(x0-i,y0-i,z0-i))                 
        cube.redraw()
	time.sleep(0.1)
    return (x0, y0, z0) # return the final coordinate

def rain(cube,counter,minimum,maximum,axis=3):
    for x in range(0,10):
        for y in range(0,10):
            for z in range(0,9):
                cube.set_led(x,y,z,cube.get_led(x,y,z+1))
                cube.set_led(x,y,z+1,0)  
    """for i in range(1,10):
	shiftPlane(cube,axis,10-i,-1)"""
    #if counter%10 == 0:
    setPlane(cube,axis,9,randPlane(cube,minimum,maximum))


    
def planeBounce(cube,axis,counter):

    i = counter%20
    if i:
        if i<10:          #to turn off the previous plane
            setPlane(cube,axis,i-1,0)
        elif i>10:
            setPlane(cube,axis,20-i,0)
    if i<10:
        setPlane(cube,axis,i)
    elif i>10:
        setPlane(cube,axis,19-i)
      
def square(cube,size,translate=(0,0)):
    x0,y0 = translate
    array = numpy.array([[0]*cube.dimension] * cube.dimension)
    for i in range(0,size):
	    for j in range(0,size):
	        array[i+x0][j+y0] = 1
    return array

def distance(point1,point2):
    x0,y0 = point1
    x1,y1 = point2
    return (x0-x1)**2 + (y0-y1)**2

def circle(cube,radius,translate=(0,0)):
    x1,y1 = translate
    array = numpy.array([[0]*cube.dimension] * cube.dimension)
    for i in range(0,2*radius):
        for j in range(0,2*radius):
	    if distance((i,j),(radius,radius))<=radius:
		array[i+x1][j+y1] = 1
    return array

def wierdshape(cube,diagonal,translate=(0,0)):
    x1,y1 = translate
    array =  numpy.array([[0]*cube.dimension] * cube.dimension)
    if diagonal%2 == 0:
		diagonal-=1
    for y in range(0,diagonal):
		for x in range(0,diagonal):
			if(y>=diagonal/2):
				if(x<=diagonal/2):
					if(x>=y):
						array[x][y] = 1
				else:
					if(x<=y):
						array[x][y] = 1
			else:
				if(x<=diagonal/2):
					if(x+y>=diagonal/2):
						array[x][y] = 1
				else:
					if(x+y<=diagonal/2):
						array[x][y] = 1		
    return array
def fillCube(cube,level=1):
    for x in range(0,cube.dimension):
	for y in range(0,cube.dimension):
	    for z in range(0,cube.dimension):
		cube.set_led(x,y,z,level)
    
def voxel(cube,counter,point):
     x,y = point
     if(counter==0):
         fillCube(cube,0)
	 for x in range(0,cube.dimension):
            for y in range(0,cube.dimension):
    	        cube.set_led(x,y,random.choice([0,cube.dimension-1]))    
     if counter%10==0:
         x = random.choice([i for i in range(0,cube.dimension)])
         y = random.choice([i for i in range(0,cube.dimension)])
     if cube.get_led(x,y,0)==1:
	 cube.set_led(x,y,counter%10)
	 cube.set_led(x,y,(counter-1)%10,0)
     else:
	 cube.set_led(x,y,8-(counter%10))
	 cube.set_led(x,y,9-(counter)%10,0)
     return (x,y)

def sine_wave(cube,counter):
    fillCube(cube,0)
    center = (cube.dimension-1)/2.0
    for x in range(0,cube.dimension):
	for y in range(0,cube.dimension):
            dist = distance((x,y),(center,center))
	    cube.set_led(x,y,int(9*numpy.sin(dist+counter)))
	    
