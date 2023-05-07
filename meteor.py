from settings import *

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
