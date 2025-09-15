class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def add(self, user_id):
        return self.user_repository.add(user_id)

    def list(self):
        return self.user_repository.list()

    def delete(self, user_id):
        return self.user_repository.delete(user_id)
