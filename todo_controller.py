from datetime import datetime
from todo_model import TaskModel, TaskStatus
from todo_view import TaskView

class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view

    def run(self):
        while True:
            self.view.display_menu()
            choice = self.view.get_input("Оберіть дію: ")

            if choice == '1':
                self._create_task()
            elif choice == '2':
                self._change_status()
            elif choice == '3':
                self._delete_task()
            elif choice == '4':
                self._edit_task()
            elif choice == '5':
                self._show_all()
            elif choice == '6':
                self._filter_by_status()
            elif choice == '7':
                self._show_by_id()
            elif choice == '0':
                self.view.display_message("Вихід з програми. До побачення!")
                break
            else:
                self.view.display_error("Невірний вибір, спробуйте ще раз.")

    def _create_task(self):
        desc = self.view.get_input("Введіть опис завдання: ")
        date_str = self.view.get_input("Запланувати на (формат YYYY-MM-DD HH:MM): ")
        try:
            schedule_for = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            task = self.model.add_task(desc, schedule_for)
            self.view.display_message(f"Завдання створено! (ID: {str(task.id)[:8]})")
        except ValueError:
            self.view.display_error("Невірний формат дати. Використовуйте YYYY-MM-DD HH:MM")

    def _change_status(self):
        task_id = self.view.get_input("Введіть ID завдання (мінімум перші 4 символи): ")
        print("Статуси: 1 -> ToDo, 2 -> InProgress, 3 -> Done")
        st_choice = self.view.get_input("Оберіть новий статус (1-3): ")
        
        status_map = {'1': TaskStatus.TODO, '2': TaskStatus.IN_PROGRESS, '3': TaskStatus.DONE}
        
        if st_choice in status_map:
            if self.model.update_task_status(task_id, status_map[st_choice]):
                self.view.display_message("Статус успішно оновлено.")
            else:
                self.view.display_error("Завдання з таким ID не знайдено.")
        else:
            self.view.display_error("Невірний вибір статусу.")

    def _delete_task(self):
        task_id = self.view.get_input("Введіть ID завдання для видалення: ")
        if self.model.delete_task(task_id):
            self.view.display_message("Завдання успішно видалено.")
        else:
            self.view.display_error("Завдання не знайдено.")

    def _edit_task(self):
        task_id = self.view.get_input("Введіть ID завдання для зміни опису: ")
        new_desc = self.view.get_input("Введіть новий опис: ")
        if self.model.update_task_description(task_id, new_desc):
            self.view.display_message("Опис успішно оновлено.")
        else:
            self.view.display_error("Завдання не знайдено.")

    def _show_all(self):
        tasks = self.model.get_all_tasks()
        self.view.display_tasks(tasks)

    def _filter_by_status(self):
        print("Статуси: 1 -> ToDo, 2 -> InProgress, 3 -> Done")
        st_choice = self.view.get_input("Який статус показати? (1-3): ")
        status_map = {'1': TaskStatus.TODO, '2': TaskStatus.IN_PROGRESS, '3': TaskStatus.DONE}
        
        if st_choice in status_map:
            tasks = self.model.filter_by_status(status_map[st_choice])
            self.view.display_tasks(tasks)
        else:
            self.view.display_error("Невірний вибір статусу.")

    def _show_by_id(self):
        task_id = self.view.get_input("Введіть ID завдання: ")
        task = self.model.get_task_by_id(task_id)
        self.view.display_task_details(task)