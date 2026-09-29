class DomainError(Exception):
    def __init__(self, message: str, status: int = 400, code: str = "domain"):
        self.message = message
        self.status = status
        self.code = code
class Unauthorized(DomainError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401, "unauthorized")
class NotFound(DomainError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, 404, "not_found")
class BudgetExceeded(DomainError):
    def __init__(self, message: str = "Token budget exceeded"):
        super().__init__(message, 429, "budget")
