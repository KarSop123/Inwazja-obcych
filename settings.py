import pygame, sys
from random import randint, uniform

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# creating groups
player_group = pygame.sprite.GroupSingle()
meteor_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_laser_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

#clock
clock = pygame.time.Clock()

#enemy
max_enemy_group = 3
enemy_duration = 500

