#-*-coding:UTF-8 -*-
# import the pygame module
import pygame

# import random for random numbers!
import random

# import pygame.locals for easier access to key coordinates
from pygame.locals import *

#定义Player类
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.Surface((75, 25))
		self.surf.fill((0, 255, 0)) #绿色
		self.rect = self.surf.get_rect()

	def update(self, pressed_keys):
		if pressed_keys[K_UP]:
			self.rect.move_ip(0, -5)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 5)
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-5, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(5, 0)

		#限制plaer的移动范围，不能超出屏幕
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > 800:
			self.rect.right = 800
		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > 600:
			self.rect.bottom = 600

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surf = pygame.Surface((20, 10))
		self.surf.fill((255, 0, 0))#红色
		self.rect = self.surf.get_rect(center = (820, random.randint(0, 600)))
		self.speed = random.randint(5, 20)

	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()


# initialize pygame
pygame.init()

# create the screen object
# here we pass it a size of 800x600
screen = pygame.display.set_mode((800, 600))

#创建游戏背景
background = pygame.Surface(screen.get_size())
background.fill((135, 206, 250))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

#创建plaer
player = Player()

#创建敌人
enemies = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#main loop
running = True
while running:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False
		elif event.type == ADDENEMY:
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)

	screen.blit(background, (0, 0))
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)
	enemies.update()

	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)

	if pygame.sprite.spritecollideany(player, enemies):
		player.kill()

	#将两次flip之间的修改更新到整个屏幕
	pygame.display.flip()
