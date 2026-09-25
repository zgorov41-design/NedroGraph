import pygame
import os
import webbrowser
import uuid
import network
import languages
import subprocess
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(["auto_config.bat"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

import config

pygame.init()

screen = pygame.display.set_mode((800, 600))

if config.sys_lan == "en-US":
    pygame.display.set_caption(languages.lan_en["en"]["con"])
else:
    pygame.display.set_caption(languages.lan_ru["ru"]["con"])

font = pygame.font.SysFont("calibri", 28)
font_c = pygame.font.Font(None, 48)
text = ""

enter = False
panel = False
settings_s = False
settings_l = False
circle_ru = False
circle_en = False
version = "0.4.1"
y_name = str(uuid.uuid4())

if config.sys_lan == "en-US":
    i_name = languages.lan_en["en"]["inter"]
    circle_en = True
else:
    i_name = languages.lan_ru["ru"]["inter"]
    circle_ru = True

icon = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(icon)
settings = pygame.image.load("settings.png").convert_alpha()
language = pygame.image.load("language.png").convert_alpha()
language_l = pygame.image.load("language_l.png").convert_alpha()
language_l = pygame.transform.scale(language_l, (32, 32))

network.connect_to_server(config.SERVER_IP, y_name)
pygame.display.set_caption("NedroGraph — Messenger")

if config.sys_lan == "en-US":
    text_surface = font.render(languages.lan_en["en"]["ver"] + version, True, (240, 240, 240))
else:
    text_surface = font.render(languages.lan_ru["ru"]["ver"] + version, True, (240, 240, 240))

text_rect = text_surface.get_rect(topleft=(522, 570))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos

                if 5 <= x <= 705 and 520 <= y <= 590 and panel == False:
                    enter = True

                elif 734 <= x <= 789 and 17 <= y <= 43:
                    panel = not panel
                    settings_s = False
                    settings_l = False

                elif 523 <= x <= 560 and 530 <= y <= 590 and panel:
                    settings_s = True
                    settings_l = False

                elif 220 <= x <= 300 and 543 <= y <= 575 and settings_s:
                    settings_l = True
                    settings_s = False

                elif 570 <= x <= 600 and 15 <= y <= 45:
                    settings_s = False
                    settings_l = False

                elif 203 <= x <= 233 and 62 <= y <= 88 and settings_l:
                    circle_ru = True
                    circle_en = False

                    config.sys_lan = "ru-RU"
                    i_name = languages.lan_ru["ru"]["inter"]
                elif 203 <= x <= 233 and 98 <= y <= 123 and settings_l:
                    circle_en = True
                    circle_ru = False

                    config.sys_lan = "en-US"
                    i_name = languages.lan_en["en"]["inter"]
                elif text_rect.collidepoint(event.pos):
                    webbrowser.open("https://t.me/mono_projects")

        if panel == False:
            if enter:
                if event.type == pygame.TEXTINPUT:
                    text += event.text

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]

                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if text.strip() != "":

                            network.send_message(y_name, text)
                            print("Message:", text)
                            text = ""
                            enter = False

    messages = network.get_messages()
    max_visible_messages = 12
    start_index = max(0, len(messages) - max_visible_messages)
    visible_messages = messages[start_index:]

    if config.sys_lan == "en-US":
        title_surface = font.render(languages.lan_en["en"]["title"] + i_name, True, (240, 240, 240))
    else:
        title_surface = font.render(languages.lan_ru["ru"]["title"] + i_name, True, (240, 240, 240))

    input_surface = font.render(text, True, (5, 5, 5))
    placeholder_surface = None

    if not enter and text == "":
        if config.sys_lan == "en-US":
            placeholder_surface = font.render(languages.lan_en["en"]["placeh"], True, (0, 0, 0))
        else:
            placeholder_surface = font.render(languages.lan_ru["ru"]["placeh"], True, (0, 0, 0))

    message_surfaces = []
    message_y = 80

    for message in visible_messages:
        if message["username"] == y_name:
            if config.sys_lan == "en-US":
                username = languages.lan_en["en"]["you"]
            else:
                username = languages.lan_ru["ru"]["you"]
        else:
            if config.sys_lan == "en-US":
                username = languages.lan_en["en"]["inter"]
            else:
                username = languages.lan_ru["ru"]["inter"]

        message_surface = font.render(username + ": " + message["text"], True, (0, 0, 0))
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
    if panel == False:
        if text != "":
            screen.blit(input_surface, (20, 545))

    if panel:
        pygame.draw.rect(screen, (40, 45, 55), (520, 0, 800, 600))
    pygame.draw.rect(screen, (255, 255, 255), (735, 18, 53, 3))
    pygame.draw.rect(screen, (255, 255, 255), (735, 30, 53, 3))
    pygame.draw.rect(screen, (255, 255, 255), (735, 42, 53, 3))

    if panel:
        if config.sys_lan == "en-US":
            text_surface = font.render(languages.lan_en["en"]["ver"] + version, True, (240, 240, 240))
        else:
            text_surface = font.render(languages.lan_ru["ru"]["ver"] + version, True, (240, 240, 240))
        text_rect = text_surface.get_rect(topleft=(522, 570))
        screen.blit(text_surface, text_rect)
        screen.blit(settings, (523, 530))

        if config.sys_lan == "en-US":
            settings_surface = font.render(languages.lan_en["en"]["sett"], True, (240, 240, 240))
        else:
            settings_surface = font.render(languages.lan_ru["ru"]["sett"], True, (240, 240, 240))
        screen.blit(settings_surface, (555, 533))
        pygame.draw.rect(screen, (255, 255, 255), (523, 594, 139, 1))

    if settings_s and settings_l == False:
        pygame.draw.rect(screen, (20, 20, 25), (200, 15, 400, 575))

        if config.sys_lan == "en-US":
            language_surface = font.render(languages.lan_en["en"]["sett"], True, (240, 240, 240))
        else:
            language_surface = font.render(languages.lan_ru["ru"]["sett"], True, (240, 240, 240))
        screen.blit(language_surface, (342, 25))
        screen.blit(language_l, (220, 543))

        if config.sys_lan == "en-US":
            language_surface = font.render(languages.lan_en["en"]["lang"], True, (240, 240, 240))
        else:
            language_surface = font.render(languages.lan_ru["ru"]["lang"], True, (240, 240, 240))
        screen.blit(language_surface, (257, 548))
        cross_surface = font_c.render("×", True, (255, 5, 5))
        screen.blit(cross_surface, (576, 12))

    if settings_l:
        pygame.draw.rect(screen, (20, 20, 25), (200, 15, 400, 575))
        cross_surface = font_c.render("×", True, (255, 5, 5))
        screen.blit(cross_surface, (576, 12))

        if config.sys_lan == "en-US":
            language_surface = font.render(languages.lan_en["en"]["lang"], True, (240, 240, 240))
        else:
            language_surface = font.render(languages.lan_ru["ru"]["lang"], True, (240, 240, 240))
        screen.blit(language_surface, (342, 25))
        pygame.draw.circle(screen, (15, 115, 135), (220, 75), 11, 2)

        if circle_ru:
            pygame.draw.circle(screen, (15, 115, 135), (220, 75), 6)
        ruslang_surface = font.render("Русский", True, (240, 240, 240))
        screen.blit(ruslang_surface, (237, 63))
        pygame.draw.circle(screen, (15, 115, 135), (220, 110), 11, 2)

        if circle_en:
            pygame.draw.circle(screen, (15, 115, 135), (220, 110), 6)
        ruslang_surface = font.render("English", True, (240, 240, 240))
        screen.blit(ruslang_surface, (237, 98))

    pygame.display.flip()
network.disconnect()
pygame.quit()