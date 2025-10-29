class UploadService:
    def upload_file(self, file_storage):
        """Upload a Werkzeug FileStorage and return (success, public_url)."""
        raise NotImplementedError

    def delete_file(self, url: str) -> bool:
        """Delete a file by its public URL. Return True on success."""
        raise NotImplementedError
