
from cubelib import mywireframe
from cubelib import emulator
import random
import time
def wireframeCubeCenter(cube,size,CUBE_SIZE = 10):
        if size % 2 == 1:
                size = size+1
        half = size/2
        start = CUBE_SIZE/2 - half
        end = CUBE_SIZE/2 + half - 1
        for x in range(0,CUBE_SIZE):
		for y in range(0,CUBE_SIZE):
			for z in range(0,CUBE_SIZE):
				cube.set_led(x,y,z,0)
	for x in (start,end):
		for y in (start,end):
			for z in range(start,end+1):
				cube.set_led(x,y,z)
				cube.set_led(x,z,y)
				cube.set_led(z,x,y)

def wireframeCube(cube,START,END,CUBE_SIZE = 10):
        x0,y0,z0 = START
	x1,y1,z1 = END
        for x in range(0,CUBE_SIZE):
                for y in range(0,CUBE_SIZE):
                        for z in range(0,CUBE_SIZE):
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

def solidCubeCenter(cube,size,CUBE_SIZE = 10):
        if size % 2 == 1:
                size = size+1
        half = size/2 
	start = CUBE_SIZE/2 - half
        end = CUBE_SIZE/2 + half
	for x in range(0,CUBE_SIZE):
                for y in range(0,CUBE_SIZE):
                        for z in range(0,CUBE_SIZE):
                                cube.set_led(x,y,z,0)
        for i in range(start,end):
                for j in range(start,end):
                        for k in range(start,end):
				cube.set_led(i,j,k)

def solidCube(cube,START,END,CUBE_SIZE = 10):
        x0,y0,z0 = START
        x1,y1,z1 = END
	for x in range(0,CUBE_SIZE):
                for y in range(0,CUBE_SIZE):
                        for z in range(0,CUBE_SIZE):
                                cube.set_led(x,y,z,0)
	for i in range(x0,x1+1):
                for j in range(y0,y1+1):
                        for k in range(z0,z1+1):
                                cube.set_led(i,j,k)

def setPlane(cube,axis,x,level = 1,CUBE_SIZE = 10):
	if axis == 1:
		for i in range(0,CUBE_SIZE):
			for j in range(0,CUBE_SIZE):
				cube.set_led(x,i,j,level)
	elif axis == 2:
		for i in range(0,CUBE_SIZE):
                        for j in range(0,CUBE_SIZE):
                                cube.set_led(i,x,j,level)
	else :
		for i in range(0,CUBE_SIZE):
                        for j in range(0,CUBE_SIZE):
                                cube.set_led(i,j,x,level)


def wireframeExpandContract(cube,CUBE_SIZE = 10):
	max_coord = CUBE_SIZE - 1
	corners = [0,max_coord]
	x0 = random.choice(corners)
	y0 = random.choice(corners)
	z0 = random.choice(corners)
	for i in range(0,CUBE_SIZE):
		j = CUBE_SIZE - i - 1
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
		time.sleep(.1)
	x0 = random.choice(corners)
        y0 = random.choice(corners)
        z0 = random.choice(corners)

	for j in range(0,CUBE_SIZE):
                i = CUBE_SIZE - j - 1
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
		time.sleep(.1)

def rain(cube,iterations=1000,CUBE_SIZE = 10):
	for x in range(0,CUBE_SIZE):
                for y in range(0,CUBE_SIZE):
                        for z in range(0,CUBE_SIZE):
                                cube.set_led(x,y,z,0)
	for i in range(0,iterations):
		number = random.choice([1,2])
		for j in range(0,number+1):
			x = random.choice([i for i in range(0,10)])
			y = random.choice([i for i in range(0,10)])
			cube.set_led(x,y,9)
		time.sleep(.1)
		cube.redraw()
		for x in range(0,10):
			for y in range(0,10):
				for z in range(0,9):
					cube.set_led(x,y,z,cube.get_led(x,y,z+1))
					cube.set_led(x,y,z+1,0)	

def planeBounce(cube,axis=1,repeat = False,CUBE_SIZE = 10):
	
	for i in range(0,CUBE_SIZE):
		setPlane(cube,axis,i)
		cube.redraw()
		time.sleep(.1)
		setPlane(cube,axis,i,0)
	for i in range(1,CUBE_SIZE+1):
		j = CUBE_SIZE - i
                setPlane(cube,axis,j)
                cube.redraw()
                time.sleep(.1)
                setPlane(cube,axis,j,0)
	if(repeat):
		planeBounce(cube,random.choice([1,2,3]),True)

