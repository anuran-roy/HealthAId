from llms.openai import get_single_message
from fastapi import FastAPI
from typing import Any, Dict, List
from pydantic import BaseModel
from utils.pipeline import get_data
from data.scrapers import drugs_com
app = FastAPI(title="LLM Backend for FastAPI", description="LLM backend for FastAPI")


class MessageSchema(BaseModel):
    userID: str
    email: str
    msgs: List[Dict[str, Any]]
    sources: List[str]

def generate_prompt(data: str, query: str):
    data = "" if data is None else data
    query = "" if data is None else query
    prompt = """
You are supposed to be a medical question-answering bot. You are NOT supposed to answer anything other than the user's question, provided under the questions section.

You MUST answer from ONLY inside the Data Section.

You should follow the following examples of a good conversation. U means the User, and A means the Assistant. The conversation examples are:

```
U: I am having nausea late at nights. What should I do?
A: Hey, there are a wide variety of issues whose symptoms are nausea. Can you please tell me some more details/symptoms?
U: I am also having trouble breathing when I go to sleep.
A: Hey so, that seems like a stomach issue. Any more details?
U: I faint sometimes.
A: Hey, so that seems like an issue of Peptic Ulcer. You should visit a Gastroenterologist as soon as possible. A few things you can do right now are:
    - Take more rest and less stress
    - Go to sleep in time
    ...
```

Now given the example, you have to answer the user's question. The required Data section is:

  ```Data
  {data}
  ```

  ```Question
  {query}
  ```
    """
    return prompt.format(data=data, query=query)
def augment_data(extracted_messages: List[Dict], sources: List[str]):
    latest_message = extracted_messages[-1]["content"]
    total_len = sum([len(x["content"]) for x in extracted_messages])
    data = "\n".join([get_data(latest_message, source) for source in sources if source not in ["drugs_com"]])

    print("Would enter conditional block")
    if "drugs_com" in sources:
        print("We will scrape Drugs.com.")
        latest_data = drugs_com.get_data(latest_message)
        print("Data fetched from drugs.com = ", latest_data)
        data += "\n".join([f"```{key}\n{value}\n```" for key, value in latest_data.items()])

    print(data[:300])
    final_prompt = generate_prompt(data=data, query=latest_message)
    
    extracted_messages[-1]["content"] = final_prompt

    return extracted_messages

@app.post("/get_prompt")
def get_prompt(message_ob: MessageSchema):
    received_messages: List[Dict[str, Any]] = message_ob.msgs
    # print(received_messages)
    extracted_messages: List[Dict[str, Any]] = list(map(lambda msg: {"role": msg.get(
        "role", "user"), "content": msg["content"]}, received_messages))
    print(extracted_messages)
    result = get_single_message(messages=augment_data(extracted_messages, sources=message_ob.sources))
    print(result)
    return result
