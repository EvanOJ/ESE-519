import pygame,itertools,math,time,os
import numpy as np 
from scipy.interpolate import interp1d
import os
import sys
import pdb
#add the package to the python directory
#cur_path = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[0 : -1])
cur_path = os.path.dirname(os.path.abspath(__file__))
cur_path = os.path.join(cur_path, "ShareMemory")
sys.path.append(cur_path)
from MemShare import ShareMemReader


   
def mapRange(value,Amin,Amax,Bmin,Bmax):
	if value >= Amax:
		value = Amax
	elif(value <= Amin):
		value = Amin

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

class visualFeedback():
    def __init__(self,width,height,text,text2):
        self.width = width
        self.height = height
        self.text=""
        self.text2 = ""
        self.text3 = ""
        #os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        #info = pygame.display.Info()
        #self.width,self.height = info.current_w,info.current_h
        #self.screen = pygame.display.set_mode((self.width,self.height),pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.NOFRAME|pygame.mouse.set_visible(0))
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.surface = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        

        #set fullscreen here^^
    def updateColor(self,color):
        self.screen.fill(color)
    
    def updateScreen(self):
        self.screen.blit(self.surface,(0,0))
        rect = self.text.get_rect(center=(self.width/2,self.height/2))
        rect2 = self.text2.get_rect(center=(self.width/2,(self.height/2)-50))
        rect3 = self.text.get_rect(center=(self.width/2,(self.height/2)-100))
        self.screen.blit(self.text,rect)
        self.screen.blit(self.text2,rect2)
        self.screen.blit(self.timer,rect3)
        pygame.display.update()
 
    def updateText(self,state,color,timer):
        font = pygame.font.SysFont("Arial",25)
        self.timer = font.render(timer,True,color)
        if(state==-1):
            self.text = font.render("Device is warming up.",True,color)
            self.text2 = font.render("Please wait...",True,color)
        elif(state ==0):
            self.text = font.render("Collecting baseline data.",True,color)
            self.text2 = font.render("Meditation will begin in 60 seconds...",True,color)
        elif(state ==1):
            self.text = font.render("Pre-meditation Routine.",True,color)
            self.text2 = font.render("Visualize a relaxing meditation routine.",True,color)
           # print("update text")
        elif(state == 2):
            self.text = font.render("Concentration Routine.", True, color)
            self.text2 = font.render("For the next 4 minutes concentrate on the breath by counting the in/out breath cycle, focusing at the nostrils.", True, color)
            self.text3 = font.render("Recognize, relax and return when having distracting thoughts or feelings.",True,color)

            
        elif(state ==3):
            self.text = font.render("Now, rapture by sending thoughts of compassion and kindness to others for another 4 minutes.",True,color)

        elif(state ==4):

            self.text = font.render("For the next 7 minutes reflect on distracying feelings and thoughts that arose earlier.", True, color)
            self.text2 = font.render("Disentangle habits and patterns by asking 'Why?' sequentially.",True,color)

        elif(state==5):

            self.text = font.render("Conclude by recalling the lessons you've learned during reflection for 2 minutes.",True,color)

        elif(state ==6):

            self.text = font.render("Now that meditation is concluded, journal your ideas onto your smartphone or computer.",True,color)
        
        elif(state==-11):
            
            self.text = font.render("INCREASE/MOTIVATION TEXT",True,color)
            self.text2=font.render("",True,color)
        
        elif(state==11):
            self.text = font.render("DECREASE/RELAXATION TEXT",True,color)
            self.text2=font.render("",True,color)
        
        else:
            self.text = font.render("",True,color)
            self.text2=font.render("",True,color)

def fade(GUI,state,period,currBPM,targetBPM,timer):
    global prevColor
    global nextColor

    #current_color = prevColor
    
    differential = (currBPM - targetBPM)/(currBPM + 0.0000001)
    FPS = 120
    change_every_x_seconds = mapRange(differential,0,0.5,3,4)							#according to wenjie this is also a variable, threshold is 50% disscrep. between cur rand rtarget 
    number_of_steps = change_every_x_seconds * FPS
    step = 1
    
    #bpm = 0
    #bpmBaseline = 75 #check with nalaka 

    alphaVal = 0

    running = True

#    while running:

 #       for event in pygame.event.get():
  #          if event.type == pygame.QUIT:
   #            running = False

    while step < number_of_steps:
        # (y-x)/number_of_steps calculates the amount of change per step required to 
        # fade one channel of the old color to the new color
        # We multiply it with the current step counter

        
        bpmToColorTemp = mapRange(differential,-0.1,0.1,2000,5000)

       # if(currBPM<=targetBPM):
        #    bpmToColorTemp = mapRange(currBPM,50,120,1500,6000)
         #   alphaVal = mapRange(bpmToColorTemp,1500,6000,0,255)

            #GUI.updateText(-11,complementColor,timer)
            #GUI.updateScreen()

       # else:
       #     bpmToColorTemp = mapRange(currBPM,50,120,1500,6000)
       #     alphaVal = mapRange(bpmToColorTemp,6000,1500,0,255)
            #GUI.updateText(11,complementColor,timer)
            #GUI.updateScreen()
        
        nextColor = tempToRGB(bpmToColorTemp) # ideally this would be calculated based on a data input 
        #period = calcPeriod(bpm,bpmBaseline)
#        alphaVal = mapRange(bpmToColorTemp,1500,6000,0,255)
        current_color = [x + (((y-x)/number_of_steps)*step) for x, y in zip(prevColor, nextColor)]

        prevComplementColor = complement(prevColor[0],prevColor[1],prevColor[2])
        prevComplementColor = (prevComplementColor[0],prevComplementColor[1],prevComplementColor[2],alphaVal)
        
        complementColor = complement(current_color[0],current_color[1],current_color[2])
        complementColor = (complementColor[0],complementColor[1],complementColor[2],alphaVal)

        complementColor = [x + (((y-x)/number_of_steps)*step) for x, y in zip(prevComplementColor, complementColor)]
        complementColor = complement(current_color[0],current_color[1],current_color[2])
        complementColor = (complementColor[0],complementColor[1],complementColor[2],alphaVal)
        prevColor = current_color
        GUI.updateColor(current_color)
        #timer = str(time.time())
#        GUI.updateText(state,complementColor,timer)
        GUI.updateScreen()
        #print(step)
        step += 1
        time.sleep(0.01)
             
        
    #GUI.text1 = ""
    #GUI.text2 = None
    #GUI.text3 = None
    #running = False
    
def main():

#   screenWidth = 480
#   screenHeight = 320
#   pygame.init()
    global prevColor
    global nextColor
    prevColor = (255,255,255)
    nextColor = (255,255,255)


    #cur_dir = "/".join(os.getcwd().split("/")[0: -1])
    cur_dir = os.getcwd()
    cur_path = os.path.join(cur_dir, "memorymap", "data_visual.txt")
    
    GUI = visualFeedback(480,320,"","")
    #pdb.set_trace()
    with open(cur_path, "r+", encoding="UTF-8") as fshare:
        smr = ShareMemReader(fshare, cur_path, int_size = 4)
        #print("start reading --------------------------")
        smr.create_mapping()
        smr.read_data_size()
        ti = 0
        while (True):
            
            ti = ti + 1
            #tic = time.clock()
            smr.create_mapping()
            smr.copy_buffer()
            smr.read_data_header()
            result = smr.read_data_body()
            #toc = time.clock()
            print("getting result")
            print(np.array(result))
            #print("time", 1000 * (tic - toc))
            state = int(result[0])
            cur_bpm = int(result[1])
            target_bpm = int(result[2])
            timer = str(result[3])
            GUI.updateText(state, (255, 255, 255), timer)
            fade(GUI, state, 2, cur_bpm, target_bpm, timer)
            #print("the state value is ", state)
            #GUI.updateScreen()
            #GUI.updateText(99, (255, 255, 255),  timer)
           # GUI.updateScreen()
            #time.sleep(3)
            
            #fade(GUI, state, 2, cur_bpm, target_bpm, timer)
            smr.reset()
            smr.close()
            time.sleep(10)
            #if pygame.key.get_pressed():
             #   pygame.quit()
    #screen = pygame.display.set_mode((screenWidth, screenHeight)) #add ",pygame.FULLSCREEN" for fullscreen mode

    #target= 75#updated per state based on where you need to end up at the end of that state

#    fade(GUI,0,2,99,target,"timer here")
  #  fade(GUI,1,1,98,target,"timer here")
 #   fade(GUI,2,1,90,target,"timer here")
#    fade(GUI,3,1,80,target,"timer here")
   # fade(GUI,4,1,88,target,"timer here")
   # fade(GUI,5,1,81,target,"timer here")
  #  fade(GUI,6,1,87,target,"timer here")
 #   fade(GUI,-11,1,55,target,"timer here")
#    fade(GUI,11,1,100,target,"timer here")
    pygame.quit()


    #colors = itertools.cycle(['green', 'blue', 'purple', 'pink', 'red', 'orange'])

    #clock = pygame.time.Clock()

    #base_color = next(colors)
    #next_color = next(colors)
#    prevColor = (255,255,255)
#    nextColor = (255,255,255)

#    current_color = prevColor
#    period = 3.
#    FPS = 120
#   change_every_x_seconds = period							#according to wenjie this is also a variable 
#    number_of_steps = change_every_x_seconds * FPS
#    step = 1
#    bpm = 0
#    bpmBaseline = 75 #check with nalaka 
#    fakeDataIndex = 0

    #fakeECG = [75,125,120,115,110,109,150,90,89,80,79,77,76,75,80,85,88,89,90,93,95,99,100] # this buffer of BPM values would be 1 min long and dynamically updated

#    alphaVal = 0

#    font = pygame.font.SysFont('Arial', 20)

#    running = True

#    while running:

#        for event in pygame.event.get():
 #           if event.type == pygame.QUIT:
  #             running = False
#
 #       step += 1
  #      if step < number_of_steps:
   #         # (y-x)/number_of_steps calculates the amount of change per step required to 
    #        # fade one channel of the old color to the new color
     #       # We multiply it with the current step counter
      #      current_color = [x + (((y-x)/number_of_steps)*step) for x, y in zip(prevColor, nextColor)]
       # else:
        #    step = 1
         #   prevColor = current_color
          #  bpm = fakeECG[fakeDataIndex]
           # fakeDataIndex +=1 
            
            #bpmToColorTemp = mapRange(bpm,50,100,1500,7000)
            
            #nextColor = tempToRGB(bpmToColorTemp) # ideally this would be calculated based on a data input 
            #period = calcPeriod(bpm,bpmBaseline)
            #alphaVal = mapRange(bpmToColorTemp,1500,7000,0,255)
            #print(alphaVal)
            #print(period)
            
#       text = font.render('bpm:{a} color: {b}'.format(a=bpm, b=current_color), True, pygame.color.Color('white'))
        
        #complementColor = complement(current_color[0],current_color[1],current_color[2])
        #complementColor = (complementColor[0],complementColor[1],complementColor[2],alphaVal)


 #       surface = pygame.Surface((GUI.width,GUI.height), pygame.SRCALPHA)

 #       GUI.screen.fill(current_color)
 #       GUI.updateColor(current_color)
 #       pygame.draw.circle(surface, complementColor, GUI.screen.get_rect().center, 50)
 #       GUI.screen.blit(text, (0,0))
 #       GUI.screen.blit(surface, (0,0))
  #      pygame.display.update()
        #would be timer counter from mindfulnessMonitor
 #       timer = str(time.time())
 #       GUI.updateText(1,complementColor,timer)
  #      GUI.updateScreen()
#        clock.tick(FPS)
if __name__ == "__main__":
    main()

