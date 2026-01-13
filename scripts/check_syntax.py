import compileall
import os
import sys

def check_syntax(directory):
    print(f"Checking syntax in {directory}...")
    success = compileall.compile_dir(directory, force=True, quiet=1)
    if success:
        print("No syntax errors found.")
    else:
        print("Syntax errors found!")

if __name__ == "__main__":
    check_syntax(os.getcwd())
