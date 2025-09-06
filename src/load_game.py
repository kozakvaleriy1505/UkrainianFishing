import os
import pygame
from game_window import run as run_game

def run(screen):
    # Шрифти
    pygame.font.init()
    title_font = pygame.font.SysFont("arial", 36)
    item_font  = pygame.font.SysFont("arial", 28)

    # Зчитуємо всі json-файли у папці save/
    save_dir = "save"
    try:
        files = [f for f in os.listdir(save_dir) if f.endswith(".json")]
    except FileNotFoundError:
        files = []

    if not files:
        # Якщо папки нема або немає збережень
        screen.fill((50, 80, 120))
        text = title_font.render("Немає жодного збереження", True, (255, 200, 200))
        screen.blit(text, (200, 250))
        pygame.display.flip()

        # Чекаємо ESC або закриття
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
        return

    # Індикація вибраного профілю
    selected = 0

    # Основний цикл вікна завантаження
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        clock.tick(30)
        screen.fill((50, 80, 120))

        # Заголовок
        header = title_font.render("Завантажити профіль", True, (255, 255, 255))
        screen.blit(header, (200, 100))

        # Малюємо список файлів
        y_start = 180
        item_height = 40
        for idx, filename in enumerate(files):
            name = filename[:-5]  # обрізати ".json"
            color = (255, 255, 0) if idx == selected else (200, 200, 200)
            label = item_font.render(name, True, color)
            pos = (200, y_start + idx * item_height)
            screen.blit(label, pos)

        pygame.display.flip()

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(files)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(files)
                elif event.key == pygame.K_RETURN:
                    # Обираємо файл і запускаємо гру
                    save_path = os.path.join(save_dir, files[selected])
                    run_game(screen, save_path)
                    waiting = False
                    break

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Перевіряємо кліки по кожному рядку
                for idx, filename in enumerate(files):
                    rect = pygame.Rect(200, y_start + idx * item_height, 300, item_height)
                    if rect.collidepoint(mx, my):
                        save_path = os.path.join(save_dir, filename)
                        run_game(screen, save_path)
                        waiting = False
                        break