import pygame
import os
import webbrowser
import uuid
import network
import languages
import colors
import subprocess
import os
from pathlib import Path
import re

#panel = {"r":40 , "g":45 , "b":55} 
#backg = {"r":255 , "g":255 , "b":255} 
#sett = {"r":20 , "g":20 , "b":25} 
#font = {"r":240 ,"g":240 ,"b":240}

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run(["auto_config.bat"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

import config

pygame.init()

screen = pygame.display.set_mode((800, 600))
# Заголовок окна
if config.sys_lan == "en-US":
    pygame.display.set_caption(languages.lan_en["en"]["con"])
else:
    pygame.display.set_caption(languages.lan_ru["ru"]["con"])

# Шрифты
font = pygame.font.SysFont("calibri", 28)
font_c = pygame.font.Font(None, 48)

# RGB текста
text11 = ""
text12 = ""
text13 = ""
text21 = ""
text22 = ""
text23 = ""
text31 = ""
text32 = ""
text33 = ""
text41 = ""
text42 = ""
text43 = ""
# RGB поля
rgb11 = False
rgb12 = False
rgb13 = False
rgb21 = False
rgb22 = False
rgb23 = False
rgb31 = False
rgb32 = False
rgb33 = False
rgb41 = False
rgb42 = False
rgb43 = False
# Переменные
text = ""
enter = False
panel = False
reset = False
settings_s = False
settings_l = False
settings_c = False
circle_ru = False
circle_en = False
version = "0.4.2"
y_name = str(uuid.uuid4())
config_file = Path("config.py")
new_language = ""

def rgb(text, rgb, color):
    if settings_c and rgb:
        if event.type == pygame.TEXTINPUT:
            if len(text) < 3  and event.text.isdigit():
                text += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if text.strip() != "" and 0 <= int(text) <= 255:
                    print("Value:", text)
                    rgb = False
                    colors.panel[color] = int(text)
                    config_file = Path("colors.py")
                    config_text = config_file.read_text(encoding="utf-8")
                    lines = config_text.splitlines()
                    for i, line in enumerate(lines):
                        if line.strip().startswith("panel ="):
                            lines[i] = re.sub(rf'("{color}"\s*:\s*)\d+',rf'\g<1>{text}',line)
                            break
                    config_file.write_text("\n".join(lines) + "\n",encoding="utf-8")
    return text, rgb



if config.sys_lan == "en-US":
    i_name = languages.lan_en["en"]["inter"]
    circle_en = True
else:
    i_name = languages.lan_ru["ru"]["inter"]
    circle_ru = True
# Импорт иконки
icon = pygame.image.load("icon(1).png").convert_alpha()
pygame.display.set_icon(icon)
# Импорт спрайтова
settings = pygame.image.load("settings.png").convert_alpha()
language = pygame.image.load("language.png").convert_alpha()
language_l = pygame.image.load("language_l.png").convert_alpha()
language_l = pygame.transform.scale(language_l, (32, 32))
customize = pygame.image.load("customize.png").convert_alpha()

network.connect_to_server(config.SERVER_IP, y_name)
# Заголовок окна
pygame.display.set_caption("NedroGraph — Messenger")
# .текст. Версия
if config.sys_lan == "en-US":
    text_surface = font.render(languages.lan_en["en"]["ver"] + version, True, (240, 240, 240))
else:
    text_surface = font.render(languages.lan_ru["ru"]["ver"] + version, True, (240, 240, 240))
# x,y гипер-ссылки
text_rect = text_surface.get_rect(topleft=(522, 570))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Блок кнопок
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                # Ввод
                if 5 <= x <= 705 and 520 <= y <= 590 and panel == False:
                    enter = True
                # Открытие панели
                elif 734 <= x <= 789 and 17 <= y <= 43:
                    panel = not panel
                    settings_s = False
                    settings_l = False
                # Открытие общих настроек
                elif 523 <= x <= 650 + settings_surface.get_width() and 530 <= y <= 590 + settings_surface() and panel:
                    settings_s = True
                    settings_l = False
                # Открытие настроек языка
                elif 220 <= x <= 320 and 543 <= y <= 575 and settings_s:
                    settings_l = True
                    settings_s = False
                # Закрытие через крестик
                elif 570 <= x <= 600 and 15 <= y <= 45:
                    settings_s = False
                    settings_l = False
                    settings_c = False
                # поля RGB
                if settings_c:
                    if 211 <= x <= 262 and 73 <= y <= 103: 
                        rgb11 = True
                        text11 = ""
                    elif 275 <= x <= 326 and 73 <= y <= 103:
                        rgb12 = True
                        text12 = ""
                    elif 339 <= x <= 390 and 73 <= y <= 103:
                        rgb13 = True
                        text13 = ""
                    elif 211 <= x <= 262 and 133 <= y <= 163:
                        rgb21 = True
                        text21 = ""
                    elif 275 <= x <= 326 and 133 <= y <= 163:
                        rgb22 = True
                        text22 = ""
                    elif 339 <= x <= 390 and 133 <= y <= 163:
                        rgb23 = True 
                        text23 = "" 
                    elif 211 <= x <= 262 and 193 <= y <= 223:
                        rgb31 = True
                        text31 = ""
                    elif 275 <= x <= 326 and 193 <= y <= 223:
                        rgb32 = True
                        text32 = "" 
                    elif 339 <= x <= 390 and 193 <= y <= 223:
                        rgb33 = True
                        text33 = ""
                    elif 211 <= x <= 262 and 253 <= y <= 283:
                        rgb41 = True
                        text41 = "" 
                    elif 275 <= x <= 326 and 253 <= y <= 283:
                        rgb42 = True
                        text42 = "" 
                    elif 339 <= x <= 390 and 253 <= y <= 283:
                        rgb43 = True
                        text43 = "" 

                # Выбор языка русский
                elif 203 <= x <= 233 and 62 <= y <= 88 and settings_l:
                    circle_ru = True
                    circle_en = False
                    config.sys_lan = "ru-RU"
                    i_name = languages.lan_ru["ru"]["inter"]
                    # перезапись языка
                    new_language = "ru-RU"
                    text = config_file.read_text(encoding="utf-8")
                    lines = text.splitlines()
                    for i, line in enumerate(lines):
                        if line.startswith("sys_lan"):
                            lines[i] = f'sys_lan = "{new_language}"'
                            config_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
                # Выбор языка английский
                elif 203 <= x <= 233 and 98 <= y <= 123 and settings_l:
                    circle_en = True
                    circle_ru = False
                    config.sys_lan = "en-US"
                    i_name = languages.lan_en["en"]["inter"]
                    new_language = "en-US"
                    text = config_file.read_text(encoding="utf-8")
                    lines = text.splitlines()
                    for i, line in enumerate(lines):
                        if line.startswith("sys_lan"):
                            lines[i] = f'sys_lan = "{new_language}"'
                            config_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
                # Открытие настроек кастомизации
                elif 220 <= x <= 350 and 505 <= y <= 540 and settings_s:
                    settings_c = True
                # Гипер-сслыка на тгк 
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

        text11, rgb11 = rgb(text11, rgb11, "r")
        text12, rgb12 = rgb(text12, rgb12, "g")
        text13, rgb13 = rgb(text13, rgb13, "b")
        text21, rgb21 = rgb(text21, rgb21, "r")
        text22, rgb22 = rgb(text22, rgb22, "g")
        text23, rgb23 = rgb(text23, rgb23, "b")
        text31, rgb31 = rgb(text31, rgb31, "r")
        text32, rgb32 = rgb(text32, rgb32, "g")
        text33, rgb33 = rgb(text33, rgb33, "b")
        text41, rgb41 = rgb(text41, rgb41, "r")
        text42, rgb42 = rgb(text42, rgb42, "g")
        text43, rgb43 = rgb(text43, rgb43, "b")
    
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
    # Задний фон
    pygame.draw.rect(screen, (colors.backg["r"], colors.backg["g"], colors.backg["b"], ), (0, 0, 800, 600))

    for message_surface, message_y in message_surfaces:
        screen.blit(message_surface, (20, message_y))
    # Верхняя панель
    pygame.draw.rect(screen, (colors.panel["r"], colors.panel["g"], colors.panel["b"]), (0, 0, 720, 65))
    # чат с
    screen.blit(title_surface, (10, 15))
    # Боковая панель
    pygame.draw.rect(screen, (colors.panel["r"], colors.panel["g"], colors.panel["b"]), (720, 0, 800, 600))
    # Поле ввода
    pygame.draw.rect(screen, (5, 5, 5), (5, 530, 705, 70))
    pygame.draw.rect(screen, (240, 240, 240), (7, 532, 701, 66))
    # Вводимый текст
    if placeholder_surface:
        screen.blit(placeholder_surface, (20, 552))
    if panel == False:
        if text != "":
            screen.blit(input_surface, (20, 545))

    if panel:
        # Открытая панель
        pygame.draw.rect(screen, (colors.panel["r"], colors.panel["g"], colors.panel["b"]), (520, 0, 800, 600))
    # Полоски панели
    pygame.draw.rect(screen, (255, 255, 255), (735, 18, 53, 3))
    pygame.draw.rect(screen, (255, 255, 255), (735, 30, 53, 3))
    pygame.draw.rect(screen, (255, 255, 255), (735, 42, 53, 3))
    # Открытая панель
    if panel:
        # .текст. Версия
        if config.sys_lan == "en-US":
            text_surface = font.render(languages.lan_en["en"]["ver"] + version, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            text_surface = font.render(languages.lan_ru["ru"]["ver"] + version, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        text_rect = text_surface.get_rect(topleft=(522, 570))

        screen.blit(text_surface, text_rect)
        screen.blit(settings, (523, 530))
        # .текст. Настройки
        if config.sys_lan == "en-US":
            settings_surface = font.render(languages.lan_en["en"]["sett"], True, (colors.font["r"], colors.font["g"], colors.font["b"]))
        else:
            settings_surface = font.render(languages.lan_ru["ru"]["sett"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        screen.blit(settings_surface, (555, 533))
        pygame.draw.rect(screen, (255, 255, 255), (523, 594, 139, 1))
    # Общие настройки
    if settings_s and settings_l == False:
        pygame.draw.rect(screen, (20, 20, 25), (200, 15, 400, 575))
        # .текст. Настройки
        if config.sys_lan == "en-US":
            language_surface = font.render(languages.lan_en["en"]["sett"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            language_surface = font.render(languages.lan_ru["ru"]["sett"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))

        screen.blit(language_surface, (342, 25))
        screen.blit(language_l, (220, 543))
        # .текст. Язык
        if config.sys_lan == "en-US":
            language_surface = font.render(languages.lan_en["en"]["lang"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            language_surface = font.render(languages.lan_ru["ru"]["lang"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))

        screen.blit(language_surface, (257, 548))
        cross_surface = font.render("×", True, (255, 5, 5))
        screen.blit(cross_surface, (576, 12))

        # .текст. Кастомизация
        screen.blit(customize, (220, 500))
        if config.sys_lan == "en-US":
            customize_surface = font.render(languages.lan_en["en"]["custom"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            customize_surface = font.render(languages.lan_ru["ru"]["custom"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        screen.blit(customize_surface, (257, 505))
    # Настройки языка
    if settings_l:
        # Меню выбора языка
        pygame.draw.rect(screen, (20, 20, 25), (200, 15, 400, 575))
        cross_surface = font.render("×", True, (255, 5, 5))
        screen.blit(cross_surface, (576, 12))
        # .текст. Язык
        if config.sys_lan == "en-US":
            language_surface = font.render(languages.lan_en["en"]["lang"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            language_surface = font.render(languages.lan_ru["ru"]["lang"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        screen.blit(language_surface, (342, 25))

        # Выбор русского языка
        pygame.draw.circle(screen, (15, 115, 135), (220, 75), 11, 2)
        if circle_ru:
            pygame.draw.circle(screen, (15, 115, 135), (220, 75), 6)
        ruslang_surface = font.render("Русский", True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        screen.blit(ruslang_surface, (237, 63))

        # Выбор английского языка
        pygame.draw.circle(screen, (15, 115, 135), (220, 110), 11, 2)
        if circle_en:
            pygame.draw.circle(screen, (15, 115, 135), (220, 110), 6)
        ruslang_surface = font.render("English", True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        screen.blit(ruslang_surface, (237, 98))
    # Настройки кастомизации
    if settings_c:
        rgb_backg = font.render((str(colors.backg["r"]) + "      " + str(colors.backg["g"]) + "      " + str(colors.backg["b"])), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        screen.blit(rgb_backg, (215, 135))

        pygame.draw.rect(screen, (20, 20, 25), (200, 15, 400, 575))
        # Крестик
        cross_surface = font.render("×", True, (255, 5, 5))
        screen.blit(cross_surface, (576, 12))

        # Панель
        pygame.draw.rect(screen, (255, 255, 255), (211, 73, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (213, 75, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (275, 73, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (277, 75, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (339, 73, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (341, 75, 47, 26))
        surface_rgb11 = font.render(str(colors.panel["r"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb12 = font.render(str(colors.panel["g"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb13 = font.render(str(colors.panel["b"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb21 = font.render(str(colors.panel["r"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb22 = font.render(str(colors.panel["g"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb23 = font.render(str(colors.panel["b"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb31 = font.render(str(colors.panel["r"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb32 = font.render(str(colors.panel["g"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb33 = font.render(str(colors.panel["b"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb41 = font.render(str(colors.panel["r"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb42 = font.render(str(colors.panel["g"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb43 = font.render(str(colors.panel["b"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        
        if rgb11:
            rgb11_surface = font.render(text11, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb11_surface, (215, 75))
        else:
            screen.blit(surface_rgb11, (215, 75))
        if rgb12:
            rgb12_surface = font.render(text12, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb12_surface, (279, 75))
        else:
            screen.blit(surface_rgb12, (279, 75))
        if rgb13:
            rgb13_surface = font.render(text13, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb13_surface, (343, 75))
        else:
            screen.blit(surface_rgb13, (343, 75))
                
        if rgb11:
            rgb11_surface = font.render(text11, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb11_surface, (215, 75))
        if rgb12:
            rgb12_surface = font.render(text12, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb12_surface, (279, 75))
        if rgb13:
            rgb13_surface = font.render(text13, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb13_surface, (343, 75))

        if rgb21:
            rgb21_surface = font.render(text21, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb21_surface, (215, 135))
        if rgb22:
            rgb22_surface = font.render(text22, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb22_surface, (279, 135))
        if rgb23:
            rgb23_surface = font.render(text23, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb23_surface, (343, 135))

        if rgb31:
            rgb31_surface = font.render(text31, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb31_surface, (215, 195))
        if rgb32:
            rgb32_surface = font.render(text32, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb32_surface, (279, 195))
        if rgb33:
            rgb33_surface = font.render(text33, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb33_surface, (343, 195))

        if rgb41:
            rgb41_surface = font.render(text41, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb41_surface, (215, 225))
        if rgb42:
            rgb42_surface = font.render(text42, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb42_surface, (279, 225))
        if rgb43:
            rgb43_surface = font.render(text43, True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
            screen.blit(rgb43_surface, (343, 225))
        # Задний фон
        pygame.draw.rect(screen, (255, 255, 255), (211, 133, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (213, 135, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (275, 133, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (277, 135, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (339, 133, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (341, 135, 47, 26))
        surface_rgb21 = font.render(str(colors.backg["r"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb22 = font.render(str(colors.backg["g"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb23 = font.render(str(colors.backg["b"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        if rgb21:
            rgb21_surface = font.render(text21, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb21_surface, (215, 135))
        else:
            screen.blit(surface_rgb21, (215, 135))
        if rgb22:
            rgb22_surface = font.render(text22, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb22_surface, (279, 135))
        else:
            screen.blit(surface_rgb22, (279, 135))
        if rgb23:
            rgb23_surface = font.render(text23, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb23_surface, (343, 135))
        else:
            screen.blit(surface_rgb23, (343, 135))
        # Цвет окна настроек
        pygame.draw.rect(screen, (255, 255, 255), (211, 193, 51, 30))   
        pygame.draw.rect(screen, (70, 80, 95), (213, 195, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (275, 193, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (277, 195, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (339, 193, 51, 30))   
        pygame.draw.rect(screen, (70, 80, 95), (341, 195, 47, 26))
        surface_rgb31 = font.render(str(colors.sett["r"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb32 = font.render(str(colors.sett["g"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb33 = font.render(str(colors.sett["b"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        if rgb31:
            rgb31_surface = font.render(text31, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb31_surface, (215, 195))
        else:
            screen.blit(surface_rgb31, (215, 195))
        if rgb32:
            rgb22_surface = font.render(text32, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb32_surface, (279, 195))
        else:
            screen.blit(surface_rgb32, (279, 195))
        if rgb33:
            rgb23_surface = font.render(text33, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb33_surface, (343, 195))
        else:
            screen.blit(surface_rgb33, (343, 195))
        # Цвет текста
        pygame.draw.rect(screen, (255, 255, 255), (211, 253, 51, 30))  
        pygame.draw.rect(screen, (70, 80, 95), (213, 255, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (275, 253, 51, 30))   
        pygame.draw.rect(screen, (70, 80, 95), (277, 255, 47, 26))
        pygame.draw.rect(screen, (255, 255, 255), (339, 253, 51, 30)) 
        pygame.draw.rect(screen, (70, 80, 95), (341, 255, 47, 26))
        surface_rgb41 = font.render(str(colors.font["r"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb42 = font.render(str(colors.font["g"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        surface_rgb43 = font.render(str(colors.font["b"]), True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        if rgb41:
            rgb41_surface = font.render(text41, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb41_surface, (215, 255))
        else:
            screen.blit(surface_rgb41, (215, 255))
        if rgb42:
            rgb42_surface = font.render(text42, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb42_surface, (279, 255))
        else:
            screen.blit(surface_rgb42, (279, 255))
        if rgb43:
            rgb43_surface = font.render(text43, True, (colors.font["r"], colors.font["g"], colors.font["b"]))
            screen.blit(rgb43_surface, (343, 255))
        else:
            screen.blit(surface_rgb43, (343, 255))

        #.текст. Цвет панели
        if config.sys_lan == "en-US":
            surface_1 = font.render(languages.lan_en["en"]["panel"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            surface_1 = font.render(languages.lan_ru["ru"]["panel"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))

        pygame.draw.rect(screen, (255, 255, 255), (450, 73, 38, 28))
        pygame.draw.rect(screen, (colors.panel["r"], colors.panel["g"], colors.panel["b"]), (452, 75, 34 , 24))
        screen.blit(surface_1, (215, 45))

        #.текст. Цвет заднего фона
        if config.sys_lan == "en-US":
            surface_2 = font.render(languages.lan_en["en"]["backg"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            surface_2 = font.render(languages.lan_ru["ru"]["backg"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))

        pygame.draw.rect(screen, (255, 255, 255), (450, 133, 38, 28))
        pygame.draw.rect(screen, (colors.backg["r"], colors.backg["g"], colors.backg["b"]), (452, 135, 34 , 24))
        screen.blit(surface_2, (215, 105))
        #.текст. Цвет настроек
        if config.sys_lan == "en-US":
            surface_2 = font.render(languages.lan_en["en"]["sett_c"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            surface_2 = font.render(languages.lan_ru["ru"]["sett_c"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))

        pygame.draw.rect(screen, (255, 255, 255), (450, 193, 38, 28))
        pygame.draw.rect(screen, (colors.sett["r"], colors.sett["g"], colors.sett["b"]), (452, 195, 34 , 24))
        screen.blit(surface_2, (215, 165))
        #.текст. Цвет текста
        if config.sys_lan == "en-US":
            surface_2 = font.render(languages.lan_en["en"]["font"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            surface_2 = font.render(languages.lan_ru["ru"]["font"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))

        pygame.draw.rect(screen, (255, 255, 255), (450, 253, 38, 28))
        pygame.draw.rect(screen, (colors.font["r"], colors.font["g"], colors.font["b"]), (452, 255, 34 , 24))
        screen.blit(surface_2, (215, 225))

        if config.sys_lan == "en-US":
            res_surface = font.render(languages.lan_en["en"]["res"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        else:
            res_surface = font.render(languages.lan_ru["ru"]["res"], True, (colors.font["r"], colors.font["g"] , colors.font["b"]))
        screen.blit(res_surface, (515, 555))
        if settings_c and 515 <= x <= 515 + res_surface.get_width() and 555 <= y <= 555 + res_surface.get_height():
            reset = True
        if reset:
            config_file = Path(__file__).parent / "colors.py"
            config_file.write_text('panel = {"r":40 , "g":45 , "b":55}\nbackg = {"r":255 , "g":255 , "b":255}\nsett = {"r":20 , "g":20 , "b":25}\nfont = {"r":240 ,"g":240 ,"b":240}\n', encoding="utf-8")
            colors.panel = {"r":40, "g":45, "b":55}
            colors.backg = {"r":255, "g":255, "b":255}
            colors.sett = {"r":20, "g":20, "b":25}
            colors.font = {"r":240, "g":240, "b":240}
            reset = False

    pygame.display.flip()
network.disconnect()
pygame.quit()