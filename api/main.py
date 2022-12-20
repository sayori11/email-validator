from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from email_validator import validate_email, EmailNotValidError

from utils import get_disposable_emails
from schema import Email
from exceptions import CustomException

app = FastAPI(
    title="Email validator",
    description="API for validating emails",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.exception_handler(CustomException)
async def exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={
            "error": {
                "message": exc.message,
                "code": exc.code
            }
        },
    )

disposable_emails = get_disposable_emails()

@app.get('/validate')
def validate(email: str):
    try:
        pydantic_validation = Email(email=email)
        email = pydantic_validation.email
    except ValidationError as e:
        raise CustomException("Invalid Format", code=status.HTTP_403_FORBIDDEN)

    email_domain = email.split('@')[-1]
    if email_domain in disposable_emails:
        raise CustomException("Unprocessable Entity", code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    try:
        validation = validate_email(email)
        return {
            "data": validation.as_dict()
        }
    except EmailNotValidError as e:
        raise CustomException(str(e),code=status.HTTP_400_BAD_REQUEST)