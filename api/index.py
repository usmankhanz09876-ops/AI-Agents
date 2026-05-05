import os
import json
from datetime import date
from groq import Groq
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# In-memory store (resets on cold start — replace with a DB for persistence)
entries_store: list = []


class UserInput(BaseModel):
    text: str


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/add")
def add_entries(body: UserInput):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract budget entries from user input. "
                    "Return ONLY a JSON object with a single key 'entries' containing an array of objects with keys: "
                    "type (income/expense), category, amount (number), description."
                ),
            },
            {"role": "user", "content": body.text},
        ],
    )
    entries = json.loads(response.choices[0].message.content)["entries"]
    for e in entries:
        e["date"] = str(date.today())
        entries_store.append(e)
    return {"entries": entries}


@app.get("/analyze")
def analyze():
    if not entries_store:
        raise HTTPException(status_code=400, detail="No data yet. Add some income/expenses first.")
    summary = {"income": 0, "expenses": {}}
    for e in entries_store:
        if e["type"] == "income":
            summary["income"] += e["amount"]
        elif e["type"] == "expense":
            summary["expenses"][e["category"]] = summary["expenses"].get(e["category"], 0) + e["amount"]
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a personal finance advisor. "
                    "Analyze the budget summary and give concise, actionable savings tips. "
                    "Mention percentage breakdowns where relevant. Be direct and brief."
                ),
            },
            {"role": "user", "content": f"Budget summary: {json.dumps(summary)}"},
        ],
    )
    return {"advice": response.choices[0].message.content.strip(), "summary": summary}


@app.get("/entries")
def get_entries():
    return {"entries": entries_store}


app.mount("/static", StaticFiles(directory="static"), name="static")
