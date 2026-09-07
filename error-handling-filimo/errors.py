class FilimoError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code



def error_body(code: str, message: str) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
        }
    }
