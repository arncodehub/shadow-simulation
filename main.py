import math
import time

import pygame
pygame.init()

window = pygame.display.set_mode((800, 450))
pygame.display.set_caption("Shadow Simulator")
pygame.display.update()

BLACK = (0, 0, 0)
GRAY = (63, 63, 63)
WHITE = (255, 255, 255)
BROWN = (50, 34, 6)
clock = pygame.time.Clock()

# Sun distance from point (400, 450) should always be 999600 units
global simulationTime
simulationTime = 0 # Daytime in seconds, 0 <= x < 86400

def emit_light(sunX, sunY):
    numRays = 360
    radiansPerRay = (2 * math.pi) / numRays
    radianDirection = 0
    for i in range(numRays):
        #print(f"Ray {i}")
        rayJ = []
        rayX, rayY = sunX, sunY
        xStep, yStep = math.cos(radianDirection), math.sin(radianDirection)
        intersected = False
        while not intersected:
            if 0 <= rayX <= 800 and 0 <= rayY <= 400:
                rayJ.append([rayX, rayY]) # If on screen, note this as part of the ray's journey.
            if math.sqrt(rayX**2 + rayY**2) < 20000:
                rayX += xStep*4
                rayY += yStep*4
            else:
                rayX += 10000*xStep
                rayY += 10000*yStep
            if 375 <= rayX <= 425 and 250 <= rayY <= 400:
                intersected = True # Collided with tower!
            if 0 <= rayX <= 800 and 400 <= rayY <= 450:
                intersected = True # Collided with ground!
            if math.sqrt(rayX**2 + rayY**2) >= 2000:
                intersected = True # Too far away, never will intersect, quit.
            if 0 <= rayX <= 800 and 0 <= rayY <= 400:
                rayJ.append([rayX, rayY]) # If on screen, note this as part of the ray's journey.
        if rayJ != []: # If the ray was on screen at some point, draw its journey.
            pygame.draw.line(window, WHITE, (rayJ[0][0], rayJ[0][1]), (rayJ[-1][0], rayJ[-1][1]))
        radianDirection += radiansPerRay

def main():
    run = True
    while run:
        st = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.fill(BLACK)
        global simulationTime
        simulationTime = simulationTime % 86400
        divisor = 86400 / (2 * math.pi)
        radian = simulationTime / divisor
        radian = (2 * math.pi) - radian
        YCo = math.sin(radian)
        XCo = math.cos(radian)
        sunX, sunY = 400 + 500*XCo, 450 + 500*YCo
        print(simulationTime)
        pygame.draw.rect(window, GRAY, [375, 250, 50, 150])
        pygame.draw.rect(window, BROWN, [0, 400, 800, 50])
        emit_light(sunX, sunY)
        et = time.time()
        dt = et-st
        simulationTime += dt*60*12
        simulationTime = round(simulationTime)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
