import pygame, sys
from random import randint, uniform
# creating player
class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        player_surf = pygame.image.load('graphics/x-wing.png').convert_alpha()
        player_size = pygame.math.Vector2(player_surf.get_size()) * 2.5
        self.scaled_surf = pygame.transform.scale(player_surf,(round(player_size.x),round(player_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

        #speed
        self.speed = 400

        #health
        self.hearts = 3
        self.can_bonus = True

        #shooting
        self.shoot_time = 0
        self.can_shoot = True
        self.duration = 500

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt

    def collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.hearts -= 1
            heart_group.remove(heart_group.sprites()[self.hearts])



            if self.hearts == 0:
                pygame.quit()
                sys.exit()

    def laser_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_time > self.duration:
            self.can_shoot = True

    def laser_shoot(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            Laser(self.rect.midtop, laser_group)
            self.shoot_time = pygame.time.get_ticks()

    def update(self, dt):
        self.laser_timer()
        self.laser_shoot()
        self.movement(dt)
        self.collision()


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        laser_surf = pygame.image.load('graphics/laser.png')
        laser_size = pygame.math.Vector2(laser_surf.get_size()) * 2.5
        self.scaled_surf = pygame.transform.scale(laser_surf,(round(laser_size.x),round(laser_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 500

        self.rotation = 0
        self.rotation_speed = 300
    def movement(self, dt):
        self.rect.y -= self.speed * dt

    def rotate(self, dt):
        self.rotation -= self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.scaled_surf, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.kill()

    def update(self, dt):
        #self.rotate(dt)
        self.movement(dt)
        self.collision()
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        enemy_surf = pygame.image.load('graphics/enemy.png')
        enemy_size = pygame.math.Vector2(enemy_surf.get_size()) * 2.5
        self.scaled_surf = pygame.transform.scale(enemy_surf,(round(enemy_size.x),round(enemy_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 1

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


    def update(self, dt):
        self.movement(dt)

class Meteor(pygame.sprite.Sprite):
    def __init__(self,pos, group):
        super().__init__(group)
        meteor_surf = pygame.image.load('graphics/meteor.png').convert_alpha()
        meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(meteor_surf,(round(meteor_size.x),round(meteor_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.rotation = 0
        self.rotation_speed = randint(10, 40)

        #float based position
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,600)

    def movement(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def rotate(self, dt):
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotate(self.scaled_surf, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.movement(dt)
        self.rotate(dt)

        if self.rect.top > SCREEN_WIDTH:
            self.kill()

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        heart_surf = pygame.image.load('graphics/heart.png').convert_alpha()
        heart_size = pygame.math.Vector2(heart_surf.get_size()) * 2.5
        self.scaled_surf = pygame.transform.scale(heart_surf,(round(heart_size.x),round(heart_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

pygame.init()

SCREEN_WIDTH, SCREEN_HIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
pygame.display.set_caption("Gra")
clock = pygame.time.Clock()

# creating background
background = pygame.image.load('graphics/background.png')

# creating groups
player_group = pygame.sprite.GroupSingle()
meteor_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

# creating player
player = Player(player_group)
enemy = Enemy((randint(200,1000), randint(100,300)), enemy_group)

#timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)


#creating hearts
heart_surf = pygame.image.load('graphics/heart.png').convert_alpha()
heart_size = pygame.math.Vector2(heart_surf.get_size()) * 2.5
for i in range(player.hearts):
    Heart((SCREEN_WIDTH - heart_size.x * i - 30, heart_size.y + 10), heart_group)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == meteor_timer:
            meteor_x_pos = randint(0, SCREEN_WIDTH)
            Meteor((meteor_x_pos,-50), meteor_group)



    dt = clock.tick() / 1000


    #updateing
    meteor_group.update(dt)
    player_group.update(dt)
    laser_group.update(dt)
    enemy_group.update(dt)


    # drawing
    screen.blit(background, (0, 0))
    meteor_group.draw(screen)
    player_group.draw(screen)
    laser_group.draw(screen)
    enemy_group.draw(screen)

    #drawing upgrades and hearts
    heart_group.draw(screen)

    pygame.display.flip()
