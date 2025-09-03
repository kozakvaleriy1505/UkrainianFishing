import pygame

def run(screen):
    pygame.font.init()
    font = pygame.font.SysFont("arial", 32)
    small_font = pygame.font.SysFont("arial", 24)

    input_text = "Я у мами риболов"
    active_input = True

    difficulties = ["Легка", "Нормально", "Важка"]
    selected = 1  # за замовчуванням "Нормально"

    running = True
    while running:
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
                    print(f"▶ Створення профілю: {input_text}, складність: {difficulties[selected]}")
                    # TODO: збереження профілю та перехід до гри
                    running = False