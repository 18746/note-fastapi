from pydantic import Field

def NameStrDef(default: str | None = None):
    return Field(default=default, max_length=50, min_length=1)

def PhoneStrDef(default: str | None = None):
    return Field(default=default, pattern="^1[3456789]\d{9}$")

def EmailStrDef(default: str | None = None):
    return Field(default=default, pattern="^$|^([A-Za-z0-9\\u4e00-\\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z]{2,8})+)$")

def PasswordStrDef(default: str | None = None):
    return Field(default=default, min_length=8)

def TokenStrDef(default: str = None):
    return Field(default=default, min_length=6)

def TimeLimitIntDef(default: int | None = 30):
    return Field(default=default, ge=0)


