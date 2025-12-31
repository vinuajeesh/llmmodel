import sys
import os

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def check_dependencies():
    """Checks if critical dependencies are installed."""
    required_modules = [
        ('customtkinter', 'customtkinter'),
        ('mss', 'mss'),
        ('psutil', 'psutil'),
        ('duckduckgo_search', 'duckduckgo-search'),
        ('llama_cpp', 'llama-cpp-python'),
        ('PIL', 'Pillow')
    ]

    missing = []
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)

    if missing:
        print("="*60)
        print("ERROR: Missing Dependencies")
        print("="*60)
        print(f"The following required packages are missing:\n")
        for pkg in missing:
            print(f" - {pkg}")
        print("\nPlease install them by running the following command in your terminal:\n")

        req_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'requirements.txt')
        print(f"    pip install -r \"{req_path}\"")
        print("="*60)

        # Pause so user can see the message if running from a double-click
        try:
            input("\nPress Enter to exit...")
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    check_dependencies()

    try:
        from ui.main_window import MainWindow
        app = MainWindow()
        app.mainloop()
    except ImportError as e:
        print(f"Critical Import Error: {e}")
        try:
            input("\nPress Enter to exit...")
        except:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        try:
            input("\nPress Enter to exit...")
        except:
            pass
        sys.exit(1)
