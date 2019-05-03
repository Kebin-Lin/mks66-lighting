import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    lhat = [light[0][:], light[1]]
    nhat = normal[:]
    vhat = view[:]
    normalize(lhat[0])
    normalize(nhat)
    normalize(vhat)
    amb = calculate_ambient(ambient, areflect)
    diff = calculate_diffuse(lhat, dreflect, nhat)
    spec = calculate_specular(lhat, sreflect, vhat, nhat)
    limit_color(amb)
    limit_color(diff)
    limit_color(spec)
    output = [amb[x] + diff[x] + spec[x] for x in range(3)]
    limit_color(output)
    return output

def calculate_ambient(alight, areflect):
    # return [0,0,0]
    return [alight[x] * areflect[x] for x in range(3)]

def calculate_diffuse(light, dreflect, normal):
    # return [0,0,0]
    return [light[1][x] * dreflect[x] * dot_product(normal, light[0]) for x in range(3)]

def calculate_specular(light, sreflect, view, normal):
    # return [0,0,0]
    ndotl = dot_product(normal, light[0])
    phatmult2 = [2 * ndotl * x for x in normal]
    rhat = [phatmult2[x] - light[0][x] for x in range(3)]
    rdotvton = dot_product(rhat, view) ** SPECULAR_EXP
    return [light[1][x] * sreflect[x] * rdotvton for x in range(3)]

def limit_color(color):
    for i in range(3):
        if color[i] < 0:
            color[i] = 0
        elif color[i] > 255:
            color[i] = 255
        else:
            color[i] = int(color[i])

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
