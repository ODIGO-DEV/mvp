import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

from .base import UploadService


class LocalUploadService(UploadService):
    def __init__(self):
        # Avoid touching current_app at import time; defer to method calls
        pass

    def _ensure_upload_dir(self) -> str:
        upload_folder = current_app.config.get("UPLOAD_FOLDER")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder, exist_ok=True)
        return upload_folder

    def upload_file(self, file_storage):
        if not file_storage or not getattr(file_storage, "filename", ""):
            return False, ""

        upload_folder = self._ensure_upload_dir()

        # Generate a safe, semi-unique filename to avoid collisions
        original = secure_filename(file_storage.filename)
        name, ext = os.path.splitext(original)
        unique_name = f"{name}-{uuid.uuid4().hex[:8]}{ext}"
        file_path = os.path.join(upload_folder, unique_name)

        file_storage.save(file_path)
        # The app exposes uploads at /uploads/<filename>
        return True, f"/uploads/{unique_name}"

    def delete_file(self, url: str) -> bool:
        if not url:
            return False
        # Expect urls like /uploads/<filename>
        prefix = "/uploads/"
        if not url.startswith(prefix):
            return False
        filename = url[len(prefix) :]
        upload_folder = current_app.config.get("UPLOAD_FOLDER")
        file_path = os.path.join(upload_folder, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except OSError:
                return False
        return False
