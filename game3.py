import pygame
import random
import time
import json
import requests
from pathlib import Path
from io import BytesIO


class MemoryModel:
    """
    Manages card data, timer, moves, matches, and game logic.
    """

    def __init__(self, grid_size=4, timer_limit=120):
        self.grid_size = grid_size
        self.timer_limit = timer_limit

        self.card_state = [False] * (grid_size ** 2)
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0

        self.timer_start = time.time()
        self.flip_delay = 1.0
        self.checking_match = False
        self.match_check_time = 0

        self.images = self.load_images_from_json()
        self.cards = self.prepare_cards(self.images)

    def load_images_from_json(self):
        """
        Loads card image URLs from assets/images/images.json.
        """
        root = Path(__file__).resolve().parent.parent
        path = root / "assets" /"images"/ "images.json"

        if not path.exists():
            raise FileNotFoundError(f"Missing images.json at {path}")

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        return data["images"]

    def prepare_cards(self, urls):
        """
        Duplicate the image list to make pairs and shuffle.
        """
        cards = urls * 2
        random.shuffle(cards)
        return cards

    def reset(self):
        """
        Reset game to initial state.
        """
        self.card_state = [False] * (self.grid_size ** 2)
        self.flipped_cards = []
        self.matched_pairs = 0
        self.moves = 0
        self.timer_start = time.time()
        self.checking_match = False
        self.cards = self.prepare_cards(self.images)

    def can_flip(self, index):
        return not self.card_state[index] and len(self.flipped_cards) < 2

    def flip_card(self, index):
        self.card_state[index] = True
        self.flipped_cards.append(index)
        self.moves += 1

        if len(self.flipped_cards) == 2:
            self.checking_match = True
            self.match_check_time = time.time()

    def update_match_logic(self):
        """
        Check if flipped cards match.
        """
        if len(self.flipped_cards) < 2:
            return

        i1, i2 = self.flipped_cards
        if self.cards[i1] == self.cards[i2]:
            self.matched_pairs += 1
        else:
            self.card_state[i1] = False
            self.card_state[i2] = False

        self.flipped_cards = []
        self.checking_match = False

    def is_game_over(self):
        return self.matched_pairs == (self.grid_size ** 2) // 2

    def time_remaining(self):
        elapsed = time.time() - self.timer_start
        return max(0, self.timer_limit - int(elapsed))

    def out_of_time(self):
        return self.time_remaining() <= 0


class AssetLoader:
    """
    Loads card images, local or URL.
    """

    def __init__(self):
        root = Path(__file__).resolve().parent.parent
        self.assets_dir = root / "assets"

    def load_card_back(self):
        path = self.assets_dir / "card_back.png"

        if path.exists():
            return pygame.image.load(str(path))

        url = "https://img.icons8.com/ios11/512/F25081/monster-energy.png"
        req = requests.get(url)
        req.raise_for_status()
        return pygame.image.load(BytesIO(req.content))

    def load_image(self, identifier):
        """
        Loads a URL or local file.
        """

        local = self.assets_dir / identifier
        if local.exists():
            return pygame.image.load(str(local))

        req = requests.get(identifier)
        req.raise_for_status()
        return pygame.image.load(BytesIO(req.content))


class MemoryView:
    """
    Draws everything on screen — cards, timer, moves, UI.
    """

    def __init__(self, model):
        pygame.init()

        self.model = model
        self.width = 400
        self.height = 450
        self.card_size = 100
        self.top_margin = 50

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GOLD = (255, 215, 0)

        self.font = pygame.font.Font(None, 24)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Memory Puzzle Game")

        loader = AssetLoader()
        self.card_back = loader.load_card_back()
        self.card_back = pygame.transform.scale(self.card_back, (self.card_size - 10, self.card_size - 10))

        self.loader = loader
        self.cached = {}

    def load_card(self, identifier):
        if identifier not in self.cached:
            img = self.loader.load_image(identifier)
            img = pygame.transform.scale(img, (self.card_size - 10, self.card_size - 10))
            self.cached[identifier] = img
        return self.cached[identifier]

    def draw_restart_button(self):
        rect = (self.width - 110, 10, 100, 30)
        pygame.draw.rect(self.screen, self.WHITE, rect)
        pygame.draw.rect(self.screen, self.GOLD, rect, 2)

        text = self.font.render("Restart", True, self.BLACK)
        self.screen.blit(text, text.get_rect(center=(self.width - 60, 25)))

        return rect

    def draw(self):
        self.screen.fill(self.WHITE)

        idx = 0
        for row in range(self.model.grid_size):
            for col in range(self.model.grid_size):
                x = col * self.card_size
                y = self.top_margin + row * self.card_size

                rect = pygame.Rect(x, y, self.card_size, self.card_size)
                pygame.draw.rect(self.screen, self.WHITE, rect)
                pygame.draw.rect(self.screen, self.GOLD, rect, 3)

                if self.model.card_state[idx]:
                    img = self.load_card(self.model.cards[idx])
                else:
                    img = self.card_back

                self.screen.blit(img, (x + 5, y + 5))
                idx += 1

        moves_text = self.font.render(f"Moves: {self.model.moves}", True, self.BLACK)
        self.screen.blit(moves_text, (10, 10))

        self.draw_restart_button()

        remaining = self.model.time_remaining()
        timer_text = self.font.render(f"Time: {remaining // 60}:{remaining % 60:02d}", True, self.BLACK)
        self.screen.blit(timer_text, (10, 30))

        pygame.display.flip()

    def show_message(self, message):
        text = self.font.render(message, True, self.BLACK)
        rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()


class MemoryGameController:
    """
    Handles events, updates model, and runs loop.
    """

    def __init__(self):
        self.model = MemoryModel()
        self.view = MemoryView(self.model)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update_logic()
            self.view.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.model.checking_match:
                mx, my = pygame.mouse.get_pos()

                if self.in_rect(mx, my, (self.view.width - 110, 10, 100, 30)):
                    self.model.reset()
                    return

                row = (my - self.view.top_margin) // self.view.card_size
                col = mx // self.view.card_size

                if 0 <= row < self.model.grid_size:
                    idx = row * self.model.grid_size + col
                    if self.model.can_flip(idx):
                        self.model.flip_card(idx)

    def update_logic(self):
        if self.model.checking_match and time.time() - self.model.match_check_time >= self.model.flip_delay:
            self.model.update_match_logic()

        if self.model.is_game_over():
            self.view.show_message("Congratulations!")
            time.sleep(2)
            self.model.reset()

        if self.model.out_of_time():
            self.view.show_message("Time's up!")
            time.sleep(2)
            self.model.reset()

    @staticmethod
    def in_rect(x, y, rect):
        rx, ry, rw, rh = rect
        return rx < x < rx + rw and ry < y < ry + rh


def main():
    pygame.init()
    controller = MemoryGameController()
    controller.run()


if __name__ == "__main__":
    main()
