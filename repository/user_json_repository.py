import json

from filelock import FileLock

from repository.user_repository_interface import UserRepositoryInterface


class UserJsonRepository(UserRepositoryInterface):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock_path = f"{file_path}.lock"

    def _load(self) -> list[str]:
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save(self, data: list[str]):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def add(self, user_id: str):
        with FileLock(self.lock_path):
            users = self._load()
            if user_id not in users:
                users.append(user_id)
                self._save(users)

    def list(self) -> list[str]:
        with FileLock(self.lock_path):
            return self._load()

    def delete(self, user_id: str):
        with FileLock(self.lock_path):
            users = self._load()
            if user_id in users:
                users.remove(user_id)
                self._save(users)
