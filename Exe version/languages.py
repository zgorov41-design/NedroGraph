import config
lan_en = {
    "en": {
        "con": "Connect ...","inter": "Interlocutor","ver": "Version","lang": "language","sett": "settings","you": "You","placeh": "Enter a message:","title": "Chat with "
    }
}
lan_ru = {
    "ru": {
        "con": "Подключение ...","inter": "Собеседник","ver": "Версия","lang": "Язык","sett": "Настройки","you": "Ты","placeh": "Введите сообщение:","title": "Чат с"
    }
}
if config.sys_lan == "ru-RU":
    config.sys_lan = lan_ru
if config.sys_lan == "en_EN":
    config.sys_lan = lan_en
