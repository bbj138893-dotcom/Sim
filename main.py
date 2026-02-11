import os
import telebot
import requests
from telebot import types

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")   # Railway Variable
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

API_URL = "https://howler-database-api.vercel.app/api/lookup?phone="


# ===== INLINE BUTTONS =====
def main_buttons():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📢 Channel", url="https://t.me/ZAMINTRICKS"),
        types.InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/SIGMAXZAMIN")
    )
    kb.add(
        types.InlineKeyboardButton("ℹ️ Disclaimer", callback_data="disclaimer"),
        types.InlineKeyboardButton("🔄 New Search", callback_data="new_search")
    )
    return kb


# ===== START =====
@bot.message_handler(commands=["start"])
def start(message):
    text = (
        "🚀 <b>WELCOME TO SIM DATABASE BOT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "✨ <b>FEATURES</b>\n"
        "➤ SIM Owner Lookup\n"
        "➤ Network Information\n"
        "➤ Fast API Response\n"
        "➤ 24/7 Online\n\n"
        "⚡ <b>HOW TO USE</b>\n"
        "➤ Send phone number\n"
        "➤ Example: <code>03012345678</code>\n\n"
        "👇 <b>USE BUTTONS BELOW</b>"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_buttons())


# ===== DISCLAIMER =====
@bot.callback_query_handler(func=lambda c: c.data == "disclaimer")
def disclaimer(call):
    text = (
        "📢 <b>DISCLAIMER</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "➤ Educational & testing purposes only\n"
        "➤ Any misuse is strictly prohibited\n"
        "➤ User is responsible for usage\n"
        "➤ No data is stored\n\n"
        "⚠️ <b>USE RESPONSIBLY</b>"
    )
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=main_buttons()
    )


# ===== NEW SEARCH =====
@bot.callback_query_handler(func=lambda c: c.data == "new_search")
def new_search(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "📱 <b>Send phone number</b>\nExample: <code>03012345678</code>",
        reply_markup=main_buttons()
    )


# ===== LOOKUP =====
@bot.message_handler(func=lambda m: m.text and m.text.isdigit())
def lookup(message):
    phone = message.text.strip()

    if not phone.startswith("03") or len(phone) < 10:
        bot.reply_to(
            message,
            "❌ <b>Invalid number format</b>\nUse: <code>03XXXXXXXXX</code>",
            reply_markup=main_buttons()
        )
        return

    bot.reply_to(message, "🔍 <b>Searching database...</b>")

    try:
        r = requests.get(API_URL + phone, timeout=15)
        data = r.json()

        if not data:
            bot.send_message(
                message.chat.id,
                "❌ <b>No record found</b>",
                reply_markup=main_buttons()
            )
            return

        result = (
            "📊 <b>SIM DATABASE RESULT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 <b>Number:</b> <code>{phone}</code>\n"
            f"👤 <b>Name:</b> {data.get('name','N/A')}\n"
            f"🆔 <b>CNIC:</b> {data.get('cnic','N/A')}\n"
            f"📡 <b>Network:</b> {data.get('network','N/A')}\n"
            f"📍 <b>Address:</b> {data.get('address','N/A')}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "👨‍💻 <b>Developer:</b> @SIGMAXZAMIN\n"
            "📢 <b>Channel:</b> @ZAMINTRICKS"
        )

        bot.send_message(message.chat.id, result, reply_markup=main_buttons())

    except Exception:
        bot.send_message(
            message.chat.id,
            "⚠️ <b>API Error</b>\nTry again later.",
            reply_markup=main_buttons()
        )


# ===== RUN =====
bot.infinity_polling()
