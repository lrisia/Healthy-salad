class EnvExcept(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"EnvExcept: {self.message}"