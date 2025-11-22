"""
Скрипт для миграции базы данных - добавляет недостающие колонки
"""
import sqlite3
import os

def migrate_database():
    """Добавляет недостающие колонки в существующую базу данных"""
    db_path = 'db/base.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Проверяем, существует ли колонка balance
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'balance' not in columns:
            print("Добавляем колонку balance в таблицу users...")
            cursor.execute("ALTER TABLE users ADD COLUMN balance INTEGER DEFAULT 0")
            conn.commit()
            print("Колонка balance добавлена успешно!")
        else:
            print("Колонка balance уже существует")
        
        # Проверяем таблицу quests
        try:
            cursor.execute("PRAGMA table_info(quests)")
            quest_columns = [column[1] for column in cursor.fetchall()]
            print(f"Таблица quests существует. Колонки: {quest_columns}")
        except sqlite3.OperationalError:
            print("Таблица quests не существует, будет создана при следующем запуске")
        
        # Проверяем таблицу quest_reports
        try:
            cursor.execute("PRAGMA table_info(quest_reports)")
            report_columns = [column[1] for column in cursor.fetchall()]
            print(f"Таблица quest_reports существует. Колонки: {report_columns}")
        except sqlite3.OperationalError:
            print("Таблица quest_reports не существует, будет создана при следующем запуске")
        
        # Обновляем существующих пользователей, устанавливая balance = 0 если NULL
        cursor.execute("UPDATE users SET balance = 0 WHERE balance IS NULL")
        conn.commit()
        print("Баланс существующих пользователей обновлен")
        
    except Exception as e:
        print(f"Ошибка при миграции: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Начинаем миграцию базы данных...")
    migrate_database()
    print("Миграция завершена!")
    print("\nТеперь можно запустить init_db.py для создания admin пользователя и квестов")

