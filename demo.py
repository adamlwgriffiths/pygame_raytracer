import pygame
from pygame.locals import *
import math
import vector
import matrix
import ray
import sphere


WIDTH, HEIGHT, DISTANCE = 1024, 768, 1.0
FOV = 70
ASPECT_RATIO = WIDTH / HEIGHT
PIXEL_SCALE = 5
MAX_STEPS = 15
MAX_DISTANCE = 15.0
TOLERANCE = 0.1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Software Raytracer')

surface = pygame.Surface(screen.get_size())

scene = {
    'camera': matrix.eye(),
    'spheres': [
        # position, radius, colour, specular
        [[0.0, 0.0, -5.0], 0.5, [255, 0, 0], 10.0],
        [[1.0, 1.0, -3.0], 0.5, [0, 255, 0], 0.5],
        [[-3.0, -1.0, -10.0], 1.5, [0, 100, 255], 2.0],
    ],
}

def min_distance(point):
    # this should also return the sphere itself
    distances = [sphere.distance_to(s, point) for s in scene['spheres']]
    closest = min(distances)
    index = distances.index(closest)
    return closest, scene['spheres'][index]
    #return min([sphere.distance_to(s, point) for s in scene['spheres']])

def create_source_ray(x, y):
    # https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-generating-camera-rays/generating-camera-rays
    cameraToWorld = scene['camera']

    width = WIDTH / PIXEL_SCALE
    height = HEIGHT / PIXEL_SCALE

    a = math.tan(FOV / 2.0 * math.pi / 180.0)
    Px = (2.0 * ((x + 0.5) / width) - 1) * a * ASPECT_RATIO
    Py = (1.0 - 2.0 * ((y + 0.5) / height)) * a
    Rp = [Px, Py, -1.0]
    Ro = vector.origin()
    Row = matrix.apply(cameraToWorld, Ro)
    Rpw = matrix.apply(cameraToWorld, Rp)
    Rdw = vector.subtract(Rpw, Row)
    Rdw = vector.normalize(Rdw)

    return [Row, Rdw]

def ray_colour(r, s):
    normal = sphere.normal(s, r[0])
    # calculate angle to ray
    dot = abs(vector.dot_product(r[1], normal) / 2.0)
    # apply specular
    dot = dot * s[3]
    # scale colour by the brightness
    colour = vector.scale(s[2], dot)
    # clamp to 255
    colour = [min(colour[0], 255), min(colour[1], 255), min(colour[2], 255)]
    return colour

def cast_ray(r):
    # walk the ray the distance to the nearest object
    start = r[0]
    for s in range(MAX_STEPS):
        if vector.length(vector.subtract(r[0], start)) > MAX_DISTANCE:
            break
        d, s = min_distance(r[0])
        if d < TOLERANCE:
            return ray_colour(r, s)
        r[0] = vector.add(r[0], vector.scale(r[1], d))
    return 0, 0, 0

def update(time, delta):
    #rotation = matrix.y_rotation((2 * math.pi) * (delta * 0.01))
    rotation = matrix.y_rotation(math.pi * 2 / 360.0)
    scene['camera'] = matrix.multiply(scene['camera'], rotation)

def draw(surface):
    camera = scene['camera']
    # cast rays
    # scale each of the pixels
    for x in range(int(WIDTH / PIXEL_SCALE)):
        for y in range(int(HEIGHT / PIXEL_SCALE)):
            r = create_source_ray(x, y)
            colour = cast_ray(r)
            #surface.set_at((x, y), colour)
            rect = pygame.Rect(int(x * PIXEL_SCALE), int(y * PIXEL_SCALE), PIXEL_SCALE, PIXEL_SCALE)
            surface.fill(colour, rect)

def time_seconds():
    return pygame.time.get_ticks() / 1000.0

def run():
    time = time_seconds()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        current = time_seconds()
        delta = current - time
        update(time, delta)
        time = current

        print('Drawing')
        surface.fill((0, 0, 0))
        draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.flip()


run()
