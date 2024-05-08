from fastapi import FastAPI

from socialapi.models.post import UserPost, UserPostIn

app = FastAPI()


post_table = {}


@app.post("/post")
async def create_post(post: UserPostIn) -> UserPost:
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = UserPost(**data, id=last_record_id)
    post_table[last_record_id] = new_post
    return new_post


@app.get("/post")
async def list_posts() -> list[UserPost]:
    return list(post_table.values())
