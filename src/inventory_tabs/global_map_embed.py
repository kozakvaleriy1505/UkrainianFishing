# global_map_embed.py

import pygame

# Координати маркерів водойм (можна розширювати)
LOCATION_MARKERS = {
    "Річка Молочна": (320, 180),
    "Озеро Сиваш": (480, 220),
    "Дніпро": (600, 160),
    # Додай інші водойми тут
}

def draw_map(screen, area, profile):
    try:
        bg = pygame.image.load("assets/icons/notebook/global_map0.png")
        bg = pygame.transform.scale(bg, (area.width, area.height))
        screen.blit(bg, area.topleft)
    except Exception as e:
        font = pygame.font.SysFont("arial", 24)
        screen.blit(font.render("Не вдалося завантажити мапу", True, (255, 100, 100)), area.topleft)
        return

    # Визначаємо активну водойму
    current_waterbody = profile.get("location", {}).get("waterbody", "")
    marker_pos = LOCATION_MARKERS.get(current_waterbody)

    if marker_pos:
        # Перетворюємо координати у межах MAP_AREA
        marker_x = area.x + marker_pos[0]
        marker_y = area.y + marker_pos[1]

        # Малюємо маркер активної локації
        pygame.draw.circle(screen, (0, 255, 0), (marker_x, marker_y), 10)
        font = pygame.font.SysFont("arial", 18)
        label = font.render(current_waterbody, True, (255, 255, 255))
        screen.blit(label, (marker_x + 12, marker_y - 10))