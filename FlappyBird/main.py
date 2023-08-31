import pygame
from sys import exit
from random import randint
from obstacle import Obstacle
from player import Player


class Game:
    def __init__(self):
        self.background = pygame.image.load("graphics/flappy_background.png").convert_alpha()
        self.grass_surf = pygame.image.load("graphics/flappy_grass.png").convert_alpha()
        self.grass_rect = self.grass_surf.get_rect(topleft=((0, 775)))
        self.grass2_rect = self.grass_surf.get_rect(topleft=(1400, 775))

        self.obstacle_group = pygame.sprite.Group()
        self.OBSTACLE_TIMER = pygame.USEREVENT + 1
        pygame.time.set_timer(self.OBSTACLE_TIMER, 1200)
        self.game_state = "Start"

        self.player_sprite = Player((screen_width / 2, screen_height / 2), screen_height)
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player_sprite)

        self.font = pygame.font.Font("font/Pixeled.ttf", 30)
        self.font2 = pygame.font.Font("font/Pixeled.ttf", 40)
        self.score = 0
        self.score_board1 = pygame.image.load("graphics/score_board.png").convert_alpha()
        self.score_board2 = pygame.image.load("graphics/score_board2.png").convert_alpha()
        self.score_image = self.score_board1
        self.score_rect = self.score_image.get_rect(midtop=(screen_width / 2, -376))
        self.reset_game_time = 0
        self.score_ready = False

        self.obstacle_animation_time = 0
        self.OBSTACLE_ANIMATION_TIMER = pygame.USEREVENT + 2
        pygame.time.set_timer(self.OBSTACLE_ANIMATION_TIMER, 600)

        self.point_sound = pygame.mixer.Sound("sound/point_sound.wav")
        self.point_sound.set_volume(0.3)
        self.restart_sound = pygame.mixer.Sound("sound/restart_sound.mp3")
        self.point_sound.set_volume(0.1)
        self.game_over_sound = pygame.mixer.Sound("sound/game_over.wav")
        self.game_over_sound.set_volume(0.1)

    def display_background(self):
        screen.blit(self.background, (0, 0))

    def display_grass(self):
        screen.blit(self.grass_surf, self.grass_rect)
        screen.blit(self.grass_surf, self.grass2_rect)

    def grass_setup(self):
        if self.grass_rect.left <= -1400:
            self.grass_rect.left = 1400
        elif self.grass2_rect.left <= -1400:
            self.grass2_rect.left = 1400
        self.grass_rect.x -= 3
        self.grass2_rect.x -= 3

    def obstacle_setup(self):
        y_up = randint(150, 400)
        y_down = y_up + 250
        self.obstacle_group.add(Obstacle((screen_width + 150, y_down), 3, "down"))
        self.obstacle_group.add(Obstacle((screen_width + 150, y_up), 3, "up"))

    def collisions(self):
        if self.obstacle_group:
            for obstacle in self.obstacle_group.sprites():
                if pygame.sprite.spritecollide(obstacle, self.player_group, False):
                    self.game_state = "End"
                    self.game_over_sound.play()
        if self.player_sprite.constraint() == "Game over":
            self.game_over_sound.play()
            self.game_state = "End"

    def score_setup(self):
        score_surf = self.font.render("{}".format(int(self.score)), True, "#B39E82")
        score_rect = score_surf.get_rect(center=(screen_width / 2, 30))
        screen.blit(score_surf, score_rect)

    def score_updating(self):
        if self.obstacle_group:
            for obstacle in self.obstacle_group.sprites():
                if abs(self.player_sprite.rect.x - obstacle.rect.x) <= 1:
                    self.score += 0.5
                    self.point_sound.play()

    def losing_screen(self):

        surf1 = self.font2.render("{}".format(int(self.score)), True, "#B39E82")
        rect1 = surf1.get_rect(midbottom=(screen_width / 2, screen_height / 2 + 40))
        self.player_group.draw(screen)
        self.obstacle_group.draw(screen)
        self.finall_score_animation()
        if self.score_ready:
            screen.blit(surf1, rect1)

    def game_restart(self):
        self.score_image = self.score_board1
        self.obstacle_group.empty()
        self.player_sprite.rect.center = (screen_width / 2, screen_height / 2)
        self.score = 0
        self.player_sprite.gravity = 0
        self.player_sprite.image = self.player_sprite.player1
        self.score_rect.top = -376
        self.score_ready = False

    def obstacle_animation(self):
        if self.obstacle_group:
            for obstacle in self.obstacle_group.sprites():
                if -130 <= obstacle.rect.left <= 800:
                    obstacle.image = obstacle.obstacle2
                    self.obstacle_animation_time = pygame.time.get_ticks()

    def obstacle_animation2(self):
        current_time = pygame.time.get_ticks()
        if self.obstacle_group and current_time - self.obstacle_animation_time >= 300:
            for obstacle in self.obstacle_group.sprites():
                obstacle.image = obstacle.obstacle1

    def restart_button_animation(self):
        if self.score_image == self.score_board1:
            self.score_image = self.score_board2
            self.restart_sound.play()
            self.reset_game_time = pygame.time.get_ticks()

    def restart_button_animation2(self):
        current_time = pygame.time.get_ticks()
        if self.game_state == "End" and 380 <= current_time - self.reset_game_time <= 410:
            self.game_state = "Start"

    def finall_score_animation(self):
        screen.blit(self.score_image, self.score_rect)
        if self.game_state == "End" and self.score_rect.midtop[1] <= 262:
            self.score_rect.y += 8
        if self.score_rect.midtop[1] >= 262:
            self.score_ready = True

    def run(self):
        if self.game_state == "Game":
            self.display_background()
            self.obstacle_group.update()
            self.obstacle_group.draw(screen)
            self.player_group.update()
            self.player_group.draw(screen)
            self.display_grass()
            self.collisions()
            self.grass_setup()
            self.score_setup()
            self.score_updating()
            self.obstacle_animation2()
        elif self.game_state == "Start":
            self.game_restart()
            self.display_background()
            self.player_group.draw(screen)
            self.score_setup()
            self.display_grass()
        elif self.game_state == "End":
            self.display_background()
            self.losing_screen()
            self.display_grass()
            self.restart_button_animation2()


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen_width, screen_height = 700, 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flappy Bird")
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif game.game_state == "Game" and event.type == game.OBSTACLE_TIMER:
                game.obstacle_setup()
            elif game.game_state == "Game" and event.type == game.OBSTACLE_ANIMATION_TIMER:
                game.obstacle_animation()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game.game_state == "End":
                game.game_state = "Game"
            elif game.game_state == "End" and event.type == pygame.MOUSEBUTTONDOWN and \
                    (268 <= pygame.mouse.get_pos()[0] <= 430 and 520 <= pygame.mouse.get_pos()[1] <= 580):
                game.restart_button_animation()

        game.run()
        clock.tick(120)
        pygame.display.update()
