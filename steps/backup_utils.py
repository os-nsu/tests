#steps/backup_utils.py

import os
import shutil
import pytest

def create_file_backup(file_path):
    if not os.path.exists(file_path):
        return None
    backup_path = file_path + ".bak"

    shutil.copy2(file_path, backup_path)

    os.remove(file_path)
    return backup_path

def restore_file_backup(file_path, backup_path):
    if os.path.exists(file_path):
        os.remove(file_path)

    if backup_path and os.path.exists(backup_path):
        shutil.move(backup_path, file_path)

class FileBackup:
    def __init__(self):
        self._backup_map = {}

    def backup(self, file_path):
        backup_path = create_file_backup(file_path)
        self._backup_map[file_path] = backup_path
        return backup_path

    def restore_all(self):
        for file_path, backup_path in self._backup_map.items():
            restore_file_backup(file_path, backup_path)
        self._backup_map.clear()
