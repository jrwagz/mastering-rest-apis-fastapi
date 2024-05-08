from fastapi import APIRouter, HTTPException

from socialapi.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)

router = APIRouter()


post_table = {}
comment_table = {}


@router.post("/post", status_code=201)
async def create_post(post: UserPostIn) -> UserPost:
    data = post.model_dump()
    last_record_id = len(post_table)
    new_post = UserPost(**data, id=last_record_id)
    post_table[last_record_id] = new_post
    return new_post


@router.get("/post")
async def list_posts() -> list[UserPost]:
    return list(post_table.values())


def find_post(post_id: int) -> UserPost:
    post = post_table.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found.")
    return post


@router.post("/comment", status_code=201)
async def create_comment(comment: CommentIn) -> Comment:
    find_post(post_id=comment.post_id)
    data = comment.model_dump()
    last_record_id = len(comment_table)
    new_comment = Comment(**data, id=last_record_id)
    comment_table[last_record_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment")
async def get_post_comments(post_id: int) -> list[Comment]:
    find_post(post_id=post_id)
    post_comments = [c for c in comment_table.values() if c.post_id == post_id]
    return post_comments


@router.get("/post/{post_id}")
async def get_post_with_comments(post_id: int) -> UserPostWithComments:
    post = find_post(post_id=post_id)
    return UserPostWithComments(
        post=post,
        comments=await get_post_comments(post_id=post_id),
    )
