# Бот помощник службы поддержки  

Чат-боты помогают службе поддержки, отвечая на частые вопросы. Используя облачный сервис распознавания естественного языка от Google - DialogFlow.  

Назначение программ:  
- tg_bot.py: чат-бот для Telegram.  
- vk_bot.py: чат-бот для VK.  
- create_intent.py: программа для загрузки данных (вопросы, ответы) на DialogFlow.  
  
### Как установить

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```bash
pip install -r requirements.txt
```

### Первоначальная настройка

Скопируйте файл `.env.Example` и переименуйте его в `.env`.  

Заполните переменные окружения в файле `.env`:  
`TELEGRAM_TOKEN` - токен телеграм бота.  
`TELEGRAM_CHAT_ID` - id телеграм чата (для вывода сообщений об ошибках чат-бота Telegram).  
`GOOGLE_APPLICATION_CREDENTIALS` - путь к JSON ключу Google.  
`GOOGLE_PROJECT_ID` - ID проекта Google.  
`VK_GROUP_TOKEN` - токен группы VK.  

### Как запускать

Для запуска чат-бота Telegram:  
```bash
python tg_bot.py
```

Для запуска чат-бота VK:  
```bash
python vk_bot.py
```

Для загрузки данных в DialogFlow:  
```bash
python create_intent.py
```
