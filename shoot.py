import sys
import os
import random
import pygame
from pygame.locals import *
from pygame.color import *
import freenect
import cv
import numpy as np



def load_bullet() :
	return pygame.image.load(os.path.join('data','bullet.png'))

def load_ball() :
	return pygame.image.load(os.path.join('data','ball.png'))
	
def main():
	pygame.init()
	cv.NamedWindow('Depth')
	screen = pygame.display.set_mode((480,640))
	pygame.display.set_caption("Shoot")
	clock = pygame.time.Clock()
	x, y = 0, 0
	running = True
	load = True
	shoot = False
	change = False
	ball_load = True
	while running:
		depth, _ = freenect.sync_get_depth()
		rgb, _ = freenect.sync_get_rgb()
		
		if load :
			bullet = load_bullet()
			bullet_rect = bullet.get_rect()
			load = False
		
		if ball_load :
			ball = load_ball()
			ball_rect = ball.get_rect()
			y_axis = random.randrange(20, 610)
			ball_rect.move_ip(430, y_axis)
			ball_load = False
		
		if depth[240, 20] > 2000 :
			shoot = True
			change = True
		elif depth[470, 520] > 1800 :
			x, y = 0, 5
			change = True
		elif depth[20, 620] > 1700 :
			x, y = 0, -5
			change = True
	
		for event in pygame.event.get() :
			if event.type == QUIT:
				running = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
			elif event.type == KEYDOWN and event.key == K_UP:
				x, y = 0, -5
			elif event.type == KEYDOWN and event.key == K_DOWN:
				x, y = 0, 5
			elif event.type == KEYDOWN  and event.key == K_RIGHT:
				shoot = True

			bullet_rect.move_ip(x, y)
			screen.fill(THECOLORS['white'])
			screen.blit(bullet, bullet_rect)
			screen.blit(ball, ball_rect)
		

		if change :
			bullet_rect.move_ip(x, y)
			screen.fill(THECOLORS['white'])
			screen.blit(bullet, bullet_rect)
			screen.blit(ball, ball_rect)
			change = False

		if shoot :
			x, y = 10, 0
			bullet_rect.move_ip(x, y)
			screen.fill(THECOLORS['white'])
			screen.blit(bullet, bullet_rect)
			screen.blit(ball, ball_rect)
			if bullet_rect.x > 430 and bullet_rect.y < y_axis+30 and bullet_rect.y > y_axis-30:
				ball_rect.move_ip(x,y)
				screen.fill(THECOLORS['white'])
				screen.blit(ball, ball_rect)
				del(ball)
				del(bullet)
				screen.fill(THECOLORS['white'])
				load = True
				shoot = False
				ball_load = True
			elif bullet_rect.x > 480 :
				del(bullet)
				load = True
				shoot = False
				ball_load = False
							
				
		pygame.display.update()		
		pygame.display.flip()
		clock.tick(50)
		cv.ShowImage('Depth', depth.astype(np.uint8))
		cv.WaitKey(10)
			

if __name__ == '__main__':
	sys.exit(main())
