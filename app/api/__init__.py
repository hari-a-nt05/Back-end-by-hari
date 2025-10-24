from fastapi import APIRouter, Depends

from app.api import auth, candidate, candidateskill, config, jobpost, outlook, users

api_router = APIRouter()
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    jobpost.router,
    prefix="/jobposts",
    tags=["jobposts"],
    dependencies=[Depends(auth.get_current_user)],
)
api_router.include_router(
    candidate.router,
    prefix="/candidates",
    tags=["candidates"],
    dependencies=[Depends(auth.get_current_user)],
)
api_router.include_router(
    candidateskill.router,
    prefix="/candidateskills",
    tags=["candidateskills"],
    dependencies=[Depends(auth.get_current_user)],
)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_current_user)],
)
api_router.include_router(
    config.router,
    prefix="/config",
    tags=["config"],
    dependencies=[Depends(auth.get_current_user)],
)

api_router.include_router(
    outlook.router,
    prefix="/mail",
    tags=["mail"],
    dependencies=[Depends(auth.get_current_user)],
)
