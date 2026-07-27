from pathlib import Path
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "db.sqlite3"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "GlowCart AI Backend Running"}


@app.get("/recommend")
def recommend(skin: str):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, price
        FROM shop_product
        WHERE skin_type = ? OR skin_type = 'all'
    """, (skin.lower(),))

    rows = cursor.fetchall()

    conn.close()

    products = []

    for row in rows:
        products.append({
            "name": row[0],
            "price": float(row[1])
        })

    return {
        "skin": skin,
        "recommendations": products
    }
@app.get("/chat")
def chat(message: str):

    msg = message.lower()

    # Detect skin type
    if "oily" in msg:
        skin = "oily"

    elif "dry" in msg:
        skin = "dry"

    elif "all" in msg:
        skin = "all"

    else:
        return {
            "reply": "Please tell me your skin type (oily, dry or all)."
        }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, price
        FROM shop_product
        WHERE skin_type = ? OR skin_type = 'all'
    """, (skin,))

    rows = cursor.fetchall()

    conn.close()

    if len(rows) == 0:
        return {
            "reply": "Sorry, no products found."
        }

    reply = f"Recommended products for {skin} skin:\n\n"

    for product in rows:
        reply += f"• {product[0]} - ₹{product[1]}\n"

    return {
        "reply": reply
    }