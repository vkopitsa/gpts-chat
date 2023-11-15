from typing import List
from fastapi import Depends, APIRouter, Path, Request
from app.models import ListMessage, Message
from app.auth import get_api_key
from app.chat import Chat


router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    dependencies=[Depends(get_api_key)],
    responses={404: {"description": "Not found"}},
)


@router.post("/chats/{chat:str}/messages",
             summary="Post Message",
             description="This endpoint posts a new message to the chat.",
             response_description="Message posted successfully",
             response_model=List[ListMessage])
async def post_message(
    request: Request,
    message: Message,
    chat: str = Path(..., description="Name of the chat, use main as default"),
) -> list[ListMessage]:
    return await Chat.post_message(message, chat)


@router.get("/chats/{chat:str}/messages",
            summary="Get Messages",
            description="This endpoint retrieves messages from the chat.",
            response_description="Successful Response",
            response_model=List[ListMessage])
async def get_messages(request: Request, chat: str = Path(..., description="Name of the chat, use main as default")) -> list[ListMessage]:
    return await Chat.get_messages(chat)


@router.patch("/chats/{chat:str}/clear",
              summary="Clear Messages",
              description="This endpoint to clear messges from the chat.",
              response_description="Successful Response",
              response_model=List[ListMessage])
async def clear_messages(chat: str = Path(..., description="Name of the chat, use main as default")) -> list[ListMessage]:
    return await Chat.clear_messages(chat)
