"""
SB2411LuckyGZbot — Telegram Bot (Hindi)
Sends daily productivity and focus tips in Hindi, on request or subscription.

Run locally:
    export BOT_TOKEN="your-token-from-botfather"
    python bot.py

Deployed on Railway, BOT_TOKEN is read from an environment variable you set
in the Railway dashboard (Variables tab) — never hard-code it in this file.
"""

import json
import logging
import os
import random
from datetime import time as dtime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

SUBSCRIBERS_FILE = "subscribers.json"

# ---------------------------------------------------------------------------
# CONTENT LIBRARY (Hindi) — distinct tip set from SB244, add entries any time
# ---------------------------------------------------------------------------

TIPS = [
    {
        "title": "🧱 सबसे छोटे रूप से शुरुआत करें",
        "body": (
            "जब कोई काम बहुत बड़ा लगे, तो उसे इतना छोटा कर दें कि टालना मुश्किल "
            "हो जाए।\n\n"
            "'एक लाइन लिखना' शुरू करना 'पूरी रिपोर्ट लिखना' से कहीं आसान है — "
            "और शुरुआत करना ही सबसे मुश्किल हिस्सा होता है।"
        ),
    },
    {
        "title": "🚪 इच्छाशक्ति नहीं, माहौल बदलें",
        "body": (
            "इच्छाशक्ति खत्म हो सकती है, पर माहौल नहीं।\n\n"
            "जो चीज़ें आप ज़्यादा करना चाहते हैं उन्हें पास रखें, और जो कम करना "
            "चाहते हैं उन्हें थोड़ा दूर रखें।"
        ),
    },
    {
        "title": "⏳ लिस्ट नहीं, समय तय करें",
        "body": (
            "टू-डू लिस्ट बताती है क्या करना है। कैलेंडर बताता है कब करना है।\n\n"
            "किसी काम को एक तय समय देने से वह सच में पूरा होने की संभावना "
            "कहीं ज़्यादा बढ़ जाती है।"
        ),
    },
    {
        "title": "🔕 फोकस के समय को सुरक्षित रखें",
        "body": (
            "नोटिफिकेशन सिर्फ बाधा नहीं डालते — उनसे वापस फोकस में आने में भी "
            "समय लगता है।\n\n"
            "फोकस के समय नोटिफिकेशन बंद रखना, बाधा से भी ज़्यादा समय बचाता है।"
        ),
    },
    {
        "title": "🎯 पांच नहीं, एक प्राथमिकता",
        "body": (
            "जिस दिन में पांच 'सबसे ज़रूरी काम' हों, असल में कोई प्राथमिकता "
            "होती ही नहीं।\n\n"
            "वह एक काम चुनें जो दिन को सफल बना दे, और उसे सबसे पहले करें।"
        ),
    },
    {
        "title": "🧠 अधूरे काम दिमाग से निकालें",
        "body": (
            "कोई अधूरा काम दिमाग के पीछे चुपचाप ध्यान खींचता रहता है, भले ही "
            "आप उसके बारे में सोच न रहे हों।\n\n"
            "उसे लिख लेने से — सिर्फ अगला कदम भी — दिमाग हल्का हो जाता है।"
        ),
    },
    {
        "title": "🪫 आराम भी सिस्टम का हिस्सा है",
        "body": (
            "थकान के बावजूद काम करते रहने से अक्सर काम धीमा और कमज़ोर होता है, "
            "तेज़ नहीं।\n\n"
            "आराम का समय बर्बाद नहीं होता — यह अगले फोकस के समय को मुमकिन बनाता है।"
        ),
    },
    {
        "title": "📏 प्रगति नापें, सिर्फ व्यस्तता नहीं",
        "body": (
            "व्यस्त रहना और प्रोडक्टिव होना एक बात नहीं है।\n\n"
            "दिन के अंत में देखें कि असल में क्या आगे बढ़ा — सिर्फ कितना समय "
            "भरा, यह नहीं।"
        ),
    },
]

WELCOME_MESSAGE = (
    "👋 स्वागत है!\n\n"
    "यह बॉट आपको फोकस और प्रोडक्टिविटी से जुड़े छोटे, व्यावहारिक सुझाव भेजता है।\n\n"
    "कमांड्स:\n"
    "/tip — एक रैंडम सुझाव पाएं\n"
    "/subscribe — रोज़ाना सुझाव अपने आप पाएं\n"
    "/unsubscribe — रोज़ाना सुझाव बंद करें\n"
    "/help — यह मैसेज फिर से देखें"
)

# ---------------------------------------------------------------------------
# SUBSCRIBER STORAGE
# ---------------------------------------------------------------------------


def load_subscribers() -> set:
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_subscribers(subscribers: set) -> None:
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(list(subscribers), f)


subscribers = load_subscribers()

# ---------------------------------------------------------------------------
# COMMAND HANDLERS
# ---------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE)


async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pick = random.choice(TIPS)
    text = f"{pick['title']}\n\n{pick['body']}"
    await update.message.reply_text(text)


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id in subscribers:
        await update.message.reply_text("आप पहले से ही रोज़ाना सुझावों के लिए सब्सक्राइब हैं।")
        return
    subscribers.add(chat_id)
    save_subscribers(subscribers)
    await update.message.reply_text(
        "✅ सब्सक्राइब हो गया! अब आपको रोज़ एक सुझाव मिलेगा। कभी भी बंद करने के लिए /unsubscribe भेजें।"
    )


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id not in subscribers:
        await update.message.reply_text("आप अभी सब्सक्राइब नहीं हैं।")
        return
    subscribers.discard(chat_id)
    save_subscribers(subscribers)
    await update.message.reply_text("रोज़ाना सुझाव बंद कर दिए गए हैं।")


async def send_daily_tip(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs once a day, sends one random tip to every subscriber."""
    if not subscribers:
        return
    pick = random.choice(TIPS)
    text = f"{pick['title']}\n\n{pick['body']}"
    for chat_id in list(subscribers):
        try:
            await context.bot.send_message(chat_id=chat_id, text=text)
        except Exception as exc:
            logger.warning("Failed to send to %s: %s", chat_id, exc)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------


def main() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "BOT_TOKEN environment variable is not set. "
            "Set it locally with `export BOT_TOKEN=...` or in Railway's Variables tab."
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tip", tip))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Daily tip at 09:00 UTC — adjust the hour to suit your audience's timezone.
    job_queue = application.job_queue
    job_queue.run_daily(send_daily_tip, time=dtime(hour=9, minute=0))

    logger.info("Bot starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
