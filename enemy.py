import pygame.sprite

from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        enemy_surf = pygame.image.load('graphics/enemy.png')
        enemy_size = pygame.math.Vector2(enemy_surf.get_size()) * 4
        self.scaled_surf = pygame.transform.scale(enemy_surf,(round(enemy_size.x),round(enemy_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 1

        self.duration = enemy_duration
        self.last_shoot = pygame.time.get_ticks()

        #float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300
        self.direction = pygame.math.Vector2(1,0)

    def movement(self,dt):
        if self.rect.x <= -20:
            self.direction = pygame.math.Vector2(1,0)
        if self.rect.x >= SCREEN_WIDTH-60:
            self.direction = pygame.math.Vector2(-1,0)
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def shooting(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot > self.duration:
            self.last_shoot = pygame.time.get_ticks()
            EnemyLaser(self.rect.midbottom, enemy_laser_group)


    def update(self, dt):
        self.movement(dt)
        self.shooting()


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self,pos, group):
        super().__init__(group)
        laser_surf = pygame.image.load('graphics/adolf.png')
        laser_size = pygame.math.Vector2(laser_surf.get_size()) * 2.5
        self.scaled_surf = pygame.transform.scale(laser_surf,(round(laser_size.x),round(laser_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

        #float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 400

    def movement(self, dt):
        self.rect.y += self.speed * dt

    def collision(self):
        if pygame.sprite.spritecollide(self, player_group, True, pygame.sprite.collide_mask):
            self.kill()


    def update(self, dt):
        self.movement(dt)

