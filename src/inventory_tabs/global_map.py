import os
import pygame
import pkgutil
import importlib

def load_locations():
    locs = []
    loc_dir = os.path.join(os.path.dirname(__file__), "locations")
    for finder, name, ispkg in pkgutil.iter_modules([loc_dir]):
        module = importlib.import_module(f"locations.{name}")
        if hasattr(module, "name") and hasattr(module, "coords") and hasattr(module, "run"):
            icon = None
            if hasattr(module, "icon_path"):
                try:
                    icon = pygame.image.load(module.icon_path)
                except:
                    icon = None
            locs.append({
                "module": module,
                "name": module.name,
                "coords": module.coords,
                "icon": icon
            })
    return locs

def run(screen, profile):
    pygame.font.init()
    clock = pygame.time.Clock()

    # Фон глобальної мапи
    try:
        bg = pygame.image.load("assets/icons/notebook/global_map0.png")
        bg = pygame.transform.scale(bg, screen.get_size())
    except Exception as e:
        screen.fill((20, 40, 60))
        font = pygame.font.SysFont("arial", 24)
        screen.blit(font.render("Не вдалося завантажити мапу", True, (255, 100, 100)), (50, 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        return

    # Завантаження локацій
    locations = load_locations()

    # Розмітка маркерів
    markers = []
    for loc in locations:
        x, y = loc["coords"]
        rect = pygame.Rect(x, y, 32, 32)
        markers.append((loc, rect))

    running = True
    while running:
        clock.tick(30)
        screen.blit(bg, (0, 0))

        # Малюємо маркери
        for loc, rect in markers:
            if loc["icon"]:
                screen.blit(loc["icon"], rect.topleft)
            else:
                pygame.draw.circle(screen, (255, 0, 0), rect.center, 10)

            font = pygame.font.SysFont("arial", 16)
            label = font.render(loc["name"], True, (255, 255, 255))
            screen.blit(label, (rect.x - 10, rect.y + 20))

        # Підсвічування активної водойми
        current = profile.get("location", {}).get("waterbody", "")
        for loc, rect in markers:
            if loc["name"] == current:
                pygame.draw.rect(screen, (0, 255, 0), rect, 2)
                label = font.render("Активна локація", True, (0, 255, 0))
                screen.blit(label, (rect.x, rect.y - 20))

        pygame.display.flip()

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for loc, rect in markers:
                    if rect.collidepoint(mx, my):
                        profile["location"]["waterbody"] = loc["name"]
                        profile["location"]["spot"] = "Берег"  # або дефолтна точка
                        try:
                            loc["module"].run(screen, profile)
                        except Exception as e:
                            print(f"[!] Не вдалося запустити локацію '{loc['name']}': {e}")
                        running = False
                        break

def draw_embedded_map(screen, area, profile):
    try:
        bg = pygame.image.load("assets/icons/notebook/global_map0.png")
        bg = pygame.transform.scale(bg, (area.width, area.height))
        screen.blit(bg, area.topleft)
    except Exception as e:
        font = pygame.font.SysFont("arial", 24)
        screen.blit(font.render("Не вдалося завантажити мапу", True, (255, 100, 100)), area.topleft)
        return

    # Завантаження локацій
    locations = load_locations()

    # Малюємо маркери
    for loc in locations:
        x, y = loc["coords"]
        marker_x = area.x + x
        marker_y = area.y + y
        rect = pygame.Rect(marker_x, marker_y, 32, 32)

        if loc["icon"]:
            screen.blit(loc["icon"], rect.topleft)
        else:
            pygame.draw.circle(screen, (255, 0, 0), rect.center, 10)

        font = pygame.font.SysFont("arial", 16)
        label = font.render(loc["name"], True, (255, 255, 255))
        screen.blit(label, (rect.x - 10, rect.y + 20))

    # Підсвічування активної водойми
    current = profile.get("location", {}).get("waterbody", "")
    for loc in locations:
        rect = pygame.Rect(marker_x, marker_y, 32, 32)
        if mouse_pos and rect.collidepoint(mouse_pos):
            profile["hovered_location"] = loc["name"]
        if loc["name"] == current:
            marker_x = area.x + loc["coords"][0]
            marker_y = area.y + loc["coords"][1]
            rect = pygame.Rect(marker_x, marker_y, 32, 32)
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)
            label = font.render("Активна локація", True, (0, 255, 0))
            screen.blit(label, (rect.x, rect.y - 20))

