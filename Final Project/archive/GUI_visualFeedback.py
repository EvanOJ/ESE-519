from tkinter import *
import pygame
import random
import os

screenWidth = 480
screenHeight = 320

root = Tk()
embed = Frame(root, width=screenWidth, height=screenHeight)
embed.grid(row=0,column=2)
root.update()

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

pygame.display.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.flip()

while True:
    #your code here
    screen.fill((255,255,255))
    pygame.display.flip()
    root.update()