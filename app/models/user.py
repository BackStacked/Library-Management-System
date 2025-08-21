from uuid import uuid4

class User:
    def __init__(self, name: str, email: str, password: str, id: str | None = None, role: str = "user"):
        self.id = id or str(uuid4())   # use given id or generate new one
        self.name = name
        self.email = email.lower()
        self.password = password
        self.role = role.lower()  # default "user"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
        }

