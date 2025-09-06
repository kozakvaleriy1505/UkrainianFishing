import pygame

# Основна сцена (турбаза, водойма, магазин тощо)
SCENE_AREA = pygame.Rect(0, 60, 1000, 440)

# Нижня панель інвентаря та стану гравця
BOTTOM_PANEL = pygame.Rect(0, 500, 900, 100)

# Верхня панель (час, гроші, день тижня)
TOP_PANEL = pygame.Rect(0, 0, 800, 60)

# Область для віджету навантаження на снасті
TENSION_AREA = pygame.Rect(
    BOTTOM_PANEL.x + BOTTOM_PANEL.width // 2 - 80 + 40,  # центр по X
    BOTTOM_PANEL.y - 40,                            # трохи нижче верхнього краю
    160, 130
)

# Вузька бокова панель зліва
SIDE_PANEL = pygame.Rect(900, 60, 100, 440)
# інфопанель
INFO_PANEL = pygame.Rect(770, 500, 240, 100)



