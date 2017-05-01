#-*-coding:UTF-8 -*-
# import the pygame module
import pygame

# import random for random numbers!
import random

# import pygame.locals for easier access to key coordinates
from pygame.locals import *

#定义游戏的屏幕大小
width = 1200
hight = 800

#定义Player类
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		image = pygame.image.load('GodPlane2.png').convert()
		self.image = pygame.transform.scale(image, (64, 64))
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center = (width/2, 600))#set the plaer's init position

	def update(self, pressed_keys):
		if pressed_keys[K_UP]:
			self.rect.move_ip(0, -2)
		if pressed_keys[K_DOWN]:
			self.rect.move_ip(0, 2)
		if pressed_keys[K_LEFT]:
			self.rect.move_ip(-2, 0)
		if pressed_keys[K_RIGHT]:
			self.rect.move_ip(2, 0)

		#限制plaer的移动范围，不能超出屏幕
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > width:
			self.rect.right = width
		if self.rect.top < 0:
			self.rect.top = 0
		elif self.rect.bottom > hight:
			self.rect.bottom = hight 

#定义血点奖励类
class RewardBlood(pygame.sprite.Sprite):
	def __init__(self):
		super(RewardBlood, self).__init__()
		image = pygame.image.load('sphere2.png').convert()
		self.image = pygame.transform.scale(image, (32, 32))
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center = (random.randint(0, width), 0))
		self.speed = random.randint(1, 2)

	def update(self):
		self.rect.move_ip(0, self.speed)
		if self.rect.bottom > hight:
			self.kill()

#定义敌人类
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		if random.randint(1,2) == 1:
			image = pygame.image.load('JpPlane2.png').convert()
		else:
			image = pygame.image.load('GreenPlane2.png').convert()
		self.image = pygame.transform.scale(image, (32, 32))
		self.init_position = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1190]
		self.image.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.image.get_rect(center = (self.init_position[random.randint(0, 12)], 0))
		self.speed = random.randint(1, 2)

	def update(self):
		self.rect.move_ip(0, self.speed)
		if self.rect.bottom > hight:
			self.kill()

#定义云朵类
class Cloud(pygame.sprite.Sprite):
	"""docstring for Cloud"""
	def __init__(self):
		super(Cloud, self).__init__()
		self.image = pygame.image.load('cloud.png').convert()
		self.image.set_colorkey((0, 0, 0), RLEACCEL)
		self.rect = self.image.get_rect(center = (random.randint(0, width), 0))
		self.speed = random.randint(1,3)

	def update(self):
		self.rect.move_ip(0, self.speed)
		if self.rect.bottom > hight:
			self.kill()

# initialize pygame
pygame.init()

# create the screen object
# here we pass it a size of 800x600
screen = pygame.display.set_mode((width, hight))

#创建游戏背景
background = pygame.Surface(screen.get_size())
background.fill((135, 206, 250))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDREWARD = pygame.USEREVENT + 3
pygame.time.set_timer(ADDREWARD, 1000)

#创建plaer
player = Player()

#创建敌人
enemies = pygame.sprite.Group()

#创建云彩
clouds = pygame.sprite.Group()

#创建奖励
rewardBloods = pygame.sprite.Group()

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
		elif event.type == ADDCLOUD:
			new_cloud = Cloud()
			clouds.add(new_cloud)
			all_sprites.add(new_cloud)
		elif event.type == ADDREWARD:
			new_reward = RewardBlood()
			rewardBloods.add(new_reward)
			all_sprites.add(new_reward)

	screen.blit(background, (0, 0))
	clouds.update()
	enemies.update()
	rewardBloods.update()
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)

	for entity in all_sprites:
		screen.blit(entity.image, entity.rect)

	if pygame.sprite.spritecollideany(player, enemies):
		player.kill()
		running = False
		print "Game over"

	#将两次flip之间的修改更新到整个屏幕
	pygame.display.flip()
