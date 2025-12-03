import random
import pygame
import sys
from pygame.math import Vector2 

CELL_SIZE = 40
CELL_NUMBER = 20
BACKGROUND_COLOR = (255,209,220)
TITLE_TEXT = "SANA'S STRAWBERRY SNAKE GAME"

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direc = Vector2(1,0)
        self.new_block = False

            #pygame.draw.rect(screen,(143,111,122),body_part)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+self.direc)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direc)
            self.body = body_copy[:]

    def extend_snake(self):
        self.new_block = True

class Fruit:
    def __init__(self):
        self.x = random.randint(9,CELL_NUMBER-1)
        self.y = random.randint(0,CELL_NUMBER-1)
        self.pos = Vector2(self.x,self.y)


    def change_fruit_loc(self):
        self.x = random.randint(9,CELL_NUMBER-1)
        self.y = random.randint(0,CELL_NUMBER-1)
        self.pos = Vector2(self.x,self.y)

class Main:
    def __init__(self,screen,font,snake_image,fruit_image):
        self.snake = Snake()
        self.fruit = Fruit()
        self.screen = screen
        self.font = font
        self.snake_image = snake_image
        self.fruit_image = fruit_image

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.fail()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.change_fruit_loc()
            self.snake.extend_snake()

    def fail(self):
        if self.snake.body[0].x < 0 or self.snake.body[0].x >= CELL_NUMBER:
            self.game_over()
        if self.snake.body[0].y < 0 or self.snake.body[0].y >= CELL_NUMBER:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_elements(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_snake()
        self.draw_fruit()
        self.write_scor()
        self.title()

    def draw_snake(self):
        for block in self.snake.body:
            body_part = pygame.Rect(int(block.x*CELL_SIZE),int(block.y*CELL_SIZE),CELL_SIZE,CELL_SIZE)
            self.screen.blit(self.snake_image,body_part)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.fruit.pos.x*CELL_SIZE),int(self.fruit.pos.y*CELL_SIZE),CELL_SIZE,CELL_SIZE)
        self.screen.blit(self.fruit_image,fruit_rect)

    def title(self):
        title = "SANA'S STRAWBERRY SNAKE GAME"
        title_surface = self.font.render(title,True,(255,85,163))
        title_x = int(CELL_SIZE*CELL_NUMBER-400)
        title_y = int(CELL_SIZE*CELL_NUMBER-770)
        title_rect = title_surface.get_rect(center = (title_x,title_y))
        self.screen.blit(title_surface,title_rect)

    def write_scor(self):
        score = str(len(self.snake.body) - 3)
        score_surface = self.font.render(score,True,(255,85,163))
        score_x = int(CELL_SIZE*CELL_NUMBER-60)
        score_y = int(CELL_SIZE*CELL_NUMBER -40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        strawberry_rect = self.fruit_image.get_rect(midright=(score_rect.left,score_rect.centery))
        self.screen.blit(score_surface,score_rect)
        self.screen.blit(self.fruit_image,strawberry_rect)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((CELL_NUMBER*CELL_SIZE,CELL_NUMBER*CELL_SIZE))
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load('assets/music/game1.wav') 
        pygame.mixer.music.play(-1,0.0)
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE,150)

        fruit_image = pygame.image.load('assets/images/strawberry4.png').convert_alpha()
        fruit_image = pygame.transform.scale(fruit_image,(40,40))
        snake_image = pygame.image.load('assets/images/snake_body.png').convert_alpha()
        snake_image = pygame.transform.scale(snake_image,(40,40))
        font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf",25)
        SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(SCREEN_UPDATE,150)
        self.main_game = Main(self.screen,font,snake_image,fruit_image)

    def run(self):
        while True:
            self.handle_events()
            self.main_game.draw_elements()
            pygame.display.update()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.SCREEN_UPDATE:
                self.main_game.update()
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key):
        snake = self.main_game.snake
        if key == pygame.K_UP:
            if snake.direc.y != 1:
                snake.direc = Vector2(0,-1)
        if key == pygame.K_DOWN:
            if snake.direc.y != -1:
                snake.direc = Vector2(0,1)
        if key == pygame.K_LEFT:
            if snake.direc.x != 1:
                snake.direc = Vector2(-1,0)
        if key == pygame.K_RIGHT:
            if snake.direc.x != -1:
                snake.direc = Vector2(1,0)

def main():
    app = Game()
    app.run()

if __name__ == "__main__":
    main()
