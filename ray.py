import vector

def create(position, direction):
    return [position, vector.normalize(direction)]
