from typing import Any
from pydantic import EmailStr, ValidationError
import re

def validate_email(email: str) -> bool:
    try:
        EmailStr.validate(email)
        return True
    except ValidationError:
        return False

def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid" 