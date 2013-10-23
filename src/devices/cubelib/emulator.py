#!/bin/env python
#using the wireframe module downloaded from http://www.petercollingridge.co.uk/
import mywireframe as wireframe
import pygame
from pygame import display
from pygame.draw import *
import time
import numpy

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
    pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
    pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
    pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
    pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
    pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
    pygame.K_q:      (lambda x: x.rotateAll('X',  0.1)),
    pygame.K_w:      (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a:      (lambda x: x.rotateAll('Y',  0.1)),
    pygame.K_s:      (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z:      (lambda x: x.rotateAll('Z',  0.1)),
    pygame.K_x:      (lambda x: x.rotateAll('Z', -0.1))}

class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 3  #Modify to change size of the spheres

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):   
        for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
        		if event.key in key_to_function:
                		key_to_function[event.key](self)

        self.display()
        pygame.display.flip()
        
    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    if node.visiblity:
                           pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)

    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.itervalues():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        for wireframe in self.wireframes.itervalues():
            wireframe.scale((centre_x, centre_y), scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.itervalues():
            centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre, theta)
    
    def createCube(self,cube,X=[50,140], Y=[50,140], Z=[50,140]):
        cube.addNodes([(x,y,z) for x in X for y in Y for z in Z]) #adding the nodes of the cube framework. 
        allnodes = []
    	cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)]) #creating edges of the cube framework.
    	for i in range(0,10):
        	for j in range(0,10):
                	for k in range(0,10):
                        	allnodes.append((X[0]+(X[1]-X[0])/9 * i,Y[0]+(Y[1] - Y[0])/9 * j,Z[0] + (Z[1]-Z[0])/9 * k))

    	cube.addNodes(allnodes)
    	#cube.outputNodes()
    	self.addWireframe('cube',cube)



def findIndex(coords): #Send coordinates of the points you want lit up. Will convert to neede 

	indices = []
	for nodes in coords:
		x,y,z = nodes
		index = x*100+y*10+z + 8
		indices.append(index)
	return indices

def findIndexArray(array): #Takes a 3-D numpy array containing bool of all the LED points.

	indices = []
	for i in range(0,10):
		for j in range(0,10):
			for k in range(0,10):
				if(array[i][j][k] == 1):
					index = i*100+j*10+ k + 8
					indices.append(index)
	return indices


def wireframecube(size):
	if size % 2 == 1:
		size = size+1
	half = size/2
	start = 5 - half
	end = 5 + half - 1
	cubecords = [(x,y,z) for x in (start,end) for y in (start,end) for z in range(start,end+1)]+[(x,z,y) for x in (start,end) for y in (start,end) for z in range(start,end+1)] + [(z,y,x) for x in (start,end) for y in (start,end) for z in range(start,end+1)]
	return cubecords

def cubes(size):
	if size % 2 == 1:
		size = size+1
	half = size/2
	cubecords = []
	for i in range(0,size):
		for j in range(0,size):
			for k in range(0,size):
				cubecords.append((5-half+i,5-half+j,5-half+k))	
	return cubecords
if __name__ == '__main__':
    
    pv = ProjectionViewer(400, 300)
    allnodes =[]
    cube = wireframe.Wireframe() #storing all the nodes in this wireframe object.
    X = [50,140]
    Y = [50,140]
    Z = [50,140] 
    pv.createCube(cube,X,Y,Z)
    YZface = findIndex((0,y,z) for y in range(0,10) for z in range(0,10)) 
    count = 0 
    for k in range(1,150000):
	if k%5000 ==2500:
		count = (count+2)%11                        
		cube.setVisible(findIndex(wireframecube(count)))
	pv.run()
		
