import os
from werkzeug.utils import secure_filename
from flask import current_app

from .base import UploadService


class LocalUploadService(UploadService):
    def __init__(self):
        self.upload_folder = current_app.config.get("UPLOAD_FOLDER")
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def upload_file(self, file_storage):
        if file_storage:
            filename = secure_filename(file_storage.filename)
            file_path = os.path.join(self.upload_folder, filename)
            file_storage.save(file_path)
            return (
                True,
                f"/uploads/{filename}",
            )  # Return a URL relative to static folder
        return False, ""
