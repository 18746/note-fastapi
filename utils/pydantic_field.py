from pydantic import Field

def NameStrDef(default: str | None = None):
    return Field(default=default, max_length=50, min_length=1)

def PhoneStrDef(default: str | None = None):
    return Field(default=default, pattern="^1[3456789]\d{9}$")

def EmailStrDef(default: str | None = None):
    return Field(default=default, pattern="^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$")

def PasswordStrDef(default: str | None = None):
    return Field(default=default, min_length=8)

def TokenStrDef(default: str = None):
    return Field(default=default, min_length=6)

def TimeLimitIntDef(default: int | None = 30):
    return Field(default=default, ge=0)


