import pygame
import json
import os

def run(screen, save_path):
    import json
    font = pygame.font.SysFont("arial", 48)
    small_font = pygame.font.SysFont("arial", 24)

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
    save_rect = save_text.get_rect(topright=(680, 10))

    menu_text = small_font.render("Меню", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(topright=(780, 10))

    waiting = True
    # You may need to import time and initialize last_tick and tick_interval
    import time as pytime
    last_tick = pytime.time()
    tick_interval = 1  # seconds

    while waiting:
        now = pytime.time()
        if now - last_tick >= tick_interval:
            time.tick(1)
            last_tick = now

        screen.fill((50, 80, 120))

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

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

