import sqlite3
from datetime import datetime

#nazwa pliku bazy danych
DB_NAME = 'laba5.db'

#lista dopuszczalnych statusów zadań
ALLOWED_STATUSES = ['do zrobienia', 'w trakcie', 'zrobione']

def init_db():
    """Tworzy tabelę 'tasks' w bazie danych SQLite jeśli jeszcze nie istnieje"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
        )""")

    conn.commit()
    conn.close()


def show_tasks():
    """1. Pobiera i wyświetla listę wszystkich zadań z bazy danych."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, status, created_at FROM tasks ORDER BY id ASC"

    )
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print("\n[!] Baza danyzh jest pusta. Brak zadań do wyświetlenia.")
        return

    print('\n' + '=' * 70)
    print(
        f"{'ID':<5} | {'TYTUŁ':<25} | {'STATUS':<15} | {'DATA DODANIA':<20}"
    )
    print('=' * 70)

    for task in tasks:
        task_id, title, status, created_at = task
        #przycinanie długiego tytułu na potrzeby czytelnego wyświetlenia 
        display_title = title if len(title) <= 24 else title[:21] + '...'
        print(
            f"{task_id:<5} | {display_title:<25} | {status:<15} | {created_at:<20}"
        )

    print('=' * 70)

def add_task():
    """2. Dodaje nowe zadania z domyślnym statusem 'do zrobienia' oraz znacznikiem czasu"""
    title = input("\nPodaj treść zadania: ").strip()

    if not title:
        print("[!] Błąd: Treść zadania nie może być pusta")
        return

    default_status = "do zrobienia"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #użycie parametru? zapobiega atakom SQL Injection
    cursor.execute(
        "INSERT INTO tasks (title, status, created_at) VALUES (?, ?, ?)",
        (title, default_status, created_at)
    )

    conn.commit()
    conn.close()

    print(
        f"[+] Pomyślnie dodano zadania: '{title}' ze statusem '{default_status}'"
    )

def change_status():
    """3. Aktualizuje status wybranego zadania po wcześniejszym sprawdzeniu poprawności danych"""
    try:
        task_id = int(input("\nPodaj ID zadania, którego status chcesz zmienić: "))
    except ValueError:
        print("[!] Błąd: ID zadania musi być liczbą całkowitą")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, status FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        print(f"[!] Błąd: Zadania o (ID {task_id}): '{task[1]}'")
        conn.close()
        return

    print(f"Obecny status zadania (ID {task_id}): '{task[1]}'")
    print(f"Dopuszczalne statusy: {', '.join(ALLOWED_STATUSES)}")
    new_status = input("Podaj nowy status: ").strip().lower()

    if new_status not in ALLOWED_STATUSES:
        print(
            f"[!] Błąd: '{new_status}' nie jest poprawnym statusem. Wybierz jeden z podanych wyżej."
        )
        conn.close()
        return

    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id)
    )
    conn.commit()
    conn.close()

    print(
        f"[+] Status zadania o ID {task_id} został zmieniony na '{new_status}'."

    )

def delete_task():
    """4. Usuwa zadania z bd po ID"""
    try:
        task_id = int(input("\nPodaj ID zadania do usunięcia: "))
    except ValueError:
        print("[!] Błąd: ID zadania musi być liczbą całkowitą")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        print(f"[!] Błąd: Zadania o ID {task_id} nie istnieje w BD")
        conn.close()
        return

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    print(f"[+] Zadania o ID {task_id} zostało pomyślnie usunięte z bazy")


def main():
    """Główna pętla programu zarządzająca menu konsolowyn"""
    init_db()

    while True:
        print('\n' + '=' * 35)
        print("    APLIKACJA TO-DO LIST (SQLite)    ")
        print('=' * 35)
        print("1. Wyświetl listę zadań")
        print("2. Dodaj nowe zadanie")
        print("3. Zmień status zadania")
        print("4. Usuń zadanie")
        print("5. Wyjdz z programu")

        choice = input("\nWybierz opcję (1-5): ").strip()
        if choice == '1':
            show_tasks()
        elif choice == '2':
            add_task()
        elif choice == '3':
            change_status()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            print("\nZamknięcie połączenia z bd. Koniec programu")
            break
        else:
            print("[!] Nieprawidłowy wybór. Wpisz cyfrę od 1 do 5")


if __name__ == "__main__":
    main()