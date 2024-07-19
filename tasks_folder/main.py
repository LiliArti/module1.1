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

