from fastapi import FastAPI

from routers import route_linebot, route_practice

app = FastAPI()
app.include_router(route_linebot.router)
app.include_router(route_practice.router)


@app.get("/")
def root():
    return {"message": "Welcome to Fast API"}
