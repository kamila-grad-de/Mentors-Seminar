import sqlite3
import os
import random
import string
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import RedirectResponse

DB_PATH = "/app/data/shorturl.db"

app = FastAPI(title="Short URL Service")


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def gen_id(n=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


@app.on_event("startup")
def init_db():
    with get_conn() as conn:
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS urls (
            short_id TEXT PRIMARY KEY,
            full_url TEXT NOT NULL
        )
        """
        )


@app.post("/shorten")
def shorten(data: dict = Body(...)):
    url = data["url"]
    short_id = gen_id()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO urls (short_id, full_url) VALUES (?, ?)",
            (short_id, url),
        )
    return {"short_url": f"/{short_id}"}


@app.get("/{short_id}")
def redirect(short_id: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT full_url FROM urls WHERE short_id = ?",
            (short_id,),
        ).fetchone()
        if not row:
            raise HTTPException(404)
        return RedirectResponse(row[0])


@app.get("/stats/{short_id}")
def stats(short_id: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT short_id, full_url FROM urls WHERE short_id = ?",
            (short_id,),
        ).fetchone()
        if not row:
            raise HTTPException(404)
        return {"short_id": row[0], "full_url": row[1]}
