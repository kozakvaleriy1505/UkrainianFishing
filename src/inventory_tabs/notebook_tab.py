# notebook_tab.py

import os
import pygame
from inventory_tabs import global_map_embed

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
    title_font = pygame.font.SysFont("arial", 24)
    content_font = pygame.font.SysFont("arial", 20)

    # Список розділів із іменами та іконками
    sections = [
        ("Статистика",    loaded_icons["Статистика"]),
        ("Рекорди",       loaded_icons["Рекорди"]),
        ("Повідомлення",   loaded_icons["Повідомлення"]),
        ("Глобальна мапа", loaded_icons["Глобальна мапа"]),
        ("Ліцензії",      loaded_icons["Ліцензії"]),
        ("Нагороди",      loaded_icons["Нагороди"]),
    ]
    active_idx = 0  # індекс активного розділу

    # Позиціонування панелі розділів
    start_x = 40
    icon_y   = 20
    padding  = 160

    clock = pygame.time.Clock()
    waiting = True
    MAP_AREA = pygame.Rect(200, 130, 800, 460)

    while waiting:
        clock.tick(30)
        screen.fill((20, 40, 60))

        # Малюємо панель розділів
        section_rects = []
        for i, (name, icon) in enumerate(sections):
            x = start_x + i * padding
            rect = pygame.Rect(x, icon_y, 64, 64)
            section_rects.append(rect)

            # Іконка або текст замість неї
            if icon:
                screen.blit(icon, (x, icon_y))
            else:
                placeholder = title_font.render(name, True, (200, 200, 200))
                screen.blit(placeholder, (x, icon_y + 20))

            # Підпис
            color = (255, 255, 255) if i == active_idx else (150, 150, 150)
            label = title_font.render(name, True, color)
            label_rect = label.get_rect(center=(x + 32, icon_y + 80))
            screen.blit(label, label_rect)

            # Обведення активного розділу
            if i == active_idx:
                pygame.draw.rect(screen, (0, 200, 255), rect, 2)

        # Малюємо контент активного розділу
            section_name = sections[active_idx][0]

            if section_name == "Глобальна мапа":
                pygame.draw.rect(screen, (30, 40, 60), MAP_AREA)
                pygame.draw.rect(screen, (80, 100, 130), MAP_AREA, 2)
                global_map_embed.draw_map(screen, MAP_AREA, profile)
            else:
                content_text = f"[{section_name}] Заглушка контенту"
                content_label = content_font.render(content_text, True, (255, 255, 255))
                screen.blit(content_label, (MAP_AREA.x + 20, MAP_AREA.y + 20))


        pygame.display.flip()

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                elif event.key == pygame.K_RIGHT:
                    active_idx = (active_idx + 1) % len(sections)
                elif event.key == pygame.K_LEFT:
                    active_idx = (active_idx - 1) % len(sections)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Натиск на іконку розділу
                for i, rect in enumerate(section_rects):
                    if rect.collidepoint(mx, my):
                        active_idx = i
                        break

    # Повернутись до попереднього вікна
    return