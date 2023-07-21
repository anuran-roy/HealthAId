from typing import Any, Dict, List
from pydantic import BaseModel

from llms.openai import get_single_message
from fastapi import FastAPI

app = FastAPI(title="LLM Backend for FastAPI",
              description="LLM backend for FastAPI")


class MessageSchema(BaseModel):
    userID: str
    email: str
    msgs: List[Dict[str, Any]]


@app.post("/get_prompt")
def get_prompt(message_ob: MessageSchema):
    received_messages: List[Dict[str, Any]] = message_ob.msgs
    # print(received_messages)
    extracted_messages: List[Dict[str, Any]] = list(map(lambda msg: {"role": msg.get(
        "role", "user"), "content": msg["content"]}, received_messages))
    print(extracted_messages)
    return get_single_message(messages=extracted_messages[:1])
