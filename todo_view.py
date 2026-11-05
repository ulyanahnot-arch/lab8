from typing import List
from todo_model import Task

class TaskView:
    @staticmethod
    def display_menu():
        print("\n" + "="*50)
        print(" To-Do List (MVC Pattern)")
        print("="*50)
        print("1. Додати завдання")
        print("2. Змінити статус завдання")
        print("3. Видалити завдання")
        print("4. Змінити опис завдання")
        print("5. Показати всі завдання")
        print("6. Фільтрувати за статусом")
        print("7. Показати детальну інформацію по ID")
        print("0. Вийти")
        print("="*50)

    @staticmethod
    def get_input(prompt: str) -> str:
        return input(prompt).strip()

    @staticmethod
    def display_tasks(tasks: List[Task]):
        if not tasks:
            print("\n[*] Список завдань порожній.")
            return
        
        print(f"\n{'ID (початок)':<12} | {'Опис':<25} | {'Заплановано на':<16} | {'Статус':<12}")
        print("-" * 75)
        for t in tasks:
            short_id = str(t.id)[:8]
            scheduled = t.schedule_for.strftime("%Y-%m-%d %H:%M")

            desc = t.description[:22] + "..." if len(t.description) > 25 else t.description
            print(f"{short_id:<12} | {desc:<25} | {scheduled:<16} | {t.status.value:<12}")

    @staticmethod
    def display_task_details(task: Task):
        if not task:
            print("\n[!] Завдання не знайдено.")
            return
        print("\n--- Деталі завдання ---")
        print(f"Повний ID:    {task.id}")
        print(f"Опис:         {task.description}")
        print(f"Створено:     {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Заплановано:  {task.schedule_for.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Статус:       {task.status.value}")
        print("-----------------------")

    @staticmethod
    def display_message(msg: str):
        print(f"\n[*] {msg}")

    @staticmethod
    def display_error(msg: str):
        print(f"\n[!] ПОМИЛКА: {msg}")