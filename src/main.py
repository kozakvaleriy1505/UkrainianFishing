import pygame
import sys
import os

class TextButton:
    def __init__(self, text, pos, font, default_color, hover_color):
        self.text = text
        self.pos = pos
        self.font = font
        self.default_color = default_color
        self.hover_color = hover_color
        self.rect = None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect and self.rect.collidepoint(mouse_pos) else self.default_color
        label = self.font.render(self.text, True, color)
        self.rect = label.get_rect(center=self.pos)
        screen.blit(label, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect and self.rect.collidepoint(event.pos):
                return True
        return False
    
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ukrainian Fishing")

# Спроба завантажити фон
try:
    background = pygame.image.load("assets/backgrounds/main_menu.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    use_image = True
except:
    use_image = False

# Шрифт і кнопки
font = pygame.font.SysFont("arial", 36)
buttons = [
    TextButton("Нова гра", (WIDTH // 2, 200), font, (255, 255, 255), (255, 255, 0)),
    TextButton("Завантажити гру", (WIDTH // 2, 260), font, (255, 255, 255), (255, 255, 0)),
    TextButton("Налаштування", (WIDTH // 2, 320), font, (255, 255, 255), (255, 255, 0)),
    TextButton("Вихід", (WIDTH // 2, 380), font, (255, 255, 255), (255, 100, 100))
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
            if button.is_clicked(event):
                if button.text == "Нова гра":
                    try:
                        import new_game
                        new_game.run(screen)  # або будь-яка функція, яку ти там визначиш
                    except Exception as e:
                        print(f"[!] Не вдалося запустити 'нова гра': {e}")
                elif button.text == "Завантажити гру":
                    try:
                        import load_game
                        load_game.run(screen)  # або будь-яка функція, яку ти там визначиш
                    except Exception as e:
                        print(f"[!] Не вдалося запустити 'завантаження': {e}")
                elif button.text == "Налаштування":
                    try:
                        import options
                        options.run(screen)  # або будь-яка функція, яку ти там визначиш
                    except Exception as e:
                        print(f"[!] Не вдалося запустити 'налаштування': {e}")
                elif button.text == "Вихід":
                    running = False

    # Відображення фону
    if use_image:
        screen.blit(background, (0, 0))
    else:
        screen.fill((20, 40, 60))

    # Відображення кнопок
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()