import pygame
import json
import os
from layout import SCENE_AREA, BOTTOM_PANEL, TOP_PANEL, TENSION_AREA, SIDE_PANEL, INFO_PANEL
from widgets import tension_meter
from widgets import info_panel

def run(screen, save_path):
    import json
    font = pygame.font.SysFont("arial", 48)
    small_font = pygame.font.SysFont("arial", 24)

    try:
        map_icon = pygame.image.load("assets/icons/map.png")
        map_icon = pygame.transform.scale(map_icon, (64, 64))  # або інший розмір
    except Exception as e:
        print(f"[!] Не вдалося завантажити іконку мапи: {e}")
        map_icon = None
    
    # інфотаб
    active_info_tab = "Чат"

    # Завантаження профілю
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
    except Exception as e:
        print(f"[!] Не вдалося завантажити профіль: {e}")
        return
    
    # Завантаження часу гри
    from time_manager import TimeManager
    time = TimeManager(profile["time"])

    # Ініціалізація кнопок
    save_text = small_font.render("Збереж", True, (255, 255, 255))
    save_rect = save_text.get_rect(topright=(880, 10))

    menu_text = small_font.render("Меню", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(topright=(980, 10))

    waiting = True
    # You may need to import time and initialize last_tick and tick_interval
    import time as pytime
    last_tick = pytime.time()
    tick_interval = 1  # seconds

    inventory_icons = {
        "Снасті": "assets/icons/tackle.png",
        "Речі": "assets/icons/items.png",
        "Нотатник": "assets/icons/notebook.png",
        "Садок": "assets/icons/cage.png",
        "Їжа": "assets/icons/food.png"
    }
    # Завантаження іконок
    loaded_icons = {}
    for name, path in inventory_icons.items():
        try:
            icon = pygame.image.load(path)
            icon = pygame.transform.scale(icon, (48, 48))  # або інший розмір
            loaded_icons[name] = icon
        except Exception as e:
            print(f"[!] Не вдалося завантажити іконку '{name}': {e}")

    inventory_items = ["Снасті", "Речі", "Нотатник", "Садок", "Їжа"]
    inventory_rects = []



    while waiting:
        now = pytime.time()
        if now - last_tick >= tick_interval:
            time.tick(1)
            last_tick = now

        screen.fill((50, 80, 120))

        # області

        pygame.draw.rect(screen, (70, 100, 130), SCENE_AREA)
        scene_text = small_font.render("Локація: Туристична база", True, (255, 255, 255))
        screen.blit(scene_text, (SCENE_AREA.x + 20, SCENE_AREA.y + 20))

        pygame.draw.rect(screen, (30, 40, 60), BOTTOM_PANEL)
        inventory_items = ["Снасті", "Речі", "Нотатник", "Садок", "Їжа"]
        for i, item in enumerate(inventory_items):
            icon = loaded_icons.get(item)
            if icon:
                screen.blit(icon, (BOTTOM_PANEL.x + 20 + i * 80, BOTTOM_PANEL.y + 20))
            else:
                label = small_font.render(item, True, (200, 200, 200))
                screen.blit(label, (BOTTOM_PANEL.x + 20 + i * 80, BOTTOM_PANEL.y + 20))

        pygame.draw.rect(screen, (40, 50, 70), SIDE_PANEL)
        pygame.draw.rect(screen, (80, 100, 130), SIDE_PANEL, 2)
        if map_icon:
            screen.blit(map_icon, (SIDE_PANEL.x + 18, SIDE_PANEL.y + 60))  # центровано

        # Напис-посилання
        link_font = pygame.font.SysFont("arial", 20)
        link_text = link_font.render("На базу", True, (0, 200, 255))
        link_rect = link_text.get_rect(center=(SIDE_PANEL.x + 50, SIDE_PANEL.y + 240))
        screen.blit(link_text, link_rect)


        side_font = pygame.font.SysFont("arial", 18)

        location_label = "Локація:"
        location_value = profile["location"]["spot"]

        days_label = "Залишок днів:"
        days_value = str(profile.get("meta", {}).get("days_paid", 0))

        screen.blit(side_font.render(location_label, True, (255, 255, 255)), (SIDE_PANEL.x + 10, SIDE_PANEL.y + 350))
        screen.blit(side_font.render(location_value, True, (200, 200, 200)), (SIDE_PANEL.x + 10, SIDE_PANEL.y + 370))

        screen.blit(side_font.render(days_label, True, (255, 255, 255)), (SIDE_PANEL.x + 10, SIDE_PANEL.y + 400))
        screen.blit(side_font.render(days_value, True, (200, 200, 200)), (SIDE_PANEL.x + 10, SIDE_PANEL.y + 420))



        info_panel.draw(screen, INFO_PANEL, active_tab=active_info_tab)
        
        # Віджет навантаження на снасті
        tension_meter.draw(screen, TENSION_AREA, tension=60, line=20, reel=90)



        saturation = profile["stats"]["saturation"]
        alcohol = profile["stats"]["alcohol_level"]
        status_text = small_font.render(f"Голод: {saturation}% | Оп’яніння: {alcohol:.1f}", True, (255, 255, 255))
        screen.blit(status_text, (BOTTOM_PANEL.x + 20, BOTTOM_PANEL.y + 70))



        # Вивід профілю
        text = font.render(f"Гравець: {profile['nickname']}", True, (255, 255, 255))
        screen.blit(text, (200, 200))
        money_text = font.render(f"Гроші: {profile['money']} грн", True, (255, 255, 0))
        screen.blit(money_text, (200, 260))

        # Вивід верхньої панелі часу
        top_text = small_font.render(
            f"{time.get_weekday()} | {time.get_time_str()} | {profile['money']} грн",
            True, (255, 255, 255)
        )
        top_rect = top_text.get_rect(topleft=(20, 20))
        screen.blit(top_text, top_rect)

        # Кнопки
        screen.blit(save_text, save_rect)
        screen.blit(menu_text, menu_rect)

        pygame.display.flip()

        inventory_rects.clear()
        for i, item in enumerate(inventory_items):
            x = BOTTOM_PANEL.x + 20 + i * 80
            y = BOTTOM_PANEL.y + 20
            rect = pygame.Rect(x, y, 48, 48)
            inventory_rects.append((item, rect))


        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                if save_rect.collidepoint(event.pos):
                    print("[✓] Збереження профілю (заглушка)")

                elif menu_rect.collidepoint(event.pos):
                    print("[↩] Повернення в головне меню")
                    try:
                        import main
                        main.main()
                    except Exception as e:
                        print(f"[!] Не вдалося повернутись у меню: {e}")
                    waiting = False

                if link_rect.collidepoint(event.pos):
                    print("[↪] Гравець повертається на базу")
                    # TODO: змінити локацію в profile["location"]

                elif INFO_PANEL.collidepoint(x, y):
                    if INFO_PANEL.x + 10 <= x <= INFO_PANEL.x + 70:
                        active_info_tab = "Чат"
                    elif INFO_PANEL.x + 80 <= x <= INFO_PANEL.x + 150:
                        active_info_tab = "Події"
                    elif INFO_PANEL.x + 160 <= x <= INFO_PANEL.x + 230:
                        active_info_tab = "Гравці"
            
            for item, rect in inventory_rects:
                if rect.collidepoint(event.pos):
                    active_inventory_tab = item
                    print(f"[📦] Активна вкладка: {item}")

                    try:
                        if item == "Снасті":
                            from inventory_tabs import tackle_tab
                            tackle_tab.run(screen, profile)
                        elif item == "Речі":
                            from inventory_tabs import items_tab
                            items_tab.run(screen, profile)
                        elif item == "Нотатник":
                            from inventory_tabs import notebook_tab
                            notebook_tab.run(screen, profile)
                        elif item == "Садок":
                            from inventory_tabs import cage_tab
                            cage_tab.run(screen, profile)
                        elif item == "Їжа":
                            from inventory_tabs import food_tab
                            food_tab.run(screen, profile)
                    except Exception as e:
                        print(f"[!] Не вдалося відкрити вкладку '{item}': {e}")






        

