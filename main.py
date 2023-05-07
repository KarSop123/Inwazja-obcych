from settings import *
from player import Player
from enemy import Enemy
from meteor import Meteor

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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gra")


# creating background
background = pygame.image.load('graphics/background.png')

# creating player
player = Player(player_group)

#timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)

enemy_timer = pygame.event.custom_type()
pygame.time.set_timer(enemy_timer, 3000)


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

        if event.type == enemy_timer and len(enemy_group) < max_enemy_group:
            Enemy((randint(30, SCREEN_WIDTH-30),randint(50,300)), enemy_group)

    dt = clock.tick() / 1000


    #updateing
    meteor_group.update(dt)
    player_group.update(dt)
    enemy_group.update(dt)
    laser_group.update(dt)
    enemy_laser_group.update(dt)


    # drawing
    screen.blit(background, (0, 0))
    meteor_group.draw(screen)
    player_group.draw(screen)
    enemy_group.draw(screen)
    laser_group.draw(screen)
    enemy_laser_group.draw(screen)

    #drawing upgrades and hearts
    heart_group.draw(screen)

    pygame.display.flip()
