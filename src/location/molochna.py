# locations/molochna.py

# Назва, яка виводиться на глобальній карті
name = "Річка Молочна"

# Піксельні координати маркера на глобальній карті
coords = (320, 180)

# Іконка маркера (за бажанням)
icon_path = "assets/locations/molochna/marker.png"

def run(screen, profile):
    # тут імпортуєш і запускаєш сцену місцевості
    import pygame
    pygame.font.init()
    font = pygame.font.SysFont("arial", 36)
    screen.fill((20, 40, 60))
    screen.blit(font.render("Тут сцена Річки Молочна", True, (255,255,255)), (100,100))
    pygame.display.flip()

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                waiting = False