"""
Модуль для анализа обещаний и извлечения сроков выполнения
Можно использовать как библиотеку для интеграции в другие системы
"""

import json
import re
import openai
from typing import Optional, Dict, List
from datetime import datetime, timedelta

# API ключ OpenAI (используем тот же, что и в city_support_assistant.py)
OPENAI_API_KEY = ""

# Модель для использования
# GPT-4o-mini - самая быстрая и экономичная модель OpenAI
# Другие варианты: "gpt-4o", "gpt-4-turbo" (медленнее, но точнее)
OPENAI_MODEL = "gpt-4o-mini"

# ОПТИМИЗАЦИИ ДЛЯ СКОРОСТИ (уже применены):
# 1. temperature=0.1 - быстрее и детерминированнее
# 2. max_tokens=200 - ограничение длины ответа (JSON короткий)
# 3. GPT-4o-mini - самая быстрая модель OpenAI

# Создаем клиент OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def is_promise(description: str) -> Dict:
    """
    Определяет, является ли описание обещанием решить проблему
    
    Args:
        description: Текст описания
        
    Returns:
        Словарь с результатом анализа:
        {
            "is_promise": 0 или 1,
            "confidence": "высокая/средняя/низкая",
            "reason": "краткое объяснение",
            "success": True/False,
            "error": "сообщение об ошибке" (если success=False)
        }
    """
    if not description or not description.strip():
        return {
            "is_promise": 0,
            "confidence": "низкая",
            "reason": "пустое описание",
            "success": True,
            "error": None
        }
    
    prompt = f"""Проанализируй следующее описание и определи, является ли оно обещанием решить проблему или выполнить работу.

Обещание - это текст, который содержит ЛЮБОЕ из следующего:
- Конкретное обязательство выполнить работу (например, "будет выполнено", "обещаем решить", "гарантируем", "исправим", "отремонтировано")
- Указание на срок или дату выполнения (например, "до 15.12", "в течение 3 дней", "к концу недели")
- Ответственность за выполнение (например, "мы исправим", "будет отремонтировано", "примем меры", "решим вопрос")
- План действий от лица организации (например, "направим специалиста", "проведем работы", "устраним")
- Упоминание о том, что работа будет сделана (например, "выполним", "осуществим", "произведем")
- Формальные ответы с планами рассмотрения и возможной реализацией (например, "будет рассмотрено", "реализация возможна", "при составлении плана", "при выделении финансирования")

ВАЖНО: Будь более мягким в определении. Если в тексте есть хоть какое-то указание на то, что проблема будет решена или работа будет выполнена - это может быть обещанием.

Пример ОБЕЩАНИЯ:
"Добрый день. Ваше предложение будет рассмотрено при составлении плана работ на 2026 и последующие года, реализация возможна при отсутствии коммуникаций (учитывая их охранные зоны) и выделении целевого финансирования."
Это ОБЕЩАНИЕ, потому что содержит указание на рассмотрение и возможную реализацию, что является формой обязательства.

НЕ является обещанием ТОЛЬКО если:
- Это чисто описание проблемы без упоминания о решении
- Это только вопросы без ответов
- Это только жалобы без упоминания о действиях

Верни ТОЛЬКО JSON в формате:
{{
    "is_promise": 0 или 1,
    "confidence": "высокая" или "средняя" или "низкая",
    "reason": "краткое объяснение"
}}

Описание:
{description}

JSON:"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Ты эксперт по анализу текстов. Твоя задача - определить, является ли текст обещанием. Отвечай ТОЛЬКО валидным JSON без дополнительного текста."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.1,  # Снижено для более быстрых и детерминированных ответов
            max_tokens=200  # Ограничение токенов для ускорения (JSON ответ короткий)
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
            is_promise_val = result.get("is_promise", 0)
            confidence = result.get("confidence", "низкая")
            reason = result.get("reason", "")
            
            # Нормализуем значения
            if is_promise_val not in [0, 1]:
                is_promise_val = 1 if is_promise_val > 0 else 0
            
            return {
                "is_promise": is_promise_val,
                "confidence": confidence,
                "reason": reason,
                "success": True,
                "error": None
            }
        except json.JSONDecodeError:
            # Если не удалось распарсить JSON, пытаемся извлечь информацию
            is_promise_val = 0
            confidence = "низкая"
            
            answer_lower = answer.lower()
            if '"is_promise": 1' in answer_lower or '"is_promise":1' in answer_lower or 'is_promise": 1' in answer_lower:
                is_promise_val = 1
            elif '"is_promise": 0' in answer_lower or '"is_promise":0' in answer_lower or 'is_promise": 0' in answer_lower:
                is_promise_val = 0
            elif "да" in answer_lower or "yes" in answer_lower or "является" in answer_lower:
                is_promise_val = 1
                confidence = "средняя"
            elif "нет" in answer_lower or "no" in answer_lower or "не является" in answer_lower:
                is_promise_val = 0
                confidence = "средняя"
            
            return {
                "is_promise": is_promise_val,
                "confidence": confidence,
                "reason": "автоматическое определение",
                "success": True,
                "error": None
            }
        
    except Exception as e:
        return {
            "is_promise": 0,
            "confidence": "низкая",
            "reason": "ошибка при анализе",
            "success": False,
            "error": str(e)
        }


def calculate_exact_date(deadline_text: str, deadline_type: str, creation_date: Optional[str] = None) -> Optional[str]:
    """
    Вычисляет точную дату на основе текста срока и даты создания заявки
    
    Args:
        deadline_text: Текст срока из описания
        deadline_type: Тип срока
        creation_date: Дата создания заявки в формате YYYY-MM-DD или datetime string
        
    Returns:
        Дата в формате YYYY-MM-DD или None
    """
    if not creation_date:
        return None
    
    try:
        # Парсим дату создания
        if isinstance(creation_date, str):
            # Пробуем разные форматы
            for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y", "%d/%m/%Y"]:
                try:
                    base_date = datetime.strptime(creation_date.split()[0], fmt)
                    break
                except ValueError:
                    continue
            else:
                return None
        else:
            base_date = creation_date
        
        text_lower = deadline_text.lower()
        
        # Извлекаем количество дней (различные варианты формулировок)
        days_patterns = [
            r'(\d+)\s*(?:день|дня|дней|рабочий день|рабочих дня|рабочих дней)',
            r'в течение\s*(\d+)\s*(?:день|дня|дней|рабочий день|рабочих дня|рабочих дней)',
            r'за\s*(\d+)\s*(?:день|дня|дней|рабочий день|рабочих дня|рабочих дней)',
            r'через\s*(\d+)\s*(?:день|дня|дней)',
        ]
        
        for pattern in days_patterns:
            days_match = re.search(pattern, text_lower)
            if days_match:
                days = int(days_match.group(1))
                # Для рабочих дней считаем только будние дни
                if 'рабоч' in text_lower:
                    result_date = base_date
                    added_days = 0
                    while added_days < days:
                        result_date += timedelta(days=1)
                        # Пропускаем выходные (суббота=5, воскресенье=6)
                        if result_date.weekday() < 5:
                            added_days += 1
                    return result_date.strftime("%Y-%m-%d")
                else:
                    result_date = base_date + timedelta(days=days)
                    return result_date.strftime("%Y-%m-%d")
        
        # Обработка "через неделю" (7 дней)
        if 'через неделю' in text_lower or 'через 1 неделю' in text_lower:
            result_date = base_date + timedelta(weeks=1)
            return result_date.strftime("%Y-%m-%d")
        
        # Извлекаем количество недель (различные варианты)
        weeks_patterns = [
            r'(\d+)\s*(?:недел|неделя|недели|недель)',
            r'в течение\s*(\d+)\s*(?:недел|неделя|недели|недель)',
            r'через\s*(\d+)\s*(?:недел|неделя|недели|недель)',
        ]
        
        for pattern in weeks_patterns:
            weeks_match = re.search(pattern, text_lower)
            if weeks_match:
                weeks = int(weeks_match.group(1))
                result_date = base_date + timedelta(weeks=weeks)
                return result_date.strftime("%Y-%m-%d")
        
        # Извлекаем количество месяцев (различные варианты)
        months_patterns = [
            r'(\d+)\s*(?:месяц|месяца|месяцев)',
            r'в течение\s*(\d+)\s*(?:месяц|месяца|месяцев)',
            r'через\s*(\d+)\s*(?:месяц|месяца|месяцев)',
        ]
        
        for pattern in months_patterns:
            months_match = re.search(pattern, text_lower)
            if months_match:
                months = int(months_match.group(1))
                # Приблизительно: 1 месяц = 30 дней
                result_date = base_date + timedelta(days=months * 30)
                return result_date.strftime("%Y-%m-%d")
        
        # Обработка "через месяц" (30 дней)
        if 'через месяц' in text_lower or 'через 1 месяц' in text_lower:
            result_date = base_date + timedelta(days=30)
            return result_date.strftime("%Y-%m-%d")
        
        # Специальные случаи
        if 'конец недели' in text_lower or 'концу недели' in text_lower:
            # Находим воскресенье текущей недели
            days_until_sunday = (6 - base_date.weekday()) % 7
            if days_until_sunday == 0 and base_date.weekday() != 6:
                days_until_sunday = 7
            result_date = base_date + timedelta(days=days_until_sunday)
            return result_date.strftime("%Y-%m-%d")
        
        if 'конец месяца' in text_lower or 'концу месяца' in text_lower:
            # Последний день месяца
            if base_date.month == 12:
                result_date = datetime(base_date.year + 1, 1, 1) - timedelta(days=1)
            else:
                result_date = datetime(base_date.year, base_date.month + 1, 1) - timedelta(days=1)
            return result_date.strftime("%Y-%m-%d")
        
        if 'ближайшее время' in text_lower or 'скоро' in text_lower:
            # Приблизительно 3 дня
            result_date = base_date + timedelta(days=3)
            return result_date.strftime("%Y-%m-%d")
        
    except Exception as e:
        return None
    
    return None


def extract_deadline(description: str, creation_date: Optional[str] = None) -> Dict:
    """
    Извлекает дату или срок выполнения из описания
    
    Args:
        description: Текст описания
        creation_date: Дата создания заявки в формате YYYY-MM-DD или datetime string (опционально)
        
    Returns:
        Словарь с результатом извлечения:
        {
            "has_deadline": 0 или 1,
            "deadline_text": "текст срока",
            "deadline_date": "дата в формате YYYY-MM-DD или None",
            "deadline_type": "конкретная дата/срок в днях/срок в неделях/относительный срок/нет",
            "success": True/False,
            "error": "сообщение об ошибке" (если success=False)
        }
    """
    if not description or not description.strip():
        return {
            "has_deadline": 0,
            "deadline_text": "",
            "deadline_date": None,
            "deadline_type": "нет",
            "success": True,
            "error": None
        }
    
    creation_date_info = ""
    if creation_date:
        # Вычисляем пример для демонстрации
        example_date = None
        try:
            example_date = calculate_exact_date("3 дня", "срок в днях", creation_date)
        except:
            pass
        example_text = f" (например, для 'в течение 3 дней' от {creation_date} дата будет {example_date or 'вычисли сам'})" if example_date else ""
        creation_date_info = f"\n\nВАЖНО: Дата создания заявки: {creation_date}. Если найден относительный срок (например, 'в течение 3 дней', 'к концу недели', 'за 5 рабочих дней'), ВЫЧИСЛИ точную дату выполнения, прибавив срок к дате создания заявки.{example_text} Всегда возвращай deadline_date в формате YYYY-MM-DD для относительных сроков."
    
    prompt = f"""Проанализируй следующее описание и найди информацию о сроке или дате выполнения работы.

Ищи:
- Конкретные даты (например, "до 15.11.2025", "к 25 ноября", "2025-11-30")
- Сроки в днях (например, "в течение 3 дней", "за 5 рабочих дней", "через неделю")
- Сроки в неделях (например, "в течение 2 недель", "через месяц")
- Относительные сроки (например, "до конца недели", "в ближайшее время", "в течение месяца")

Верни ТОЛЬКО JSON в формате:
{{
    "has_deadline": 0 или 1,
    "deadline_text": "точный текст срока из описания или пустая строка",
    "deadline_date": "дата в формате YYYY-MM-DD или null если не найдена",
    "deadline_type": "конкретная дата" или "срок в днях" или "срок в неделях" или "относительный срок" или "нет"
}}

ВАЖНО: Если найден относительный срок (например, "в течение 3 дней", "к концу недели") и указана дата создания заявки, ВЫЧИСЛИ точную дату выполнения, прибавив срок к дате создания. Всегда возвращай deadline_date в формате YYYY-MM-DD, если это возможно вычислить.

Описание:
{description}{creation_date_info}

JSON:"""

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Ты эксперт по извлечению дат и сроков из текстов. Отвечай ТОЛЬКО валидным JSON без дополнительного текста."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.1,  # Снижено для более быстрых и детерминированных ответов
            max_tokens=200  # Ограничение токенов для ускорения (JSON ответ короткий)
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
            has_deadline = result.get("has_deadline", 0)
            deadline_text = result.get("deadline_text", "")
            deadline_date = result.get("deadline_date")
            deadline_type = result.get("deadline_type", "нет")
            
            # Нормализуем значения
            if has_deadline not in [0, 1]:
                has_deadline = 1 if has_deadline > 0 else 0
            
            # Проверяем валидность даты
            if deadline_date and deadline_date != "null" and deadline_date != "None":
                try:
                    # Пробуем распарсить дату
                    datetime.strptime(deadline_date, "%Y-%m-%d")
                except (ValueError, TypeError):
                    deadline_date = None
            
            if deadline_date == "null" or deadline_date == "None":
                deadline_date = None
            
            # ВСЕГДА вычисляем дату, если есть относительный срок и дата создания
            # Это гарантирует, что мы получим точную дату обещания
            if has_deadline == 1 and deadline_text and creation_date:
                # Если дата уже есть, проверяем её валидность
                if deadline_date:
                    try:
                        datetime.strptime(deadline_date, "%Y-%m-%d")
                        # Дата валидна, но если это относительный срок - пересчитываем для точности
                        if deadline_type in ['срок в днях', 'срок в неделях', 'относительный срок']:
                            calculated_date = calculate_exact_date(deadline_text, deadline_type, creation_date)
                            if calculated_date:
                                deadline_date = calculated_date
                    except (ValueError, TypeError):
                        # Дата невалидна, вычисляем заново
                        calculated_date = calculate_exact_date(deadline_text, deadline_type, creation_date)
                        if calculated_date:
                            deadline_date = calculated_date
                else:
                    # Даты нет, вычисляем на основе срока
                    calculated_date = calculate_exact_date(deadline_text, deadline_type, creation_date)
                    if calculated_date:
                        deadline_date = calculated_date
            
            return {
                "has_deadline": has_deadline,
                "deadline_text": deadline_text,
                "deadline_date": deadline_date,
                "deadline_type": deadline_type,
                "success": True,
                "error": None
            }
        except json.JSONDecodeError:
            # Если не удалось распарсить, пытаемся извлечь вручную
            manual_result = extract_deadline_manual(description, creation_date)
            manual_result["success"] = True
            manual_result["error"] = None
            return manual_result
        
    except Exception as e:
        manual_result = extract_deadline_manual(description, creation_date)
        manual_result["success"] = False
        manual_result["error"] = str(e)
        return manual_result


def extract_deadline_manual(description: str, creation_date: Optional[str] = None) -> Dict:
    """Ручное извлечение срока из описания (fallback)"""
    text = description.lower()
    
    # Паттерны для поиска дат
    date_patterns = [
        r'\d{1,2}[\.\-/]\d{1,2}[\.\-/]\d{2,4}',  # ДД.ММ.ГГГГ
        r'\d{4}[\.\-/]\d{1,2}[\.\-/]\d{1,2}',     # ГГГГ.ММ.ДД
    ]
    
    # Паттерны для сроков
    days_patterns = [
        r'(\d+)\s*(?:день|дня|дней|рабочий день|рабочих дня|рабочих дней)',
        r'в течение\s*(\d+)\s*(?:день|дня|дней)',
        r'за\s*(\d+)\s*(?:день|дня|дней)',
    ]
    
    weeks_patterns = [
        r'(\d+)\s*(?:недел|неделя|недели|недель)',
        r'в течение\s*(\d+)\s*(?:недел|неделя|недели|недель)',
    ]
    
    # Ищем даты
    for pattern in date_patterns:
        match = re.search(pattern, description)
        if match:
            date_text = match.group(0)
            # Пробуем распарсить дату
            deadline_date = None
            try:
                # Пробуем разные форматы
                for fmt in ["%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d", "%d.%m.%y", "%d/%m/%y", "%Y.%m.%d"]:
                    try:
                        parsed_date = datetime.strptime(date_text, fmt)
                        deadline_date = parsed_date.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
            except:
                pass
            
            return {
                "has_deadline": 1,
                "deadline_text": date_text,
                "deadline_date": deadline_date,
                "deadline_type": "конкретная дата"
            }
    
    # Ищем сроки в днях
    for pattern in days_patterns:
        match = re.search(pattern, text)
        if match:
            deadline_text = match.group(0)
            deadline_date = calculate_exact_date(deadline_text, "срок в днях", creation_date)
            return {
                "has_deadline": 1,
                "deadline_text": deadline_text,
                "deadline_date": deadline_date,
                "deadline_type": "срок в днях"
            }
    
    # Ищем сроки в неделях
    for pattern in weeks_patterns:
        match = re.search(pattern, text)
        if match:
            deadline_text = match.group(0)
            deadline_date = calculate_exact_date(deadline_text, "срок в неделях", creation_date)
            return {
                "has_deadline": 1,
                "deadline_text": deadline_text,
                "deadline_date": deadline_date,
                "deadline_type": "срок в неделях"
            }
    
    # Ищем относительные сроки
    relative_patterns = [
        (r'конец недели|концу недели', 'конец недели'),
        (r'конец месяца|концу месяца', 'конец месяца'),
        (r'ближайшее время|скоро', 'ближайшее время'),
    ]
    
    for pattern, rel_type in relative_patterns:
        if re.search(pattern, text):
            deadline_text = re.search(pattern, text).group(0)
            deadline_date = calculate_exact_date(deadline_text, "относительный срок", creation_date)
            return {
                "has_deadline": 1,
                "deadline_text": deadline_text,
                "deadline_date": deadline_date,
                "deadline_type": "относительный срок"
            }
    
    return {
        "has_deadline": 0,
        "deadline_text": "",
        "deadline_date": None,
        "deadline_type": "нет"
    }


def analyze_promise(description: str, creation_date: Optional[str] = None) -> Dict:
    """
    Полный анализ описания: определяет обещание и извлекает срок
    
    Args:
        description: Текст описания
        creation_date: Дата создания заявки в формате YYYY-MM-DD или datetime string (опционально)
        
    Returns:
        Словарь с полным результатом анализа:
        {
            "is_promise": 0 или 1,
            "confidence": "высокая/средняя/низкая",
            "reason": "краткое объяснение",
            "has_deadline": 0 или 1,
            "deadline_text": "текст срока",
            "deadline_date": "дата в формате YYYY-MM-DD или None",
            "deadline_type": "тип срока",
            "success": True/False,
            "error": "сообщение об ошибке" (если success=False)
        }
    """
    if not description or not description.strip():
        return {
            "is_promise": 0,
            "confidence": "низкая",
            "reason": "пустое описание",
            "has_deadline": 0,
            "deadline_text": "",
            "deadline_date": None,
            "deadline_type": "нет",
            "success": True,
            "error": None
        }
    
    # Анализ обещания
    promise_result = is_promise(description)
    
    # Извлечение срока
    deadline_result = extract_deadline(description, creation_date)
    
    # Если есть срок, но не определили как обещание - повышаем вероятность
    if deadline_result.get('has_deadline', 0) == 1 and promise_result.get('is_promise', 0) == 0:
        # Если есть конкретный срок - это вероятно обещание
        if deadline_result.get('deadline_type') in ['конкретная дата', 'срок в днях', 'срок в неделях']:
            promise_result['is_promise'] = 1
            if promise_result.get('confidence') == 'низкая':
                promise_result['confidence'] = 'средняя'
            promise_result['reason'] = f"найден срок выполнения: {deadline_result.get('deadline_text', '')}"
    
    # Объединяем результаты
    result = {
        **promise_result,
        **deadline_result
    }
    
    # ФИНАЛЬНАЯ ПРОВЕРКА: если есть срок и дата создания, но нет точной даты - вычисляем
    if result.get('has_deadline', 0) == 1 and result.get('deadline_text') and creation_date:
        if not result.get('deadline_date'):
            # Пытаемся вычислить дату на основе срока
            calculated_date = calculate_exact_date(
                result.get('deadline_text', ''),
                result.get('deadline_type', ''),
                creation_date
            )
            if calculated_date:
                result['deadline_date'] = calculated_date
        else:
            # Даже если дата есть, для относительных сроков пересчитываем для точности
            deadline_type = result.get('deadline_type', '')
            if deadline_type in ['срок в днях', 'срок в неделях', 'относительный срок']:
                calculated_date = calculate_exact_date(
                    result.get('deadline_text', ''),
                    deadline_type,
                    creation_date
                )
                if calculated_date:
                    result['deadline_date'] = calculated_date
    
    # Общий success - если хотя бы одна операция успешна
    result['success'] = promise_result.get('success', False) or deadline_result.get('success', False)
    
    # Объединяем ошибки если есть
    errors = []
    if promise_result.get('error'):
        errors.append(f"Обещание: {promise_result['error']}")
    if deadline_result.get('error'):
        errors.append(f"Срок: {deadline_result['error']}")
    result['error'] = "; ".join(errors) if errors else None
    
    return result


def analyze_batch(descriptions: List[str], creation_dates: Optional[List[str]] = None) -> List[Dict]:
    """
    Анализирует список описаний
    
    Args:
        descriptions: Список текстов описаний
        creation_dates: Список дат создания заявок (опционально, должен совпадать по длине с descriptions)
        
    Returns:
        Список словарей с результатами анализа для каждого описания
    """
    results = []
    for i, description in enumerate(descriptions):
        creation_date = creation_dates[i] if creation_dates and i < len(creation_dates) else None
        result = analyze_promise(description, creation_date)
        results.append(result)
    return results


# Пример использования
if __name__ == "__main__":
    # Пример 1: Анализ одного описания
    print("=" * 60)
    print("Пример использования promise_analyzer")
    print("=" * 60)
    
    test_description = "В подъезде дома по адресу ул. Ленина, д. 10 уже неделю нет освещения. Очень темно и опасно, особенно вечером. Жители не могут безопасно подниматься по лестнице."
    test_creation_date = "2025-11-20"
    
    print(f"\n📝 Тестовое описание:")
    print(f"{test_description}")
    print(f"\n📅 Дата создания заявки: {test_creation_date}")
    
    print(f"\n🔍 Анализ...")
    result = analyze_promise(test_description, test_creation_date)
    
    print(f"\n📊 Результат:")
    print(f"   - Обещание: {'Да' if result['is_promise'] == 1 else 'Нет'} (уверенность: {result['confidence']})")
    print(f"   - Причина: {result['reason']}")
    if result['has_deadline'] == 1:
        print(f"   - Срок: {result['deadline_text']} ({result['deadline_type']})")
        if result['deadline_date']:
            print(f"   - Дата: {result['deadline_date']}")
    else:
        print(f"   - Срок: не найден")
    print(f"   - Успешно: {result['success']}")
    if result['error']:
        print(f"   - Ошибка: {result['error']}")
    
    # Пример 2: Пакетный анализ
    print(f"\n" + "=" * 60)
    print("Пример пакетного анализа")
    print("=" * 60)
    
    test_descriptions = [
        "В подъезде нет освещения, просим исправить.",  # Просьба, не обещание
        "Проблема будет решена в течение 3 рабочих дней.",  # Обещание со сроком
        "Направим специалиста к 25 ноября для устранения проблемы.",  # Обещание с датой
        "В квартире течет крыша, нужна помощь.",  # Просто описание проблемы
        "Когда будет отремонтирован лифт? Уже месяц не работает."  # Вопрос, не обещание
    ]
    test_creation_dates = ["2025-11-20"] * len(test_descriptions)
    
    print(f"\n📝 Анализ {len(test_descriptions)} описаний...")
    print(f"📅 Дата создания заявок: {test_creation_dates[0]}")
    batch_results = analyze_batch(test_descriptions, test_creation_dates)
    
    for i, (desc, res) in enumerate(zip(test_descriptions, batch_results), 1):
        print(f"\n{i}. Описание: {desc[:50]}...")
        promise_text = 'Да' if res['is_promise'] == 1 else 'Нет'
        deadline_text = 'Да' if res['has_deadline'] == 1 else 'Нет'
        
        output = f"   Обещание: {promise_text}, Срок: {deadline_text}"
        
        # ВСЕГДА выводим дату выполнения
        if res.get('deadline_date'):
            output += f", Дата выполнения: {res['deadline_date']}"
        elif res.get('has_deadline') == 1:
            # Если есть срок, но нет даты - пытаемся вычислить
            if test_creation_dates and i <= len(test_creation_dates):
                calculated_date = calculate_exact_date(
                    res.get('deadline_text', ''),
                    res.get('deadline_type', ''),
                    test_creation_dates[i-1]
                )
                if calculated_date:
                    output += f", Дата выполнения: {calculated_date}"
                elif res.get('deadline_text'):
                    output += f", Дата выполнения: не определена (срок: {res['deadline_text']})"
                else:
                    output += f", Дата выполнения: не определена"
            else:
                output += f", Дата выполнения: не определена (нет даты создания заявки)"
        else:
            output += f", Дата выполнения: нет"
        
        print(output)


# ============================================================================
# ПРИМЕРЫ ИНТЕГРАЦИИ ДЛЯ ВЕБ-САЙТА
# ============================================================================

"""
ПРИМЕР 1: Flask API

from flask import Flask, request, jsonify
from promise_analyzer import analyze_promise

app = Flask(__name__)

@app.route('/api/analyze-promise', methods=['POST'])
def analyze_promise_endpoint():
    data = request.json
    description = data.get('description', '')
    creation_date = data.get('creation_date', None)  # Опционально: дата создания заявки
    
    if not description:
        return jsonify({"error": "Описание не предоставлено"}), 400
    
    result = analyze_promise(description, creation_date)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

---

ПРИМЕР 2: FastAPI

from fastapi import FastAPI
from pydantic import BaseModel
from promise_analyzer import analyze_promise

app = FastAPI()

class DescriptionRequest(BaseModel):
    description: str
    creation_date: Optional[str] = None  # Опционально: дата создания заявки

@app.post("/api/analyze-promise")
async def analyze_promise_endpoint(request: DescriptionRequest):
    result = analyze_promise(request.description, request.creation_date)
    return result

---

ПРИМЕР 3: Django View

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from promise_analyzer import analyze_promise

@csrf_exempt
@require_http_methods(["POST"])
def analyze_promise_view(request):
    try:
        data = json.loads(request.body)
        description = data.get('description', '')
        creation_date = data.get('creation_date', None)  # Опционально: дата создания заявки
        
        if not description:
            return JsonResponse({"error": "Описание не предоставлено"}, status=400)
        
        result = analyze_promise(description, creation_date)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

---

ПРИМЕР 4: Прямое использование в коде

from promise_analyzer import analyze_promise, is_promise, extract_deadline

# Простой анализ
description = "Обещаем решить проблему в течение 3 рабочих дней"
creation_date = "2025-11-20"  # Дата создания заявки
result = analyze_promise(description, creation_date)

if result['success']:
    if result['is_promise'] == 1:
        print(f"Найдено обещание! Уверенность: {result['confidence']}")
        if result['has_deadline'] == 1:
            print(f"Срок: {result['deadline_text']}")
            if result['deadline_date']:
                print(f"Дата: {result['deadline_date']}")
"""

