import sqlite3

def create_table():
    conn = sqlite3.connect('todolist.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            status TEXT NOT NULL,
            due_date TEXT NOT NULL,
            assignee TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()