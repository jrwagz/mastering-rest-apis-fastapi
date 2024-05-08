from fastapi import FastAPI

from socialapi.routers.post import router as router_post

app = FastAPI()

app.include_router(router=router_post)
