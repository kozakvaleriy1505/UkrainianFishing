# notebook_tab.py

import os
import pygame
from inventory_tabs.global_map import load_locations

# Шляхи до іконок розділів
ICON_PATHS = {
    "Статистика":    "assets/icons/notebook/statistics.png",
    "Рекорди":       "assets/icons/notebook/records.png",
    "Повідомлення":   "assets/icons/notebook/messages.png",
    "Глобальна мапа": "assets/icons/notebook/global_map.png",
    "Ліцензії":      "assets/icons/notebook/licenses.png",
    "Нагороди":      "assets/icons/notebook/awards.png",
}

# Завантажуємо іконки заздалегідь
loaded_icons = {}
for name, path in ICON_PATHS.items():
    try:
        img = pygame.image.load(path)
        loaded_icons[name] = pygame.transform.scale(img, (64, 64))
    except Exception:
        loaded_icons[name] = None

def run(screen, profile):
    pygame.font.init()
    title_font   = pygame.font.SysFont("arial", 24)
    content_font = pygame.font.SysFont("arial", 20)
    info_font    = pygame.font.SysFont("arial", 18)

    # Список розділів із іменами та іконками
    sections = [
        ("Статистика",    loaded_icons["Статистика"]),
        ("Рекорди",       loaded_icons["Рекорди"]),
        ("Повідомлення",   loaded_icons["Повідомлення"]),
        ("Глобальна мапа", loaded_icons["Глобальна мапа"]),
        ("Ліцензії",      loaded_icons["Ліцензії"]),
        ("Нагороди",      loaded_icons["Нагороди"]),
    ]
    active_idx = 0

    # Розміри та області
    start_x    = 40
    icon_y     = 20
    padding    = 160
    MAP_AREA   = pygame.Rect(200, 130, 800, 460)
    INFO_AREA  = pygame.Rect(40, 130, 140, 460)

    selected_marker = None  # для збереження кліку по мітці

    clock   = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        screen.fill((20, 40, 60))

        # 1) Панель розділів
        section_rects = []
        for i, (name, icon) in enumerate(sections):
            x = start_x + i * padding
            rect = pygame.Rect(x, icon_y, 64, 64)
            section_rects.append(rect)

            if icon:
                screen.blit(icon, (x, icon_y))
            else:
                placeholder = title_font.render(name, True, (200, 200, 200))
                screen.blit(placeholder, (x, icon_y + 20))

            color = (255,255,255) if i == active_idx else (150,150,150)
            label = title_font.render(name, True, color)
            lbl_rect = label.get_rect(center=(x+32, icon_y+80))
            screen.blit(label, lbl_rect)

            if i == active_idx:
                pygame.draw.rect(screen, (0,200,255), rect, 2)

        # 2) Вміст активного розділу
        section_name = sections[active_idx][0]

        if section_name == "Глобальна мапа":
            # Контейнери
            pygame.draw.rect(screen, (30,40,60), MAP_AREA)
            pygame.draw.rect(screen, (80,100,130), MAP_AREA, 2)
            pygame.draw.rect(screen, (40,50,70), INFO_AREA)
            pygame.draw.rect(screen, (80,100,130), INFO_AREA, 2)

            # Фон мапи в MAP_AREA
            try:
                bg = pygame.image.load("assets/icons/notebook/global_map0.png")
                bg = pygame.transform.scale(bg, (MAP_AREA.width, MAP_AREA.height))
                screen.blit(bg, MAP_AREA.topleft)
            except Exception:
                screen.blit(
                    title_font.render("Не вдалося завантажити мапу", True, (255,100,100)),
                    (MAP_AREA.x+20, MAP_AREA.y+20)
                )

            # Підвантажуємо локації та малюємо маркери
            locations = load_locations()
            marker_rects = []
            for loc in locations:
                lx, ly = loc["coords"]
                mx = MAP_AREA.x + lx
                my = MAP_AREA.y + ly
                rect = pygame.Rect(mx-16, my-16, 32, 32)
                marker_rects.append((loc["name"], rect))

                if loc["icon"]:
                    screen.blit(loc["icon"], rect.topleft)
                else:
                    pygame.draw.circle(screen, (255,0,0), rect.center, 10)

                # Назва під маркером
                lbl = info_font.render(loc["name"], True, (255,255,255))
                screen.blit(lbl, (rect.x-10, rect.y+20))

            # Підсвічуємо активну водойму
            current = profile.get("location", {}).get("waterbody", "")
            for name, rect in marker_rects:
                if name == current:
                    pygame.draw.rect(screen, (0,255,0), rect, 2)
                    lbl = info_font.render("Активно", True, (0,255,0))
                    screen.blit(lbl, (rect.x, rect.y-20))

            # Вивід інформації про вибрану мітку
            if selected_marker:
                txt = f"Клікнуто: {selected_marker}"
                info_lbl = info_font.render(txt, True, (255,255,255))
                screen.blit(info_lbl, (INFO_AREA.x+10, INFO_AREA.y+20))

        else:
            # Заглушка по інших розділах
            text = f"[{section_name}] Заглушка контенту"
            lbl = content_font.render(text, True, (255,255,255))
            screen.blit(lbl, (MAP_AREA.x+20, MAP_AREA.y+20))

        pygame.display.flip()

        # 3) Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RIGHT:
                    active_idx = (active_idx + 1) % len(sections)
                    selected_marker = None
                elif event.key == pygame.K_LEFT:
                    active_idx = (active_idx - 1) % len(sections)
                    selected_marker = None

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Перемикаємо вкладку
                for i, rect in enumerate(section_rects):
                    if rect.collidepoint(mx, my):
                        active_idx = i
                        selected_marker = None
                        break

                # Якщо активна "Глобальна мапа" — перевіряємо кліки по маркерах
                if section_name == "Глобальна мапа" and MAP_AREA.collidepoint(mx, my):
                    for name, rect in marker_rects:
                        if rect.collidepoint(mx, my):
                            selected_marker = name
                            # сюди можна додати profile оновлення або імпорт модуля локації
                            break

    # Повернення до попереднього вікна
    return