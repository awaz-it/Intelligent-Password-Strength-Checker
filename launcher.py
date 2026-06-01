"""
Launcher Script for Intelligent Password Strength Checker
Allows user to choose between GUI and CLI versions.
"""

import sys
import os


def print_banner():
    """Print application banner."""
    print("\n" + "="*70)
    print("🔐 INTELLIGENT PASSWORD STRENGTH CHECKER - LAUNCHER")
    print("="*70)
    print()


def show_menu():
    """Display version selection menu."""
    print("Choose your preferred version:\n")
    print("  1. 🪟 GUI Version (Modern Window Application)")
    print("     - Beautiful, professional interface")
    print("     - Visual progress bars and colors")
    print("     - Point-and-click operation")
    print("     - Recommended for most users\n")
    
    print("  2. 💻 CLI Version (Terminal-Based)")
    print("     - Command-line interface")
    print("     - Text-based operation")
    print("     - Lightweight and scriptable")
    print("     - Great for automation\n")
    
    print("  3. ❌ Exit\n")


def launch_gui():
    """Launch the GUI version."""
    print("\n🚀 Launching GUI version...")
    print("📦 Loading ML model...\n")
    try:
        from ui import launch_gui
        launch_gui()
    except ImportError as e:
        print("❌ Error: GUI dependencies not found.")
        print("Please install: pip install ttkbootstrap")
        print(f"\nDetails: {e}")
        input("\nPress Enter to return to menu...")


def launch_cli():
    """Launch the CLI version."""
    print("\n🚀 Launching CLI version...\n")
    try:
        # Import and run the CLI main function
        import main_cli
        main_cli.main()
    except ImportError as e:
        print("❌ Error: CLI module not found.")
        print(f"Details: {e}")
        input("\nPress Enter to return to menu...")
    except Exception as e:
        print(f"❌ Error launching CLI: {e}")
        input("\nPress Enter to return to menu...")


def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    try:
        import sklearn
    except ImportError:
        missing.append("scikit-learn")
    
    try:
        import pandas
    except ImportError:
        missing.append("pandas")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    if missing:
        print("⚠️  WARNING: Missing dependencies detected!")
        print(f"   Missing: {', '.join(missing)}")
        print("\n   Please install with: pip install -r requirements.txt\n")
        input("Press Enter to continue anyway...")
        return False
    
    return True


def main():
    """Main launcher function."""
    while True:
        print_banner()
        
        # Check dependencies on first iteration
        if not hasattr(main, 'checked_deps'):
            check_dependencies()
            main.checked_deps = True
        
        show_menu()
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                launch_gui()
                
            elif choice == '2':
                launch_cli()
                
            elif choice == '3':
                print("\n👋 Thank you for using Password Strength Checker!")
                print("💡 Remember: Use strong, unique passwords for each account.\n")
                sys.exit(0)
                
            else:
                print("\n⚠️  Invalid choice. Please enter 1, 2, or 3.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")


if __name__ == '__main__':
    main()
