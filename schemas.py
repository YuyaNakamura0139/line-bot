from pydantic import BaseModel


class SuccessMsg(BaseModel):
    message: str


class Practice(BaseModel):
    id: str
    practice_period: int
    practice_name: str
    url: str


class PracticeBody(BaseModel):
    practice_period: int
    practice_name: str
    url: str
