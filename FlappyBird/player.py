import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, border):
        super().__init__()
        self.player1 = pygame.image.load("graphics/parrot1.png").convert_alpha()
        self.player2 = pygame.image.load("graphics/parrot2.png").convert_alpha()
        self.player3 = pygame.image.load("graphics/parrot3.png").convert_alpha()
        self.player_fall1 = pygame.image.load("graphics/parrot_fall1.png").convert_alpha()
        self.player_fall2 = pygame.image.load("graphics/parrot_fall2.png").convert_alpha()
        self.image = self.player1
        self.rect = self.image.get_rect(center=(pos))

        self.ready = True
        self.jump_cooldown = 120
        self.jump_timer = 0
        self.gravity = 0

        self.border = border
        self.player_animation_time = 0

    def player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.ready and self.gravity >= -2:
            self.gravity = -5
            self.ready = False
            self.jump_timer = pygame.time.get_ticks()
            self.image = self.player1

    def jump_cd(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.jump_timer >= self.jump_cooldown:
                self.ready = True

    def apply_gravity(self):
        self.gravity += 0.15
        self.rect.y += int(self.gravity)

    def constraint(self):
        if self.rect.y <= 0:
            self.rect.top = 0
        if self.rect.y >= self.border - 150:
            return "Game over"

    def player_animation(self):
        current_time = pygame.time.get_ticks()
        if self.image == self.player1 and current_time - self.player_animation_time >= 100 and self.gravity <= 6:
            self.image = self.player2
            self.player_animation_time = pygame.time.get_ticks()
        elif self.image == self.player2 and current_time - self.player_animation_time >= 100 and self.gravity <= 6:
            self.image = self.player3
            self.player_animation_time = pygame.time.get_ticks()
        elif self.image == self.player3 and current_time - self.player_animation_time >= 100 and self.gravity <= 6:
            self.image = self.player1
            self.player_animation_time = pygame.time.get_ticks()

    def player_fall_animation(self):
        if 6 <= self.gravity <= 8.5:
            self.image = self.player_fall1
        elif self.gravity >= 8.5:
            self.image = self.player_fall2

    def update(self):
        self.player_movement()
        self.apply_gravity()
        self.player_animation()
        self.player_fall_animation()
        self.jump_cd()
        self.constraint()
