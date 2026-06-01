"""
Intelligent Password Strength Checker - GUI Application Entry Point

This is the main entry point for the GUI version of the password strength checker.
It launches a modern graphical user interface using ttkbootstrap.

For the command-line version, run: python main_cli.py
"""

import sys
import os

# Ensure the UI module can be imported
try:
    from ui import launch_gui
except ImportError as e:
    print("❌ Error: Required modules not found.")
    print("Please install dependencies: pip install -r requirements.txt")
    print(f"\nDetails: {e}")
    sys.exit(1)


def main():
    """
    Main entry point for the GUI application.
    Launches the Password Strength Checker GUI window.
    """
    try:
        print("🚀 Launching Intelligent Password Strength Checker GUI...")
        print("📦 Loading ML model...")
        
        # Launch the GUI application
        launch_gui()
        
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user.")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
