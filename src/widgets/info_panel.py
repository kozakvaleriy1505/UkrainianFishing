# widgets/info_panel.py

import pygame

def draw(screen, area, active_tab="Чат"):
    pygame.draw.rect(screen, (30, 40, 60), area)
    pygame.draw.rect(screen, (80, 100, 130), area, 2)

    font = pygame.font.SysFont("arial", 18)
    tabs = ["Чат", "Події", "Гравці"]

    # Вкладки
    for i, tab in enumerate(tabs):
        color = (255, 255, 255) if tab == active_tab else (150, 150, 150)
        label = font.render(tab, True, color)
        screen.blit(label, (area.x + 10 + i * 70, area.y + 10))

    # Заглушка контенту
    screen.blit(font.render(f"[{active_tab}] Поки що порожньо", True, (200, 200, 200)), (area.x + 10, area.y + 40))