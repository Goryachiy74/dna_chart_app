import os
import subprocess
from gui import main as gui_main


def open_charts_folder(folder):
    if not folder or not os.path.exists(folder):
        print("\n❌ No charts found. Please generate charts first.")
        return

    try:
        if os.name == 'nt':  # Windows
            os.startfile(folder)
        elif os.name == 'posix':  # MacOS or Linux
            subprocess.Popen(['xdg-open', folder])
        else:
            print("\n❌ Unsupported operating system.")
    except Exception as e:
        print(f"\n❌ Error opening folder: {e}")


def main():
    print("\n🔎 Select mode:")
    print("1. Generate Charts")
    print("2. Open Saved Charts")
    print("3. GUI Interface")

    choice = input("\nEnter choice (1, 2, or 3): ")

    if choice == '1':
        # Existing CLI chart generation logic
        pass
    elif choice == '2':
        folder = input("\nEnter output directory path: ").strip()
        open_charts_folder(folder)
    elif choice == '3':
        gui_main()
    else:
        print("\n❌ Invalid choice.")


if __name__ == "__main__":
    main()
