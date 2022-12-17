# Fractal Terrain Generator
# (c) 2017 Kevin Roche

# User-defined parameters
d = 5 # detail (integer from 0 to 9, inclusive)
r = 1.0 # roughness of terrain (decimal from 0 to 1, inclusive)

# Move the mouse to pan across the image
# Click to generate a new terrain

def setup():
    import math
    global heights
    heights = [[0 for x in range(2**d)] for y in range(2**d)]  # array to represent heights of vertices
    size(800, 600, P3D)
    stroke(0, 0, 0)
    camera(-350, 100, -350, 0, -80, 0, 0, -1, 0)
    generate() # generate an initial height map

def draw():
    background(255, 255, 255)
    render() # draw the terrain on screen
    
def render():
    sf = 512 / 2**d # scale factor to account for differing amounts of detail
    
    for i in range(2**d):
        for j in range(2**d):
            beginShape() # draw a quadrilateral with the appropriate dimensions
            vertex(i*sf - 256, heights[i][j]*sf, j*sf - 256)
            vertex((i+1)*sf - 256, heights[(i+1)%(2**d)][j]*sf, j*sf - 256)
            vertex((i+1)*sf - 256, heights[(i+1)%(2**d)][(j+1)%(2**d)]*sf, (j+1)*sf - 256)
            vertex(i*sf - 256, heights[i][(j+1)%(2**d)]*sf, (j+1)*sf - 256)
            vertex(i*sf - 256, heights[i][j]*sf, j*sf - 256)
            endShape()

def mouseMoved():
    camera(-350, mouseY, -350, 0, -80, 0, 0, -1, 0) # pan the camera

def mouseClicked():
    global heights
    heights = [[0 for x in range(2**d)] for y in range(2**d)]  # array to represent heights of vertices
    generate() # generate a new height map

def displaceHorizontalEdge(xc, yc, step):
    global heights, d
    heights[yc][xc] = (heights[yc][(xc - step / 2) % (2**d)] +
                       heights[yc][(xc + step / 2) % (2**d)]) / 2 + random(-1, 1) * step / 4 * r

def displaceVerticalEdge(xc, yc, step):
    global heights, d
    heights[yc][xc] = (heights[(yc - step / 2) % (2**d)][xc] +
                       heights[(yc + step / 2) % (2**d)][xc]) / 2 + random(-1, 1) * step / 4 * r

def displaceCenter(xc, yc, step):
    global heights, d
    heights[yc][xc] = (heights[(yc - step / 2) % (2**d)][(xc - step / 2) % (2**d)] +
                       heights[(yc + step / 2) % (2**d)][(xc - step / 2) % (2**d)] +
                       heights[(yc - step / 2) % (2**d)][(xc + step / 2) % (2**d)] +
                       heights[(yc + step / 2) % (2**d)][(xc + step / 2) % (2**d)]) / 4 + random(-1, 1) * step / 4 * r

def generate():
    for iteration in range(1, d+1):
        step = 2**(d - iteration + 1) # how much we increment by when iterating on this iteration
        
        # displace across rows
        ycursor=0
        for j in range(2**(iteration - 1)): # iterate through
            xcursor = 2**(d - iteration)
            for i in range(2**(iteration - 1)):
                displaceHorizontalEdge(xcursor, ycursor, step)
                xcursor += step
            ycursor += step
        
        # displace down columns
        xcursor=0
        for i in range(2**(iteration - 1)):
            ycursor = 2**(d - iteration)
            for j in range(2**(iteration - 1)):
                displaceVerticalEdge(xcursor, ycursor, step)
                ycursor += step
            xcursor += step
        
        # displace centers
        ycursor = xcursor = 2**(d - iteration)
        for i in range(2**(iteration - 1)):
            ycursor = 2**(d - iteration)
            for j in range(2**(iteration - 1)):
                displaceCenter (xcursor, ycursor, step)
                ycursor += step
            xcursor += step

        iteration += 1