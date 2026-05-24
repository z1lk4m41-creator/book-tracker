import json
import os
from datetime import datetime

BOOKS_FILE = "books.json"


def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_books(books):
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def add_book(books):
    author = input("Автор: ").strip()
    title  = input("Название: ").strip()
    for book in books:
        if book["author"].lower() == author.lower() and \
           book["title"].lower() == title.lower():
            print("Эта книга уже есть в трекере.")
            return
    while True:
        try:
            rating = int(input("Оценка (1–5): "))
            if 1 <= rating <= 5:
                break
            print("Введите число от 1 до 5.")
        except ValueError:
            print("Некорректный ввод.")
    date = input(f"Дата прочтения [{datetime.today().strftime('%d.%m.%Y')}]: ").strip()
    if not date:
        date = datetime.today().strftime("%d.%m.%Y")
    books.append({"author": author, "title": title, "rating": rating, "date": date})
    save_books(books)
    print(f'Книга "{title}" добавлена.')


def list_books(books):
    if not books:
        print("Список книг пуст.")
        return
    print(f"\n{'№':<4} {'Автор':<20} {'Название':<30} {'Оценка':<8} {'Дата'}")
    print("-" * 70)
    for i, b in enumerate(books, 1):
        print(f"{i:<4} {b['author']:<20} {b['title']:<30} {b['rating']:<8} {b['date']}")
    print()


def average_rating(books):
    if not books:
        print("Нет данных для расчёта.")
        return
    avg = sum(b["rating"] for b in books) / len(books)
    print(f"Средняя оценка: {avg:.2f} (из {len(books)} книг)")


def author_stats(books):
    if not books:
        print("Нет данных.")
        return
    stats = {}
    for b in books:
        stats[b["author"]] = stats.get(b["author"], 0) + 1
    print("\nСтатистика по авторам:")
    for author, count in sorted(stats.items()):
        print(f"  {author}: {count} кн.")
    print()


def delete_book(books):
    if not books:
        print("Список книг пуст.")
        return
    list_books(books)
    try:
        idx = int(input("Введите номер книги для удаления: ")) - 1
        if 0 <= idx < len(books):
            removed = books.pop(idx)
            save_books(books)
            print(f'Книга "{removed["title"]}" удалена.')
        else:
            print("Неверный номер.")
    except ValueError:
        print("Введите целое число.")


def show_menu():
    print("\n=== Трекер прочитанных книг ===")
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Показать среднюю оценку")
    print("4. Статистика по авторам")
    print("5. Удалить книгу")
    print("6. Выход")


def main():
    books = load_books()
    while True:
        show_menu()
        choice = input("Выберите пункт: ").strip()
        if   choice == "1": add_book(books)
        elif choice == "2": list_books(books)
        elif choice == "3": average_rating(books)
        elif choice == "4": author_stats(books)
        elif choice == "5": delete_book(books)
        elif choice == "6": print("До свидания!"); break
        else: print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
