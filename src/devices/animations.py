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
    print "start:",START,"end:",END
    for x in range(0,cube.dimension):
        for y in range(0,cube.dimension):
                for z in range(0,cube.dimension):
                        cube.set_led(x,y,z,0)
    for x in (x0,x1):
        for y in (y0,y1):
            if z0<z1:
                for z in range(z0,z1+1):
                    cube.set_led(x,y,z)
		    print x,y,z, "set-1st condition"
            else:
                for z in range(z1,z0+1):
                    cube.set_led(x,y,z)
		    print x,y,z, "set-2nd condition"
    for x in (x0,x1):
        for z in (z0,z1):
            if y0<y1:
                for y in range(y0,y1+1):
                    cube.set_led(x,y,z)
		    print x,y,z, "Set - 1st"
            else:
                for y in range(y1,y0+1):
                    cube.set_led(x,y,z)
		    print x,y,z, "Set - 2nd"

    for y in (y0,y1):
        for z in (z0,z1):
            if x0<x1:
                for x in range(x0,x1+1):
                    cube.set_led(x,y,z)
		    print x,y,z, "SET - 1st"
            else:
                for x in range(x1,x0+1):
                    cube.set_led(x,y,z)
                    print x,y,z, "SET - 2nd"

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
    shiftCube(cube,3,1)
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
    return numpy.sqrt((x0-x1)**2 + (y0-y1)**2)

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
     if counter%9==0:
         x = random.choice([i for i in range(0,cube.dimension)])
         y = random.choice([i for i in range(0,cube.dimension)])
     if cube.get_led(x,y,counter%9)==1:
	     cube.set_led(x,y,counter%9+1)
	     cube.set_led(x,y,counter%9,0)
     else:
         cube.set_led(x,y,8-(counter%9))
         cube.set_led(x,y,9-(counter%9),0)
     return (x,y)

def shiftCube(cube,axis,delta):
       
      for x in range(0,10):
        for y in range(0,10):
            for z in range(0,9):
                if axis == 3:
                    cube.set_led(x,y,z,cube.get_led(x,y,z+delta))
                    cube.set_led(x,y,z+delta,0)
                elif axis == 2:
                    cube.set_led(x,z,y,cube.get_led(x,z+delta,y))
                    cube.set_led(x,y,z+delta,0)
                elif axis == 1:
                    cube.set_led(z,x,y,cube.get_led(z+delta,x,y))
                    cube.set_led(z+delta,x,y,0)


def pyramids(cube,counter,axis = 3):
    if(counter%20 <cube.dimension):
        size = counter%10 + 1
        setPlane(cube,axis,cube.dimension-1,square(cube,counter%10 + 1,((cube.dimension-counter%10-1)/2,(cube.dimension-counter%10-1)/2)))
        shiftCube(cube,axis,1)
    else:
	size = 9 - (counter-10)%10
	translate = (cube.dimension - size)/2
        setPlane(cube,axis,cube.dimension-1,square(cube,size,(translate,translate)))
	shiftCube(cube,axis,1)
    time.sleep(0)
    print "counter = ",counter,"size=",size

def sine_wave(cube,counter):
    fillCube(cube,0)
    center = (cube.dimension-1)/2.0
    for x in range(0,cube.dimension):
	for y in range(0,cube.dimension):
            dist = distance((x,y),(center,center))
	    cube.set_led(x,y,int(counter%10+numpy.sin(dist+counter)))

def side_waves(cube,counter):
    fillCube(cube,0)
    origin_x=4.5;
    origin_y=4.5;
    for x in range(0,10):
	for y in range(0,10):
            origin_x=numpy.sin(counter);
            origin_y=numpy.cos(counter);
            z=int(numpy.sin(numpy.sqrt(((x-origin_x)*(x-origin_x))+((y-origin_y)*(y-origin_y))))+counter%10);
            cube.set_led(x,y,z);

def fireworks(cube,n):
    origin_x = 3;
    origin_y = 3;
    origin_z = 3;
    #Particles and their position, x,y,z and their movement,dx, dy, dz
    origin_x = random.choice([i for i in range(0,4)])
    origin_y = random.choice([i for i in range(0,4)])
    origin_z = random.choice([i for i in range(0,4)])
    origin_z +=5;
    origin_x +=2;
    origin_y +=2;
    particles = [[None for _ in range(6)] for _ in range(n)]
    print particles
    #shoot a particle up in the air value was 600+500
    for e in range(0,origin_z):
        cube.set_led(origin_x,origin_y,e,1);
	time.sleep(.05+.02*e);
        cube.redraw()
	fillCube(cube,0)
    for f in range(0,n):
        #Position
        particles[f][0] = origin_x
	particles[f][1] = origin_y
	particles[f][2] = origin_z
	rand_x = random.choice([i for i in range(0,200)])
	rand_y = random.choice([i for i in range(0,200)])
	rand_z = random.choice([i for i in range(0,200)])

	try:
	    #Movement
            particles[f][3] = 1-rand_x/100.0  #dx
            particles[f][4] = 1-rand_y/100.0  #dy
            particles[f][5] = 1-rand_z/100.0  #dz
	except:
	    print "f:",f
    #explode
    for e in range(0,25):
        slowrate = 1+numpy.tan((e+0.1)/20)*10
        gravity = numpy.tan((e+0.1)/20)/2
        for f in range(0,n):
            particles[f][0] += particles[f][3]/slowrate
            particles[f][1] += particles[f][4]/slowrate
            particles[f][2] += particles[f][5]/slowrate;
            particles[f][2] -= gravity;
            cube.set_led(int(particles[f][0]),int(particles[f][1]),int(particles[f][2]))
    time.sleep(1000)

def T():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
    for i in range(3,7):
        for j in range(3,10):	        
            plane[i][j] = 1
    return plane

def E():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
	for j in range(4,7):
	    plane[i][j] = 1
	for j in range(8,10):
            plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    return plane

def B():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,2):
	    plane[i][j] = 1	
	for j in range(4,6):
	    plane[i][j] = 1
	for j in range(8,10):
            plane[i][j] = 1
    for j in range(0,10):
        for i in range(0,3):	        
            plane[i][j] = 1
	for i in range(7,10):
	    plane[i][j] = 1	    
    plane[9][0] = 0
    plane[9][9] = 0
    return plane

def A():
    plane = numpy.array([[0]*10] *10) 
    for i in range(0,10):
        for j in range(0,2):
	    plane[i][j] = 1	
	for j in range(4,7):
	    plane[i][j] = 1
    for j in range(0,10):
        for i in range(0,3):	        
            plane[i][j] = 1
	for i in range(7,10):
	    plane[i][j]	= 1    
    return plane

def C():
    plane = numpy.array([[0]*10] *10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
	for j in range(7,10):
            plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    return plane

def D():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,2):
	    plane[i][j] = 1	
	for j in range(8,10):
            plane[i][j] = 1
    for j in range(0,10):
        for i in range(0,2):	        
            plane[i][j] = 1
	for i in range(8,10):
            plane[i][j] = 1
    plane[9][0] = 0
    plane[9][9] = 0 
    return plane
def F():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
	for j in range(4,7):
	    plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    return plane

def H():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):	
	for j in range(4,7):
	    plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    for i in range(7,10):
        for j in range(0,10):	        
            plane[i][j] = 1
    return plane

def G():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
	for j in range(7,10):
            plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    for i in range(7,10):
        for j in range(4,10):
	    plane[i][j] = 1
    for i in range(4,10):
        for j in range(4,6):
            plane[i][j] = 1
    return plane

def J():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
    for i in range(3,7):
        for j in range(3,10):	        
            plane[i][j] = 1
    for i in range(0,3):
	for j in range(7,10):
            plane[i][j] = 1
    return plane

def K():
    plane = numpy.array([[0]*10]*10)
    for j in range(0,10):
	for i in range(0,2):
            plane[i][j] = 1
    for i in range(0,10):
	for j in range(0,10):
	     if(i == j):
	        plane[i][5+j/2] = 1
                try:
                    plane[i-1][4+j/2] = 1
                    plane[i+1][4+j/2] = 1
		except:
		    print "Blaaah"
	     
	     if(i+j==9):
	        plane[i][j/2] = 1
                try:
                    plane[i-1][j/2] = 1
                    plane[i+1][j/2] = 1
		except:
		    print "Blaaah"
    plane[9][5] = 0
    plane[9][4] = 0
    return plane

def L():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):	
	for j in range(7,10):
            plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    return plane

def M():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,2):
        for j in range(0,10):
	    plane[i][j] = 1
    for i in range(8,10):
        for j in range(0,10):
            plane[i][j] = 1
    #for i in range(4,7):
	#for j in range(0,10):
	 #   plane[i][j] = 1
    for i in range(0,10):
        for j in range(0,10):
            if(i == j):
	        plane[i/2][j] = 1
                try:
                    plane[i/2][j-1] = 1
                    plane[i/2][j+1] = 1
		except:
		    print "Blaaah"
            if(i+j==9):
	        plane[5 + i/2][j] = 1
                try:
                    plane[5+i/2][j-1] = 1
                    plane[5+i/2][j+1] = 1
		except:
		    print "Blaaah"

    return plane

def N():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,3):
        for j in range(0,10):
	    plane[i][j] = 1
    for i in range(7,10):
        for j in range(0,10):
            plane[i][j] = 1
    for i in range(0,10):
        for j in range(0,10):
            if(i == j):
	        plane[i][j] = 1
                try:
                    plane[i][j-1] = 1
                    plane[i][j+1] = 1
		except:
		    print "Blaaah"
    return plane

def O():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
	for j in range(7,10):
            plane[i][j] = 1
    for j in range(0,10):
        for i in range(0,3):	        
            plane[i][j] = 1
        for i in range(7,10):
            plane[i][j] = 1
    return plane

def P():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,2):
	    plane[i][j] = 1	
	for j in range(4,7):
	    plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    for i in range(7,10):
        for j in range(0,4):
            plane[i][j] = 1
    return plane

def Q():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,2):
	    plane[i][j] = 1	
	for j in range(8,10):
            plane[i][j] = 1
    for j in range(0,10):
        for i in range(0,2):	        
            plane[i][j] = 1
        for i in range(8,10):
            plane[i][j] = 1
    for i in range(5,10):
        for j in range(5,10):
            if(i == j):
	        plane[i][j] = 1
                try:
                    plane[i][j-1] = 1
                    plane[i][j+1] = 1
		except:
		    print "Blaaah"
 
    return plane

def R():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
	for j in range(4,6):
	    plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,10):	        
            plane[i][j] = 1
    for i in range(7,10):
        for j in range(0,4):
            plane[i][j] = 1
    for i in range(0,10):
	for j in range(0,10):
	     if(i == j):
	        plane[i][5+j/2] = 1
                try:
                    plane[i-1][4+j/2] = 1
                    plane[i+1][4+j/2] = 1
		except:
		    print "Blaaah"

    return plane


def I():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1
	for j in range(7,10):
            plane[i][j] = 1		
    for i in range(3,7):
        for j in range(3,10):	        
            plane[i][j] = 1
    
    return plane

def S():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,3):
	    plane[i][j] = 1	
	for j in range(4,7):
	    plane[i][j] = 1
	for j in range(8,10):
            plane[i][j] = 1
    for i in range(0,3):
        for j in range(0,7):	        
            plane[i][j] = 1
    for i in range(7,10):
	for j in range(4,10):
	    plane[i][j] = 1
    return plane

def U():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):	
	for j in range(7,10):
            plane[i][j] = 1
    for j in range(0,10):
        for i in range(0,3):	        
            plane[i][j] = 1
	for i in range(7,10):
            plane[i][j] = 1
    return plane

def V():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,10):
        for j in range(0,10):
            if(i == j):
	        plane[i/2][j] = 1
                try:
                    plane[i/2][j-1] = 1
                    plane[i/2][j+1] = 1
		except:
		    print "Blaaah"
            if(i+j==9):
	        plane[5 + i/2][j] = 1
                try:
                    plane[5+i/2][j-1] = 1
                    plane[5+i/2][j+1] = 1
		except:
		    print "Blaaah"
    plane[0][9] = 0
    plane[9][9] = 0
    return plane

def W():
    plane = numpy.array([[0]*10] * 10) 
    for i in range(0,2):
        for j in range(0,10):
	    plane[i][j] = 1
    for i in range(8,10):
        for j in range(0,10):
            plane[i][j] = 1
    #for i in range(4,7):
	#for j in range(0,10):
	 #   plane[i][j] = 1
    for i in range(0,10):
        for j in range(0,10):
            if(i == j):
	        plane[5+i/2][j] = 1
                try:
                    plane[5+i/2][j+2] = 1
                    plane[5+i/2][j+1] = 1
		except:
		    print "Blaaah"
            if(i+j==9):
	        plane[i/2][j] = 1
                try:
                    plane[i/2][j+2] = 1
                    plane[i/2][j+1] = 1
		except:
		    print "Blaaah"

    return plane
def X():
    plane = numpy.array([[0]*10]*10)
    for i in range(0,10):
        for j in range(0,10):
            if(i == j):
	        plane[i][j] = 1
                try:
                    plane[i][j-1] = 1
                    plane[i][j+1] = 1
		except:
		    print "Blaaah"
            if(i+j == 9):
                plane[i][j] = 1
                try:
                    plane[i][j-1] = 1
                    plane[i][j+1] = 1
		except:
		    print "Blaaah"

    return plane

def Y():
    plane = numpy.array([[0]*10]*10)
    for i in range(0,10):
        for j in range(0,5):
            if(i == j):
	        plane[i][j] = 1
                try:
                    plane[i][j-1] = 1
                    plane[i][j+1] = 1
		except:
		    print "Blaaah"
            if(i+j == 9):
                plane[i][j] = 1
                try:
                    plane[i][j-1] = 1
                    plane[i][j+1] = 1
		except:
		    print "Blaaah"
    for i in range(4,6):
	for j in range(5,10):
            plane[i][j] = 1
    plane[0][9] = 0
    plane[0][0] = 0
    return plane

def Z():
    plane = numpy.array([[0]*10]*10)
    for i in range(0,10):
        for j in range(0,10):
            if(i+j == 9):
                plane[i][j] = 1
                try:
                    plane[i][j-1] = 1
                    plane[i][j+1] = 1
		except:
		    print "Blaaah"
    for i in range(0,10):
	for j in range(0,3):
	    plane[i][j] = 1
	for j in range(7,10):
	    plane[i][j] = 1
    return plane

def stringPrint(cube,string,counter=0,axis = 3):
	if counter%10 ==0:
		fillCube(cube,0)
		i = string[(counter/10)%len(string)]
		if i == 'A':
			setPlane(cube,axis,9,A())
    		elif i == 'B':
    			setPlane(cube,axis,9,B())
		elif i == 'C':
			setPlane(cube,axis,9,C())
		elif i == 'D':
			setPlane(cube,axis,9,D())
		elif i == 'E':
			setPlane(cube,axis,9,E())
		elif i == 'F':
			setPlane(cube,axis,9,F())
		elif i == 'G':
			setPlane(cube,axis,9,G())
		elif i == 'H':
			setPlane(cube,axis,9,H())
		elif i == 'I':
			setPlane(cube,axis,9,I())
		elif i == 'J':
			setPlane(cube,axis,9,J())
		elif i == 'K':
			setPlane(cube,axis,9,K())
		elif i == 'L':
			setPlane(cube,axis,9,L())
		elif i == 'M':
			setPlane(cube,axis,9,M())
		elif i == 'N':
			setPlane(cube,axis,9,N())
		elif i == 'O':
			setPlane(cube,axis,9,O())
		elif i == 'P':
			setPlane(cube,axis,9,P())
		elif i == 'Q':
			setPlane(cube,axis,9,Q())
		elif i == 'R':
			setPlane(cube,axis,9,R())
		elif i == 'S':
			setPlane(cube,axis,9,S())
		elif i == 'T':
			setPlane(cube,axis,9,T())
		elif i == 'U':
			setPlane(cube,axis,9,U())
		elif i == 'V':
			setPlane(cube,axis,9,V())
		elif i == 'W':
			setPlane(cube,axis,9,W())
		elif i == 'X':
			setPlane(cube,axis,9,X())
		elif i == 'Y':
			setPlane(cube,axis,9,Y())
		elif i == 'Z':
			setPlane(cube,axis,9,Z())
	else:
		shiftCube(cube,axis,1)

def stringfly(cube,axis):
    shiftCube(cube,axis,1)

def technites(cube,counter,axis = 3):
	alpha = counter/9
	if(counter%90 == 0): 
	    fillCube(cube,0)
	    setPlane(cube,axis,9,T(cube))
        elif(counter%90 == 10):
	    fillCube(cube,0)
            setPlane(cube,axis,9,E(cube))
	elif(counter%90 == 20):
	    fillCube(cube,0)
            setPlane(cube,axis,9,C(cube))
	elif(counter%90 == 30):
	    fillCube(cube,0)
            setPlane(cube,axis,9,H(cube))
	elif(counter%90 == 40):
	    fillCube(cube,0)
            setPlane(cube,axis,9,N(cube))
        elif(counter%90 == 50):
	    fillCube(cube,0)
            setPlane(cube,axis,9,I(cube))
	elif(counter%90 == 60):
	    fillCube(cube,0)
            setPlane(cube,axis,9,T(cube))    
        elif(counter%90 == 70):
	    fillCube(cube,0)
            setPlane(cube,axis,9,E(cube))
	elif(counter%90 == 80):
	    fillCube(cube,0)
            setPlane(cube,axis,9,S(cube))
        else:
	    stringfly(cube,axis)
def moveFaces(cube):
	Z0 = numpy.array([[0]*cube.dimension]*cube.dimension)
	Z9 = numpy.array([[0]*cube.dimension]*cube.dimension)
	X0 = numpy.array([[0]*cube.dimension]*cube.dimension)
	X9 = numpy.array([[0]*cube.dimension]*cube.dimension)
	for i in range(1,cube.dimension):
	    for j in range(0,cube.dimension):
		X0[i-1][j] = cube.get_led(i,j,0)
	for j in range(0,cube.dimension):
	    X0[9][j] = cube.get_led(9,j,0)
        
	for i in range(0,cube.dimension-1):
	    for j in range(0,cube.dimension):
		Z0[i+1][j] = cube.get_led(0,j,i)

	for j in range(0,cube.dimension):
	    Z0[0][j] = cube.get_led(0,j,0)
     
	for i in range(0,cube.dimension-1):
	    for j in range(0,cube.dimension):
		X9[i+1][j] = cube.get_led(i,j,9)
	for j in range(0,cube.dimension):
	    X9[0][j] = cube.get_led(0,j,9)

        for i in range(1,cube.dimension):
	    for j in range(0,cube.dimension):
		Z9[i-1][j] = cube.get_led(9,j,i)

	for j in range(0,cube.dimension):
	    Z9[9][j] = cube.get_led(9,j,9)
	fillCube(cube,0)
	setPlane(cube,3,0,X0)
	setPlane(cube,1,0,Z0)
	setPlane(cube,3,9,X9)
	setPlane(cube,1,9,Z9)

