import pygame

def draw_bar_horizontal(screen, x, y, width, height, value):
    # Обчислення ширини заповнення
    fill_width = int(width * (value / 100))

    # Колір залежно від навантаження
    if value < 50:
        color = (0, 200, 0)      # зелений
    elif value < 80:
        color = (255, 200, 0)    # жовтий
    else:
        color = (255, 0, 0)      # червоний

    # Рамка
    pygame.draw.rect(screen, (80, 100, 130), (x, y, width, height), 2)
    # Заповнення
    pygame.draw.rect(screen, color, (x + 2, y + 2, fill_width - 4, height - 4))

def draw(screen, area, tension=0, line=0, reel=0):
    pygame.draw.rect(screen, (25, 35, 55), area)
    pygame.draw.rect(screen, (80, 100, 130), area, 2)

    font = pygame.font.SysFont("arial", 18)

    # Параметри шкал
    bar_width = 120
    bar_height = 16
    spacing = 35
    start_x = area.x + 20
    start_y = area.y + 30

    # Вудка
    screen.blit(font.render("Вудка", True, (200, 200, 200)), (start_x, start_y - 20))
    draw_bar_horizontal(screen, start_x, start_y, bar_width, bar_height, tension)

    # Волосінь
    screen.blit(font.render("Волосінь", True, (200, 200, 200)), (start_x, start_y + spacing - 20))
    draw_bar_horizontal(screen, start_x, start_y + spacing, bar_width, bar_height, line)

    # Котушка
    screen.blit(font.render("Котушка", True, (200, 200, 200)), (start_x, start_y + spacing * 2 - 20))
    draw_bar_horizontal(screen, start_x, start_y + spacing * 2, bar_width, bar_height, reel)