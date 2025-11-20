import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
from openai import OpenAI


# ===================== НАСТРОЙКИ =====================

# ЖЁСТКО ЗАШИТЫЙ КЛЮЧ ДЛЯ ХАКАТОНА (БЕЗ ENV)
# При необходимости поменяй на свой.
OPENAI_API_KEY = "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"

CHAT_MODEL = "gpt-4o-mini"
EMBED_MODEL = "text-embedding-3-small"


# Базовые категории тикетов (можно править под город)
TICKET_CATEGORIES = [
    "ЖКХ",
    "Экология",
    "Транспорт",
    "Дороги",
    "Озеленение и благоустройство",
    "Безопасность",
    "Социальная поддержка",
    "Связь и интернет",
    "Другое",
]


# Примеры исторических тикетов для RAG-классификатора
# Реально вы потом можете вытаскивать это из базы.
EXAMPLE_TICKETS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "category": "ЖКХ",
        "text": "В подъезде по адресу ул. Ленина, дом 10 уже неделю нет освещения, очень темно и опасно.",
    },
    {
        "id": 2,
        "category": "ЖКХ",
        "text": "В квартире по адресу проспект Гагарина, 25 из батарей течет вода, нужна срочная помощь.",
    },
    {
        "id": 3,
        "category": "Экология",
        "text": "Во дворе дома по улице Пушкина 5 постоянно горит мусор, стоит сильный запах гари.",
    },
    {
        "id": 4,
        "category": "Экология",
        "text": "На берегу реки свалка пластиковых бутылок и другого мусора, нужна уборка.",
    },
    {
        "id": 5,
        "category": "Транспорт",
        "text": "Автобус номер 15 регулярно опаздывает на 20–30 минут в час пик.",
    },
    {
        "id": 6,
        "category": "Дороги",
        "text": "На перекрестке улиц Советская и Лесная огромная яма на дороге, машины объезжают по встречке.",
    },
    {
        "id": 7,
        "category": "Озеленение и благоустройство",
        "text": "В сквере возле школы сломаны лавочки и не работает освещение.",
    },
    {
        "id": 8,
        "category": "Безопасность",
        "text": "Во дворе по адресу ул. Молодежная 12 вечерами собираются шумные компании, жители жалуются на драки.",
    },
    {
        "id": 9,
        "category": "Связь и интернет",
        "text": "В районе улицы Университетской пропадает мобильная связь, невозможно позвонить.",
    },
    {
        "id": 10,
        "category": "Социальная поддержка",
        "text": "Пенсионеры жалуются, что в МФЦ большие очереди и они не могут записаться на прием.",
    },
]


# ===================== КЛИЕНТ OPENAI =====================


def get_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY не задан. "
            "Установи переменную окружения OPENAI_API_KEY или пропиши ключ в коде."
        )
    return OpenAI(api_key=OPENAI_API_KEY)


def embed_texts(client: OpenAI, texts: List[str]) -> np.ndarray:
    """Получить эмбеддинги для списка текстов."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vectors = [item.embedding for item in resp.data]
    return np.array(vectors, dtype=np.float32)


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


# ===================== RAG-КЛАССИФИКАТОР ТИКЕТОВ =====================


class RAGTicketClassifier:
    """
    Простой RAG: находит похожие исторические тикеты по эмбеддингам
    и по ним определяет категорию нового обращения.
    """

    def __init__(self, client: OpenAI, examples: List[Dict[str, Any]]):
        self.client = client
        self.examples = examples
        self.embeddings = self._build_index()

    def _build_index(self) -> np.ndarray:
        texts = [e["text"] for e in self.examples]
        return embed_texts(self.client, texts)

    def categorize(
        self, text: str, k: int = 3
    ) -> Dict[str, Any]:
        """
        Возвращает:
        {
            "predicted_category": "...",
            "similar_examples": [ {id, category, text, score}, ... ]
        }
        """
        query_vec = embed_texts(self.client, [text])[0]

        scores = [
            cosine_sim(query_vec, self.embeddings[i])
            for i in range(len(self.examples))
        ]

        # индексы k самых похожих
        top_idx = np.argsort(scores)[::-1][:k]
        similar = []
        for idx in top_idx:
            ex = dict(self.examples[idx])
            ex["score"] = float(scores[idx])
            similar.append(ex)

        # по похожим примерам считаем "голосование" категорий
        category_votes: Dict[str, float] = {}
        for ex in similar:
            cat = ex["category"]
            category_votes[cat] = category_votes.get(cat, 0.0) + ex["score"]

        if category_votes:
            predicted_category = max(category_votes.items(), key=lambda kv: kv[1])[0]
        else:
            predicted_category = "Другое"

        return {
            "predicted_category": predicted_category,
            "similar_examples": similar,
        }


# ===================== МОДЕЛЬ ТИКЕТА =====================


@dataclass
class Ticket:
    """
    Упрощённая структура тикета.
    В реальном бекенде сюда добавите id пользователя, статус, приоритет и т.д.
    """

    address: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    urgency: Optional[str] = None

    def is_complete(self) -> bool:
        """Минимальные поля, чтобы отправить в backend."""
        return bool(self.address and self.description and self.category)


REQUIRED_FIELDS_ORDER = ["address", "description", "category"]


FIELD_HINTS_RU: Dict[str, str] = {
    "address": "адрес происшествия (город, улица, дом, подъезд/квартира при необходимости)",
    "description": "краткое, но понятное описание проблемы (что случилось, с чем связана жалоба)",
    "category": "основная категория проблемы (например: ЖКХ, Экология, Транспорт, Дороги и т.п.)",
    "urgency": "насколько срочно нужно решить проблему (низкий, средний, высокий приоритет)",
}


class TicketFillingAssistant:
    """
    Нейросетевой помощник, который:
    1) Из текста пользователя вытаскивает поля тикета.
    2) Если чего-то не хватает, формулирует вежливый уточняющий вопрос.
    """

    def __init__(self, client: OpenAI):
        self.client = client

    def extract_fields_from_text(self, text: str) -> Ticket:
        """
        Просим модель аккуратно распарсить текст пользователя в JSON с полями тикета.
        """
        system_msg = (
            "Ты помощник оператора городского контакт-центра. "
            "По тексту обращения жителя нужно извлечь структурированную информацию о проблеме. "
            "Отвечай СТРОГО в формате JSON без комментариев и пояснений. "
            "Если поле нельзя определить, ставь null."
        )

        user_msg = (
            "Извлеки из текста обращения следующие поля:\n"
            "- address: точный адрес происшествия, если указан явно.\n"
            "- description: краткое описание проблемы своими словами (1–2 предложения).\n"
            "- category: одна из категорий: "
            + ", ".join(TICKET_CATEGORIES)
            + ". Если не уверен — выбери 'Другое'.\n"
            "- urgency: низкий, средний или высокий приоритет, если это понятно из текста.\n\n"
            "Текст обращения:\n"
            f"\"{text}\""
        )

        resp = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.1,
        )

        raw = resp.choices[0].message.content.strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # fallback — ничего не распарсили
            data = {}

        return Ticket(
            address=data.get("address") or None,
            description=data.get("description") or None,
            category=data.get("category") or None,
            urgency=data.get("urgency") or None,
        )

    def suggest_next_question(self, ticket: Ticket) -> Optional[str]:
        """
        Если каких-то полей не хватает — задаём аккуратный вопрос.
        Если всё есть — возвращаем None.
        """
        if ticket.is_complete():
            return None

        # Находим первое обязательное поле, которое не заполнено
        missing_field = None
        for f in REQUIRED_FIELDS_ORDER:
            if getattr(ticket, f) in (None, "", []):
                missing_field = f
                break

        if missing_field is None:
            return None

        # Попросим модель сформулировать вопрос на основе уже известных полей
        known_fields = {
            k: v for k, v in asdict(ticket).items() if v is not None
        }

        system_msg = (
            "Ты вежливый ассистент, который помогает горожанину оформить обращение. "
            "Нужно задать ОДИН короткий и понятный вопрос, чтобы уточнить недостающее поле."
        )

        user_msg = (
            "Сейчас у нас есть такая информация по тикету (JSON):\n"
            f"{json.dumps(known_fields, ensure_ascii=False, indent=2)}\n\n"
            f"Не хватает поля '{missing_field}', которое означает: {FIELD_HINTS_RU.get(missing_field, missing_field)}.\n"
            "Сформулируй, пожалуйста, один вежливый вопрос по-русски, без лишних пояснений и без кавычек вокруг."
        )

        resp = self.client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.4,
        )
        question = resp.choices[0].message.content.strip()
        return question


# ===================== ПРОСТОЙ NLP-ЧАТ =====================


class CitySupportChat:
    """
    Обёртка, которая:
    - ведёт диалог с пользователем;
    - использует RAG для определения категории;
    - добирает недостающие поля тикета;
    - демонстрирует использование NLP для ответов.
    """

    def __init__(self, client: OpenAI):
        self.client = client
        self.classifier = RAGTicketClassifier(client, EXAMPLE_TICKETS)
        self.ticket_assistant = TicketFillingAssistant(client)
        self.current_ticket = Ticket()
        self.history: List[Dict[str, str]] = []

    def _update_ticket_from_text(self, text: str) -> None:
        """Обновляем текущий тикет новыми данными из текста пользователя."""
        extracted = self.ticket_assistant.extract_fields_from_text(text)
        # Простейшая стратегия: перезаписываем, если ранее поля не было
        for field in ["address", "description", "category", "urgency"]:
            current_value = getattr(self.current_ticket, field)
            new_value = getattr(extracted, field)
            if current_value in (None, "", []) and new_value not in (None, "", []):
                setattr(self.current_ticket, field, new_value)

    def _ensure_category_with_rag(self, user_text: str) -> None:
        """Если у тикета нет категории — определяем через RAG-классификатор."""
        if self.current_ticket.category:
            return
        rag_result = self.classifier.categorize(user_text, k=3)
        self.current_ticket.category = rag_result["predicted_category"]

    def handle_user_message(self, user_text: str) -> str:
        """
        Основной метод: принимает текст пользователя и возвращает ответ ассистента.
        """
        self.history.append({"role": "user", "content": user_text})

        # 1. Обновляем структуру тикета из текста
        self._update_ticket_from_text(user_text)

        # 2. Если нет категории — определяем её через RAG
        self._ensure_category_with_rag(user_text)

        # 3. Проверяем, хватает ли полей
        next_q = self.ticket_assistant.suggest_next_question(self.current_ticket)
        if next_q:
            assistant_reply = next_q
        else:
            # Все нужные поля есть — "создаём" тикет (здесь просто печатаем JSON)
            ticket_json = json.dumps(
                asdict(self.current_ticket), ensure_ascii=False, indent=2
            )
            assistant_reply = (
                "Спасибо, я собрал все необходимые данные и создал обращение.\n"
                "Краткое содержание вашего тикета:\n"
                f"{ticket_json}\n"
                "Эти данные можно отправить в backend в виде JSON."
            )

        self.history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply


# ===================== ДЕМО-ЗАПУСК =====================


def rag_classifier(client: OpenAI) -> None:
    print("\n=== DEMO 1: RAG-классификатор категорий тикета ===\n")

    classifier = RAGTicketClassifier(client, EXAMPLE_TICKETS)
    demo_text = (
        "Во дворе по адресу улица Ленина, дом 10 уже неделю не вывозят переполненные мусорные контейнеры, "
        "появился неприятный запах."
    )
    result = classifier.categorize(demo_text, k=3)

    print("Текст обращения:")
    print(demo_text)
    print("\nПредсказанная категория:", result["predicted_category"])
    print("\nПохожие исторические тикеты:")
    for ex in result["similar_examples"]:
        print(f"- id={ex['id']} | категория={ex['category']} | score={ex['score']:.3f}")
        print(f"  текст: {ex['text']}")


def demo_ticket_dialog(client: OpenAI) -> None:
    print("\n=== DEMO 2: Нейросетевой сбор недостающих полей тикета ===\n")

    chat = CitySupportChat(client)

    # Пример сценария, где сначала пользователь пишет неполное обращение,
    # а потом отвечает на уточняющий вопрос.
    user_messages = [
        "Здравствуйте! У нас во дворе огромная яма на дороге, машины постоянно бьют подвеску.",
        "Это улица Центральная, дом 15, во дворе между первым и вторым подъездами.",
    ]

    for i, msg in enumerate(user_messages, start=1):
        print(f"\n--- Сообщение пользователя #{i} ---")
        print(msg)
        reply = chat.handle_user_message(msg)
        print("\nОтвет ассистента:")
        print(reply)


def main():
    client = get_client()

    rag_classifier(client)
    demo_ticket_dialog(client)


if __name__ == "__main__":
    main()


