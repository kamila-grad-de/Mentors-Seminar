import sqlite3
import os
from fastapi import Body, FastAPI, HTTPException
from typing import Optional

DB_PATH = "/app/data/todo.db"

app = FastAPI(title="Todo Service")


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


@app.on_event("startup")
def init_db():
    with get_conn() as conn:
        conn.execute(
            """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER NOT NULL DEFAULT 0
        )
        """
        )


@app.post("/items")
def create_item(item: dict = Body(...)):
    title = item["title"]
    description = item.get("description")
    completed = item.get("completed", False)
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO items (title, description, completed) VALUES (?, ?, ?)",
            (title, description, int(completed)),
        )
        return {
            "id": cur.lastrowid,
            "title": title,
            "description": description,
            "completed": completed,
        }


@app.get("/items")
def get_items():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, description, completed FROM items"
        ).fetchall()
        return [
            {"id": r[0], "title": r[1], "description": r[2], "completed": bool(r[3])}
            for r in rows
        ]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, title, description, completed FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()
        if not row:
            raise HTTPException(404)
        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": bool(row[3]),
        }


@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
):
    item = get_item(item_id)

    title = title if title is not None else item["title"]
    description = description if description is not None else item["description"]
    completed = completed if completed is not None else item["completed"]

    with get_conn() as conn:
        conn.execute(
            "UPDATE items SET title=?, description=?, completed=? WHERE id=?",
            (title, description, int(completed), item_id),
        )

    return {
        "id": item_id,
        "title": title,
        "description": description,
        "completed": completed,
    }


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
        if cur.rowcount == 0:
            raise HTTPException(404)
    return {"status": "deleted"}
