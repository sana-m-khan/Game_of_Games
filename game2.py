import pygame
import random
from pygame import Surface

class GameController:

    def __init__(self):
        self.model = DoggoModel()
        self.view = GameView(self.model)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.view.render()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.model.check_click(pos)

    def update(self):
        pass

class DoggoModel:

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 750
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    def __init__(self):
        # Load assets
        self.big_dog = pygame.image.load(
            r"assets\images\annoyingdog.png"
        )
        self.small_dog = pygame.image.load(
            r"assets\images\annoyingdog_smallest.png"
        )
        self.background = pygame.image.load(
            r"assets\images\pygamebg3.png"
        )

        pygame.mixer.music.load(
            r"assets\music\IRWSAYH[8-Bit].mp3"
        )
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Dog positions
        self.positions = [
            (110, 675),
            (765, 215),
            (295, 400),
            (10, 10),
            (990, 10),
            (10, 740),
            (990, 740)
        ]

        # State
        self.found_count = 0
        self.small_dog_rect = None
        self.place_new_small_dog()

    def place_new_small_dog(self):
        pos = random.choice(self.positions)
        self.small_dog_rect = self.small_dog.get_rect(topleft=pos)

    def check_click(self, pos):
        if self.small_dog_rect.collidepoint(pos):
            self.found_count += 1
            self.place_new_small_dog()
            return True
        return False

class GameView:

    def __init__(self, model):
        self.model = model
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 25)

        self.screen = pygame.display.set_mode(model.SCREEN_SIZE)
        pygame.display.set_caption("Where Is Doggo?")
        pygame.display.set_icon(model.big_dog)

    def draw_background(self):
        self.screen.blit(self.model.background, (0, 0))

    def draw_small_dog(self):
        self.screen.blit(self.model.small_dog, self.model.small_dog_rect.topleft)
        pygame.draw.rect(self.screen, (255, 255, 255), self.model.small_dog_rect, 2)

    def draw_big_example(self):
        self.screen.blit(self.model.big_dog, (100, 100))
        self.draw_text("This is a dog, find it here", 200, 90, (0, 255, 0))

    def draw_found_count(self):
        text = self.font_small.render(
            f"Doggos Found: {self.model.found_count}", True, (255, 255, 255)
        )
        self.screen.blit(text, (450, 0))

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        surf = self.font_large.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)

    def render(self):
        self.draw_background()
        self.draw_small_dog()
        self.draw_found_count()

        if self.model.found_count >= 10:
            self.draw_text("You found all the Doggos!", 
                           self.model.SCREEN_WIDTH // 2, 50, (0, 255, 0))
        else:
            self.draw_big_example()

        pygame.display.flip()

def main():
    pygame.init()
    pygame.mixer.init()

    controller = GameController()
    controller.run()

if __name__ == "__main__":
    main()