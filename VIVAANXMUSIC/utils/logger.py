from pyrogram.enums import ParseMode

from VIVAANXMUSIC import app
from VIVAANXMUSIC.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype, query: str = None, source: str = None):
    if await is_on_off(2):
        if query is None:
            try:
                query = message.text.split(None, 1)[1]
            except Exception:
                query = "-"

        source_line = f"\n<b>SOURCE :</b> {source}" if source else ""
        logger_text = f"""
<b>{app.mention} PLAY LOG</b>

<b>CHAT ID :</b> <code>{message.chat.id}</code>
<b>CHAT NAME :</b> {message.chat.title}
<b>CHAT USERNAME :</b> @{message.chat.username}

<b>USER ID :</b> <code>{message.from_user.id}</code>
<b>NAME :</b> {message.from_user.mention}
<b>USERNAME :</b> @{message.from_user.username}

<b>QUERY :</b> {query}
<b>STREAMTYPE :</b> {streamtype}{source_line}"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception:
                pass
        return
