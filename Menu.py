import pygame
import os


class Menu:
    BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 800
    BUTTON_WIDTH = 300
    COLOR = (255, 255, 255)

    def __init__(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    @staticmethod
    def _get_font():
        pygame.font.init()
        return pygame.font.SysFont('arial', 30)

    def _get_button_center(self):
        mid_screen = self.SCREEN_WIDTH / 2
        mid_button = self.BUTTON_WIDTH / 2

        return mid_screen - mid_button

    def _get_font_center(self, font_width):
        mid_screen = self.SCREEN_WIDTH / 2
        mid_font = font_width / 2

        return mid_screen - mid_font

    def _generate_button_in_screen(self, text, y_position):
        font = self._get_font()
        button_center = self._get_button_center()

        difficulty = font.render(text, 1, (255, 255, 255))
        font_center = self._get_font_center(difficulty.get_width())
        self.screen.blit(difficulty, (font_center, y_position + (30 - (difficulty.get_height() / 2))))

        return pygame.draw.rect(self.screen, self.COLOR, pygame.Rect(button_center, y_position, self.BUTTON_WIDTH, 60), 2)

    def _generate_screen_difficulty(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        easy_button = self._generate_button_in_screen("EASY", 120)
        medium_button = self._generate_button_in_screen("MEDIUM", 200)
        hard_button = self._generate_button_in_screen("HARD", 280)

        # Update Display
        pygame.display.update()

        return easy_button, medium_button, hard_button

    def select_difficulty(self):
        frames_per_second = pygame.time.Clock()
        difficulty = ""

        while difficulty == "":
            frames_per_second.tick(30)

            (easy_button, medium_button, hard_button) = self._generate_screen_difficulty()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(pygame.mouse.get_pos()):
                        difficulty = "EASY"
                    elif medium_button.collidepoint(pygame.mouse.get_pos()):
                        difficulty = "MEDIUM"
                    elif hard_button.collidepoint(pygame.mouse.get_pos()):
                        difficulty = "HARD"

        return difficulty

    def _generate_screen_game_mode(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        user_button = self._generate_button_in_screen("USER", 120)
        ia_button = self._generate_button_in_screen("IA", 200)

        # Update Display
        pygame.display.update()

        return user_button, ia_button

    def select_mode(self):
        frames_per_second = pygame.time.Clock()
        mode = ""

        while mode == "":
            frames_per_second.tick(30)

            (user_button, ia_button) = self._generate_screen_game_mode()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if user_button.collidepoint(pygame.mouse.get_pos()):
                        mode = "USER"
                    elif ia_button.collidepoint(pygame.mouse.get_pos()):
                        mode = "IA"

        return mode
