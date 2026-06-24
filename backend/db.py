import sqlite3

def init_db():
    conn=sqlite3.connect("app.db")
    cursor=conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL          
        )
     """)
    
    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS tasks(
           id INTEGER  PRIMARY KEY AUTOINCREMENT,
           title TEXT NOT NULL,
           description TEXT,
           priority TEXT NOT NULL,
           status TEXT NOT NULL,
           due_date TEXT,
           owner_email TEXT NOT NULL,
           FOREIGN KEY(owner_email)
           REFERENCES users(email)                                        
        )
     """)
    conn.commit()
    conn.close()
def get_connection():
    conn=sqlite3.connect("app.db")
    conn.row_factory=sqlite3.Row
    return conn
def get_user_by_email(email):
    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    conn.close()

    if user:
        return dict(user)

    return None
def create_user(email, hashed_password):
    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO users(email, hashed_password)
        VALUES (?, ?)
        """,
        (email, hashed_password)
    )

    conn.commit()

    user_id = cursor.lastrowid

    user = conn.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    ).fetchone()

    conn.close()

    return dict(user)
def create_task(
    title,
    description,
    priority,
    status,
    due_date,
    owner_email
):
    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO tasks(
            title,
            description,
            priority,
            status,
            due_date,
            owner_email
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            priority,
            status,
            due_date,
            owner_email
        )
    )

    conn.commit()

    task_id = cursor.lastrowid

    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?",
        (task_id,)
    ).fetchone()

    conn.close()

    return dict(task)
def get_tasks_by_owner(owner_email):
    conn = get_connection()

    tasks = conn.execute(
        """
        SELECT * FROM tasks
        WHERE owner_email=?
        """,
        (owner_email,)
    ).fetchall()

    conn.close()

    return [dict(task) for task in tasks]

def get_task_by_id(task_id):
    conn = get_connection()

    task = conn.execute(
        """
        SELECT * FROM tasks
        WHERE id=?
        """,
        (task_id,)
    ).fetchone()

    conn.close()

    if task:
        return dict(task)

    return None

def delete_task(task_id):
    conn = get_connection()

    conn.execute(
        """
        DELETE FROM tasks
        WHERE id=?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()
def update_task(
    task_id,
    title,
    description,
    priority,
    status,
    due_date
):
    conn = get_connection()

    conn.execute(
        """
        UPDATE tasks
        SET title=?,
            description=?,
            priority=?,
            status=?,
            due_date=?
        WHERE id=?
        """,
        (
            title,
            description,
            priority,
            status,
            due_date,
            task_id
        )
    )

    conn.commit()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?",
        (task_id,)
    ).fetchone()

    conn.close()

    return dict(task)

def update_task_status(
    task_id,
    status
):
    conn = get_connection()

    conn.execute(
        """
        UPDATE tasks
        SET status=?
        WHERE id=?
        """,
        (
            status,
            task_id
        )
    )

    conn.commit()

    task = conn.execute(
        """
        SELECT * FROM tasks
        WHERE id=?
        """,
        (task_id,)
    ).fetchone()

    conn.close()

    return dict(task)

def get_filtered_tasks(
    owner_email,
    status=None,
    priority=None
):
    conn = get_connection()

    query = """
        SELECT * FROM tasks
        WHERE owner_email=?
    """

    params = [owner_email]

    if status:
        query += " AND status=?"
        params.append(status)

    if priority:
        query += " AND priority=?"
        params.append(priority)

    tasks = conn.execute(
        query,
        tuple(params)
    ).fetchall()

    conn.close()

    return [dict(task) for task in tasks]

def get_task_summary(owner_email):
    conn = get_connection()

    total = conn.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE owner_email=?
        """,
        (owner_email,)
    ).fetchone()[0]

    pending = conn.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE owner_email=?
        AND status='pending'
        """,
        (owner_email,)
    ).fetchone()[0]

    in_progress = conn.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE owner_email=?
        AND status='in_progress'
        """,
        (owner_email,)
    ).fetchone()[0]

    done = conn.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE owner_email=?
        AND status='done'
        """,
        (owner_email,)
    ).fetchone()[0]

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "done": done
    }