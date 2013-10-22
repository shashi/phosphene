#!/bin/env python
#using the wireframe module downloaded from http://www.petercollingridge.co.uk/
import wireframe3 as wireframe
import pygame
from pygame import display
from pygame.draw import *

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
           
        self.display()  
        for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
        		if event.key in key_to_function:
                		key_to_function[event.key](self)

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

if __name__ == '__main__':
    pv = ProjectionViewer(400, 300)
    cube = wireframe.Wireframe() #storing all the nodes in this wireframe object.
    empty = wireframe.Wireframe() #to storing no nodes except the cube ones. 
    cube.addNodes([(x,y,z) for x in (50,150) for y in (50,150) for z in (50,150)]) #adding the nodes of the cube framework. 
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)]) #creating edges of the cube framework.
    #empty.addNodes([(x,y,z) for x in (50,150) for y in (50,150) for z in (50,150)]) #adding the nodes of the cube framework. 
    #empty.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)]) #creating edges of the cube framework.
    for j in range(0,11):
	for k in range(0,11):
	
		allon = [(50+10*j,50+10*k,50)] + [(50+10*j,50+10*k,150)] + [(50,50+10*j,50+10*k)] + [(150,50+10*j,50+10*k)] + [(50+10*j,50,50+10*k)] + [(50+10*j,150,50+10*k)] 
		cube.addNodes(allon)
    for k in range(1,11111111): #just to make it happen for some time. 
   	if k%100>=50:                            #Will make it flash from fully lit to nothing lit
        	pv.addWireframe('cube', cube) 
    		pv.run()
        else:
    		pv.addWireframe('cube',empty)
    		pv.run()
        
		 
