
class UsersRepository:
    users_db = {}

    @classmethod
    def add_user(cls, email: str, full_name: str, password: str, photo: str = None):
        if email in cls.users_db:
            return False  # Пользователь уже существует
        cls.users_db[email] = {
            "full_name": full_name,
            "password": password,
            "photo": photo
        }
        return True

    @classmethod
    def get_user(cls, email: str):
        return cls.users_db.get(email)
