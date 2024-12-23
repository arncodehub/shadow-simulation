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
    numRays = 720
    radiansPerRay = (2 * math.pi) / numRays
    radianDirection = -radiansPerRay
    for i in range(numRays):
        radianDirection += radiansPerRay
        if sunX > 800 and (radianDirection > (3/2)*math.pi or radianDirection < (1/2)*math.pi):
            continue
        if sunX < 0 and ((1/2)*math.pi < radianDirection < (3/2)*math.pi):
            continue
        if sunY < 0 and radianDirection > math.pi:
            continue
        if sunY > 450 and radianDirection < math.pi:
            continue
        #print(f"Ray {i}")
        rayJ = []
        rayX, rayY = sunX, sunY
        xStep, yStep = math.cos(radianDirection), math.sin(radianDirection)
        intersected = False
        while not intersected:
            if 0 <= rayX <= 800 and 0 <= rayY <= 400:
                rayJ.append([rayX, rayY]) # If on screen, note this as part of the ray's journey.
            pillarDistance = 0 # Distance to pillar
            if rayX <= 375 and 250 <= rayY <= 400: # Left region
                pillarDistance = 375 - rayX
            if 375 <= rayX <= 425 and rayY <= 250: # Up region
                pillarDistance = 250 - rayY                
            if rayX >= 425 and 250 <= rayY <= 400: # Right region
                pillarDistance = rayX - 425
            if 375 <= rayX <= 425 and rayY >= 400: # Down region
                pillarDistance = rayY - 400
            if rayX <= 375 and rayY <= 250: # Upleft region
                pillarDistance = math.sqrt((375 - rayX)**2 + (250 - rayY)**2)
            if rayX >= 425 and rayY <= 250: # Upright region
                pillarDistance = math.sqrt((rayX - 425)**2 + (250 - rayY)**2)
            if rayX <= 375 and rayY >= 400: # Downleft region
                pillarDistance = math.sqrt((375 - rayX)**2 + (rayY - 250)**2)
            if rayX >= 425 and rayY >= 400: # Downright region
                pillarDistance = math.sqrt((rayX - 425)**2 + (rayY - 250)**2)
            floorDistance = 0 # Distance to floor
            if rayX <= 0 and 400 <= rayY <= 450: # Left region
                floorDistance = 0 - rayX
            if 0 <= rayX <= 800 and rayY <= 400: # Up region
                floorDistance = 400 - rayY               
            if rayX >= 800 and 400 <= rayY <= 450: # Right region
                floorDistance = rayX - 800
            if 0 <= rayX <= 800 and rayY >= 450: # Down region
                floorDistance = rayY - 450
            if rayX <= 0 and rayY <= 400: # Upleft region
                floorDistance = math.sqrt((0 - rayX)**2 + (400 - rayY)**2)
            if rayX >= 800 and rayY <= 400: # Upright region
                floorDistance = math.sqrt((rayX - 800)**2 + (400 - rayY)**2)
            if rayX <= 0 and rayY >= 450: # Downleft region
                floorDistance = math.sqrt((0 - rayX)**2 + (rayY - 450)**2)
            if rayX >= 800 and rayY >= 450: # Downright region
                floorDistance = math.sqrt((rayX - 800)**2 + (rayY - 450)**2)
            screenDistance = float('inf') # Distance to entering screen?
            if rayX < 0 or rayX > 800 or rayY < 0 or rayY > 450:
                if rayX < 0 and 0 <= rayY <= 450:
                    screenDistance = 0 - rayX
                if 0 <= rayX <= 800 and rayY < 0:
                    screenDistance = 0 - rayY
                if rayX > 800 and 0 <= rayY <= 450:
                    screenDistance = rayX - 800
                if 0 <= rayX <= 800 and rayY > 450:
                    screenDistance = rayY - 450
                if rayX < 0 and rayY < 0:
                    screenDistance = math.sqrt(rayX**2 + rayY**2)
                if rayX > 800 and rayY < 0:
                    screenDistance = math.sqrt((rayX - 800)**2 + rayY**2)
                if rayX < 0 and rayY > 450:
                    screenDistance = math.sqrt(rayX**2 + (450 - rayY)**2)
                if rayX > 800 and rayY > 450:
                    screenDistance = math.sqrt((rayX - 800)**2 + (rayY - 450)**2)
            if 0 <= rayX <= 800 and 0 <= rayY <= 450:
                leftD = rayX
                rightD = 800 - rayX
                upD = rayY
                downD = 450 - rayY
                screenDistance = min([upD, rightD, leftD, downD])
            moveDistance = min([floorDistance, pillarDistance, screenDistance])
            moveDistance = max(moveDistance, 1)
            rayX += xStep * moveDistance
            rayY += yStep * moveDistance
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
        h = simulationTime // 3600
        m = (simulationTime - h*3600) // 60
        s = (simulationTime - h*3600 - m*60)
        print(f"{h}:{m}:{s}")
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
