import vector

def create(point, radius):
    return [
        [point[0], point[1], point[2]],
        radius
    ]

def normal(sphere, point):
    return vector.normalize(vector.subtract(point, sphere[0]))

def distance_to(sphere, point):
    # direction = sphere.p - point
    # distance = length(direction) - radius
    d = vector.subtract(point, sphere[0])
    return vector.length(d) - sphere[1]
