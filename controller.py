import pygame
import sys
from src import game1
from src import game2
from src import game3
from src import game4

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70
BUTTON_SPACING = 100

class Controller:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.font = pygame.font.SysFont(None,48)
        self.small_font = pygame.font.SysFont(None, 28)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Game Menu")

        self.games = {
            "Strawberry Snake": game1,
            "Where's Doggo": game2,
            "Puzzle Game": game3,
            "game 4": game4
        }
        
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        y = 200
        for name in self.games.keys():
            rect = pygame.Rect(
                SCREEN_WIDTH //2 - BUTTON_WIDTH//2,y, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.buttons.append((name,rect))
            y+=BUTTON_SPACING

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_menu_events(event.pos)

            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_menu_events(self, mouse_pos):
        for name, rect in self.buttons:
            if rect.collidepoint(mouse_pos):
                game_module = self.games[name]
                game_module.main()

    def draw_menu(self):
        self.screen.fill((35,35,35))

        title = self.font.render("Game Title",True, (255,255,255))
        self.screen.blit(title, (SCREEN_WIDTH//2-title.get_width()//2,100))

        for name, rect in self.buttons:
            pygame.draw.rect(self.screen, (255,105,180), rect, border_radius = 15)
            label = self.small_font.render(name,True,(0,0,0))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label,label_rect)
