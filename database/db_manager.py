"""
Database Manager - Singleton class for managing database connections and operations
Supports both SQLite (default) and MySQL (configured via config.json)
"""
import os
import shutil
from datetime import datetime
from typing import Optional, List, Tuple, Any
import config
from utils.resource_helper import resource_path

# Import database drivers based on configuration
if config.USE_MYSQL:
    import pymysql
    pymysql.install_as_MySQLdb()  # Make it compatible with MySQLdb interface
else:
    import sqlite3


class DatabaseManager:
    """Singleton Database Manager for SQLite and MySQL operations"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database connection"""
        if self._connection is None:
            self.connect()
    
    def connect(self):
        """Establish database connection (MySQL or SQLite based on config)"""
        try:
            if config.USE_MYSQL:
                self._connect_mysql()
            else:
                self._connect_sqlite()
        except Exception as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    def _connect_mysql(self):
        """Connect to MySQL database"""
        try:
            self._connection = pymysql.connect(
                host=config.MYSQL_HOST,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                port=config.MYSQL_PORT,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,  # Return results as dictionaries
                ssl={'ssl': True} if config.MYSQL_PORT == 4000 else None  # Enable SSL for TiDB
            )
            print(f"✓ MySQL connected: {config.MYSQL_USER}@{config.MYSQL_HOST}/{config.MYSQL_DATABASE}")
            print("✓ Multi-PC support enabled")
        except Exception as e:
            print(f"✗ MySQL connection error: {e}")
            print(f"  Host: {config.MYSQL_HOST}")
            print(f"  User: {config.MYSQL_USER}")
            print(f"  Database: {config.MYSQL_DATABASE}")
            raise
    
    def _connect_sqlite(self):
        """Connect to SQLite database (fallback)"""
        self._connection = sqlite3.connect(
            config.DATABASE_PATH,
            check_same_thread=False,
            timeout=30.0,
            isolation_level='DEFERRED'
        )
        self._connection.row_factory = sqlite3.Row
        
        # Enable Write-Ahead Logging (WAL) mode for better concurrency
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._connection.execute("PRAGMA busy_timeout = 30000")
        self._connection.execute("PRAGMA synchronous = NORMAL")
        self._connection.execute("PRAGMA cache_size = -10000")
        
        print(f"✓ SQLite connected: {config.DATABASE_PATH}")
        print("✓ WAL mode enabled for better concurrency")
    
    def get_connection(self):
        """Get the database connection, reconnecting if necessary"""
        if self._connection is None:
            self.connect()
        
        # Check if connection is still alive (MySQL)
        if config.USE_MYSQL:
            try:
                self._connection.ping(reconnect=True)
            except:
                print("⚠ MySQL connection lost, reconnecting...")
                self.connect()
        
        return self._connection
    
    def _convert_placeholders(self, query: str) -> str:
        """Convert SQLite placeholders (?) to MySQL placeholders (%s) if needed"""
        if config.USE_MYSQL and '?' in query:
            # Simple replacement - works for most cases
            return query.replace('?', '%s')
        return query
    
    def initialize_schema(self):
        """Initialize database schema from SQL file"""
        try:
            schema_path = resource_path(os.path.join('database', 'schema.sql'))
            
            print(f"Loading schema from: {schema_path}")
            
            if not os.path.exists(schema_path):
                print(f"✗ Schema file not found at: {schema_path}")
                return False
                
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if config.USE_MYSQL:
                # Execute statements one by one for MySQL
                statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
                for statement in statements:
                    if statement:
                        cursor.execute(statement)
            else:
                cursor.executescript(schema_sql)
            
            conn.commit()
            print("✓ Database schema initialized successfully")
            return True
        except Exception as e:
            print(f"✗ Schema initialization error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[dict]]:
        """
        Execute a SELECT query and return results as list of dictionaries
        
        Args:
            query: SQL query string (can use ? placeholders, will auto-convert for MySQL)
            params: Query parameters (for parameterized queries)
        
        Returns:
            List of dictionaries or None on error
        """
        try:
            query = self._convert_placeholders(query)
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if config.USE_MYSQL:
                # PyMySQL with DictCursor returns dictionaries automatically
                rows = cursor.fetchall()
                # Convert Decimal to float for compatibility
                result = []
                for row in rows:
                    row_dict = {}
                    for col, val in row.items():
                        # Convert Decimal to float
                        if val is not None and type(val).__name__ == 'Decimal':
                            row_dict[col] = float(val)
                        else:
                            row_dict[col] = val
                    result.append(row_dict)
                return result
            else:
                # SQLite with Row factory
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"✗ Query execution error: {e}")
            print(f"  Query: {query}")
            print(f"  Params: {params}")
            import traceback
            traceback.print_exc()
            return None
    
    def execute_update(self, query: str, params: tuple = ()) -> Tuple[bool, int]:
        """
        Execute an INSERT, UPDATE, or DELETE query
        
        Args:
            query: SQL query string (can use ? placeholders, will auto-convert for MySQL)
            params: Query parameters
        
        Returns:
            Tuple of (success: bool, last_row_id or rows_affected: int)
        """
        try:
            query = self._convert_placeholders(query)
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
            # Return last row ID for INSERT, rows affected for UPDATE/DELETE
            if query.strip().upper().startswith('INSERT'):
                if config.USE_MYSQL:
                    return True, cursor.lastrowid
                else:
                    return True, cursor.lastrowid
            else:
                return True, cursor.rowcount
        except Exception as e:
            conn = self.get_connection()
            conn.rollback()
            print(f"✗ Update execution error: {e}")
            print(f"  Query: {query}")
            print(f"  Params: {params}")
            import traceback
            traceback.print_exc()
            return False, 0
    
    def execute_many(self, query: str, params_list: List[tuple]) -> Tuple[bool, int]:
        """
        Execute multiple queries with different parameters (bulk insert/update)
        
        Args:
            query: SQL query string (can use ? placeholders, will auto-convert for MySQL)
            params_list: List of parameter tuples
        
        Returns:
            Tuple of (success: bool, rows_affected: int)
        """
        try:
            query = self._convert_placeholders(query)
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return True, cursor.rowcount
        except Exception as e:
            conn = self.get_connection()
            conn.rollback()
            print(f"✗ Bulk execution error: {e}")
            import traceback
            traceback.print_exc()
            return False, 0
    
    def begin_transaction(self):
        """Begin a transaction"""
        conn = self.get_connection()
        if config.USE_MYSQL:
            conn.start_transaction()
        else:
            conn.execute("BEGIN TRANSACTION")
    
    def commit(self):
        """Commit current transaction"""
        conn = self.get_connection()
        conn.commit()
    
    def rollback(self):
        """Rollback current transaction"""
        conn = self.get_connection()
        conn.rollback()
    
    def backup_database(self, backup_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        Create a backup of the database
        Note: For MySQL, this creates a SQL dump. For SQLite, copies the file.
        
        Args:
            backup_path: Optional custom backup path
        
        Returns:
            Tuple of (success: bool, backup_file_path: str)
        """
        try:
            if config.USE_MYSQL:
                return self._backup_mysql(backup_path)
            else:
                return self._backup_sqlite(backup_path)
        except Exception as e:
            print(f"✗ Backup error: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)
    
    def _backup_mysql(self, backup_path: Optional[str] = None) -> Tuple[bool, str]:
        """Backup MySQL database using mysqldump"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"exam_system_backup_{timestamp}.sql"
            backup_path = os.path.join(config.BACKUP_DIR, backup_filename)
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Use mysqldump command
        import subprocess
        cmd = [
            'mysqldump',
            '-h', config.MYSQL_HOST,
            '-u', config.MYSQL_USER,
            f'-p{config.MYSQL_PASSWORD}',
            config.MYSQL_DATABASE,
            '--result-file=' + backup_path
        ]
        
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ MySQL backup created: {backup_path}")
                return True, backup_path
            else:
                print(f"✗ MySQL backup failed: {result.stderr}")
                return False, result.stderr
        except FileNotFoundError:
            # mysqldump not found in PATH
            msg = "mysqldump not found. Install MySQL client tools or add MySQL bin directory to PATH"
            print(f"⚠ {msg}")
            return False, msg
        except Exception as e:
            print(f"✗ Backup error: {e}")
            return False, str(e)
    
    def _backup_sqlite(self, backup_path: Optional[str] = None) -> Tuple[bool, str]:
        """Backup SQLite database"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"exam_system_backup_{timestamp}.db"
            backup_path = os.path.join(config.BACKUP_DIR, backup_filename)
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        conn = self.get_connection()
        backup_conn = sqlite3.connect(backup_path)
        
        with backup_conn:
            conn.backup(backup_conn, pages=100, progress=self._backup_progress)
        
        backup_conn.close()
        
        # Verify backup integrity
        verify_conn = sqlite3.connect(backup_path)
        verify_conn.execute("PRAGMA integrity_check")
        verify_conn.close()
        
        print(f"✓ SQLite backup created: {backup_path}")
        return True, backup_path
    
    def _backup_progress(self, status, remaining, total):
        """Progress callback for backup operation"""
        if remaining == 0:
            print(f"✓ Backup complete: {total} pages copied")
    
    def restore_database(self, backup_path: str) -> bool:
        """
        Restore database from a backup file
        Note: Only works for SQLite backups
        
        Args:
            backup_path: Path to backup file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if config.USE_MYSQL:
                print("⚠ Restore not implemented for MySQL yet. Please use MySQL Workbench.")
                return False
            
            if not os.path.exists(backup_path):
                print(f"✗ Backup file not found: {backup_path}")
                return False
            
            # Close current connection
            self.close_connection()
            
            # Copy backup file to database location
            shutil.copy2(backup_path, config.DATABASE_PATH)
            
            # Reconnect
            self.connect()
            
            print(f"✓ Database restored from: {backup_path}")
            return True
        except Exception as e:
            print(f"✗ Restore error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database"""
        try:
            if config.USE_MYSQL:
                query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?"
                result = self.execute_query(query, (config.MYSQL_DATABASE, table_name))
                return result[0]['COUNT(*)'] > 0 if result else False
            else:
                query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
                result = self.execute_query(query, (table_name,))
                return len(result) > 0 if result else False
        except Exception:
            return False


# Global database instance
db = DatabaseManager()
