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