import numpy as np
import time
from matplotlib import pyplot
import math

#manager = pyplot.get_current_fig_manager()
#manager.full_screen_toggle()

def boundary(x,y):
    if x > Nx:
        x = Nx
    if y > Ny:
        y = Ny
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return (x,y)

def fixEdges():
    print("Fixing edges...")
    for x in range(Nx):
        for y in range(Ny):
            surroundings = [field[x + 1,y +1 ],
                                field[x + 1,y],
                                field[x + 1,y - 1],
                                field[x,y + 1],
                                field[x,y],
                                field[x,y - 1],
                                field[x - 1,y + 1],
                                field[x - 1, y],
                                field[x - 1, y - 1]]
            surroundings = np.array(surroundings)
            field[x,y] = np.bincount(surroundings).argmax()

def calcCircle(r,xpos=0,ypos=0):
    points = [(0,r)]
    numangles = r ** 2 + 36
    angles = np.linspace(0,np.pi * 2,numangles)
    for theta in range(len(angles)):
        y = round(r*math.sin(angles[theta]) + ypos)
        x = round(r*math.cos(angles[theta]) + xpos)
        if points[-1] != (x,y):
            points.append((x,y))
    return points

class Circle:
    def __init__(self, xpos, ypos,id=1):
        self.xpos=xpos
        self.ypos=ypos
        self.id=id
        self.kill = False
        field[self.xpos,self.ypos] = self.id
    def fill(self,points):
        if self.kill == True:
            return None
        changedPixel = False
        for point in range(len(points)):
            x,y = boundary(points[point][0] + self.xpos,points[point][1] + self.ypos)
            if field[x,y] == 0:
                field[x,y] = self.id
                changedPixel = True
        if changedPixel == False:
            self.kill = True
        return None

def main(num_of_points):
    print('Initializing circles...')
    agentlist=[]
    r=1
    for ids in range(num_of_points):
        agentlist.append(Circle(np.random.randint(0,Nx), np.random.randint(0,Ny), id=ids+1))
    print('Growing circles...')
    for t in range(Nt):
        points = calcCircle(r)
        pyplot.gca().set_axis_off()
        pyplot.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)
        pyplot.margins(0, 0)
        pyplot.imshow(field, cmap="rainbow")
        pyplot.pause(0.001)
        pyplot.cla()
        for a in range(len(agentlist)):
            agentlist[a].fill(points)
        if np.all(field) == True:
            print('Voronoi Tesselation generated successfully.')
            break
        else:
            r+=1
            continue
        break
    del agentlist
    fixEdges()
    print("Edges fixed.")

if __name__ == "__main__":
    while True:

        Nx = 800
        Ny = 1600
        num_of_points = 1000
        Nt = 1000
        field = np.zeros((Nx + 1, Ny + 1), dtype=np.int16)

        #manager = pyplot.get_current_fig_manager()
        #manager.full_screen_toggle()
        start_time = time.time()
        main(num_of_points)
        print("Finished.")
        print("--- %s seconds ---" % (time.time() - start_time))
        pyplot.cla()
        pyplot.imshow(field, cmap="rainbow")
        time.sleep(5)
        pyplot.clf()