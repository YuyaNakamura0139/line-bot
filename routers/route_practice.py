from fastapi import APIRouter
from fastapi import Response, HTTPException
from fastapi.encoders import jsonable_encoder

from starlette.status import HTTP_201_CREATED

from typing import List

from schemas import Practice, PracticeBody, SuccessMsg

from db.db_practice_menu import (
    db_get_practice_menus,
    db_create_practice_menu,
    db_delete_practice_menu,
    db_update_practice_menu,
)

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/practice", response_model=List[Practice])
def get_practice_menus():
    res = db_get_practice_menus()
    return res


@router.post("/practice", response_model=Practice)
def create_practice(response: Response, data: PracticeBody):
    practice = jsonable_encoder(data)
    res = db_create_practice_menu(practice)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(status_code=404, detail="Create practice menu failed")


@router.put("/practice/{id}", response_model=Practice)
def update_todo(id: str, data: PracticeBody):
    todo = jsonable_encoder(data)
    res = db_update_practice_menu(id, todo)
    if res:
        return res
    raise HTTPException(status_code=404, detail="Update task failed")


@router.delete("/practice/{id}", response_model=SuccessMsg)
def delete_todo(id: str):
    res = db_delete_practice_menu(id)
    if res:
        return {"message": "Successfully deleted"}
    raise HTTPException(status_code=404, detail="Delete task failed")
