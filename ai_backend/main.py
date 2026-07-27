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

    # Greetings
    if any(word in msg for word in ["hi", "hello", "hey"]):
        return {
            "reply":
            "👋 Hello! Welcome to GlowCart Beauty Store.\n\n"
            "I'm your AI Beauty Assistant 💜\n\n"
            "I can help you with:\n"
            "• Skincare\n"
            "• Makeup\n"
            "• Haircare\n"
            "• Perfumes\n"
            "• Product Recommendations\n\n"
            "How can I help you today?"
        }

    if "thank" in msg:
        return {
            "reply":
            "😊 You're welcome!\n\nHappy Shopping at GlowCart 💜"
        }

    if "bye" in msg:
        return {
            "reply":
            "👋 Goodbye!\nTake care and have a beautiful day 💜"
        }

    # Skin detection

    if "oily" in msg:
        skin = "oily"

    elif "dry" in msg:
        skin = "dry"

    elif "all" in msg or "normal" in msg:
        skin = "all"

    else:
        return {
            "reply":
            "😊 Please tell me your skin type.\n\n"
            "Example:\n"
            "• I have oily skin\n"
            "• My skin is dry\n"
            "• I have normal skin"
        }

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, price
        FROM shop_product
        WHERE skin_type=?
        LIMIT 5
    """,(skin,))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {
            "reply":"Sorry 😔 No products found."
        }

    reply = f"✨ Recommended products for {skin} skin:\n\n"

    for product in rows:

        reply += f"• {product[0]} - ₹{product[1]}\n"

    reply += "\n💜 Hope these products help!"

    return {
        "reply":reply
    }