"""
Simple test to check imports
"""
print("Testing imports...")

try:
    print("1. Testing database...")
    from database.db_manager import db
    print("   ✓ Database OK")
    
    print("2. Testing config...")
    import config
    print("   ✓ Config OK")
    
    print("3. Testing security...")
    from utils.security import hash_password
    print("   ✓ Security OK")
    
    print("4. Testing validators...")
    from utils.validators import validate_name
    print("   ✓ Validators OK")
    
    print("5. Testing controllers...")
    from controllers.auth_controller import auth
    print("   ✓ Auth controller OK")
    
    print("\n✅ All imports successful!")
    print("\nNow testing PyQt5...")
    
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    print("✓ PyQt5 OK")
    
    print("\n✅ Ready to run main.py!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
