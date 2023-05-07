from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        player_surf = pygame.image.load('graphics/x-wing.png').convert_alpha()
        player_size = pygame.math.Vector2(player_surf.get_size()) * 2.5
        self.scaled_surf = pygame.transform.scale(player_surf,(round(player_size.x),round(player_size.y)))
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
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
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(self, enemy_laser_group, True, pygame.sprite.collide_mask):
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
        self.can_rotate = False

        #score


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

        if pygame.sprite.spritecollide(self, enemy_laser_group, True, pygame.sprite.collide_mask):
            self.kill()

        if pygame.sprite.spritecollide(self, enemy_group, True, pygame.sprite.collide_mask):
            self.kill()

    def update(self, dt):
        if self.can_rotate:
            self.rotate(dt)
        self.movement(dt)
        self.collision()
        if self.rect.bottom < 0:
            self.kill()

