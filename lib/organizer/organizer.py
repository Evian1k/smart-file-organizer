# File organization logic
import os
from datetime import datetime
from lib.db.connection import SessionLocal
from lib.db.models import File, Folder, UserAction
from lib.utils.file_utils import get_file_type, move_file

class Organizer:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.session = SessionLocal()

    def organize(self):
        files_moved = []
        for entry in os.listdir(self.base_dir):
            full_path = os.path.join(self.base_dir, entry)
            if os.path.isfile(full_path):
                file_type = get_file_type(full_path)
                folder = self.session.query(Folder).filter_by(name=file_type).first()
                if not folder:
                    folder = Folder(name=file_type)
                    self.session.add(folder)
                    self.session.commit()
                new_folder_path = os.path.join(self.base_dir, file_type)
                new_path = os.path.join(new_folder_path, entry)
                move_file(full_path, new_path)
                file_record = File(
                    name=entry,
                    original_path=full_path,
                    new_path=new_path,
                    file_type=file_type,
                    date_moved=datetime.now(),
                    folder=folder
                )
                self.session.add(file_record)
                files_moved.append(file_record)
        if files_moved:
            self.session.commit()
            action = UserAction(
                action_type='organize',
                timestamp=datetime.now(),
                description=f"Organized {len(files_moved)} files in {self.base_dir}"
            )
            self.session.add(action)
            self.session.commit()
        self.session.close()
        return files_moved

    def revert(self, file_id):
        file_record = self.session.query(File).filter_by(id=file_id).first()
        if not file_record:
            self.session.close()
            return False, 'File record not found.'
        if not os.path.exists(file_record.new_path):
            self.session.close()
            return False, 'File not found at new location.'
        move_file(file_record.new_path, file_record.original_path)
        action = UserAction(
            action_type='revert',
            timestamp=datetime.now(),
            description=f"Reverted file {file_record.name} to {file_record.original_path}"
        )
        self.session.add(action)
        self.session.delete(file_record)
        self.session.commit()
        self.session.close()
        return True, 'File reverted.'

    def history(self):
        files = self.session.query(File).all()
        self.session.close()
        return files
