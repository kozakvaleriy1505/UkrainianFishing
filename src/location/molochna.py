# locations/molochna.py

"""
Модуль-локація «Річка Молочна».

Визначає метадані для глобальної мапи, інформацію для нотатника
та функцію run(screen, profile), яка запускає сцену водойми.
"""

import pygame

# 1) Метадані для глобальної мапи та нотатника
name           = "Річка Молочна"                                         # відображається на карті
coords         = (320, 180)                                              # піксельні координати маркера
icon_path      = "assets/locations/molochna/marker.png"                  # іконка маркера

# 2) Інформація для INFO_AREA у нотатнику
description    = (
    "Тиха річка з піщаними берегами, "
    "ідеальна для лову коропа та карася."
)
price_per_day  = 150  # грн за добу
transport_info = (
    "Автомобілем трасою H08 до села Приютне, "
    "далі пішки 2 км вздовж берега."
)

# 3) Точки інтересу всередині водойми
WATERBODY_LOCATIONS = {
    "Берег": {
        "pos": (100, 300),
        "bg":  "assets/locations/molochna/river_bank.png"
    },
    "Місток": {
        "pos": (300, 250),
        "bg":  "assets/locations/molochna/river_dock.png"
    },
    "Очерет": {
        "pos": (500, 280),
        "bg":  "assets/locations/molochna/river_reeds.png"
    },
}

def run(screen, profile):
    """
    Запускає сцену річки Молочної.

    Відображає фон вибраної точки (spot), її назву та кнопки
    для переходу між «Берег», «Місток» та «Очерет».
    """
    pygame.font.init()
    header_font = pygame.font.SysFont("arial", 36)
    button_font = pygame.font.SysFont("arial", 24)

    # Отримуємо або встановлюємо початкову точку
    loc_data = profile.setdefault("location", {})
    current_spot = loc_data.get("spot", "Берег")

    # Завантажуємо відповідний фон
    bg_path = WATERBODY_LOCATIONS.get(current_spot, {}) .get("bg")
    try:
        bg = pygame.image.load(bg_path)
        bg = pygame.transform.scale(bg, screen.get_size())
    except Exception:
        bg = None

    running = True
    while running:
        screen.fill((20, 40, 60))
        if bg:
            screen.blit(bg, (0, 0))
        else:
            err = button_font.render("Не вдалося завантажити фон", True, (255,100,100))
            screen.blit(err, (50,50))

        # Заголовок із назвою поточної точки
        title = header_font.render(f"Точка: {current_spot}", True, (255,255,255))
        screen.blit(title, (50, 20))

        # Малюємо кнопки для інших точок
        buttons = []
        y = screen.get_height() - 80
        for idx, spot in enumerate(WATERBODY_LOCATIONS):
            rect = pygame.Rect(50 + idx * 160, y, 140, 40)
            pygame.draw.rect(screen, (80,120,160), rect)
            lbl = button_font.render(spot, True, (255,255,255))
            screen.blit(lbl, (rect.x + 10, rect.y + 8))
            buttons.append((rect, spot))

        pygame.display.flip()

        for evt in pygame.event.get():
            if evt.type == pygame.QUIT or (evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
                running = False
            elif evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                for rect, spot in buttons:
                    if rect.collidepoint(evt.pos):
                        # Оновлюємо профіль і перезапускаємо сцену
                        loc_data["spot"] = spot
                        return run(screen, profile)
    # Повернення в попередній контекст
    return