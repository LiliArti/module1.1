LOW = "1"
MEDIUM = "2"
HIGH = "3"
PRIORITIES = {
    LOW: "низкий",
    MEDIUM: "средний",
    HIGH: "высокий"
}

NEW = "1"
IN_PROGRESS = "2"
COMPLETED = "3"
STATUSES = {
    NEW: "новая",
    IN_PROGRESS: "в процессе",
    COMPLETED: "завершенна"
}
DATA_FILE = 'tasks.txt'

def load_tasks():
    tasks = {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            lines = file.readline()
            for line in lines:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    task_id, name, description, priority, status = parts
                    tasks[task_id] = {
                        "name": name,
                        "description": description,
                        "priority": priority,
                        "status": status
                    }
                else:
                    print(f"Некорректная строка: {line.strip()}")
    except FileExistsError:
        print("Файл с задачами не найден")
    return tasks

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        for task_id, task in tasks.items():
            line = f"{task_id}|{task['name']}|{task['description']}|{task['priority']}|{task['status']}\n"
            file.write(line)

tasks = load_tasks()

def get_next_id():
    if tasks:
        return max(int(id) for id in tasks) + 1
    return 1

def create_task(name, description, priority, status):
    task_id = str(get_next_id())
    tasks[task_id] = {
        "name": name,
        "description": description,
        "priority": priority,
        "status": status
    }
    save_tasks(tasks)

def read_tasks():
    return tasks

def update_task(task_id, field, value):
    if task_id in tasks:
        if field == "priority":
            tasks[task_id]["priority"] = PRIORITIES[value]
        elif field == "status":
            tasks[task_id]["status"] = STATUSES[value]
        else:
            tasks[task_id][field] = value
        save_tasks(tasks)
    else:
        raise ValueError("Задача с таким ID не существует.")

def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        save_tasks(tasks)
    else:
        raise ValueError ("Задача с таким ID не существует.")

def main_menu():
    while True:
        print("Выберите действие: ")
        print("1 - Создать новую задачу")
        print("2 - Просмотреть задачи")
        print("3 - Обновить задачу")
        print("4 - Удалить задачу")
        print("0 - Выйти из программы")

        choice = input("Ваш выбор: ")
        if choice == "1":
            create_task_interface()
        elif choice == "2":
            view_tasks_interface()
        elif choice == "3":
            update_task_interface()
        elif choice == "4":
            delete_task_interface()
        elif choice == "0":
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

def create_task_interface():
    name = input("введите название задачи: ")
    description = input("введите описание звадачи: ")
    priority = input("введите приоритет задачи (1 - низкий, 2 - средний, 3 - высокий)")
    while priority not in PRIORITIES:
        priority = input("Неверны ввод. Введите приоритет задачи (1 - низкий, 2 - средний, 3 - высокий) ")
    status = input("Введите статус задачи (1 - новая, 2 - в процессе, 3 завершено)")
    while status not in STATUSES:
        status = input("Неверный ввод.Введите статус задачи (1 - новая, 2 - в процессе, 3 завершено)")
    create_task(name, description, priority, status)
    print("Задача создана")

def view_tasks_interface():
    print("Выберите опцию просмотра: ")
    print("1 - Отобразить задачи в изначальном виде")
    print("2 - Отсортировать по статусу")
    print("3 - Отсортировать по приоритету")
    print("4 - Осуществить поиск по названию или описанию")

    choice = input("Ваш выбор: ")
    tasks = read_tasks()

    def print_task(task_id, task):
        print(f"ID: {task_id}, Название: {task.get('name', 'Не указано')}, "
              f"Описание: {task.get('description', 'Не указано')}, "
              f"Приоритет: {task.get('priority', 'Не указано')}, "
              f"Статус: {task.get('status', 'Не указано')}")

    if choice == "1":
        for task_id, task in tasks.items():
            print_task(task_id, task)
    elif choice == "2":
        sorted_tasks = sorted(tasks.items(), key=lambda x: list(STATUSES.values()).index(x[1].get('status', '')))
        for task_id, task in sorted_tasks:
            print_task(task_id, task)
    elif choice == "3":
        sorted_tasks = sorted(tasks.items(), key=lambda x: list(PRIORITIES.values()).index(x[1].get('priority', '')))
        for task_id, task in sorted_tasks:
            print_task(task_id, task)
    elif choice == "4":
        search_term = input("Введите ключевое слово для поиска: ").lower()
        filtered_tasks = {task_id: task for task_id, task in tasks.items() if
                          search_term in task.get('name', '').lower() or search_term in task.get('description',
                                                                                                 '').lower()}
        for task_id, task in filtered_tasks.items():
            print_task(task_id, task)
    else:
        print("Неверный ввод. Возвращение в главное меню.")

def update_task_interface():
    task_id = input("Введите ID задачи, которую хотите обновить: ")
    if task_id not in tasks:
        print("Задача с таким ID не существует")
        return
    print("Выберите поле для обновления: ")
    print("1 - Название")
    print("2 - Описание")
    print("3 - Приоритет")
    print("4 - Статус")

    choice = input("Ваш выбор: ")
    if choice == "1":
        new_value = input("Введите новое название: ")
        update_task(task_id, "name", new_value)
    elif choice == "2":
        new_value = input("Введите новое описание: ")
        update_task(task_id, "description", new_value)
    elif choice == "3":
        new_value = input("Введите новый приоритет (1 - низкий, 2 - средний, 3 - высокий)")
        while new_value not in PRIORITIES:
            new_value = input("Неверны ввод. Введите приоритет задачи (1 - низкий, 2 - средний, 3 - высокий) ")
        update_task(task_id, "priority", new_value)
    elif choice == "4":
        new_value = input("Введите статус задачи (1 - новая, 2 - в процессе, 3 завершено)")
        while new_value not in STATUSES:
            new_value = input("Неверный ввод.Введите статус задачи (1 - новая, 2 - в процессе, 3 завершено)")
        update_task(task_id, "status", new_value)
    else:
        print("Неверный ввод. Возвращение в главное меню.")

def delete_task_interface():
    task_id = input("Введите ID задачи, которую хотите удалить: ")
    if task_id not in tasks:
        print("Задача с таким ID не существует!")

    delete_task(task_id)
    print("Задача удалена.")

if __name__ == "__main__":
    main_menu()