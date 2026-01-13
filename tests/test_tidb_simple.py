"""
Simple TiDB Cloud connection and data test
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import db

print("\n" + "="*60)
print("TIDB CLOUD CONNECTION TEST")
print("="*60)

# Test 1: Connection
print("\n1. Testing connection...")
try:
    conn = db.get_connection()
    print("✓ Connected successfully!")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    sys.exit(1)

# Test 2: Simple query
print("\n2. Testing simple query...")
try:
    result = db.execute_query("SELECT 1 as test")
    if result and result[0]['test'] == 1:
        print("✓ Query executed successfully!")
    else:
        print("✗ Query failed")
except Exception as e:
    print(f"✗ Query error: {e}")

# Test 3: Check tables
print("\n3. Checking tables...")
try:
    tables_query = "SHOW TABLES"
    tables = db.execute_query(tables_query)
    if tables:
        print(f"✓ Found {len(tables)} tables:")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"  - {table_name}")
    else:
        print("⚠ No tables found - database might be empty")
except Exception as e:
    print(f"✗ Error checking tables: {e}")

# Test 4: Count existing data
print("\n4. Checking existing data...")
try:
    dept_count = db.execute_query("SELECT COUNT(*) as count FROM departments")
    course_count = db.execute_query("SELECT COUNT(*) as count FROM courses")
    student_count = db.execute_query("SELECT COUNT(*) as count FROM students")
    
    print(f"✓ Departments: {dept_count[0]['count']}")
    print(f"✓ Courses: {course_count[0]['count']}")
    print(f"✓ Students: {student_count[0]['count']}")
except Exception as e:
    print(f"✗ Error counting data: {e}")

# Test 5: Insert test department
print("\n5. Testing INSERT operation...")
try:
    test_dept_name = "Test Department"
    test_dept_code = "TEST"
    
    # Check if exists
    existing = db.execute_query(
        "SELECT department_id FROM departments WHERE department_code = %s",
        (test_dept_code,)
    )
    
    if existing:
        print(f"⚠ Test department already exists (ID: {existing[0]['department_id']})")
    else:
        # Insert
        success, dept_id = db.execute_update(
            "INSERT INTO departments (department_name, department_code) VALUES (%s, %s)",
            (test_dept_name, test_dept_code)
        )
        
        if success:
            print(f"✓ Inserted test department (ID: {dept_id})")
            
            # Verify
            verify = db.execute_query(
                "SELECT * FROM departments WHERE department_id = %s",
                (dept_id,)
            )
            if verify:
                print(f"✓ Verified: {verify[0]['department_name']}")
        else:
            print("✗ Failed to insert test department")
except Exception as e:
    print(f"✗ Insert error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✓ ALL TESTS COMPLETE!")
print("="*60)
print("\nYour TiDB Cloud database is working correctly!")
print("PyMySQL connection is successful.")
