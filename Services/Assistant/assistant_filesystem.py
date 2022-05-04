import re
import unicodedata
from pathlib import Path
import os
import shutil
import pandas as pd


class AssistantFilesystem:

    @staticmethod
    def file_exist(path):
        my_file = Path(path)
        if my_file.is_file():
            # file exists
            return True
        return False

    @staticmethod
    def remove_all(path):
        folder = path
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
