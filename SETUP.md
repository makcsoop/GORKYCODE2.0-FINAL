# Инструкция по настройке и запуску Flask сервера

## Установка зависимостей

```bash
pip install -r requirements.txt
```

Или если используете виртуальное окружение:

```bash
source myenv/bin/activate  # для Linux/Mac
# или
myenv\Scripts\activate  # для Windows

pip install -r requirements.txt
```

## Структура проекта

```
GORKYCODE2.0-FINAL/
├── app.py                 # Главный файл Flask приложения
├── templates/             # HTML шаблоны
│   ├── message.html
│   ├── projects.html
│   ├── messages-list.html
│   └── rating.html
├── static/                # Статические файлы
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── img/
│       └── ...
└── db/
    └── base.db           # База данных
```

## Запуск сервера

```bash
python app.py
```

Сервер запустится на `http://127.0.0.1:8000`

## Доступные страницы

- `http://127.0.0.1:8000/` - Главная страница (message.html)
- `http://127.0.0.1:8000/projects` - Страница проектов
- `http://127.0.0.1:8000/messages-list` - Список сообщений
- `http://127.0.0.1:8000/rating` - Страница рейтинга

## API эндпоинты

Все API эндпоинты возвращают JSON и поддерживают CORS для работы с fetch.

### Пример использования fetch в JavaScript:

```javascript
// GET запрос
fetch('http://127.0.0.1:8000/getticket')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// POST запрос
fetch('http://127.0.0.1:8000/queryanalysis', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: "Проблема будет решена в течение 3 дней",
    id: "1",
    creation_date: "2025-11-20"
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

## Основные API эндпоинты

- `GET /getticket` - Получить новые тикеты
- `GET /getclosedticket` - Получить закрытые тикеты
- `POST /queryanalysis` - Анализ запроса на наличие обещаний
- `GET /count_bureaucratic_responses` - Подсчет бюрократических ответов из БД
- `POST /count_bureaucratic_responses` - Анализ переданных текстов
- `POST /analyze_bureaucratic_response` - Анализ одного ответа
- `POST /answerexecutor` - Обработка ответа исполнителя

Подробная документация в файле `API_DOCUMENTATION.md`

## Решение проблем

### Проблема: "Template not found"
Убедитесь, что:
1. Папка `templates` существует
2. HTML файлы находятся в папке `templates`
3. Имя файла в `render_template()` совпадает с именем файла

### Проблема: CSS/JS не загружаются
Убедитесь, что:
1. Папка `static` существует
2. Файлы находятся в правильных подпапках (`static/css/`, `static/js/`, `static/img/`)
3. В HTML используются правильные пути через `url_for()`

### Проблема: CORS ошибки
CORS уже настроен в коде. Если проблемы остаются, проверьте:
1. Установлен ли `flask-cors`: `pip install flask-cors`
2. Импортирован ли CORS в `app.py`
3. Правильно ли указан URL в fetch запросах

### Проблема: База данных не найдена
Убедитесь, что:
1. Папка `db` существует
2. Файл `base.db` существует или будет создан автоматически

