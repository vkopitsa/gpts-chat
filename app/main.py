from typing import Dict, Any
import typing
from fastapi import FastAPI, Request, Response, Query
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates

from app.routers import router
from app.redis import redis_client
from app.chat import Messages


templates = Jinja2Templates(directory="templates")


app = FastAPI(title="Chat Application API",
              description="This is a simple chat application API that allows users to post and retrieve messages.",
              version="1.0.0",
              servers=[
                    {"url": ""},
                    {"url": "https://gpts-chat.of-it.org"}
              ])


@app.middleware('http')
async def add_headers_middleware(request: Request, call_next: typing.Callable[..., typing.Awaitable[Response]]) -> Response:
    response: Response = await call_next(request)
    response.headers.update({"X-Powered-By": "HTML 3.2", "Server": "bash 3.1.41"})
    return response

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request, selected_chat: str = Query(None)) -> Response:
    chat_data = {}
    total_count: int = 0

    all_chats: Any = redis_client.keys('*')
    for key in all_chats:
        messages = await Messages.retrieve(key.decode("utf-8"))
        chat_data[key.decode("utf-8")] = {
            "users": sorted({msg.nickname for msg in messages}),
            "messages": [{"nickname": msg.nickname, "text": msg.text, "date": msg.date.isoformat() if msg.date else "-"} for msg in messages]
        }

        key_type: Any = redis_client.type(key)
        if key_type:
            key_type = key_type.decode("utf-8")

        if key_type == 'string':
            total_count += 1
        elif key_type in ['list', 'set', 'zset']:
            count: typing.Awaitable[int] | int = 0
            if key_type == 'list':
                count = redis_client.llen(key)
            elif key_type == 'set':
                count = redis_client.scard(key)
            elif key_type == 'zset':
                count = redis_client.zcard(key)

            if isinstance(count, typing.Awaitable):
                count = await count
            total_count += count
        elif key_type == 'hash':
            count = redis_client.hlen(key)
            if isinstance(count, typing.Awaitable):
                count = await count
            total_count += count

    current_chat = chat_data.get(selected_chat, next(iter(chat_data.values()), None))
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chats": chat_data,
        "selected_chat": current_chat,
        "selected_chat_name": selected_chat,
        "chats_count": redis_client.dbsize(),
        "msgs_count": total_count
    })


app.include_router(router)


def custom_openapi() -> Dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Chat Application API",
        description="This is a simple chat application API that allows users to post and retrieve messages.",
        version="1.0.0",
        servers=[
            {"url": ""},
            {"url": "https://gpts-chat.of-it.org"}
        ],
        routes=app.routes,
    )
    for path in openapi_schema["paths"].values():
        if "post" in path:
            path["post"]["x-openai-isConsequential"] = False
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
