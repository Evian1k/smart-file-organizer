# Smart File Organizer CLI App

## Overview

Smart File Organizer is a command-line tool that helps you declutter your folders by automatically organizing files into subfolders based on their type (e.g., Images, Documents, Videos, etc.). It tracks all file moves in a database, allowing you to view history and revert changes if needed. You can also manage directories directly from the CLI.

---

## Features

- **Organize Files by Type:** Move files into subfolders (e.g., /Images, /Documents, /Videos, etc.)
- **Track Moved Files:** Store filename, original path, new path, file type, and date moved in a database
- **View History:** See a history of all moved files
- **Revert Moves:** Restore files to their original location by file ID
- **Manage Directories:** Create, remove, and list directories from the CLI

---

## Technologies Used

- Python 3
- SQLAlchemy ORM (SQLite backend)
- Pipenv for dependency management
- OS & shutil for file system operations

---

## Setup Instructions

1. **Clone the repository**

2. **Install dependencies**

   ```bash
   pipenv install
   ```

3. **Initialize the database**

   ```bash
   pipenv run python scripts/setup_db.py
   ```

4. **Run the CLI app**

   ```bash
   pipenv run python -m lib.cli
   ```

---

## Usage

When you run the CLI, you'll see a menu like this:

```
==============================
  📁 Smart File Organizer CLI  
==============================
[1] Organize files in a directory
[2] View history of moved files
[3] Revert a file move by ID
[4] Create a new directory to organize
[5] Remove an empty directory
[6] Show existing directories (from DB)
[7] Exit
```

### Example Workflow

1. **Create a directory:**
   - Choose option 4 and enter the path for your new directory.
2. **Organize files:**
   - Choose option 1 and enter the path of the directory you want to organize.
3. **View history:**
   - Choose option 2 to see all files that have been moved.
4. **Revert a move:**
   - Choose option 3 and enter the file ID to move a file back to its original location.
5. **Manage directories:**
   - Use options 4, 5, and 6 to create, remove, or list directories.

---

## Testing

To run the included tests:

```bash
pipenv run python tests/test_organizer.py
```

---

## Notes

- Only empty directories can be removed from the CLI.
- All actions are tracked in the database for auditing and undo purposes.
- The app is cross-platform and works on Linux, macOS, and Windows.

---

## License

MIT License