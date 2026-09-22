import pygame
import os
import webbrowser
import uuid
import network
import subprocess
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

subprocess.run(["auto_config.sh"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

import config

os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Подключение ...")

font = pygame.font.SysFont("calibri", 28)
text = ""
enter = False
panel = False
y_name = str(uuid.uuid4())
i_name = "Собеседник"
version = "0.4.0"

icon = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(icon)

network.connect_to_server(config.SERVER_IP, y_name)

pygame.display.set_caption("NedroGraph — Messenger")

text_surface = font.render("Версия " + version, True, (240, 240, 240))
text_rect = text_surface.get_rect(topleft=(522, 570))

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos

                if 5 <= x <= 705 and 520 <= y <= 590:
                    enter = True

                if 734 <= x <= 789 and 17 <= y <= 43:
                    panel = not panel

                if text_rect.collidepoint(event.pos):
                    webbrowser.open("https://t.me/mono_projects")

        if enter:
            if event.type == pygame.TEXTINPUT:
                text += event.text

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if text.strip() != "":
                        network.send_message(y_name, text)
                        print("Сообщение:", text)
                        text = ""
                        enter = False

    messages = network.get_messages()

    max_visible_messages = 12
    start_index = max(0, len(messages) - max_visible_messages)
    visible_messages = messages[start_index:]

    title_surface = font.render("Чат с " + i_name, True, (240, 240, 240))
    input_surface = font.render(text, True, (5, 5, 5))

    if not enter and text == "":
        placeholder_surface = font.render("Введите сообщение", True, (0, 0, 0))
    else:
        placeholder_surface = None

    message_surfaces = []
    message_y = 80

    for message in visible_messages:
        if message["username"] == y_name:
            username = "Ты"
        else:
            username = "Собеседник"

        message_surface = font.render(
            username + ": " + message["text"],
            True,
            (0, 0, 0)
        )

        message_surfaces.append((message_surface, message_y))
        message_y += 35

    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 800, 600))

    for message_surface, message_y in message_surfaces:
        screen.blit(message_surface, (20, message_y))

    pygame.draw.rect(screen, (45, 50, 60), (0, 0, 720, 65))
    screen.blit(title_surface, (10, 15))

    pygame.draw.rect(screen, (45, 50, 60), (720, 0, 800, 600))

    pygame.draw.rect(screen, (5, 5, 5), (5, 530, 705, 70))
    pygame.draw.rect(screen, (240, 240, 240), (7, 532, 701, 66))

    if placeholder_surface:
        screen.blit(placeholder_surface, (20, 552))

    if text != "":
        screen.blit(input_surface, (20, 545))

    if panel:
        pygame.draw.rect(screen, (40, 45, 55), (520, 0, 800, 600))

    pygame.draw.rect(screen, (255, 255, 255), (735, 18, 53, 3))
    pygame.draw.rect(screen, (255, 255, 255), (735, 30, 53, 3))
    pygame.draw.rect(screen, (255, 255, 255), (735, 42, 53, 3))

    if panel:
        version_surface = font.render("Версия " + version, True, (240, 240, 240))
        screen.blit(version_surface, text_rect)

        pygame.draw.rect(screen, (255, 255, 255), (523, 594, 139, 1))

    pygame.display.flip()

network.disconnect()
pygame.quit()