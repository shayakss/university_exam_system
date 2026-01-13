-- Database Migration V2 - Feature Enhancements
-- University Exam System - New Features Schema
-- Date: 2025-12-02

-- ============================================
-- ATTENDANCE TRACKING TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS student_attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    course_id INTEGER,
    attendance_date DATE NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Leave', 'Late')) DEFAULT 'Present',
    marked_by INTEGER NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL,
    FOREIGN KEY (marked_by) REFERENCES users(user_id),
    UNIQUE(student_id, course_id, attendance_date)
);

CREATE TABLE IF NOT EXISTS teacher_attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    attendance_date DATE NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Leave', 'Half Day')) DEFAULT 'Present',
    marked_by INTEGER NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (marked_by) REFERENCES users(user_id),
    UNIQUE(user_id, attendance_date)
);

-- ============================================
-- TIMETABLE & SCHEDULING TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS class_schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    day_of_week TEXT CHECK(day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_number TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS exam_schedule (
    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    exam_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    room_number TEXT,
    exam_type TEXT CHECK(exam_type IN ('Mid-Term', 'Final', 'Quiz', 'Practical')) DEFAULT 'Final',
    total_marks INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE CASCADE
);

-- ============================================
-- ASSIGNMENT TRACKING TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    total_marks INTEGER DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assignment_submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('Submitted', 'Pending', 'Late', 'Graded')) DEFAULT 'Pending',
    marks_obtained REAL,
    remarks TEXT,
    file_path TEXT,
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    UNIQUE(assignment_id, student_id)
);

-- ============================================
-- STUDENT PROMOTION TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS promotion_rules (
    rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    min_cgpa REAL DEFAULT 2.0,
    max_f_grades INTEGER DEFAULT 0,
    min_attendance_percentage REAL DEFAULT 75.0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS promotion_history (
    promotion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    from_semester INTEGER NOT NULL,
    to_semester INTEGER NOT NULL,
    promotion_date DATE NOT NULL,
    cgpa REAL,
    promoted_by INTEGER NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (promoted_by) REFERENCES users(user_id)
);

-- ============================================
-- ID CARD GENERATION TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS id_cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    user_id INTEGER,
    card_type TEXT CHECK(card_type IN ('Student', 'Teacher', 'Staff')) NOT NULL,
    card_number TEXT UNIQUE NOT NULL,
    issue_date DATE NOT NULL,
    expiry_date DATE,
    qr_code_data TEXT,
    photo_path TEXT,
    is_active INTEGER DEFAULT 1,
    generated_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (generated_by) REFERENCES users(user_id)
);

-- ============================================
-- ALUMNI DATABASE TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS alumni (
    alumni_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    graduation_year INTEGER NOT NULL,
    graduation_date DATE,
    final_cgpa REAL,
    final_grade TEXT,
    current_status TEXT CHECK(current_status IN ('Employed', 'Self-Employed', 'Higher Studies', 'Unemployed', 'Other')),
    contact_email TEXT,
    contact_phone TEXT,
    current_address TEXT,
    moved_to_alumni_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS alumni_employment (
    employment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumni_id INTEGER NOT NULL,
    company_name TEXT,
    job_title TEXT,
    start_date DATE,
    end_date DATE,
    is_current INTEGER DEFAULT 0,
    salary_range TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE
);

-- ============================================
-- RBAC (Role-Based Access Control) TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL,
    description TEXT,
    is_system_role INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_name TEXT UNIQUE NOT NULL,
    permission_code TEXT UNIQUE NOT NULL,
    description TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS role_permissions (
    role_permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions(permission_id) ON DELETE CASCADE,
    UNIQUE(role_id, permission_id)
);

CREATE TABLE IF NOT EXISTS user_roles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(user_id),
    UNIQUE(user_id, role_id)
);

-- ============================================
-- AUDIT LOGGING TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    action_type TEXT NOT NULL,
    table_name TEXT,
    record_id INTEGER,
    action_description TEXT,
    old_value TEXT,
    new_value TEXT,
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- ============================================
-- DATABASE ARCHIVING TABLES
-- ============================================

CREATE TABLE IF NOT EXISTS archived_students (
    archive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_student_id INTEGER NOT NULL,
    roll_number TEXT NOT NULL,
    name TEXT NOT NULL,
    department_id INTEGER,
    semester INTEGER,
    gender TEXT,
    date_of_birth DATE,
    email TEXT,
    phone TEXT,
    address TEXT,
    archived_date DATE DEFAULT CURRENT_DATE,
    archived_by INTEGER,
    archive_reason TEXT,
    original_data TEXT,
    FOREIGN KEY (archived_by) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS archived_marks (
    archive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_mark_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    marks_obtained REAL,
    grade TEXT,
    status TEXT,
    archived_date DATE DEFAULT CURRENT_DATE,
    original_data TEXT
);

CREATE TABLE IF NOT EXISTS archived_results (
    archive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_result_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    semester INTEGER,
    total_marks REAL,
    marks_obtained REAL,
    percentage REAL,
    sgpa REAL,
    cgpa REAL,
    overall_grade TEXT,
    status TEXT,
    archived_date DATE DEFAULT CURRENT_DATE,
    original_data TEXT
);

CREATE TABLE IF NOT EXISTS archive_metadata (
    metadata_id INTEGER PRIMARY KEY AUTOINCREMENT,
    academic_year TEXT NOT NULL,
    archive_date DATE DEFAULT CURRENT_DATE,
    archived_by INTEGER NOT NULL,
    students_count INTEGER DEFAULT 0,
    marks_count INTEGER DEFAULT 0,
    results_count INTEGER DEFAULT 0,
    archive_size_kb INTEGER,
    can_restore INTEGER DEFAULT 1,
    FOREIGN KEY (archived_by) REFERENCES users(user_id)
);

-- ============================================
-- CLOUD BACKUP CONFIGURATION TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS backup_config (
    config_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT CHECK(provider IN ('Google Drive', 'Dropbox', 'OneDrive')) NOT NULL,
    is_enabled INTEGER DEFAULT 0,
    access_token TEXT,
    refresh_token TEXT,
    folder_path TEXT,
    auto_backup_enabled INTEGER DEFAULT 0,
    backup_frequency_days INTEGER DEFAULT 7,
    last_backup_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- USER PREFERENCES TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS user_preferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    theme TEXT CHECK(theme IN ('Light', 'Dark')) DEFAULT 'Light',
    language TEXT DEFAULT 'English',
    date_format TEXT DEFAULT 'YYYY-MM-DD',
    notifications_enabled INTEGER DEFAULT 1,
    email_notifications INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Attendance Indexes
CREATE INDEX IF NOT EXISTS idx_student_attendance_student ON student_attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_student_attendance_date ON student_attendance(attendance_date);
CREATE INDEX IF NOT EXISTS idx_student_attendance_course ON student_attendance(course_id);
CREATE INDEX IF NOT EXISTS idx_teacher_attendance_user ON teacher_attendance(user_id);
CREATE INDEX IF NOT EXISTS idx_teacher_attendance_date ON teacher_attendance(attendance_date);

-- Schedule Indexes
CREATE INDEX IF NOT EXISTS idx_class_schedule_course ON class_schedule(course_id);
CREATE INDEX IF NOT EXISTS idx_class_schedule_teacher ON class_schedule(teacher_id);
CREATE INDEX IF NOT EXISTS idx_class_schedule_day ON class_schedule(day_of_week);
CREATE INDEX IF NOT EXISTS idx_exam_schedule_course ON exam_schedule(course_id);
CREATE INDEX IF NOT EXISTS idx_exam_schedule_date ON exam_schedule(exam_date);

-- Assignment Indexes
CREATE INDEX IF NOT EXISTS idx_assignments_course ON assignments(course_id);
CREATE INDEX IF NOT EXISTS idx_assignments_teacher ON assignments(teacher_id);
CREATE INDEX IF NOT EXISTS idx_assignment_submissions_assignment ON assignment_submissions(assignment_id);
CREATE INDEX IF NOT EXISTS idx_assignment_submissions_student ON assignment_submissions(student_id);

-- Promotion Indexes
CREATE INDEX IF NOT EXISTS idx_promotion_history_student ON promotion_history(student_id);
CREATE INDEX IF NOT EXISTS idx_promotion_history_date ON promotion_history(promotion_date);

-- ID Card Indexes
CREATE INDEX IF NOT EXISTS idx_id_cards_student ON id_cards(student_id);
CREATE INDEX IF NOT EXISTS idx_id_cards_user ON id_cards(user_id);
CREATE INDEX IF NOT EXISTS idx_id_cards_number ON id_cards(card_number);

-- Alumni Indexes
CREATE INDEX IF NOT EXISTS idx_alumni_student ON alumni(student_id);
CREATE INDEX IF NOT EXISTS idx_alumni_year ON alumni(graduation_year);
CREATE INDEX IF NOT EXISTS idx_alumni_employment_alumni ON alumni_employment(alumni_id);

-- RBAC Indexes
CREATE INDEX IF NOT EXISTS idx_role_permissions_role ON role_permissions(role_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_permission ON role_permissions(permission_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_user ON user_roles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role ON user_roles(role_id);

-- Audit Indexes
CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_logs_table ON audit_logs(table_name);

-- Archive Indexes
CREATE INDEX IF NOT EXISTS idx_archived_students_original ON archived_students(original_student_id);
CREATE INDEX IF NOT EXISTS idx_archived_marks_student ON archived_marks(student_id);
CREATE INDEX IF NOT EXISTS idx_archived_results_student ON archived_results(student_id);

-- ============================================
-- INSERT DEFAULT DATA
-- ============================================

-- Insert default promotion rule
INSERT OR IGNORE INTO promotion_rules (rule_name, min_cgpa, max_f_grades, min_attendance_percentage)
VALUES ('Standard Promotion Rule', 2.0, 0, 75.0);

-- Insert default permissions
INSERT OR IGNORE INTO permissions (permission_name, permission_code, description, category) VALUES
('View Students', 'view_students', 'Can view student records', 'Students'),
('Add Students', 'add_students', 'Can add new students', 'Students'),
('Edit Students', 'edit_students', 'Can edit student records', 'Students'),
('Delete Students', 'delete_students', 'Can delete students', 'Students'),
('View Courses', 'view_courses', 'Can view courses', 'Courses'),
('Add Courses', 'add_courses', 'Can add new courses', 'Courses'),
('Edit Courses', 'edit_courses', 'Can edit courses', 'Courses'),
('Delete Courses', 'delete_courses', 'Can delete courses', 'Courses'),
('View Marks', 'view_marks', 'Can view marks', 'Marks'),
('Enter Marks', 'enter_marks', 'Can enter marks', 'Marks'),
('Edit Marks', 'edit_marks', 'Can edit marks', 'Marks'),
('Delete Marks', 'delete_marks', 'Can delete marks', 'Marks'),
('Generate Results', 'generate_results', 'Can generate results', 'Results'),
('View Results', 'view_results', 'Can view results', 'Results'),
('Mark Attendance', 'mark_attendance', 'Can mark attendance', 'Attendance'),
('View Attendance', 'view_attendance', 'Can view attendance', 'Attendance'),
('Manage Timetable', 'manage_timetable', 'Can manage timetable', 'Timetable'),
('View Timetable', 'view_timetable', 'Can view timetable', 'Timetable'),
('Manage Assignments', 'manage_assignments', 'Can manage assignments', 'Assignments'),
('View Assignments', 'view_assignments', 'Can view assignments', 'Assignments'),
('Promote Students', 'promote_students', 'Can promote students', 'Promotion'),
('Generate ID Cards', 'generate_id_cards', 'Can generate ID cards', 'ID Cards'),
('Manage Alumni', 'manage_alumni', 'Can manage alumni records', 'Alumni'),
('View Alumni', 'view_alumni', 'Can view alumni records', 'Alumni'),
('Manage Users', 'manage_users', 'Can manage users', 'Users'),
('Manage Roles', 'manage_roles', 'Can manage roles and permissions', 'RBAC'),
('View Audit Logs', 'view_audit_logs', 'Can view audit logs', 'Audit'),
('Archive Data', 'archive_data', 'Can archive old data', 'Archive'),
('Restore Data', 'restore_data', 'Can restore archived data', 'Archive'),
('Manage Backups', 'manage_backups', 'Can manage backups', 'Backup'),
('View Analytics', 'view_analytics', 'Can view analytics', 'Analytics');

-- Insert default roles
INSERT OR IGNORE INTO roles (role_name, description, is_system_role) VALUES
('Admin', 'Full system access', 1),
('Teacher', 'Academic operations access', 1),
('Student', 'Personal records access', 1),
('Exam Coordinator', 'Exam and result management', 0),
('HOD', 'Department head access', 0);

-- ============================================
-- MIGRATION COMPLETE
-- ============================================
