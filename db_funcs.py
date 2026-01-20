# import sqlite3
# import pandas as pd
#
# DB_PATH = 'todolist.db'
#
# # 1. Thêm công việc
# def add_task(task_name, status, due_date, assignee, notes):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('INSERT INTO tasks (task_name, status, due_date, assignee, notes) VALUES (?,?,?,?,?)',
#               (task_name, status, str(due_date), assignee, notes))
#     conn.commit()
#     conn.close()
#
# # 2. Lấy danh sách công việc (có thể lọc theo điều kiện nếu cần)
# def load_tasks():
#     conn = sqlite3.connect(DB_PATH)
#     df = pd.read_sql_query("SELECT * FROM tasks", conn)
#     conn.close()
#     return df
#
# # 3. Lấy thông tin 1 công việc theo ID (để hiển thị lên form sửa)
# def get_task_by_id(task_id):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
#     data = c.fetchone()
#     conn.close()
#     return data
#
# # 4. Cập nhật trạng thái nhanh
# def update_status(task_id, new_status):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('UPDATE tasks SET status=? WHERE id=?', (new_status, task_id))
#     conn.commit()
#     conn.close()
#
# # 5. Cập nhật toàn bộ thông tin công việc
# def update_task(task_id, task_name, status, due_date, assignee, notes):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('''
#         UPDATE tasks
#         SET task_name=?, status=?, due_date=?, assignee=?, notes=?
#         WHERE id=?
#     ''', (task_name, status, str(due_date), assignee, notes, task_id))
#     conn.commit()
#     conn.close()
#
# # 6. Xóa công việc
# def delete_task(task_id):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
#     conn.commit()
#     conn.close()

import sqlite3
import pandas as pd

DB_PATH = 'todolist.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

# 1. Thêm công việc
def add_task(task_name, status, due_date, assignee, notes):
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO tasks (task_name, status, due_date, assignee, notes) VALUES (?,?,?,?,?)',
            (task_name, status, str(due_date), assignee, notes)
        )

# 2. Lấy danh sách công việc
def load_tasks():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM tasks", conn)

# 3. Lấy công việc theo ID
def get_task_by_id(task_id):
    with get_connection() as conn:
        cur = conn.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
        return cur.fetchone()

# 4. Cập nhật trạng thái
def update_status(task_id, new_status):
    with get_connection() as conn:
        conn.execute(
            'UPDATE tasks SET status=? WHERE id=?',
            (new_status, task_id)
        )

# 5. Cập nhật toàn bộ công việc
def update_task(task_id, task_name, status, due_date, assignee, notes):
    with get_connection() as conn:
        conn.execute('''
            UPDATE tasks 
            SET task_name=?, status=?, due_date=?, assignee=?, notes=? 
            WHERE id=?
        ''', (task_name, status, str(due_date), assignee, notes, task_id))

# 6. Xóa công việc
def delete_task(task_id):
    with get_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE id=?', (task_id,))
