"""
Скрипт для обновления изображений в существующих квестах
"""
from data import db_session
from data.quests import Quest

def update_quest_images():
    """Обновляет изображения в существующих квестах"""
    db_path = 'db/base.db'
    db_session.global_init(db_path)
    db_sess = db_session.create_session()
    
    try:
        # Получаем все квесты
        quests = db_sess.query(Quest).all()
        
        if len(quests) == 0:
            print("Квесты не найдены. Запустите init_db.py для создания квестов.")
            db_sess.close()
            return
        
        # Обновляем изображения
        # Первый квест - last.png
        if len(quests) > 0:
            quests[0].image_path = "static/img/last.png"
            print(f"Обновлен квест '{quests[0].title}': {quests[0].image_path}")
        
        # Второй квест - kak.png
        if len(quests) > 1:
            quests[1].image_path = "static/img/kak.png"
            print(f"Обновлен квест '{quests[1].title}': {quests[1].image_path}")
        
        # Остальные квесты (если есть) - чередуем изображения
        for i in range(2, len(quests)):
            if i % 2 == 0:
                quests[i].image_path = "static/img/last.png"
            else:
                quests[i].image_path = "static/img/kak.png"
            print(f"Обновлен квест '{quests[i].title}': {quests[i].image_path}")
        
        db_sess.commit()
        print(f"\nОбновлено {len(quests)} квестов!")
        
    except Exception as e:
        print(f"Ошибка при обновлении: {e}")
        db_sess.rollback()
    finally:
        db_sess.close()

if __name__ == '__main__':
    print("Обновление изображений в квестах...")
    update_quest_images()
    print("Готово!")

