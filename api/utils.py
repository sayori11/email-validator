import json
from fastapi.responses import JSONResponse
from fastapi import status

def get_disposable_emails():
    with open('disposable-emails.json', 'r') as f:
        emails = json.loads(f.read())
    return emails

def error_message(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
    return JSONResponse(
        {   
            "error": {
                "message": message,
                "code": status_code
            }
        }, status_code=status_code
    )