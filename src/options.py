import pygame

def run(screen):
    font = pygame.font.SysFont("arial", 48)
    screen.fill((50, 80, 120))
    text = font.render("Налаштування", True, (255, 255, 255))
    screen.blit(text, (200, 250))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False