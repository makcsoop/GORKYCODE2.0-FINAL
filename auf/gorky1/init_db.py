"""
Скрипт для инициализации базы данных и создания пользователя admin
"""
from data import db_session
from data.users import User
from data.quests import Quest

def init_admin():
    """Создает пользователя admin если его нет, или обновляет пароль если существует"""
    db_sess = db_session.create_session()
    
    admin = db_sess.query(User).filter(User.login == 'admin').first()
    if not admin:
        admin = User()
        admin.login = 'admin'
        admin.password = 'admin'
        admin.email = 'admin@example.com'
        admin.tg_name = 'admin'
        admin.balance = 0
        db_sess.add(admin)
        db_sess.commit()
        print("Пользователь admin создан (логин: admin, пароль: admin)")
    else:
        # Обновляем пароль на случай если он был изменен
        admin.password = 'admin'
        if admin.balance is None:
            admin.balance = 0
        db_sess.commit()
        print("Пользователь admin уже существует, пароль обновлен на 'admin'")
    
    db_sess.close()

def init_sample_quests():
    """Создает примерные квесты для тестирования"""
    db_sess = db_session.create_session()
    
    # Проверяем, есть ли уже квесты
    if db_sess.query(Quest).count() > 0:
        print("Квесты уже существуют")
        db_sess.close()
        return
    
    # Примерные квесты
    sample_quests = [
        Quest(
            title="Проверка парка Горького",
            description="Необходимо проверить состояние парка Горького, наличие мусора и общее состояние территории.",
            latitude=56.3269,
            longitude=44.0075,
            points=100,
            status="не взята",
            image_path="static/img/last.png"
        ),
        Quest(
            title="Проверка набережной",
            description="Проверить состояние набережной Волги, наличие необходимой инфраструктуры.",
            latitude=56.3287,
            longitude=44.0000,
            points=150,
            status="не взята",
            image_path="static/img/kak.png"
        ),
    ]
    
    for quest in sample_quests:
        db_sess.add(quest)
    
    db_sess.commit()
    print(f"Создано {len(sample_quests)} примерных квестов")
    db_sess.close()

if __name__ == '__main__':
    db_session.global_init('db/base.db')
    init_admin()
    init_sample_quests()
    print("Инициализация базы данных завершена!")

