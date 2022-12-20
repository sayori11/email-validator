from fastapi import status

class CustomException(Exception):
    def __init__(self, message: str, code: int=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.code =code