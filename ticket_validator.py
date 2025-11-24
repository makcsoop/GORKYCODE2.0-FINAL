"""
Модуль для валидации тикетов (заявок)
Определяет, является ли заявка осмысленной и содержит ли реальную проблему
Использует GPT-4o-mini для анализа качества текста
"""

import json
import openai
from typing import Dict, Optional

# API ключ OpenAI (используем тот же, что и в других модулях)
OPENAI_API_KEY = ""

# Модель для использования
OPENAI_MODEL = "gpt-4o-mini"

# Создаем клиент OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def validate_ticket(ticket_text: str, ticket_title: Optional[str] = None) -> Dict:
    """
    Валидирует тикет: определяет, является ли заявка осмысленной и содержит ли реальную проблему
    
    Args:
        ticket_text: Текст заявки (описание проблемы)
        ticket_title: Заголовок заявки (опционально)
        
    Returns:
        Словарь с результатом валидации:
        {
            "is_valid": 1 или 0,  # 1 = валидный тикет, 0 = бред/отклонить
            "confidence": "высокая/средняя/низкая",
            "reason": "краткое объяснение",
            "problem_detected": 1 или 0,  # есть ли реальная проблема
            "category": "тип проблемы или 'бред/спам/бессмысленно'",
            "recommendation": "принять" или "отклонить",
            "success": True/False,
            "error": "сообщение об ошибке" (если success=False)
        }
    """
    if not ticket_text or not ticket_text.strip():
        return {
            "is_valid": 0,
            "confidence": "высокая",
            "reason": "пустой текст заявки",
            "problem_detected": 0,
            "category": "пусто",
            "recommendation": "отклонить",
            "success": True,
            "error": None
        }
    
    # Формируем полный текст для анализа
    full_text = ticket_text
    if ticket_title:
        full_text = f"{ticket_title}\n\n{ticket_text}"
    
    prompt = f"""Проанализируй следующую заявку (тикет) и определи, является ли она осмысленной и содержит ли реальную проблему, которую можно решить.

ВАЛИДНАЯ заявка должна содержать:
- Конкретное описание проблемы или ситуации
- Упоминание места, объекта или ситуации (адрес, дом, улица, объект и т.д.)
- Понятное изложение проблемы (что не так, что нужно исправить)
- Логичную связь между фактами

НЕ ВАЛИДНАЯ заявка (БРЕД/СПАМ) - это:
- Бессмысленный набор слов без логики
- Текст без конкретной проблемы (например, "все плохо", "ничего не работает" без деталей)
- Полностью нечитаемый текст (набор символов, случайные слова)
- Очевидный спам или реклама
- Текст, который не содержит никакой полезной информации
- Полностью абсурдные утверждения без связи с реальностью
- Повторяющиеся символы или слова без смысла

Примеры БРЕДА (отклонить):
- "ааааааааааааааааа"
- "все плохо везде ничего не работает"
- "qwertyuiop asdfghjkl zxcvbnm"
- "1234567890 0987654321"
- "дом улица проблема решить"
- "хочу чтобы все было хорошо"

Примеры ВАЛИДНЫХ заявок (принять):
- "В подъезде дома по адресу ул. Ленина, д. 10 уже неделю нет освещения. Очень темно и опасно."
- "На тротуаре по улице Пушкина, около дома 25, разбита плитка. Можно споткнуться и упасть."
- "Во дворе дома 5 по пр. Мира не вывозят мусор уже 3 дня, контейнеры переполнены."

Верни ТОЛЬКО JSON в формате:
{{
    "is_valid": 1 или 0,  # 1 = валидный тикет, 0 = бред/отклонить
    "confidence": "высокая" или "средняя" или "низкая",
    "reason": "краткое объяснение почему валидный или нет",
    "problem_detected": 1 или 0,  # есть ли реальная проблема
    "category": "тип проблемы (ЖКХ, дороги, экология и т.д.) или 'бред/спам/бессмысленно'",
    "recommendation": "принять" или "отклонить"
}}

Заявка:
{full_text}

JSON:"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Ты модератор заявок. Твоя задача - определить, является ли заявка осмысленной и содержит ли реальную проблему. Отвечай ТОЛЬКО валидным JSON без дополнительного текста."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.1,
            max_tokens=200
        )
        
        answer = response.choices[0].message.content.strip()
        
        # Убираем markdown разметку если есть
        if answer.startswith("```json"):
            answer = answer[7:]
        if answer.startswith("```"):
            answer = answer[3:]
        if answer.endswith("```"):
            answer = answer[:-3]
        answer = answer.strip()
        
        # Парсим JSON
        try:
            result = json.loads(answer)
            is_valid = result.get("is_valid", 0)
            confidence = result.get("confidence", "низкая")
            reason = result.get("reason", "")
            problem_detected = result.get("problem_detected", 0)
            category = result.get("category", "неизвестно")
            recommendation = result.get("recommendation", "отклонить")
            
            # Нормализуем значения
            if is_valid not in [0, 1]:
                is_valid = 1 if is_valid > 0 else 0
            if problem_detected not in [0, 1]:
                problem_detected = 1 if problem_detected > 0 else 0
            
            # Если recommendation не соответствует is_valid, исправляем
            if is_valid == 0 and recommendation != "отклонить":
                recommendation = "отклонить"
            elif is_valid == 1 and recommendation != "принять":
                recommendation = "принять"
            
            return {
                "is_valid": is_valid,
                "confidence": confidence,
                "reason": reason,
                "problem_detected": problem_detected,
                "category": category,
                "recommendation": recommendation,
                "success": True,
                "error": None
            }
        except json.JSONDecodeError:
            # Если не удалось распарсить JSON, пытаемся извлечь информацию
            is_valid = 1  # По умолчанию принимаем, если не можем определить
            confidence = "низкая"
            reason = "не удалось распарсить ответ ИИ"
            
            answer_lower = answer.lower()
            if '"is_valid": 0' in answer_lower or '"is_valid":0' in answer_lower or 'is_valid": 0' in answer_lower:
                is_valid = 0
            elif "отклонить" in answer_lower or "бред" in answer_lower or "спам" in answer_lower:
                is_valid = 0
            elif "принять" in answer_lower or "валид" in answer_lower:
                is_valid = 1
            
            return {
                "is_valid": is_valid,
                "confidence": confidence,
                "reason": reason,
                "problem_detected": 1 if is_valid == 1 else 0,
                "category": "неизвестно",
                "recommendation": "отклонить" if is_valid == 0 else "принять",
                "success": True,
                "error": None
            }
        
    except Exception as e:
        return {
            "is_valid": 1,  # По умолчанию принимаем при ошибке
            "confidence": "низкая",
            "reason": "ошибка при анализе",
            "problem_detected": 1,
            "category": "неизвестно",
            "recommendation": "принять",
            "success": False,
            "error": str(e)
        }


def validate_batch(tickets: list, titles: Optional[list] = None) -> list:
    """
    Валидирует список тикетов
    
    Args:
        tickets: Список текстов заявок
        titles: Список заголовков (опционально, должен совпадать по длине с tickets)
        
    Returns:
        Список словарей с результатами валидации для каждого тикета
    """
    results = []
    for i, ticket_text in enumerate(tickets):
        ticket_title = titles[i] if titles and i < len(titles) else None
        result = validate_ticket(ticket_text, ticket_title)
        results.append(result)
    return results


# Пример использования
if __name__ == "__main__":
    print("=" * 60)
    print("Валидатор тикетов (проверка на бред/спам)")
    print("=" * 60)
    
    # Примеры БРЕДА (должны быть отклонены)
    print("\n" + "=" * 60)
    print("Примеры БРЕДА (должны быть отклонены):")
    print("=" * 60)
    
    bad_examples = [
        "ааааааааааааааааа",
        "все плохо везде ничего не работает",
        "qwertyuiop asdfghjkl zxcvbnm",
        "1234567890 0987654321",
        "дом улица проблема решить",
        "хочу чтобы все было хорошо",
        "проблема проблема проблема",
    ]
    
    for i, example in enumerate(bad_examples, 1):
        print(f"\n{i}. Заявка: {example}")
        result = validate_ticket(example)
        print(f"   Результат: {'✅ ВАЛИДНЫЙ' if result['is_valid'] == 1 else '❌ ОТКЛОНИТЬ'}")
        print(f"   Уверенность: {result['confidence']}")
        print(f"   Причина: {result['reason']}")
        print(f"   Рекомендация: {result['recommendation']}")
        print(f"   Категория: {result['category']}")
    
    # Примеры ВАЛИДНЫХ заявок (должны быть приняты)
    print("\n" + "=" * 60)
    print("Примеры ВАЛИДНЫХ заявок (должны быть приняты):")
    print("=" * 60)
    
    good_examples = [
        "В подъезде дома по адресу ул. Ленина, д. 10 уже неделю нет освещения. Очень темно и опасно, особенно вечером.",
        "На тротуаре по улице Пушкина, около дома 25, разбита плитка. Можно споткнуться и упасть.",
        "Во дворе дома 5 по пр. Мира не вывозят мусор уже 3 дня, контейнеры переполнены.",
        "В квартире по адресу ул. Советская, д. 15, кв. 42 течет крыша. Вода капает в спальне.",
        "На остановке общественного транспорта на пр. Ленина отсутствует освещение. Вечером очень темно.",
    ]
    
    for i, example in enumerate(good_examples, 1):
        print(f"\n{i}. Заявка: {example[:80]}...")
        result = validate_ticket(example)
        print(f"   Результат: {'✅ ВАЛИДНЫЙ' if result['is_valid'] == 1 else '❌ ОТКЛОНИТЬ'}")
        print(f"   Уверенность: {result['confidence']}")
        print(f"   Причина: {result['reason']}")
        print(f"   Рекомендация: {result['recommendation']}")
        print(f"   Категория: {result['category']}")
        print(f"   Проблема обнаружена: {'Да' if result['problem_detected'] == 1 else 'Нет'}")
    
    # Пакетная обработка
    print("\n" + "=" * 60)
    print("Пакетная обработка:")
    print("=" * 60)
    
    test_tickets = [
        "аааааааааа",
        "В подъезде нет света",
        "qwerty",
        "На улице Ленина разбита дорога",
    ]
    
    batch_results = validate_batch(test_tickets)
    
    for i, (ticket, result) in enumerate(zip(test_tickets, batch_results), 1):
        print(f"\n{i}. {ticket[:50]}...")
        print(f"   {'✅ ПРИНЯТЬ' if result['is_valid'] == 1 else '❌ ОТКЛОНИТЬ'}")


# ============================================================================
# ПРИМЕРЫ ИНТЕГРАЦИИ ДЛЯ ВЕБ-САЙТА
# ============================================================================

"""
ПРИМЕР 1: Flask API

from flask import Flask, request, jsonify
from ticket_validator import validate_ticket

app = Flask(__name__)

@app.route('/api/validate-ticket', methods=['POST'])
def validate_ticket_endpoint():
    data = request.json
    ticket_text = data.get('ticket_text', '')
    ticket_title = data.get('ticket_title', None)
    
    if not ticket_text:
        return jsonify({"error": "Текст заявки не предоставлен"}), 400
    
    result = validate_ticket(ticket_text, ticket_title)
    
    # Если тикет не валидный - отклоняем
    if result['is_valid'] == 0:
        return jsonify({
            "status": "rejected",
            "reason": result['reason'],
            "validation": result
        }), 400
    
    return jsonify({
        "status": "accepted",
        "validation": result
    })

if __name__ == '__main__':
    app.run(debug=True)

---

ПРИМЕР 2: FastAPI

from fastapi import FastAPI
from pydantic import BaseModel
from ticket_validator import validate_ticket

app = FastAPI()

class TicketRequest(BaseModel):
    ticket_text: str
    ticket_title: Optional[str] = None

@app.post("/api/validate-ticket")
async def validate_ticket_endpoint(request: TicketRequest):
    result = validate_ticket(request.ticket_text, request.ticket_title)
    
    if result['is_valid'] == 0:
        return {"status": "rejected", "validation": result}
    
    return {"status": "accepted", "validation": result}

---

ПРИМЕР 3: Использование перед отправкой тикета Максиму

from ticket_validator import validate_ticket

def send_ticket_to_maxim(ticket_text: str, ticket_title: str = None):
    # Сначала валидируем тикет
    validation = validate_ticket(ticket_text, ticket_title)
    
    if validation['is_valid'] == 0:
        print(f"❌ Тикет отклонен: {validation['reason']}")
        return {
            "success": False,
            "error": "Тикет не прошел валидацию",
            "validation": validation
        }
    
    # Если валидный - отправляем на эндпоинт
    # ... код отправки на эндпоинт Максима ...
    
    return {
        "success": True,
        "validation": validation
    }
"""

