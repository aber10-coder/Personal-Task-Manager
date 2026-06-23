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
    