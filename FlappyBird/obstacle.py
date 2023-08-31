import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, speed, side):
        super().__init__()
        if side == "down":
            self.obstacle1 = pygame.image.load("graphics/flappy_obstacle1.png").convert_alpha()
            self.obstacle2 = pygame.image.load("graphics/flappy_obstacle2.png").convert_alpha()
            self.image = self.obstacle1
            self.rect = self.image.get_rect(midtop=(pos))
        else:
            self.obstacle1 = pygame.image.load("graphics/flappy_obstacle1.png").convert_alpha()
            self.obstacle1 = pygame.transform.rotate(self.obstacle1, 180)
            self.obstacle2 = pygame.image.load("graphics/flappy_obstacle2.png").convert_alpha()
            self.obstacle2 = pygame.transform.rotate(self.obstacle2, 180)
            self.image = self.obstacle1
            self.rect = self.image.get_rect(midbottom=(pos))

        self.speed = speed

    def obstacle_movement(self):
        self.rect.x -= self.speed

    def obstacle_clear(self):
        if self.rect.x <= - 150:
            self.kill()

    def update(self):
        self.obstacle_movement()
        self.obstacle_clear()
