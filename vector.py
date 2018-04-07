from operator import add, sub
import math

def origin():
    return [0.0, 0.0, 0.0]

def apply(v1, v2, operator):
    return list(map(lambda v: operator(v[0], v[1]), zip(v1, v2)))

def add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]
    #return apply(v1, v2, add)

def subtract(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]
    #return apply(v1, v2, sub)

def length(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def normalize(v):
    l = length(v)
    return [v[0] / l, v[1] / l, v[2] / l]

def scale(v, s):
    return [v[0] * s, v[1] * s, v[2] * s]

def dot_product(v1, v2):
    return sum([v1[0] * v2[0], v1[1] * v2[1], v1[2] * v2[2]])
