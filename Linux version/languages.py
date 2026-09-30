import config
lan_en = {
    "en": {
        "con": "Connect ...","inter": "Interlocutor","ver": "Version","lang": "language","sett": "settings","you": "You","placeh": "Enter a message:","title": "Chat with ",
        "custom": "Customize","panel": "Pannel color","backg": "Background color:","sett_c": "Settings color:","font": "Font color:","res": "Reset",
    }
}
lan_ru = {
    "ru": {
        "con": "Подключение ...","inter": "Собеседник","ver": "Версия","lang": "Язык","sett": "Настройки","you": "Ты","placeh": "Введите сообщение:","title": "Чат с ",
        "custom": "Кастомизация","panel": "Цвет панели:","backg": "Цвет фона:","sett_c": "Цвет настроек:","font": "Цвет текста:","res": "Сброс",
    }
}
if config.sys_lan == "ru-RU":
    config.sys_lan = lan_ru
if config.sys_lan == "en_EN":
    config.sys_lan = lan_en
