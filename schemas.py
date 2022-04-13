from pydantic import BaseModel


class SuccessMsg(BaseModel):
    message: str


class Practice(BaseModel):
    id: str
    practice_id: int
    practice_name: str
    url: str


class PracticeBody(BaseModel):
    practice_id: int
    practice_name: str
    url: str
