import sqlite3
import bcrypt

DB_PATH = 'dist/exam_system.db'

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def init_db():
    print(f"Initializing database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash BLOB NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        department_id INTEGER,
        student_id INTEGER,
        assigned_subject_id INTEGER,
        is_active INTEGER DEFAULT 1,
        is_locked INTEGER DEFAULT 0,
        failed_login_attempts INTEGER DEFAULT 0,
        last_login TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create departments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT UNIQUE NOT NULL,
        department_code TEXT UNIQUE NOT NULL,
        head_of_department TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Create students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_number TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        department_id INTEGER,
        semester INTEGER,
        gender TEXT,
        date_of_birth DATE,
        email TEXT,
        phone TEXT,
        address TEXT,
        registration_no TEXT,
        cnic TEXT,
        father_name TEXT,
        father_cnic TEXT,
        guardian_phone TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (department_id) REFERENCES departments (department_id)
    )
    """)
    
    # Create courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT UNIQUE NOT NULL,
        course_name TEXT NOT NULL,
        department_id INTEGER,
        semester INTEGER,
        credits INTEGER DEFAULT 3,
        max_marks INTEGER DEFAULT 100,
        pass_marks INTEGER DEFAULT 40,
        description TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (department_id) REFERENCES departments (department_id)
    )
    """)
    
    # Create marks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS marks (
        mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        marks_obtained REAL,
        max_marks INTEGER DEFAULT 100,
        grade TEXT,
        status TEXT,
        exam_date DATE,
        entered_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (course_id) REFERENCES courses (course_id),
        FOREIGN KEY (entered_by) REFERENCES users (user_id),
        UNIQUE(student_id, course_id)
    )
    """)
    
    # Create results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        semester INTEGER,
        gpa REAL,
        cgpa REAL,
        total_marks REAL,
        obtained_marks REAL,
        status TEXT,
        generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students (student_id)
    )
    """)
    
    # Create default admin
    admin_user = 'admin'
    admin_pass = 'admin123'
    # bcrypt.hashpw returns bytes, we need to decode to string for storage
    hashed = hash_password(admin_pass).decode('utf-8')
    
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)", 
                       (admin_user, hashed, 'Admin', 'System Administrator'))
        print(f"Created admin user: {admin_user} / {admin_pass}")
    except sqlite3.IntegrityError:
        print("Admin user already exists, updating password...")
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hashed, admin_user))
        print(f"Updated admin password to: {admin_pass}")
        
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
