from devices.cubelib import emulator
from devices.cubelib import mywireframe as wireframe
from devices.animations import *

pv = emulator.ProjectionViewer(640,480)
wf = wireframe.Wireframe()

def cubeProcess(cube, signal, count):
    pv.createCube(wf)
    start = (0, 0, 0)
    point = (0,0)
    #planeBounce(cube,(count/20)%2+1,count%20)
    #start = wireframeExpandContract(cube,start)
    #rain(cube,count,5,10)
    #time.sleep(.1)
        #point = voxel(cube,count,point)
    #sine_wave(cube,count)
    #pyramids(cube,count)
    #side_waves(cube,count)
    #fireworks(cube,4)
    technites(cube,count)
    cube.redraw(wf, pv)
    return count + 1
