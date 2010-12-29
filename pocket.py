#!/usr/bin/env python
import freenect
import cv
import os
import numpy as np
from pygame.locals import *
from pygame.color import *
import pygame
from math import *

cv.NamedWindow('Depth')
pygame.init()
screen = pygame.display.set_mode((480,640))
pygame.display.set_caption("Shoot")
clock = pygame.time.Clock()
bullet = pygame.image.load(os.path.join('data','bullet.png'))
bullet2 = pygame.image.load(os.path.join('data','bullet.png'))
chimp = pygame.image.load('chimp.jpg')
bullet_rect = bullet.get_rect()
bullet2_rect = bullet2.get_rect()
bullet2_rect.move_ip(240,320)
angle = 0

while 1:
	depth, timestamp = freenect.sync_get_depth()
	rgb, timestamp = freenect.sync_get_video()
#	final = np.zeros((480,640,3), dtype=np.uint8)	
#	for i in xrange(120, 360, 2):
#		for j in xrange(160, 480, 2):
#			if depth[i,j] > 1400:
#				final[i,j]  = rgb[i,j]
	if depth[440,620] > 2000 :
		angle = 180
		bullet_rect.move_ip([sin((angle+90)*0.0174)*9, cos((angle+90)*0.0174)*9])
	elif depth[440, 20] > 2000 :
		angle = 270
		bullet_rect.move_ip([sin((angle+90)*0.0174)*9, cos((angle+90)*0.0174)*9])
	elif depth[20, 620] > 2000 :
		angle = 0
		bullet_rect.move_ip([sin((angle+90)*0.0174)*9, cos((angle+90)*0.0174)*9])
	elif depth[20, 20] > 2000 :
		angle = 90
		bullet_rect.move_ip([sin((angle+90)*0.0174)*9, cos((angle+90)*0.0174)*9])	
		
	if bullet_rect == bullet2_rect :
		break
	screen.fill(THECOLORS['white'])
	screen.blit(bullet, bullet_rect)
	screen.blit(bullet2, bullet2_rect)
	pygame.display.update()
	pygame.display.flip()
	clock.tick(50)
			
	cv.ShowImage('Depth', depth.astype(np.uint8))
	cv.ShowImage('Video', rgb[::2, ::2, ::-1].astype(np.uint8))
	
	cv.WaitKey(10)

#font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX,2.0, 2.0, 0, 3, 8)
#im = cv.LoadImageM('chimp.jpg')
#cv.PutText(im, "You Win", (240,320), font, (0,0,0))
#cv.ShowImage("go",im)
screen.fill(THECOLORS['black'])
screen.blit(chimp, (0,0))
pygame.display.update()
pygame.display.flip()

