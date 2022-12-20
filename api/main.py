from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from email_validator import validate_email, EmailNotValidError

from utils import get_disposable_emails, error_message
from schema import Email

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

disposable_emails = get_disposable_emails()

@app.get('/validate')
def validate(email: str):
    try:
        pydantic_validation = Email(email=email)
        email = pydantic_validation.email
    except ValidationError as e:
        return error_message("Invalid Format", status_code=status.HTTP_403_FORBIDDEN)

    email_domain = email.split('@')[-1]
    if email_domain in disposable_emails:
        return error_message("Unprocessable Entity", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    try:
        validation = validate_email(email)
        return {
            "data": validation.as_dict()
        }
    except EmailNotValidError as e:
        return error_message(str(e), status_code=status.HTTP_400_BAD_REQUEST)