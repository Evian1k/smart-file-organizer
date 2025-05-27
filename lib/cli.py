# Command-line interface for Smart File Organizer
import sys
import os
from lib.organizer.organizer import Organizer

def print_menu():
    print("\n==============================")
    print("  📁 Smart File Organizer CLI  ")
    print("==============================")
    print("[1] Organize files in a directory")
    print("[2] View history of moved files")
    print("[3] Revert a file move by ID")
    print("[4] Create a new directory to organize")
    print("[5] Remove an empty directory")
    print("[6] Show existing directories (from DB)")
    print("[7] Exit")

def main():
    while True:
        print_menu()
        command = input("\nSelect an option [1-7]: ").strip()
        if command == '1':
            directory = input("Enter the directory to organize: ").strip()
            if not os.path.isdir(directory):
                print("❌ Directory does not exist. Please try again or create it first.")
                continue
            organizer = Organizer(directory)
            files_moved = organizer.organize()
            if files_moved:
                print(f"✅ Moved {len(files_moved)} files:")
                for f in files_moved:
                    print(f"  - {f.name} → {f.new_path}")
            else:
                print("No files were moved. The directory may already be organized or is empty.")
        elif command == '2':
            organizer = Organizer('.')
            files = organizer.history()
            if not files:
                print("No files have been moved yet.")
            else:
                print("\nMoved Files History:")
                print("ID | Name | Original Path | New Path | File Type | Date Moved")
                print("-" * 80)
                for f in files:
                    print(f"{f.id} | {f.name} | {f.original_path} | {f.new_path} | {f.file_type} | {f.date_moved.strftime('%Y-%m-%d %H:%M:%S')}")
        elif command == '3':
            file_id = input("Enter the file ID to revert: ").strip()
            if not file_id.isdigit():
                print("❌ Invalid file ID. Please enter a numeric value.")
                continue
            file_id = int(file_id)
            organizer = Organizer('.')
            success, msg = organizer.revert(file_id)
            if success:
                print(f"✅ {msg}")
            else:
                print(f"❌ {msg}")
        elif command == '4':
            new_dir = input("Enter the path for the new directory: ").strip()
            try:
                os.makedirs(new_dir, exist_ok=False)
                # Store in DB
                from lib.db.connection import SessionLocal
                from lib.db.models import Folder
                session = SessionLocal()
                folder_name = os.path.basename(new_dir)
                if not session.query(Folder).filter_by(name=folder_name).first():
                    folder = Folder(name=folder_name)
                    session.add(folder)
                    session.commit()
                    print(f"✅ Directory '{new_dir}' created and stored in database.")
                else:
                    print(f"⚠️ Directory '{folder_name}' already exists in database.")
                session.close()
            except FileExistsError:
                print(f"❌ Directory '{new_dir}' already exists.")
            except Exception as e:
                print(f"❌ Error creating directory: {e}")
        elif command == '5':
            del_dir = input("Enter the path of the directory to remove: ").strip()
            if not os.path.isdir(del_dir):
                print("❌ Directory does not exist.")
                continue
            if os.listdir(del_dir):
                print("❌ Directory is not empty. Only empty directories can be removed.")
                continue
            try:
                os.rmdir(del_dir)
                # Remove from DB
                from lib.db.connection import SessionLocal
                from lib.db.models import Folder
                session = SessionLocal()
                folder_name = os.path.basename(del_dir)
                folder = session.query(Folder).filter_by(name=folder_name).first()
                if folder:
                    session.delete(folder)
                    session.commit()
                    print(f"✅ Directory '{del_dir}' removed from filesystem and database.")
                else:
                    print(f"⚠️ Directory '{folder_name}' not found in database.")
                session.close()
            except Exception as e:
                print(f"❌ Error removing directory: {e}")
        elif command == '6':
            # Show existing directories from DB
            from lib.db.connection import SessionLocal
            from lib.db.models import Folder
            session = SessionLocal()
            folders = session.query(Folder).all()
            if not folders:
                print("No directories found in the database.")
            else:
                print("\nDirectories stored in the database:")
                for folder in folders:
                    print(f"- {folder.name}")
            session.close()
        elif command == '7':
            print("👋 Goodbye! Thanks for using Smart File Organizer.")
            sys.exit(0)
        else:
            print("❌ Unknown option. Please select a valid option [1-7].")

if __name__ == '__main__':
    main()
