import pygame
import json
import os
from layout import SCENE_AREA, BOTTOM_PANEL, TOP_PANEL, TENSION_AREA, SIDE_PANEL, INFO_PANEL
from widgets import tension_meter, info_panel

def run(screen, save_path):
    # Ініціалізація шрифтів
    font = pygame.font.SysFont("arial", 48)
    small_font = pygame.font.SysFont("arial", 24)

    # Завантажуємо іконку мапи (пізніше можна міняти залежно від локації)
    try:
        map_icon = pygame.image.load("assets/icons/map.png")
        map_icon = pygame.transform.scale(map_icon, (64, 64))
    except Exception as e:
        print(f"[!] Не вдалося завантажити іконку мапи: {e}")
        map_icon = None

    # Активні вкладки
    active_info_tab = "Чат"
    active_inventory_tab = "Снасті"

    # Завантаження профілю
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
    except Exception as e:
        print(f"[!] Не вдалося завантажити профіль: {e}")
        return

    # Таймер гри
    from time_manager import TimeManager
    time = TimeManager(profile["time"])

    # Кнопки зверху
    save_text = small_font.render("Збереж", True, (255, 255, 255))
    save_rect = save_text.get_rect(topright=(880, 10))
    menu_text = small_font.render("Меню", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(topright=(980, 10))

    # Налаштування циклу
    waiting = True
    import time as pytime
    last_tick = pytime.time()
    tick_interval = 1

    # Інвентар
    inventory_items = ["Снасті", "Речі", "Нотатник", "Садок", "Їжа"]
    inventory_rects = []

    # Завантаження іконок інвентаря
    inventory_icons = {
        "Снасті": "assets/icons/tackle.png",
        "Речі": "assets/icons/items.png",
        "Нотатник": "assets/icons/notebook.png",
        "Садок": "assets/icons/cage.png",
        "Їжа": "assets/icons/food.png"
    }
    loaded_icons = {}
    for name, path in inventory_icons.items():
        try:
            icon = pygame.image.load(path)
            icon = pygame.transform.scale(icon, (48, 48))
            loaded_icons[name] = icon
        except Exception as e:
            print(f"[!] Не вдалося завантажити іконку '{name}': {e}")

    # Головний цикл
    while waiting:
        # Оновлюємо ігровий час
        now = pytime.time()
        if now - last_tick >= tick_interval:
            time.tick(1)
            last_tick = now

        # Бекграунд
        screen.fill((50, 80, 120))

        # Основна сцена
        pygame.draw.rect(screen, (70, 100, 130), SCENE_AREA)
        scene_text = small_font.render("Локація: Туристична база", True, (255, 255, 255))
        screen.blit(scene_text, (SCENE_AREA.x + 20, SCENE_AREA.y + 20))

        # Нижня панель іконок інвентаря
        pygame.draw.rect(screen, (30, 40, 60), BOTTOM_PANEL)
        inventory_rects.clear()
        for i, item in enumerate(inventory_items):
            x = BOTTOM_PANEL.x + 20 + i * 80
            y = BOTTOM_PANEL.y + 20
            rect = pygame.Rect(x, y, 48, 48)
            inventory_rects.append((item, rect))

            icon = loaded_icons.get(item)
            if icon:
                screen.blit(icon, (x, y))
            else:
                label = small_font.render(item, True, (200, 200, 200))
                screen.blit(label, (x, y))

            # Підсвічування активної вкладки
            if item == active_inventory_tab:
                pygame.draw.rect(screen, (0, 200, 255), rect, 2)

        # Бокова панель
        pygame.draw.rect(screen, (40, 50, 70), SIDE_PANEL)
        pygame.draw.rect(screen, (80, 100, 130), SIDE_PANEL, 2)

        # Іконка мапи
        if map_icon:
            map_x = SIDE_PANEL.x + 18
            map_y = SIDE_PANEL.y + 60
            screen.blit(map_icon, (map_x, map_y))
            map_rect = pygame.Rect(map_x, map_y, 64, 64)


        # Посилання "На базу"
        link_font = pygame.font.SysFont("arial", 20)
        link_text = link_font.render("На базу", True, (0, 200, 255))
        link_rect = link_text.get_rect(center=(SIDE_PANEL.x + 50, SIDE_PANEL.y + 240))
        screen.blit(link_text, link_rect)

        # Інформаційний блок
        side_font = pygame.font.SysFont("arial", 18)
        location_label = "Локація:"
        location_value = profile["location"]["spot"]
        days_label = "Залишок днів:"
        days_value = str(profile.get("meta", {}).get("days_paid", 0))

        screen.blit(side_font.render(location_label, True, (255, 255, 255)),
                    (SIDE_PANEL.x + 10, SIDE_PANEL.y + 350))
        screen.blit(side_font.render(location_value, True, (200, 200, 200)),
                    (SIDE_PANEL.x + 10, SIDE_PANEL.y + 370))

        screen.blit(side_font.render(days_label, True, (255, 255, 255)),
                    (SIDE_PANEL.x + 10, SIDE_PANEL.y + 400))
        screen.blit(side_font.render(days_value, True, (200, 200, 200)),
                    (SIDE_PANEL.x + 10, SIDE_PANEL.y + 420))

        # Вікно чат/події/гравці
        info_panel.draw(screen, INFO_PANEL, active_tab=active_info_tab)

        # Віджет навантаження на снасті
        tension_meter.draw(screen, TENSION_AREA, tension=60, line=20, reel=90)

        # Статуси гравця
        saturation = profile["stats"]["saturation"]
        alcohol = profile["stats"]["alcohol_level"]
        status_text = small_font.render(
            f"Голод: {saturation}% | Оп’яніння: {alcohol:.1f}", True, (255, 255, 255)
        )
        screen.blit(status_text, (BOTTOM_PANEL.x + 20, BOTTOM_PANEL.y + 70))

        # Інформація про профіль
        text = font.render(f"Гравець: {profile['nickname']}", True, (255, 255, 255))
        screen.blit(text, (200, 200))
        money_text = font.render(f"Гроші: {profile['money']} грн", True, (255, 255, 0))
        screen.blit(money_text, (200, 260))

        # Верхня панель часу
        top_text = small_font.render(
            f"{time.get_weekday()} | {time.get_time_str()} | {profile['money']} грн",
            True, (255, 255, 255)
        )
        top_rect = top_text.get_rect(topleft=(20, 20))
        screen.blit(top_text, top_rect)

        # Кнопки збереження і меню
        screen.blit(save_text, save_rect)
        screen.blit(menu_text, menu_rect)

        pygame.display.flip()

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                # Збереження профілю
                if save_rect.collidepoint((x, y)):
                    print("[✓] Збереження профілю (заглушка)")

                # Повернення в меню
                elif menu_rect.collidepoint((x, y)):
                    print("[↩] Повернення в головне меню")
                    try:
                        import main
                        main.main()
                    except Exception as e:
                        print(f"[!] Не вдалося повернутись у меню: {e}")
                    waiting = False

                if map_rect.collidepoint((x, y)):
                    print("Відкриваємо вікно мапи")
                    try:
                        from inventory_tabs import map_window  # або ваш модуль
                        map_window.run(screen, profile)
                    except Exception as e:
                        print(f"[!] Помилка при відкритті мапи: {e}")


                # Перехід "На базу"
                elif link_rect.collidepoint((x, y)):
                    print("[↪] Гравець повертається на базу")
                    # TODO: змінити profile["location"]

                # Вкладки "Чат / Події / Гравці"
                elif INFO_PANEL.collidepoint(x, y):
                    rel_x = x - INFO_PANEL.x
                    if 10 <= rel_x <= 70:
                        active_info_tab = "Чат"
                    elif 80 <= rel_x <= 150:
                        active_info_tab = "Події"
                    elif 160 <= rel_x <= 230:
                        active_info_tab = "Гравці"

                # Інвентарні вкладки
                else:
                    for item, rect in inventory_rects:
                        if rect.collidepoint((x, y)):
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
    # Кінець while waiting