# Test for the organizer logic
import os
import shutil
import tempfile
from lib.organizer.organizer import Organizer

def test_organize_and_revert():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create dummy files
        file1 = os.path.join(tmpdir, 'test1.txt')
        file2 = os.path.join(tmpdir, 'test2.jpg')
        with open(file1, 'w') as f:
            f.write('hello')
        with open(file2, 'w') as f:
            f.write('world')
        organizer = Organizer(tmpdir)
        files_moved = organizer.organize()
        assert len(files_moved) == 2
        # Check files moved
        for f in files_moved:
            assert os.path.exists(f.new_path)
        # Revert one file
        file_id = files_moved[0].id
        success, msg = organizer.revert(file_id)
        assert success
        assert os.path.exists(files_moved[0].original_path)
        print('Test passed!')

if __name__ == '__main__':
    test_organize_and_revert()
