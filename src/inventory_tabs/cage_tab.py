def run(screen, profile):
    # Вивід заглушки або контенту
    import pygame
    font = pygame.font.SysFont("arial", 36)
    screen.fill((20, 40, 60))
    screen.blit(font.render("Вкладка: Риба", True, (255, 255, 255)), (100, 100))
    pygame.display.flip()

    # Очікування виходу
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                waiting = False