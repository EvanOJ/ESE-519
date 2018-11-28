import pygame
import itertools
import math
import numpy as np 
from scipy.interpolate import interp1d

def mapRange(value,Amin,Amax,Bmin,Bmax):
	if value >= Amax:
		value = Amax
	elif(value <= Amin):
		value = Amin
	
    # aSpan = Amax - Amin
	# bSpan = Bmax - Bmin
	# scaled = float(value - aSpan)/float(aSpan)
	# return bSpan + (scaled * bSpan)

	interp = interp1d([Amin,Amax],[Bmin,Bmax])
	return(interp(value))

def clamp(n,smallest,largest):
    return max(smallest,min(n,largest))

def tempToRGB(kelvin):
    temp = kelvin/100


    if(temp <= 66):
        red = 255
        green = temp
        green = tempgreen = 99.4708025861 * math.log(green) - 161.1195681661

        if(temp <= 10):
            blue = 0
        else:
            blue = temp - 10
            blue = 138.5177312231 * math.log(blue) - 305.0447927307
    else:
        red = temp - 60
        red = 329.698727446 * math.pow(red, -0.1332047592)
        green = temp - 60
        green = 288.1221695283 * math.pow(green, -0.0755148492 )
        blue = 255

    r = int(clamp(red,0,255))
    g = int(clamp(green,0,255))
    b = int(clamp(blue,0,255))

    return (r,g,b)  

def calcPeriod(bpm,bpmBaseline):
	if bpm <= bpmBaseline:
		period = 1

		return period
	else:
		diff = bpm - bpmBaseline
	print("diff: {a}".format(a=diff))
	period = 1 + 1/diff # a function to update the period. as discrepency decreases the period increases, i.e. does not need to be updated as much and vice versa
	return period 

def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))

screenWidth = 480
screenHeight = 320
pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight)) #add ",pygame.FULLSCREEN" for fullscreen mode

#colors = itertools.cycle(['green', 'blue', 'purple', 'pink', 'red', 'orange'])

clock = pygame.time.Clock()

#base_color = next(colors)
#next_color = next(colors)
prevColor = (255,255,255)
nextColor = (255,255,255)

current_color = prevColor
period = 3.
FPS = 120
change_every_x_seconds = period							#according to wenjie this is also a variable 
number_of_steps = change_every_x_seconds * FPS
step = 1
bpm = 0
bpmBaseline = 75 #check with nalaka 
fakeDataIndex = 0

fakeECG = [75,125,120,115,110,109,150,90,89,80,79,77,76,75,80,85,88,89,90,93,95,99,100] # this buffer of BPM values would be 1 min long and dynamically updated

alphaVal = 0

font = pygame.font.SysFont('Arial', 20)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    step += 1
    if step < number_of_steps:
        # (y-x)/number_of_steps calculates the amount of change per step required to 
        # fade one channel of the old color to the new color
        # We multiply it with the current step counter
        current_color = [x + (((y-x)/number_of_steps)*step) for x, y in zip(prevColor, nextColor)]
    else:
        step = 1
        prevColor = current_color
        bpm = fakeECG[fakeDataIndex]
        fakeDataIndex +=1 

        bpmToColorTemp = mapRange(bpm,50,100,1500,7000)
        
        nextColor = tempToRGB(bpmToColorTemp) # ideally this would be calculated based on a data input 
        period = calcPeriod(bpm,bpmBaseline)
        alphaVal = mapRange(bpmToColorTemp,1500,7000,0,255)
       	print(alphaVal)
        print(period)
        
    text = font.render('bpm:{a} color: {b}'.format(a=bpm, b=current_color), True, pygame.color.Color('white'))

    complementColor = complement(current_color[0],current_color[1],current_color[2])
    complementColor = (complementColor[0],complementColor[1],complementColor[2],alphaVal)


    surface = pygame.Surface((screenWidth,screenHeight), pygame.SRCALPHA)

    screen.fill(current_color)
    pygame.draw.circle(surface, complementColor, screen.get_rect().center, 50)
    screen.blit(text, (0,0))
    screen.blit(surface, (0,0))
    pygame.display.update()
    clock.tick(FPS)