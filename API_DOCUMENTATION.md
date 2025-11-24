# API Документация

## Базовый URL
```
http://127.0.0.1:3000
```

## Эндпоинты

### 1. Проверка сервера
**GET** `/`

Проверяет, что сервер работает.

**Ответ:**
```json
{
  "status": "200",
  "server": "actived"
}
```

---

### 2. Получение новых тикетов
**GET** `/getticket`

Возвращает список новых тикетов.

**Ответ:**
```json
{
  "status": "200",
  "result": [
    {
      "id": 1,
      "address": "...",
      "status": "new",
      "created_at": "...",
      "description": "...",
      "distric": 1,
      "resolution": "...",
      "execution_date": "...",
      "executor_id": 1,
      "final_status_at": "...",
      "complaint_id": "..."
    }
  ]
}
```

---

### 3. Получение закрытых тикетов
**GET** `/getclosedticket`

Возвращает список закрытых тикетов.

**Ответ:** Аналогично `/getticket`

---

### 4. Анализ запроса (определение обещаний)
**POST** `/queryanalysis`

Анализирует текст на наличие обещаний и извлекает сроки выполнения.

**Параметры (JSON или form-data):**
- `text` (обязательно) - текст для анализа
- `id` (опционально) - ID тикета
- `creation_date` (опционально) - дата создания заявки в формате YYYY-MM-DD

**Пример запроса:**
```json
{
  "text": "Проблема будет решена в течение 3 рабочих дней.",
  "id": "1",
  "creation_date": "2025-11-20"
}
```

**Ответ:**
```json
{
  "status": "200",
  "result": "add new plan",
  "analysis": {
    "is_promise": 1,
    "confidence": "высокая",
    "has_deadline": 1,
    "deadline_text": "в течение 3 рабочих дней",
    "deadline_date": "2025-11-23",
    "deadline_type": "срок в днях"
  }
}
```

---

### 5. Анализ одного бюрократического ответа
**POST** `/analyze_bureaucratic_response`

Анализирует один ответ на предмет бюрократичности.

**Параметры (JSON или form-data):**
- `text` (обязательно) - текст ответа для анализа

**Пример запроса:**
```json
{
  "text": "В соответствии с действующим законодательством и нормативными правовыми актами, регулирующими вопросы благоустройства территории, указанное обращение будет рассмотрено в установленном порядке."
}
```

**Ответ:**
```json
{
  "status": "200",
  "result": {
    "is_bureaucratic": 1,
    "confidence": "высокая",
    "reason": "Используются сложные юридические термины и формальные обороты",
    "complexity_score": 85,
    "success": true,
    "error": null
  }
}
```

---

### 6. Подсчет бюрократических ответов (POST)
**POST** `/count_bureaucratic_responses`

Анализирует переданные тексты ответов и подсчитывает количество бюрократических.

**Параметры (JSON или form-data):**
- `texts` (обязательно) - массив текстов ответов, или
- `text` (обязательно) - один текст ответа

**Пример запроса:**
```json
{
  "texts": [
    "В соответствии с действующим законодательством...",
    "Проблема будет решена в течение 3 дней.",
    "По вопросу, изложенному в обращении..."
  ]
}
```

**Ответ:**
```json
{
  "status": "200",
  "result": {
    "total": 3,
    "bureaucratic_count": 2,
    "percentage": 66.67,
    "details": [
      {
        "text": "В соответствии с действующим законодательством...",
        "is_bureaucratic": 1,
        "confidence": "высокая",
        "complexity_score": 85,
        "reason": "..."
      },
      ...
    ]
  }
}
```

---

### 7. Подсчет бюрократических ответов (GET)
**GET** `/count_bureaucratic_responses`

Подсчитывает количество бюрократических ответов из всех тикетов в базе данных.

**Ответ:**
```json
{
  "status": "200",
  "result": {
    "total": 150,
    "bureaucratic_count": 45,
    "percentage": 30.0,
    "details": [
      {
        "ticket_id": 1,
        "complaint_id": "...",
        "resolution_preview": "...",
        "is_bureaucratic": 1,
        "confidence": "высокая",
        "complexity_score": 80,
        "reason": "..."
      },
      ...
    ]
  }
}
```

---

### 8. Ответ исполнителя
**POST** `/answerexecutor`

Обрабатывает ответ исполнителя о выполнении работы.

**Параметры (form-data):**
- `answer` (обязательно) - ответ ("closed" или другой)
- `id` (обязательно) - ID тикета

**Пример запроса:**
```
answer=closed&id=1
```

**Ответ:**
```json
{
  "status": "200",
  "result": "plan closed"
}
```

---

## Коды ошибок

- `200` - Успешный запрос
- `400` - Ошибка в параметрах запроса
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера

## Примеры использования

### Python (requests)
```python
import requests

# Анализ бюрократического ответа
response = requests.post(
    "http://127.0.0.1:3000/analyze_bureaucratic_response",
    json={"text": "В соответствии с..."}
)
print(response.json())

# Подсчет из базы данных
response = requests.get("http://127.0.0.1:3000/count_bureaucratic_responses")
print(response.json())
```

### cURL
```bash
# Анализ одного ответа
curl -X POST http://127.0.0.1:3000/analyze_bureaucratic_response \
  -H "Content-Type: application/json" \
  -d '{"text": "В соответствии с..."}'

# Подсчет из БД
curl http://127.0.0.1:3000/count_bureaucratic_responses
```

## Тестирование

Для тестирования всех эндпоинтов используйте скрипт `test_api.py`:

```bash
python test_api.py
```

Убедитесь, что сервер запущен на порту 3000 перед запуском тестов.

