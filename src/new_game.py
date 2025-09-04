import pygame
import json
import os

def run(screen):
    pygame.font.init()
    font = pygame.font.SysFont("arial", 32)
    small_font = pygame.font.SysFont("arial", 24)

    #спроба завантажити фон
    try:
        background = pygame.image.load("assets/backgrounds/window.png")
        background = pygame.transform.scale(background, screen.get_size())
        use_image = True
    except Exception as e:
        print(f"[!] Не вдалося завантажити фон: {e}")
        use_image = False

    input_text = "Я у мами рибалка"
    active_input = True

    difficulties = ["Легка", "Нормально", "Важка"]
    selected = 1  # за замовчуванням "Нормально"

    running = True
    while running:
        if use_image:
            screen.blit(background, (0, 0))
        else:
            screen.fill((50, 80, 120))

        # Заголовок
        title = font.render("Створення нового профілю", True, (255, 255, 255))
        screen.blit(title, (220, 50))

        # Поле вводу нікнейму
        name_label = small_font.render("Ім’я профілю:", True, (200, 200, 200))
        screen.blit(name_label, (100, 150))
        name_input = font.render(input_text + ("|" if active_input else ""), True, (255, 255, 0))
        screen.blit(name_input, (100, 180))

        # Вибір складності
        diff_label = small_font.render("Складність:", True, (200, 200, 200))
        screen.blit(diff_label, (100, 250))
        for i, diff in enumerate(difficulties):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            diff_text = font.render(diff, True, color)
            screen.blit(diff_text, (120 + i * 180, 280))

        # Кнопка старту
        start_text = font.render("▶ Старт гри", True, (0, 255, 0))
        screen.blit(start_text, (300, 400))

        pygame.display.flip()

        # Обробка подій
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if active_input:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_input = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        input_text += event.unicode

                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(difficulties)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= x <= 500 and 400 <= y <= 440:
                    nickname = input_text.strip()
                    if nickname == "":
                        print("[!] Ім’я профілю не може бути порожнім!")
                        continue
                    print(f"▶ Створення профілю: {input_text}, складність: {difficulties[selected]}")
                    
                # Створення структури профілю

                difficulty = difficulties[selected]
                money_map = {"Легка": 1000, "Нормально": 500, "Важка": 200}
                profile_data = {
                    "nickname": nickname,
                    "difficulty": difficulty,
                    "money": money_map[difficulty],
                    "inventory": {"gear": [], "food": [], "fish": []},
                    "location": {"waterbody": "Річка Молочна", "spot": "Туристична база"},
                    "time": {"day": 1, "hour": 10, "minute": 00},
                    "stats": {"saturation": 100, "alcohol_level": 0.0}
                }
                
                # Збереження у файл
                os.makedirs("save", exist_ok=True)
                save_path = f"save/{nickname}.json"
                try:
                    with open(save_path, "w", encoding="utf-8") as f:
                        json.dump(profile_data, f, ensure_ascii=False, indent=4)
                    print(f"[✓] Профіль '{nickname}' збережено.")
                except Exception as e:
                    print(f"[!] Помилка при збереженні профілю: {e}")
                    continue

# Перехід до основної гри
                try:
                    import game_window
                    game_window.run(screen, save_path)
                except Exception as e:
                    print(f"[!] Не вдалося запустити ігролад: {e}")    
                running = False
