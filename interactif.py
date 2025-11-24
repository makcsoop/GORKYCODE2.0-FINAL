import pandas as pd
import os

def interactive_csv_viewer(file_path, encoding='windows-1251'):
    df = pd.read_csv(file_path, encoding=encoding)
    
    page_size = 10
    current_page = 0
    total_pages = (len(df) + page_size - 1) // page_size
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана
        
        print(f"Файл: {file_path} | Страница {current_page + 1}/{total_pages}")
        print("=" * 60)
        
        # Показ текущей страницы
        start_idx = current_page * page_size
        end_idx = start_idx + page_size
        print(df.iloc[start_idx:end_idx])
        
        print("\nКоманды:")
        print("n - следующая страница, p - предыдущая страница")
        print("f - первая страница, l - последняя страница")
        print("s - показать статистику, q - выход")
        
        command = input("\nВведите команду: ").lower()
        
        if command == 'n' and current_page < total_pages - 1:
            current_page += 1
        elif command == 'p' and current_page > 0:
            current_page -= 1
        elif command == 'f':
            current_page = 0
        elif command == 'l':
            current_page = total_pages - 1
        elif command == 's':
            show_statistics(df)
            input("Нажмите Enter для продолжения...")
        elif command == 'q':
            break

def show_statistics(df):
    print("\n" + "=" * 40)
    print("СТАТИСТИКА ДАННЫХ")
    print("=" * 40)
    print(f"Общее количество строк: {len(df)}")
    print(f"Количество столбцов: {len(df.columns)}")
    print("\nТипы данных:")
    print(df.dtypes)
    print("\nПустые значения:")
    print(df.isnull().sum())

# Запуск интерактивного просмотрщика
interactive_csv_viewer('complaints_clear_2.csv')