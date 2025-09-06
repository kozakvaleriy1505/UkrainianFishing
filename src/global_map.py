# global_map.py

import os
import pygame
import pkgutil
import importlib

def load_locations():
    locs = []
    loc_dir = os.path.join(os.path.dirname(__file__), "locations")
    # Перебор усіх модулів у папці locations
    for finder, name, ispkg in pkgutil.iter_modules([loc_dir]):
        module = importlib.import_module(f"locations.{name}")
        # Перевірка наявності обовʼязкових атрибутів
        if hasattr(module, "name") and hasattr(module, "coords") and hasattr(module, "run"):
            # Підвантажуємо іконку маркера, якщо є
            icon = None
            if hasattr(module, "icon_path"):
                try:
                    icon = pygame.image.load(module.icon_path)
                except:
                    icon = None
            locs.append({
                "module": module,
                "name": module.name,
                "coords": module.coords,
                "icon": icon
            })
    return locs

def run(screen, profile):
    pygame.font.init()
    clock = pygame.time.Clock()

    # Фон глобальної мапи
    bg = pygame.image.load("assets/maps/global_map.png")
    bg = pygame.transform.scale(bg, screen.get_size())

    # Підвантажуємо локації
    locations = load_locations()

    # Розмічаємо клікабельні маркери
    markers = []
    for loc in locations:
        x, y = loc["coords"]
        rect = pygame.Rect(x, y, 32, 32)  # ширина=32, висота=32
        markers.append((loc, rect))

    running = True
    while running:
        clock.tick(30)
        screen.blit(bg, (0,0))

        # Намалювати кожен маркер
        for loc, rect in markers:
            if loc["icon"]:
                screen.blit(loc["icon"], rect.topleft)
            else:
                # Простий кружечок
                pygame.draw.circle(screen, (255,0,0), rect.center, 10)
            # Підпис під маркером
            font = pygame.font.SysFont("arial", 16)
            label = font.render(loc["name"], True, (255,255,255))
            screen.blit(label, (rect.x-10, rect.y+20))

        pygame.display.flip()

        # Обробка кліків
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx,my = e.pos
                for loc, rect in markers:
                    if rect.collidepoint(mx,my):
                        # Запуск сцени локації
                        loc["module"].run(screen, profile)
                        break