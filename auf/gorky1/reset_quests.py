"""
Скрипт для сброса статусов квестов и удаления истории отчетов
"""
from data import db_session
from data.quests import Quest
from data.quest_reports import QuestReport
from data.users import User

def reset_quests_and_reports():
    """Сбрасывает статус всех квестов на 'не взята' и удаляет все отчеты"""
    db_sess = db_session.create_session()
    
    try:
        # 1. Удаляем все отчеты (история заходов)
        reports_count = db_sess.query(QuestReport).count()
        db_sess.query(QuestReport).delete()
        print(f"Удалено {reports_count} отчетов из истории")
        
        # 2. Обновляем статус всех квестов на 'не взята'
        quests = db_sess.query(Quest).all()
        updated_count = 0
        for quest in quests:
            if quest.status != 'не взята':
                quest.status = 'не взята'
                updated_count += 1
        
        # 3. Возвращаем баланс пользователей (вычитаем поинты за выполненные квесты)
        # Но так как мы удаляем отчеты, баланс уже не связан с квестами
        # Оставляем баланс как есть, так как пользователь мог получить поинты другими способами
        
        db_sess.commit()
        print(f"Обновлено {updated_count} квестов (статус установлен на 'не взята')")
        print(f"Всего квестов в базе: {len(quests)}")
        print("Сброс завершен успешно!")
        
    except Exception as e:
        db_sess.rollback()
        print(f"Ошибка при сбросе: {e}")
    finally:
        db_sess.close()

if __name__ == '__main__':
    db_session.global_init('db/base.db')
    reset_quests_and_reports()

